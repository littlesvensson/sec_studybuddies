SESSION 5, 9.7.2025 
========================

## Content of the session:

**Application Design and Build**
* Utilize persistent and ephemeral volumes (pt. 2)

**Application Environment, Configuration and Security**
* Understand ServiceAccounts
* Discover and use resources that extend Kubernetes (CRD, Operators)

**Application Observability and Maintenance**
* Understand API deprecations
* Use built-in CLI tools to monitor Kubernetes application

#### Persistent volumes
 
Persistent volumes are designed to retain data beyond the lifecycle of individual pods. <br>

They rely on resource types like PersistentVolume (PV) and PersistentVolumeClaim (PVC) to manage durable storage. By using persistent volumes, Kubernetes decouples storage from containers, enabling stateful applications to run reliably in dynamic environments.

##### Connected resource types

###### 1. PersistentVolume (pv)
- Represents a piece of storage in a cluster provisioned by an admin or dynamically provisioned.
- It's cluster-wide and exists independently of pods.

PersistentVolume cannot be created imperatively, but you can create it using a YAML manifest.

Here an example of a [PersistentVolume definition from the official documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes):

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```

###### 2. PersistentVolumeClaim (pvc)
- A request for storage by a user or app.

You can think of a PVC as a claim to a PV. It is a way for users to request storage resources without needing to know the details of the underlying storage infrastructure.

We can create simple PersistentVolumeClaims imperatively using the `k create pvc <name> --storage=<size> --access-mode=<mode> --dry-run=client -o yaml` command.

Binds to a matching PV based on:
* AccessModes
* Storage size
* StorageClass 

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
spec:
  accessModes:
    - ReadWriteOnce                # can be ReadWriteOnce, ReadOnlyMany, or ReadWriteMany
  resources:
    requests:
      storage: 1Gi
```
```yaml
volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: mypvc

volumeMounts:
  - name: my-volume
    mountPath: /data
```

###### 3. StorageClass (sc)
The additional value of StorageClasses in Kubernetes is that they enable **dynamic provisioning of persistent volumes**, removing the need for manual volume creation and management.

Instead of requiring a cluster administrator to pre-create PersistentVolumes (PVs) that exactly match each PersistentVolumeClaim (PVC), a StorageClass automates this process by defining how volumes should be provisioned (e.g., disk type, reclaim policy, provisioner). This simplifies workflows for developers, allowing them to simply request storage through a PVC while Kubernetes handles the creation, configuration, and lifecycle of the underlying storage — making persistent storage scalable, flexible, and cloud-native.

In CKAD, you will not need to create StorageClasses, but you will need to understand how they work and how to use them in the context of PersistentVolumeClaims if asked in the exam.

Example of a StorageClass definition from the official documentation:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: low-latency
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: csi-driver.example-vendor.example
reclaimPolicy: Retain                                    # default value is Delete
allowVolumeExpansion: true
mountOptions:
  - discard                                              # this might enable UNMAP / TRIM at the block storage layer
volumeBindingMode: WaitForFirstConsumers
parameters:
  guaranteedReadWriteLatency: "true"                     # provider-specific
```

Example of a PersistentVolumeClaim definition from the official documentation:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mylittleclaim
  namespace: studybuddies
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard       # specify the StorageClass to use if required by the task
  resources:
    requests:
      storage: 1Gi
```

### TASK! (#1)

Create a new PersistentVolume named `mycoolpv` with the following specifications:
  - Access mode: ReadWriteOnce
  - PersistentVolumeReclaimPolicy: Retain
  - Storage request: 2Mi
  - hostPath: /mnt/data

Then, create a PersistentVolumeClaim in the studybuddies namespace named `evencoolerpvc` that:
  - requests 2Mi of storage
  - uses the ReadWriteOnce access mode 
  - should not apply StorageClass for the binding (you can set `storageClassName: ""` in the PVC definition).
  
  > Note: reject using StorageClass for the binding by setting property `storageClassName: ""`. This property is not mandatory to write in the pvc definition, however without defining Kubernetes would assign it a default StorageClass(if any exists).

- The PVC should bound to PV correctly

