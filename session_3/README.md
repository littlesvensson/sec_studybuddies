SESSION 3, 4.7.2025 
========================

## Content of the session:

**Application Design and Build**
* Utilize persistent and ephemeral volumes

**Application Environment, Configuration and Security**
* Discover and use resources that extend Kubernetes (CRD, Operators)
* Understand requests, limits, quotas
* Define resource requirements
* Understand ServiceAccounts
* Understand Application Security (SecurityContexts, Capabilities, etc.)

**Application Observability and Maintenance**
* Understand API deprecations
* Use built-in CLI tools to monitor Kubernetes application

**wrap up, homework, next steps**


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
### TASK! (#1)

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

### HOMEWORK! (#1)

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

### Understand API deprecations

Kubernetes evolves fast. Older API versions are marked as deprecated, then eventually removed in later versions.

If you use a deprecated API, your manifests may fail to work after a Kubernetes upgrade.

How to Recognize Deprecated APIs
Check the apiVersion: field in your YAML.

# DEPRECATED (removed in 1.22)
apiVersion: apps/v1beta1
kind: Deployment

# CORRECT (current)
apiVersion: apps/v1
kind: Deployment


Helpful tools/commands
k api-resources
kubectl explain deployment | grep VERSION
k get events

### TASK! (#2)

In the folder `session_3/task3_2`, you will find a file called `sickcronjob.yaml`. Deploy the manifest to your cluster and troubleshoot any issues that arise.

Stuck on the way? Check the solution in `session_3/task3_2/solution.md`.


## Resource management



## ServiceAccounts

1. Purpose
A ServiceAccount provides an identity for a pod to interact with the Kubernetes API.

Every pod uses one — default ServiceAccount if none is specified.

 Token Is Automatically Mounted
Kubernetes mounts a token file inside the pod:


/var/run/secrets/kubernetes.io/serviceaccount/token
This token is used by the pod to authenticate to the Kubernetes API server.


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


