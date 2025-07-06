* Understand requests, limits, quotas
* Define resource requirements
* Understand Application Security (SecurityContexts, Capabilities, etc.)


**Application Observability and Maintenance**
* Understand API deprecations
* Use built-in CLI tools to monitor Kubernetes application



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

### TASK! (#4)

In the folder `session_3/task3_2`, you will find a file called `sickcronjob.yaml`. Deploy the manifest to your cluster and troubleshoot any issues that arise.

Stuck on the way? Check the solution in `session_3/task3_2/solution.md`.


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

## Resource management
