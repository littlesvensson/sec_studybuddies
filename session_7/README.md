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

### TASK! (#1)

Create a Role named `loyal-role` in the `studybuddies` namespace that allows to read and list pods. 
Then create a RoleBinding that binds this role to the ServiceAccount `loyalservant` we created some time ago within the same namespace.

Once done, send some happiness to the channel chat!


* We learned about authentication, authorization and admission control in Kubernetes


## Services

Services in Kubernetes provide stable networking for Pods, allowing them to communicate with each other and with external clients. They abstract away the underlying Pod IPs, which can change over time.

What a Service Does
A Service provides a stable network identity (IP + DNS name) to a set of Pods.
It routes traffic to matching Pods using label selectors.
It decouples clients from Pods — which may come and go.


 Types of Services (Know These!)
Type	Purpose	CKAD Notes
ClusterIP	Exposes service within the cluster	Default, used for internal communication
NodePort	Exposes service on a port on each Node’s IP	Useful for local testing, not recommended for production
LoadBalancer	Uses cloud provider's external LB	For public access in cloud setups
ExternalName	Maps to an external DNS	Rarely used in CKAD; just know what it is

### ClusterIP (default)

The default type, ClusterIP, exposes the service on a cluster-internal IP. This means that the service is only reachable from within the cluster. It is used for internal communication between Pods.   

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: myapp
  ports:
    - port: 80        # Service port
      targetPort: 8080 # Container port
```

### NodePort
NodePort exposes the service on a static port on each Node's IP. This allows external traffic to access the service by hitting any Node's IP and the specified port. It's useful for local testing, but not recommended for production.

```yaml
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30036
```
### LoadBalancer
LoadBalancer is used in cloud environments to expose the service externally. It creates an external load balancer that routes traffic to the service. This is the most common way to expose services in production.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: studybuddies
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80          # Exposed service port
      targetPort: 8080  # Container port
```

What this does:
Exposes your app to external traffic via a cloud provider's LoadBalancer.

The service is reachable via an external IP (automatically assigned).

Internally, traffic is routed to Pods with label app: myapp, hitting port 8080 on the container.

✅ Use this when:
You're in a cloud environment (AWS, GCP, Azure, etc.)

You need external access to your app.

You want automatic IP + DNS assignment via the provider.




 Important Concepts
Selector-based services: Automatically route to matching Pods.

TargetPort: Port on the container.

Port: Port exposed by the Service.

NodePort: Exposed on every node at a static port (30000–32767).

In CKAD, You Must Be Able To:
✅ Create a Service YAML from scratch or imperatively (e.g. kubectl expose)

✅ Connect Pods to Services using labels/selectors

✅ Use kubectl port-forward for quick access in exam

✅ Debug Service routing (kubectl get endpoints, curl, etc.)

✅ Understand how DNS resolution works (my-service.my-namespace.svc.cluster.local)


kubectl expose pod mypod --port=80 --target-port=8080 --name=mypod-service --type=ClusterIP


Summary Cheat Sheet
Key Concept	What You Need to Know
Service types	ClusterIP, NodePort, LoadBalancer
Ports	port, targetPort, nodePort
Selector	Matches Pods using labels
DNS names	Services have stable DNS within the cluster
Debugging	Use kubectl get endpoints, describe, logs



LoadBalancer requires a cloud provider.

In CKAD exam (which runs in a local cluster), LoadBalancer may not assign an external IP — you’ll often use port-forward or NodePort instead.


Headless Service: What It Is
A Headless Service is a Service with no ClusterIP. It doesn’t load balance; instead, it lets you reach individual Pod IPs directly.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-headless-service
  namespace: studybuddies
spec:
  clusterIP: None
  selector:
    app: myapp
  ports:
    - port: 80
```

clusterIP: None disables the default virtual IP.

DNS queries return A records for each Pod backing the service.

Useful for:

StatefulSets

Peer-to-peer apps (e.g. databases, message queues)

When each Pod needs to be contacted individually


```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: studybuddies
spec:
  clusterIP: None  # Headless
  selector:
    app: nginx
  ports:
    - port: 80
