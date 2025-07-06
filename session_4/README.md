SESSION 4, 7.7.2025 
========================

## Content of the session:

**Application Environment, Configuration and Security**
* Understand ConfigMaps
* Understand Secrets

**Application Design and Build**
* StatefulSet
* Utilize persistent and ephemeral volumes

**Application Environment, Configuration and Security**
* Understand ServiceAccounts
* Discover and use resources that extend Kubernetes (CRD, Operators)

**wrap up, homework, next steps**

#### How to use ConfigMaps in Pods
You can use ConfigMaps in your pods by mounting them as volumes or using them as environment variables. <br>
Mounting ConfigMaps as volumes in Kubernetes means making the data stored in a ConfigMap available to a container as files inside the container's filesystem. <br>

##### ConfigMaps as environment variables

Injecting key-value pairs from a ConfigMap:

```yaml
envFrom:
- configMapRef:
    name: cuteconfig
```
Injecting a specific key from a ConfigMap as an environment variable:

```yaml
env:
- name: SECURITY_MOOD
  valueFrom:
    configMapKeyRef:
      name: cuteconfig
      key: security_mood
```

##### ConfigMaps as volumes

```yaml
volumes:
- name: cute-volume
  configMap:
    name: cuteconfig

containers:
- name: app
  volumeMounts:
  - name: cute-volume
    mountPath: /etc/config
```
Each key becomes a filename, and the value is the content of the file.
You can also specify items to control which keys are mounted.

##### When to use environment variables vs. volumes

Environment variables are for key-value pairs only and the values must be plain strings. They are not well-suited for multi-line, large, or structured content (like YAML, JSON, or certificates).

Let's check an example [with both methods from the official documentation](https://kubernetes.io/docs/concepts/configuration/configmap/#configmaps-and-pods)


### TASK! (#1)

Create a deployment with 3 replicas within the studybuddies namespace with the name `nostalgic` that uses the `BESTCHAPTERINTHEWORLD` value from the `holyconfig` ConfigMap as an environment variable. 
- deployment name: nostalgic
- replicas: 3
- namespace: studybuddies
- image: busybox
- command: `sh -c "echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600"`
- environment variable: `BESTCHAPTERINTHEWORLD` from the `holyConfig` ConfigMap

Hint: You can design the deployment imperatively using the `k create deploy <name of deployment> -n <namespace name> --image=<image name> --replicas=<number of replicas> --dry-run=client -oyaml -- 'sh -c "echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600"' command, but with the `--dry-run=client -o yaml` flags to generate the YAML manifest. Then you can edit the manifest (add env from configmap) and apply it.

Time CAP: 5 minutes.

Stuck on the way? Check the solution in the [./task4_1/solution.md](./task4_1/solution.md) file.

### Secrets

Secrets are used to store sensitive information, such as passwords, tokens, or SSH keys. They are similar to ConfigMaps but are designed to handle sensitive data securely. You can create then directly from literal values, files, or directories. 
Although they are base64 encoded, they are not encrypted by default (unless encryption-at-rest is enabled). Because base64 encoding is NOT AN ENCRYPTION! The topic of encryption-at-rest is a topic of of CKAD exam, but you will encounter it in the CKA. For now, you need to know what secret is, how to create one and how to use it for your workloads.

```bash
k create secret -h

k create secret <typeofsecret> <secret name> [--from-literal=<key>=<value>] [--from-file=<key>=<path>] [--from-env-file=<path>] [--dry-run=client -o yaml] [-n <namespace name>]
```

You can create a secret using a YAML file or imperatively with the `kubectl create secret` command. There are three types of secrets you can create:
1. **Generic**: For arbitrary data, such as passwords, tokens, or SSH keys.
2. **Docker Registry**: For storing Docker registry credentials.
3. **TLS**: For storing TLS certificates and keys.

Why there are three types of secrets? Because Kubernetes needs to know how to handle the data inside the secret. For example, a Docker registry secret is used for pulling images from a private registry, while a TLS secret is used for storing certificates and keys. Also, the way you create them is different.

```bash
k create secret generic moodoftheday --from-literal=ifeel=euphoric
```
```bash
k create secret generic  --from-file=ssh-privatekey=/path/to/private/key 
```
When using from file, the file name will be used as the key in the secret. If you want to specify a different key name, you can use the `--from-file=<key>=<path>` option.

```bash
k create secret generic my-secret --from-env-file=path/to/secret.env
``` 
With env file, the keys within the file will be the names of the variables in the file and the values will be the values of the variables.

### TASK! (#2)

Create a secret in the namespace `studybuddies` with the name `mydirtysecret` that contains the following key-value pairs:

- key: thebestlecturerever
- value: jaja

When finished, write to the channel "I am a pro." (If doing outside of the session, tell out loud: "I AM A PRO!")

##### How to use Secrets in Pods

Similarly to ConfigMaps you can use Secrets in your pods by mounting them as volumes or using them as environment variables.

Using [Secrets as environment variables](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#define-a-container-environment-variable-with-data-from-a-single-secret):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-single-secret
spec:
  containers:
  - name: envars-test-container
    image: nginx
    env:
    - name: SECRET_USERNAME
      valueFrom:
        secretKeyRef:
          name: backend-user
          key: backend-username
```
We can see in the example above that we are using the `valueFrom` field to reference a specific key in the secret. The `secretKeyRef` field specifies the name of the secret and the key within that secret. So basically, we use totally the same pattern as with ConfigMaps, but instead of `configMapKeyRef`, we use `secretKeyRef`.

