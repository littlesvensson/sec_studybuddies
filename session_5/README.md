SESSION 5, 9.7.2025 
========================

## Content of the session:

**Application Design and Build**
* StatefulSet
* Utilize persistent and ephemeral volumes

**Application Environment, Configuration and Security**
* Understand ServiceAccounts
* Discover and use resources that extend Kubernetes (CRD, Operators)

**Application Observability and Maintenance**
* Understand API deprecations
* Use built-in CLI tools to monitor Kubernetes application

**Application Environment, Configuration and Security**
* Understand requests, limits, quotas
* Define resource requirements
* Understand Application Security (SecurityContexts, Capabilities, etc.)
* Understand authentication, authorization and admission control

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

### HOMEWORK! (#2)

Create a new PersistentVolume named `mycoolpv` with the following specifications:
  - Access mode: ReadWriteOnce
  - Storage request: 2Gi
  - hostPath: /mnt/data

Then, create a PersistentVolumeClaim named `evencoolerpvc` that:
  - requests 2Gi of storage
  - uses the ReadWriteOnce access mode 
  - should not define StorageClassname

- The PVC should bound to PV correctly

Finally, create a Deployment with the following specifics:
- name: `lookinggood`
- namespace `studybuddies` 
- image: `docker/whalesay`
- command: cowsay "CKAD is fun 🐳"
- uses `evencoolerpvc` PersistentVolumeClaim to mount the volume at `/data` inside the container.

Once done, check the logs of the pod to see a beautifule whale.

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
- They are mounted to pods at /var/run/secrets/kubernetes.io/serviceaccount/token.
- Can be used by applications inside the pod to call the Kubernetes API.
- You can use Role/RoleBinding (RBAC) to give a ServiceAccount permission to access API resources.

If you wish not to mount the ServiceAccount token into the pod, you can set the `automountServiceAccountToken` field to false in the Pod spec.

> Note: It is also possible to specify a ServiceAccount and still disable the automatic mounting of the ServiceAccount. This usecase is valid even if it looks a bit counterintuitive. The reason might be that you want to identify the pod in logs or auditing as belonging to a certain ServiceAccount Prevent any process in the container from using the ServiceAccount token for use with the Kubernetes API.

> Note2: In the CKAD context, you will need to be able to create a ServiceAccount and assign it to a Pod. You will not need to create Roles or RoleBindings, as they are part of the CKA exam.


### TASK! (#4)

Create a ServiceAccount named `loyalservant` in the namespace `studybuddies`. 
Then, create a deployment in the studybuddies namespace that uses this ServiceAccount. Deployment should have the name `bossdeploy` with the image `busybox`. The pod should print "I am loyal" and fall asleep for 3600 seconds. (you can use command -- sh -c 'echo "I am loyal" && sleep 3600')

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