Finally, create a Deployment with the following specifics:
- name: `lookinggood`
- namespace `studybuddies`
- image: `docker/whalesay`
- command: sh -c 'cowsay "CKAD is fun and I am looking good" && sleep 3600'
- uses `evencoolerpvc` PersistentVolumeClaim to mount the volume at `/data` inside the container.

Once done, express your happiness in the chat!

Time CAP: 5 minutes

## ServiceAccounts

1. Purpose
A ServiceAccount provides an identity for a pod to interact with the Kubernetes API.

Every pod uses one — default ServiceAccount if none is specified. Every namespace has a default ServiceAccount 

```bash
k get sa -A | grep default

default              default                                  0         13h
kube-node-lease      default                                  0         13h
kube-public          default                                  0         13h
kube-system          default                                  0         13h
local-path-storage   default                                  0         13h
studybuddies         default                                  0         5h17m
```

If you will try to delete the default ServiceAccount, Kubernetes will recreate it automatically.

```bash
k delete sa -n studybuddies default
```
```bash
k get sa -n studybuddies

k get sa -A | grep default
default              default                                  0         13h
kube-node-lease      default                                  0         13h
kube-public          default                                  0         13h
kube-system          default                                  0         13h
local-path-storage   default                                  0         13h
studybuddies         default                                  0         3s
```

To assign a ServiceAccount to a Pod, you set the `spec.serviceAccountName` field in the Pod specification. Kubernetes then automatically provides the credentials for that ServiceAccount to the Pod.

##### How ServiceAccounts Are Used
- Their tokens are mounted to pods at /var/run/secrets/kubernetes.io/serviceaccount/token.
- Can be used by applications inside the pod to call the Kubernetes API.
- You can use Role/RoleBinding (RBAC) to give a ServiceAccount permission to access API resources.

If you wish not to mount the ServiceAccount token into the pod, you can set the `automountServiceAccountToken` field to false in the Pod spec.

> Note: It is also possible to specify a ServiceAccount and still disable the automatic mounting of the ServiceAccount. This usecase is valid even if it looks a bit counterintuitive. The reason might be that you want to identify the pod in logs or auditing as belonging to a certain ServiceAccount Prevent any process in the container from using the ServiceAccount token for use with the Kubernetes API.

> Note2: In the CKAD context, you will need to be able to create a ServiceAccount and assign it to a Pod. 

### TASK! (#2)

Create a ServiceAccount named `loyalservant` in the namespace `studybuddies`. 
Then, create a deployment in the studybuddies namespace with the following specifications:
- that uses the `loyalservant` ServiceAccount
- name: `bossdeploy` 
- image: `busybox`
- replicas: 1
- The pod should print "I am loyal" and fall asleep for 3600 seconds. (you can use command -- sh -c 'echo "I am loyal" && sleep 3600')

## CRDs 

A CRD (CustomResourceDefinition ) extends the Kubernetes API with new resource types. It's basically a resource type similar to pods, services, deployments, etc., but defined by users or developers. Which means they are not built-in resources.

It allows you to define custom objects like Cluster, AppFwAPI, AppFw, etc.

Once a CRD is installed, you can use kubectl to create and manage these new resources just like built-in ones (Pods, Deployments, etc.).

For CKAD, you consume CRDs — you don't create them.

```bash
k get crd
k get <custom resource name> 
k explain <crd> --recursive
```

Lets try out together!

At first, we will install 
```bash
# Installing cert-manager CRDs
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.17.1/cert-manager.crds.yaml
```
Then, we can check the CRDs installed in our cluster:
```bash
k get crd
```
Now, let's explore the `certificates` CRD:
```bash
k explain certificates.cert-manager.io --recursive
```
With this command, you can see the structure and fields of the `certificates` resource defined by the cert-manager CRD. From this, you can learn how to create a certificate resource and what fields are available.

### TASK! (#3)

- List your current CRDs in the local cluster.
- Find out what is the apiVersion of the second one.
- Write down to the chat: "I am a pro and the version of the <`CRD name`> is <`apiVersion`>.