```

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx
  namespace: studybuddies
spec:
  serviceName: nginx   # must match the headless service name
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
```


What Happens:
Kubernetes creates:

nginx-0, nginx-1, nginx-2 pods (stable identities)

DNS entries:

nginx-0.nginx.studdybuddies.svc.cluster.local

nginx-1.nginx.studdybuddies.svc.cluster.local

etc.

The headless service enables direct DNS resolution to Pod IPs — no load balancing.



kubectl exec -it some-pod -n studybuddies -- nslookup nginx-0.nginx

### TASK! (#2)
Create a ClusterIP Service named backend-service in the studybuddies namespace.

This Service should:

Target Pods with label app=backend

Forward traffic from port 80 to container port 5000

Make sure the backend is accessible from within the cluster using the name:
backend-service.studdybuddies.svc.cluster.local


## Ingress

An Ingress is an API object that:

Exposes HTTP/HTTPS routes from outside the cluster to services inside.

Acts like a reverse proxy: routes traffic based on hostnames and paths.

Requires an Ingress Controller (e.g., NGINX Ingress Controller) to function.

What You Need to Know for CKAD
1. Understand Basic Ingress YAML
2. Know That an Ingress Controller Is Required
3. Use kubectl port-forward for testing



Common Ingress Tasks in CKAD
You may be asked to:

Create an Ingress to expose a service

Route multiple paths or hostnames

Fix an Ingress that's misconfigured (e.g., wrong pathType, wrong service name)


5. Optional: TLS Support
You’re not required to deeply configure TLS, but should recognize a TLS block:

```yaml
tls:
- hosts:
  - myapp.example.com
  secretName: tls-secret
```


## Blue/Green Deployment (CKAD Level)

Concept:
Run two separate versions of the app (e.g., v1 = "blue", v2 = "green") in parallel.
Switch traffic from blue to green by updating the Service selector.

What You Should Know:
Deploy two Deployments:

blue-deployment (label version: blue)
green-deployment (label version: green)

The Service routes traffic based on version.

### Task! (#3)

You already have a Deployment myapp-blue running in the studybuddies namespace.
Your task is to:

Deploy a new version of the app called myapp-green with label version: green.

Update the existing Service myapp-service to route traffic to the green version instead of blue.



# Service pointing to blue
selector:
  app: myapp
  version: blue


To switch traffic to green, change the selector to version: green.

Skills CKAD tests:
Modify Service.spec.selector

Label Deployments appropriately

Understand impact of traffic shifting


## Canary Deployment
Concept:
Deploy a new version (e.g., v2) to a subset of users by running a small number of pods alongside the stable version (v1).

Concept:
Deploy a new version (e.g., v2) to a subset of users by running a small number of pods alongside the stable version (v1).

What You Should Know:
Create a second Deployment with fewer replicas and a different label (e.g., version: canary)

Use label selectors to route some traffic to canary

Either:

Add both v1 and canary Pods under same Service, OR

Create two Services, and control traffic split externally (e.g., via Ingress or client-side logic)

```yaml
# Stable Deployment (v1)
metadata:
  name: myapp-v1
  labels:
    app: myapp
    version: v1

# Canary Deployment (v2)
metadata:
  name: myapp-v2
  labels:
    app: myapp
    version: canary

# Shared Service selects both
spec:
  selector:
    app: myapp
```

If v1 has 5 pods and canary has 1, about 1/6 of requests will hit canary (round-robin).

CKAD Skills:
Create multiple Deployments

Control traffic using replica count

Understand basic traffic splitting via label-based Services

In CKAD, You Might Be Asked To:
Deploy a new canary version alongside the current one

Change a Service to point to the new version (blue/green)

Scale down the old deployment after verification

### TASK! (#4)

You already have a Deployment myapp-stable with:

5 replicas
label: version: stable
Create a new Deployment myapp-canary:

1 replica
label: version: canary
image: nginx:1.21
container port: 8080

Update the Service myapp-service (already selects app: myapp) to include both versions (which already happens if both have app: myapp).

💡 Result:
5/6 of requests go to stable
1/6 go to canary