### TASK! (#5)
Task for this topic is [waiting for you in KillerCoda](https://killercoda.com/killer-shell-ckad/scenario/crd)!

https://killercoda.com/killer-shell-ckad/scenario/crd


### HOMEWORK! (#2)

If you have not done some of the tasks during the session, you can do them at home :)
Also, there are some additional tasks for you to practice at Killercoda CKAD section:
- [VIM Setup](https://killercoda.com/killer-shell-ckad/scenario/vim-setup)
- [SSH Basics](https://killercoda.com/killer-shell-ckad/scenario/ssh-basics)
- [Configmap Access in Pods](https://killercoda.com/killer-shell-ckad/scenario/configmap-pod-access)
- [Readiness Probe](https://killercoda.com/killer-shell-ckad/scenario/readiness-probe)
- [Build and Run a Container](https://killercoda.com/killer-shell-ckad/scenario/container-build)
- [Rollout Rolling](https://killercoda.com/killer-shell-ckad/scenario/rollout-rolling)


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

### TASK! (#1)

In the folder [task5_1](./task5_1/), you will find a file called [sadcronjob.yaml](./task5_1/sadcronjob.yaml). Deploy the manifest to your cluster and troubleshoot any issues that arise.

Stuck on the way? Check the solution in [session_5/task5_1/solution.md](/session_5/task5_1/solution.md).


### Use built-in CLI tools to monitor Kubernetes application

#### Inspect Pod and Deployment Health

kubectl get pods	Pod status (Running, CrashLoopBackOff, Pending)
kubectl describe pod <pod>	Detailed events, probe results, resource usage, restarts
kubectl logs <pod>	Container stdout/stderr (logs)
kubectl logs -f <pod>	Live log streaming
kubectl get deployment	Deployment status: replicas, available, updated
kubectl rollout status deployment <name>	Rollout progress
kubectl get events

#### Resource Usage Monitoring (requires metrics-server)

kubectl top pod	Shows CPU/memory usage per pod
kubectl top node	Shows node-level resource usage

#### Debugging / Troubleshooting

kubectl exec -it <pod> -- bash	Open a shell in a running container
kubectl cp <pod>:/path /local/path	Copy files from/to a pod
kubectl port-forward <pod> 8080:80	Access pod apps locally via port forwarding 

#### Status and History Checks
Command	What it shows
kubectl get all	All workload resources (pods, svc, rs, etc.) in current namespace
kubectl rollout history deployment <name>	Deployment version history
kubectl get rs	View ReplicaSets tied to a Deployment
kubectl get jobs / cronjobs

## Application Security (SecurityContexts, Capabilities, etc.)

For the CKAD exam, you need to understand application-level security features — mostly how to use SecurityContexts and basic Linux capabilities within pods and containers.

#### SecurityContext

A SecurityContext is used to define security-related settings for pods or containers (e.g., user IDs, privilege level, filesystem settings).

There are two levels:

a. Pod-level SecurityContext in `spec.securityContext`
Applies to all containers in the pod.

```bash
k explain pod.spec.securityContext --recursive
```

```yaml
KIND:       Pod
VERSION:    v1

FIELD: securityContext <PodSecurityContext>


DESCRIPTION:
    SecurityContext holds pod-level security attributes and common container
    settings. Optional: Defaults to empty.  See type description for default
    values of each field.
    PodSecurityContext holds pod-level security attributes and common container
    settings. Some fields are also present in container.securityContext.  Field
    values of container.securityContext take precedence over field values of
    PodSecurityContext.

FIELDS:
  fsGroup	<integer>
  fsGroupChangePolicy	<string>
  runAsGroup	<integer>
  runAsNonRoot	<boolean>
  runAsUser	<integer>
  seLinuxOptions	<SELinuxOptions>
    level	<string>
    role	<string>
    type	<string>
    user	<string>
  seccompProfile	<SeccompProfile>
    localhostProfile	<string>
    type	<string> -required-
    enum: Localhost, RuntimeDefault, Unconfined
  supplementalGroups	<[]integer>
  sysctls	<[]Sysctl>
    name	<string> -required-
    value	<string> -required-
  windowsOptions	<WindowsSecurityContextOptions>
    gmsaCredentialSpec	<string>
    gmsaCredentialSpecName	<string>
    hostProcess	<boolean>
    runAsUserName	<string>
```

b. Container-level SecurityContext in `spec.containers[].securityContext`
Overrides pod-level for the specific container.

```bash
k explain pod.spec.containers.securityContext --recursive
```
```yaml
KIND:       Pod
VERSION:    v1

FIELD: securityContext <SecurityContext>

DESCRIPTION:
    SecurityContext defines the security options the container should be run
    with. If set, the fields of SecurityContext override the equivalent fields
    of PodSecurityContext. More info:
    https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
    SecurityContext holds security configuration that will be applied to a
    container. Some fields are present in both SecurityContext and
    PodSecurityContext.  When both are set, the values in SecurityContext take
    precedence.

FIELDS:
  allowPrivilegeEscalation	<boolean>
  capabilities	<Capabilities>
    add	<[]string>
    drop	<[]string>
  privileged	<boolean>
  procMount	<string>
  readOnlyRootFilesystem	<boolean>
  runAsGroup	<integer>
  runAsNonRoot	<boolean>
  runAsUser	<integer>
  seLinuxOptions	<SELinuxOptions>
    level	<string>
    role	<string>
    type	<string>
    user	<string>
  seccompProfile	<SeccompProfile>
    localhostProfile	<string>
    type	<string> -required-
    enum: Localhost, RuntimeDefault, Unconfined
  windowsOptions	<WindowsSecurityContextOptions>
    gmsaCredentialSpec	<string>
    gmsaCredentialSpecName	<string>
    hostProcess	<boolean>
    runAsUserName	<string>
```

In CKAD, you will most likely be instructed to set the SecurityContext either for pod or particular container with specific fields given by the task.

2. Capabilities
Linux capabilities let you drop or add fine-grained privileges.

3. Privileged Mode
Allows the container to access host-level resources (⚠ dangerous).

4. Run as Non-Root
To improve security, run containers as non-root:

5. Read-only Filesystem
Improves container immutability:

For CKAD, you need to know how to set securityContext above mentioned fields (and ideally understand what they mean :) .

## Understand authentication, authorization and admission control

1. ✅ Authentication (Who are you?)
Kubernetes checks who is making the request.

This could be a user, service account, or external identity (via certificates, tokens, etc.).

Most commonly in CKAD, this shows up when:

Your pod is running with a service account

You get Unauthorized errors if the kubeconfig is wrong or permissions are missing

👉 CKAD-level takeaway:
Be aware that service accounts are how workloads authenticate to the API server.

2. ✅ Authorization (What can you do?)
After identifying who, Kubernetes checks what they’re allowed to do.

It uses things like:

RBAC (Role-Based Access Control) — the most common

kubectl auth can-i to test permissions

👉 CKAD-level takeaway:

Know how to check if your service account or user can perform an action:

bash
Copy
Edit
kubectl auth can-i get pods --as system:serviceaccount:myns:myaccount
3. ✅ Admission Control (Should we allow it?)
Runs after authentication and authorization, before the object is persisted.

Controls like:

ValidatingAdmissionWebhook

MutatingAdmissionWebhook

LimitRanges, PodSecurity, ResourceQuotas

👉 CKAD-level takeaway:

You may encounter errors from things like a validating webhook or namespace quota.

For example:

"Pod denied: CPU request too high"

"Missing label required by policy"

🔍 In Practice
Component	What it does	CKAD relevance
Authentication	Identifies the requestor	Mostly behind the scenes
Authorization	Approves/rejects based on roles	Important when using service accounts, RBAC
Admission control	Final checks/patches before storing	May block objects if they violate policy

🧪 What You Should Practice
Create and use service accounts

Set automountServiceAccountToken: false when needed

Use kubectl auth can-i to troubleshoot permissions

Recognize common admission control errors in kubectl describe or kubectl get events




## Resource management