### HOMEWORK! (#1)
Homework for this topic is [waiting for you in KillerCoda](https://killercoda.com/killer-shell-ckad/scenario/crd)!

https://killercoda.com/killer-shell-ckad/scenario/crd


### Understand API deprecations

Kubernetes evolves fast. Older API versions are marked as deprecated, then eventually removed in later versions.

If you use a deprecated API, your manifests may fail to work after a Kubernetes upgrade.

How to Recognize Deprecated APIs
Check the apiVersion: field in your YAML.


Helpful tools/commands
```bash
# Check available API versions
k api-resources
kubectl explain deployment | grep VERSION
```

### TASK! (#4)

In the folder [task5_4](./task5_4/), you will find a file called [sadcronjob.yaml](./task5_1/sadcronjob.yaml). Deploy the manifest to your cluster and troubleshoot any issues that arise.

Stuck on the way? Check the solution in [session_5/task5_4/solution.md](/session_5/task5_1/solution.md).


### Use built-in CLI tools to monitor Kubernetes application

Kubernetes provides several built-in CLI tools to monitor and troubleshoot applications running in the cluster. During our sessions, we have aleady used most of them, but let's summarize them:

#### Inspect Pod and Deployment Health

k get po:	Pod status (Running, CrashLoopBackOff, Pending)
k get po -A:	All pods in all namespaces
k get all:	All workload resources (basically all pods and their controllers + services) in current namespace
k get all -A: When you want everything :)
k describe po <pod>:	Detailed events, probe results, resource usage, restarts
k logs <pod>:	Container stdout/stderr (logs)
k logs <pod> -c <container>:	Specific container logs in a multi-container pod
k logs <pod> --previous:	Previous container logs (if restarted)
k logs <pod> -l app=<label>:	Filter logs by label selector
k logs deployment/<deployment>:	Choosing one random pod from the deployment to get logs
k logs -f <pod>:	Live log streaming
k get deployment:	Deployment status: replicas, available, updated
k rollout status deployment <name>:	Rollout progress
k rollout history deployment <name>:	Deployment version history
k describe <resource type> <name>:	Detailed resource information (events, conditions, etc.)
k get events: Recent events in the cluster (e.g., pod restarts, scheduling issues)

>Note: the difference between logs and events is that logs are the output of the application running inside the container, while events are Kubernetes system messages about actions taken on resources (like pod restarts, scheduling, etc.). When debuggin, you might need to inspect both of them.

#### Resource Usage Monitoring (requires metrics-server)

k top po:	Shows CPU/memory usage per pod
k top no:	Shows node-level resource usage

#### Debugging / Troubleshooting

k exec -it <pod> -- bash	Open a shell in a running container
k port-forward <pod> <local port on your machine>:<remote port on the pod>	Access pod apps locally via port forwarding 

```bash
k run little-port-test --image=nginx --port=80
k port-forward pod/little-port-test 8080:80

curl http://localhost:8080
```

### HOMEWORK! (#2)

If you have not done some of the tasks during the session, you can do them at home :)
Also, there are some additional tasks for you to practice at Killercoda CKAD section:
- [VIM Setup](https://killercoda.com/killer-shell-ckad/scenario/vim-setup)
- [SSH Basics](https://killercoda.com/killer-shell-ckad/scenario/ssh-basics)
- [Configmap Access in Pods](https://killercoda.com/killer-shell-ckad/scenario/configmap-pod-access)
- [Readiness Probe](https://killercoda.com/killer-shell-ckad/scenario/readiness-probe)
- [Build and Run a Container](https://killercoda.com/killer-shell-ckad/scenario/container-build)
- [Rollout Rolling](https://killercoda.com/killer-shell-ckad/scenario/rollout-rolling)

## Wrap up
Weheeej, you made it through the fifth session of the Study Buddies series!

Today, we have learned:

* How to work with persistent volumes
* What are ServiceAccounts for and how to use them
* What are CRDs
* Understand API deprecations
* Usage of built-in CLI tools to monitor Kubernetes application

I  hope this session was interesting for you and you were able to learn something new here and there. Please let me know your feedback and any improvement suggestions for the future, this serie is here for you and the goal is to make it as fun and efficient as possible.

