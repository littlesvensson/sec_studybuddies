SESSION 7, 14.7.2025 
========================

* Understand authentication, authorization and admission control
* Service
* Ingress, Use Ingress rules to expose applications
* Blue/Green, Canary, Rolling updates
* Provide and troubleshoot access to applications via services


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


* We learned about authentication, authorization and admission control in Kubernetes
