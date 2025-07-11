SESSION 6, 11.7.2025 
========================

## Content of the session:

**Application Observability and Maintenance**
* Understand API deprecations
* Use built-in CLI tools to monitor Kubernetes application

**Application Environment, Configuration and Security**
* Understand requests, limits, quotas, Define resource requirements
* Understand Application Security (SecurityContexts, Capabilities, etc.)
* Understand authentication, authorization and admission control

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

In the folder [task5_4](./task5_4/), you will find a file called [sadcronjob.yaml](./task5_1/sadcronjob.yaml). Deploy the manifest to your cluster and troubleshoot any issues that arise.

Stuck on the way? Check the solution in [session_5/task5_4/solution.md](/session_5/task5_1/solution.md).


### Use built-in CLI tools to monitor Kubernetes application

Kubernetes provides several built-in CLI tools to monitor and troubleshoot applications running in the cluster. During our sessions, we have aleady used most of them, but let's summarize them:

#### Inspect Pod and Deployment Health

**k get po**:	Pod status (Running, CrashLoopBackOff, Pending) <br>
**k get po -A**:	All pods in all namespaces <br>
**k get all**:	All workload resources (basically all pods and their controllers + services) in current namespace <br>
**k get all -A**: When you want everything :) <br>
**k describe po <pod>**:	Detailed events, probe results, resource usage, restarts <br>
**k logs <pod>**:	Container stdout/stderr (logs) <br>
**k logs <pod> -c <container>**:	Specific container logs in a multi-container pod <br>
**k logs <pod> --previous**:	Previous container logs (if restarted) <br>
**k logs <pod> -l app=<label>**:	Filter logs by label selector <br>
**k logs deployment/<deployment>**:	Choosing one random pod from the deployment to get logs <br>
**k logs -f <pod>**:	Live log streaming <br>
**k get deploy**:	Deployment status: replicas, available, updated <br>
**k rollout status deployment <name>**:	Rollout progress <br>
**k rollout history deployment <name>**:	Deployment version history <br>
**k describe <resource type> <name>**:	Detailed resource information (events, conditions, etc.) <br>
**k get events**: Recent events in the cluster (e.g., pod restarts, scheduling issues) <br>

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
### TASK! (#2)

In the folder [task6_2](./task6_2/), you will find manifest definitions within the file [scenario.yaml](./task6_2/scenario.yaml). Apply them to your cluster and then troubleshoot any issues that arise.

Let's **DISCUSS** what you found out!

## Application Security (SecurityContexts, Capabilities, etc.)

For the CKAD exam, you need to understand how to use SecurityContexts and basic Linux capabilities within pods and containers.

#### SecurityContext

A SecurityContext is used to define security-related settings for pods or containers (e.g., user IDs, privilege level, filesystem settings).

There are two levels:

**1. Pod-level SecurityContext in `spec.securityContext`**
Applies to all containers in the pod.

```bash
k explain pod.spec.securityContext --recursive
```

```yaml
...

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

**2. Container-level SecurityContext in `spec.containers[].securityContext`
**
Overrides pod-level for the specific container.

```bash
k explain pod.spec.containers.securityContext --recursive
```
```yaml
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
> Note: When you define a securityContext at both the pod and container level, the container-level settings take precedence over the pod-level settings.

> Note2: In CKAD, you will most likely be instructed to set the SecurityContext either for pod or particular container with specific fields given by the task.


* **runAsGroup <integer>**: specifies the primary group ID (GID) the container's main process should run as. It is the primary group the process belongs to. Each file or directory can grant read, write, execute permissions to a group (via the GID). If your process runs with a specific GID, it can access files and directories owned by that group, assuming the permissions allow it.
* **runAsUser	<integer>**: specifies the user ID (UID) the container's main process should run as. It is the user that owns the process. This is important for file permissions, as files created by the process will be owned by this UID.
* **runAsNonRoot	<boolean>**: ensures the container's main process does not run as the root user (UID 0). This is a security measure to prevent privilege escalation.
* **capabilities**: Linux capabilities let you drop or add fine-grained privileges to the container's process. For example, you can drop the `NET_ADMIN` capability to prevent network configuration changes.
* **privileged**: Allows the container to access host-level resources (which is **dangerous**).
* **readOnlyRootFilesystem**: Makes the container's root filesystem read-only. This prevents the container from modifying files in its root directory, which can enhance security.

For CKAD, you need to know how to set securityContext above mentioned fields (and ideally understand what they mean :) .

### TASK! (#3)

Create a Deployment named secure-app with the following specifications:
* Namespace: studybuddies
* Name: secure-joke
* 1 replica.
* curlimages/curl
* The container should run as user ID 1000.
* The container should use a read-only root filesystem.
* Command: curl -s https://icanhazdadjoke.com/

Once done, write your joke from the logs to the channel chat!

## Resource management

### 1. Resource Requests and Limits
These control how much CPU and memory your container can use. The resources are defined in the container spec of your pod under the `resources` field.