Using [Secrets as volumes](https://kubernetes.io/docs/concepts/configuration/secret/#using-a-secret):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cutething
spec:
  containers:
  - name: cutething
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/cute"
      readOnly: true
  volumes:
  - name: cute
    secret:
      secretName: mycutesecret
      optional: true
```
In this example, we are mounting the secret as a volume in the pod. The `secretName` field specifies the name of the secret, and the `mountPath` field specifies where the secret will be mounted inside the container. The files in the secret will be available as files in the specified directory. Again, very similar to ConfigMaps, but instead of `configMap` property, we use `secret`.


## HOMEWORK! (#1)

Create a Deployment in the studybuddies namespace with the following requirements:

- Name: secretholder
- Namespace: studybuddies
- Replicas: 2
- Container image: littlesvensson/dirtysecret
- The secret from the task 1 `mydirtysecret` must be mounted as a volume inside the deployment pods
- Mount path: /etc/secretinfo (the application should be able to read the value of thebestlecturerever from a file located at /etc/secretinfo/thebestlecturerever)

After you create the deployment, check the log of one of the created pods to find out the truth.

### StatefulSets

StatefulSets are used for managing stateful applications, which require stable, unique network identifiers and persistent storage. They provide guarantees about the ordering and uniqueness of pods, making them suitable for applications like databases or distributed systems.

Key characteristics of StatefulSets:
- **Stable Network Identity**: Each pod in a StatefulSet has a unique, stable hostname that persists across rescheduling.
- **Ordered Deployment and Scaling**: Pods are created, updated, and deleted in a specific order, ensuring that the first pod is always created first, the second pod is created after the first, and so on.
- **Persistent Storage**: StatefulSets can be associated with PersistentVolumeClaims (PVCs) to provide stable storage for each pod. Each pod gets its own PVC, which is not shared with other pods in the StatefulSet. This allows each pod to have its own persistent storage, which is crucial for stateful applications.
- **Ordered Termination**: Pods are terminated in reverse order, ensuring that the last pod is terminated first, allowing for graceful shutdowns and data preservation.

We cannot create statefulsets imperatively, but we can scale them using the `k scale sts <statefulset name> --replicas=<number of replicas>` command. Also, we can delete and edit stateful sets.

Let's check a [simple statefulset from the official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#components)

We will wait with task for a statefulset until we get to some other necessary concepts like headless service and volume claims. For now, what you need to know is that they are useful for managing stateful application and are ordered. 

### Time for increase Volume (Utilize persistent and ephemeral volumes)

A volume is a storage resource that a pod’s containers can read from or write to. Unlike the ephemeral container file system, volumes persist across container restarts (but not pod restarts — unless backed by persistent storage). <br>

There are two types of volumes in Kubernetes: *ephemeral* and *persistent*. 

##### Ephemeral volumes

Ephemeral volumes such as emptyDir, configMap, and secret, **exist only for the lifetime of a pod** (but not container lifetime - meaning when container within a pod restarts, ephemeral volumes are still there unchanged) and are typically used for temporary data, sharing files between containers, or injecting configuration. Once your pod dies, ephemeral volume data is dead too.

For a Pod that defines an `emptyDir` volume, the volume is created when the Pod is assigned to a node. As the name says, the emptyDir **volume is initially empty**. All containers in the Pod can read and write the same files in the emptyDir volume.

Example of an `emptyDir` volume spec within a Pod [from the official documentation](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-configuration-example):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:             # volumeMounts are defined within the container spec
    - mountPath: /cache       # path to mount the volume inside the container. Theoretiacally, you can have different mount paths for different containers in the same pod and they would still share the same volume
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:                    
      sizeLimit: 500Mi        # optional, but you can specify a size limit for the emptyDir volume
```
### TASK! (#3, together)

Create a deployment with the following specification:

- 1 replica
- Name: log-writer
- Namespace: studybuddies
- Containers (2):
  - Writer container:
    - Image: busybox
    - Name: log-writer
    - Command: ["sh", "-c", "while true; do date >> /shared/log.txt; sleep 5; done"]
  - Reader container:
    - Image: busybox
    - Name: log-reader
    - Command: ["sh", "-c", "while true; do cat /shared/log.txt; sleep 5; done"]
  - Use an emptyDir volume named shared-logs to share data between the two containers.
- mount the shared volume at /shared in both containers

A writer container will write the current time to /shared/log.txt every 5 seconds.
A reader container will print the contents of /shared/log.txt every 5 seconds.

We will use sleep + sh -c pattern for infinite looping (since busybox doesn't have cron or tail features).

Stuck on the way? Check the solution in the [./task4_3/solution.md](./task4_3/solution.md) file.

##### configMap and secret volumes

Mount a configMap or secret as a file inside a container.

```yaml
volumes:
  - name: config-volume
    configMap:
      name: mylittleconfig
```
```yaml
volumeMounts:
  - name: config-volume
    mountPath: /etc/config
    readOnly: true
```

```yaml
volumes:
  - name: secret-volume
    secret:
      secretName: mylittlesecret
```
```yaml
volumeMounts:
  - name: secret-volume
    mountPath: /etc/secret
    readOnly: true
```

 #### Persistent volumes
 
Persistent volumes are designed to retain data beyond the lifecycle of individual pods. They rely on resource types like PersistentVolume (PV) and PersistentVolumeClaim (PVC) to manage durable storage. By using persistent volumes, Kubernetes decouples storage from containers, enabling stateful applications to run reliably in dynamic environments.

##### Connected resource types

1. PersistentVolume (PV)
- Represents a piece of storage provisioned by an admin or dynamically provisioned.
- It's cluster-wide and exists independently of pods.

You typically won’t need to create PVs on the CKAD exam — focus on consuming them via PVCs.

2. PersistentVolumeClaim (PVC)
- A request for storage by a user or app.

Binds to a matching PV based on:

AccessModes
Storage size
StorageClass (optional)


```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
spec:
  accessModes:
    - ReadWriteOnce
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

### HOMEWORK! (#2)

- Create a new PersistentVolume named `mycoolpv` with the following specifications:
  - Access mode: ReadWriteOnce
  - Storage request: 2Gi
  - hostPath: /mnt/data

- Then, create a PersistentVolumeClaim named `evencoolerpvc` that:
  - requests 2Gi of storage
  - uses the ReadWriteOnce access mode 
  - should not define StorageClassnaem

- The PVC should bound to PV correctly

- Finally, create a Deployment named `lookinggood` in the namespace `studybuddies` that uses the `mypvc` PersistentVolumeClaim to mount the volume at `/data` inside the container.


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
Then, create a deployment in the studybuddies namespace that uses this ServiceAccount. Deployment should have the name `bossdeploy` with the image `busybox`. The pod should print "I am loyal" and fall asleep for 3600 seconds. (you can use command -- echo "I am loyal" && sleep 3600)


## CRDs 

A CRD (CustomResourceDefinition ) extends the Kubernetes API with new resource types. It's basically a resource type similar to pods, services, deployments, etc., but defined by users or developers. Which means they are not built-in resources.

It allows you to define custom objects like Cluster, AppFwAPI, AppFw, etc.

Once a CRD is installed, you can use kubectl to create and manage these new resources just like built-in ones (Pods, Deployments, etc.).

For CKAD, you consume CRDs — you don't create them.

```bash
k get crd
k get <custom resource name> 
k explain <crd> --recursive

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


## Wrap up
Congratulations on completing the fourth session of the Study Buddies series!

Today, we have learned:

* How to understand and ConfigMaps and Secrets
* What are StatefulSet
* How to utilize persistent and ephemeral volumes
* What are ServiceAccounts for and how to implement them
* What are CRDs and Kubernetees Operators

I  hope this session gave you some knowledge and inspiration and you had at least a bit of fun on the way. Please let me know your feedback and any improvement suggestions, this should help us all with preparation and the right feedback would make this serie more efficient.

