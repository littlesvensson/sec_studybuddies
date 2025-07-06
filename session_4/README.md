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
* Understand requests, limits, quotas
* Define resource requirements
* Understand Application Security (SecurityContexts, Capabilities, etc.)

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

## HOMEWORK(#1)

# TODO: mounting secret thebestlecturerever as an environment variable in the nostalgic deployment

### StatefulSets

StatefulSets are used for managing stateful applications, which require stable, unique network identifiers and persistent storage. They provide guarantees about the ordering and uniqueness of pods, making them suitable for applications like databases or distributed systems.

We cannot create statefulsets imperatively, but we can scale them using the `k scale sts <statefulset name> --replicas=<number of replicas>` command. Also, we can delete and edit stateful sets.

Let's check a [simple statefulset from the official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#components)

We will wait with task for a statefulset until we get to some other necessary concepts like headless service and volume claims. For now, what you need to know is that they are useful for managing stateful application and are ordered. 

### Time for some Volume (Utilize persistent and ephemeral volumes)

In Kubernetes, volumes are storage resources that allow containers in a pod to persist data, share data, or access configuration across restarts or between containers. <br>

There are two types of volumes in Kubernetes: *ephemeral* and *persistent*. 

##### Ephemeral volumes

Ephemeral volumes such as emptyDir, configMap, and secret, exist only for the lifetime of a pod and are typically used for temporary data, sharing files between containers, or injecting configuration. Once your pod dies, ephemeral volume data is dead too.

For a Pod that defines an `emptyDir` volume, the volume is created when the Pod is assigned to a node. As the name says, the emptyDir *volume is initially empty*. All containers in the Pod can read and write the same files in the emptyDir volume.

Example of an `emptyDir` volume spec within a Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 500Mi
      medium: Memory
```
### TASK! (#3)

Create a deployment called log-writer with 1 replica. It should:

Run a pod with two containers:

A writer container using image busybox, that writes the current time to /shared/log.txt every 5 seconds.

A reader container using image busybox, that prints the contents of /shared/log.txt every 5 seconds.

Use an emptyDir volume named shared-logs to share data between the two containers.

Use the sleep + sh -c pattern for infinite looping (since busybox doesn't have cron or tail features).

Tip: Mount the shared volume at /shared in both containers.

##### configMap and secret volumes

Mount a configMap or secret as a file inside a container.


```yaml
volumes:
  - name: config-volume
    configMap:
      name: mylittleconfig
```
```yaml
volumes:
  - name: secret-volume
    secret:
      secretName: mylittlesecret
```



 #### Persistent volumes
 , on the other hand, are designed to retain data beyond the lifecycle of individual pods. They rely on resources like PersistentVolume (PV) and PersistentVolumeClaim (PVC) to manage durable storage, often backed by external systems like cloud block storage or NFS. By using volumes, Kubernetes decouples storage from containers, enabling stateful applications to run reliably in dynamic environments.

1. PersistentVolume (PV)
Represents a piece of storage provisioned by an admin or dynamically provisioned.

It's cluster-wide and exists independently of pods.

You typically won’t need to create PVs on the CKAD exam — focus on consuming them via PVCs.

2. PersistentVolumeClaim (PVC)
A request for storage by a user or app.

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

Create a new PersistentVolume named `mycoolpv` with the following specifications:
- Access mode: ReadWriteOnce
- Storage request: 2Gi
- hostPath: /mnt/data

Then, create a PersistentVolumeClaim named `evencoolerpvc` that:
- requests 2Gi of storage
- uses the ReadWriteOnce access mode 
- should not define StorageClassnaem

The PVC should bound to PV correctly

Finally, create a Deployment named `lookinggood` in the namespace `studybuddies` that uses the `mypvc` PersistentVolumeClaim to mount the volume at `/data` inside the container.


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


### TASK! (#5)

Create a ServiceAccount named `loyalservant` in the namespace `studybuddies`. 
Then, create a deployment in the studybuddies namespace that uses this ServiceAccount. Deployment should have the name `bossdeploy` with the image `busybox`. The pod should print "I am loyal" and fall asleep for 3600 seconds. (you can use command -- echo "I am loyal" && sleep 3600)


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

## CRDs 

A CRD (CustomResourceDefinition) extends the Kubernetes API with new resource types. It's basically a resource type similar to pods, services, deployments, etc., but defined by users or developers. Which means they are not built-in resources.

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


TASK! (#6)
Task for this topic is [waiting for you in KillerCoda](https://killercoda.com/killer-shell-ckad/scenario/crd)!

https://killercoda.com/killer-shell-ckad/scenario/crd



## HOMEWORK(#1)

If you have not done some of the tasks during the session, you can do them at home :)
Also, there are some additional tasks for you to practice at Killercoda CKAD section:
- [VIM Setup](https://killercoda.com/killer-shell-ckad/scenario/vim-setup)
- [SSH Basics](https://killercoda.com/killer-shell-ckad/scenario/ssh-basics)
- [Configmap Access in Pods](https://killercoda.com/killer-shell-ckad/scenario/configmap-pod-access)
- [Readiness Probe](https://killercoda.com/killer-shell-ckad/scenario/readiness-probe)
- [Build and Run a Container](https://killercoda.com/killer-shell-ckad/scenario/container-build)
- [Rollout Rolling](https://killercoda.com/killer-shell-ckad/scenario/rollout-rolling)

