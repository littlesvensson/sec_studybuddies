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


SERVICES
Use Kubernetes primitives to implement common deployment strategies (e.g. blue/green or canary)