**Requests** = guaranteed minimum
**Limits** = hard maximum

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
``` 

**What it means** 
* The container gets at least 64Mi and 250m CPU
* The container can’t exceed 128Mi or 500m CPU

CPU is in millicores (500m = 0.5 CPU)
Memory is in bytes (e.g. Mi, Gi)

>Note: In the context of CKAD, you might be required to define requests/limits in exam tasks

### Why Use Requests and Limits?
* **Resource allocation**: Helps Kubernetes schedule pods on nodes with enough resources.
* **Performance**: Ensures your app has enough resources to run smoothly.
* **Stability**: Prevents a single pod from consuming all resources and affecting others.


>Note: Your pod might fail to schedule if a node doesn't have enough resources for the request. If a pod uses too much memory, it might be OOMKilled if it exceeds the memory limit.

### LimitRange
Automatically applies default limits/requests to pods in a namespace. This prevents pods from running without resource constraints.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit
  namespace: myns
spec:
  limits:
  - default:
      memory: 256Mi
    defaultRequest:
      memory: 128Mi
    type: Container
```

### ResourceQuota 
Limits total resources in a namespace. 

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: myns
spec:
  hard:
    pods: "10"
    requests.cpu: "1"
    requests.memory: "1Gi"
    limits.cpu: "2"
    limits.memory: "2Gi"
```


### TASK! (#4)

In the folder [task6_4](./task6_4/), you will find a file called [pod.yaml](./task6_4/pod.yaml). Adjust the manifest by addint the following specifications:
* The container requests 100Mi memory and 200m CPU
* The container limits memory to 256Mi and CPU to 500m


## Understand authentication, authorization and admission control

Knowing that Pods use service accounts
Understanding how to give a service account permissions (which uses Role/RoleBinding)
Being able to troubleshoot permission errors (e.g., app can't list pods)
Knowing that authorization is required when your app talks to the Kubernetes API

### 1. Authentication (Who are you?)

Authentication is about verifying the identity of a user or service (e.g., via kubeconfig or service account tokens). You don’t configure it, but it determines who can interact with the cluster. Kubernetes checks who is making the request.

This could be a user, service account, or external identity (via certificates, tokens, etc.).

Most commonly in CKAD, this shows up when:
* Your pod is running with a service account
* You get Unauthorized errors if the kubeconfig is wrong or permissions are missing

###  2. Authorization

Authorization controls what an authenticated user or service can do in the cluster, using RBAC (Role, RoleBinding, etc.). In CKAD, you're expected to create and use these roles to grant specific permissions to service accounts or users.

After identifying who, Kubernetes checks what they’re allowed to do. In the context of CKAD, this is often about giving your application the right permissions to access Kubernetes resources in the forme of RBAC - Role-Based Access Control.

#### Role-Based Access Control (RBAC)

RBAC is the most common way to control access in Kubernetes. It uses Roles and RoleBindings to define what actions users or service accounts can perform on resources. There is also cluster-wide RBAC using ClusterRoles and ClusterRoleBindings, but that's not typically needed for CKAD.

Roles define permissions for resources in a namespace, while ClusterRoles define permissions across the entire cluster.
Rolebindings bind a Role to a user or service account, granting them the permissions defined in the Role.

#### Example Role and RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ninjanamespace
  name: pod-ninja
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

It is possible to do it imperatively as well:

```bash
kubectl create role pod-ninga --verb=get,list,watch --resource=pods --namespace ninjanamespace
``` 

If you want to use all verbs:

```bash
kubectl create role pod-ninja --verb='*' --resource=pods --namespace ninjanamespace
``` 

Rolebinging
If we create a Role, we defined what is allowed. But if we really want to use it, we need to connect this role to either a user or a service account. This is done with RoleBinding.

Here some example from the docs:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
# This role binding allows "jaja" to read pods in the "default" namespace.
# You need to already have a Role named "pod-ninja" in that namespace.
kind: RoleBinding
metadata:
  name: pod-admin-binding
  namespace: studybuddies
subjects:
# You can specify more than one "subject"
- kind: User
  name: jaja # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" specifies the binding to a Role 
  kind: Role #this must be Role 
  name: pod-ninja # this must match the name of the Role you wish to bind to
  apiGroup: rbac.authorization.k8s.io
  ```

  Good news! We can create RoleBindings imperatively as well:

```bash
k create rolebinding pod-admin-binding --role=pod-ninja --user=jaja --namespace studybuddies
```
In general:

```bash
k create rolebinding <binding name> --role=<role name> --serviceaccount=<namespace>:<serviceaccount> --namespace studybuddies
```
How to find out what permissions a user or service account has?

```bash
k auth can-i <verb> <resource type> --as system:serviceaccount:<namespace>:<serviceaccount>
```

### 3. Admission Control
Admission controllers enforce policies on objects after authentication and authorization, but before they’re persisted. In CKAD, you're not asked to configure them, but should understand how they might reject or mutate your resources (e.g., missing resource limits or disallowed security contexts).

### TASK! (#5)

Create a Role named `loyal-role` in the `studybuddies` namespace that allows to read and list pods. 
Then create a RoleBinding that binds this role to the ServiceAccount `loyalservant` we created some time ago within the same namespace.

Once done, send some happiness to the channel chat!

## Wrap up
I don't know how, but the sixth part of our Study Buddies series is successfully finished :)

Today, we have learned:

* a bit about API deprecations
* we repeated some of the useful kubectl commands for inspecting our enviroment
* What are requests, limits, quotas and how to define them
* We learned about SecurityContexts and how to use them
* We learned about authentication, authorization and admission control in Kubernetes

That is something! We have covered a LOT up until now, soon you will be ready for the exam! In case of any feedback that could help us improve the sessions, please let me know - the content is here for you and we want to have it as efficient and useful and fun as possible.




