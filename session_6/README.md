SESSION 5, 9.7.2025 
========================

## Content of the session:

**Application Environment, Configuration and Security**
* Understand requests, limits, quotas, Define resource requirements
* Understand Application Security (SecurityContexts, Capabilities, etc.)
* Understand authentication, authorization and admission control:
    Knowing that Pods use service accounts
    Understanding how to give a service account permissions (which uses Role/RoleBinding)
    Being able to troubleshoot permission errors (e.g., app can't list pods)
    Knowing that authorization is required when your app talks to the Kubernetes API

* Service
* Ingress, Use Ingress rules to expose applications
* Blue/Green, Canary, Rolling updates


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

1. Authentication (Who are you?)
Kubernetes checks who is making the request.

This could be a user, service account, or external identity (via certificates, tokens, etc.).

Most commonly in CKAD, this shows up when:

Your pod is running with a service account

You get Unauthorized errors if the kubeconfig is wrong or permissions are missing

CKAD-level takeaway:
Be aware that service accounts are how workloads authenticate to the API server.

2. Authorization (What can you do?)
After identifying who, Kubernetes checks what they’re allowed to do.

It uses things like:

RBAC (Role-Based Access Control) — the most common

kubectl auth can-i to test permissions

CKAD-level takeaway:

Know how to check if your service account or user can perform an action:

bash
Copy
Edit
kubectl auth can-i get pods --as system:serviceaccount:myns:myaccount
3. Admission Control (Should we allow it?)
Runs after authentication and authorization, before the object is persisted.

Controls like:

ValidatingAdmissionWebhook

MutatingAdmissionWebhook

LimitRanges, PodSecurity, ResourceQuotas

 CKAD-level takeaway:

You may encounter errors from things like a validating webhook or namespace quota.

For example:

"Pod denied: CPU request too high"

"Missing label required by policy"

 In Practice
Component	What it does	CKAD relevance
Authentication	Identifies the requestor	Mostly behind the scenes
Authorization	Approves/rejects based on roles	Important when using service accounts, RBAC
Admission control	Final checks/patches before storing	May block objects if they violate policy

 What You Should Practice
Create and use service accounts

Set automountServiceAccountToken: false when needed

Use kubectl auth can-i to troubleshoot permissions

Recognize common admission control errors in kubectl describe or kubectl get events




## Resource management



