SESSION 8, 16.7.2025 
========================

* Ingress, Use Ingress rules to expose applications
* Blue/Green, Canary, Rolling updates
* Provide and troubleshoot access to applications via services
* Demonstrate basic understanding of NetworkPolicies
* Helm (just basics for CKAD)
* Kustomize (just basics for CKAD)


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
    - port: 80                                     # Exposed service port
      targetPort: 8080                             # Container port
```

*What this does:*
- Exposes your app to external traffic via a cloud provider's LoadBalancer.
- The service is reachable via an external IP (automatically assigned, will not work with local environment).
- Internally, traffic is routed to Pods with label app: myapp, hitting port 8080 on the container.

*Use this when:
- You're in a cloud environment (Openstac, AWS, GCP, Azure...)
- You need external access to your app.
- You want automatic IP + DNS assignment via the provider.


### BONUS: ExternalName Service

A Service of type ExternalName creates a DNS alias inside the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cute-external-service
  namespace: studybuddies
spec:
  type: ExternalName
  externalName: httpbin.org
```

In the example above, when looking up the host cute-external-service.prod.svc.cluster.local, the cluster DNS Service returns a CNAME record with the value httpbin.org.

Let's try it together!

In the folder [externalname](session_7/externalname), you will find two files: [pod.yaml](session_7/externalname/pod.yaml) and [service.yaml](session_7/externalname/service.yaml). Apply them in the `studybuddies` namespace.

```bash
k apply -f session_7/externalname/pod.yaml
k apply -f session_7/externalname/service.yaml
```
Now, let's test it by running a curl command in the pod:

```bash
k exec -it curl-test -n studybuddies -- curl cute-external-service/get
```

>Note: httpbin.org is a free, open-source HTTP request & response testing service. It's designed for developers to inspect HTTP requests, simulate different kinds of responses and test HTTP clients (e.g., curl, Postman, code). /get is one of its endpoints that returns a JSON response with details about the request made to it.


### Headless Service

A Headless Service is a Service with no ClusterIP. It doesn’t load balance - instead, it lets you reach individual Pod IPs directly.

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
Headless services are most commonly used with StatefulSets, where each pod needs a stable DNS name.


```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: studybuddies
spec:
  clusterIP: None                       # None = Headless
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
  serviceName: nginx                    # Must match the headless service name
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

Let's try it together! In the folder [headless](session_7/headless), you will find two files: [service.yaml](session_7/headless/service.yaml) and [statefulset.yaml](session_7/headless/statefulset.yaml). Apply them in the `studybuddies` namespace.

And now, let's test it by running a curl command in the pod:


```bash
k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

curl echo-0.echo-headless.studybuddies.svc.cluster.local:8080
```


>Notes: In the context of CKAD, you should be able to create a Service YAML from scratch or imperatively, connect pods to services using labels/selectors and understand how DNS resolution works (`my-service.my-namespace.svc.cluster.local`)


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



## Network Policies

## Helm

you should know how to use Helm to deploy applications, but only at a basic user level, not authoring charts or deep templating

1. Install and Use a Chart
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-nginx bitnami/nginx

2. Upgrade a Release
helm upgrade my-nginx bitnami/nginx --set service.type=NodePort

3. Uninstall a Release
helm uninstall my-nginx


4. View Installed Releases
helm list


5. Inspect a Chart or Values
helm show values bitnami/nginx

In the CKAD exam, you might be asked to:
Deploy a Helm chart from a public repo

Set specific values (e.g., replicas, service type)

Upgrade or delete a release

What You don’t need to know:
Writing custom Helm charts (Chart.yaml, templates, etc.)

Helm hooks, complex values.yaml logic

### TASK! (#2)

Install the Bitnami NGINX Helm chart in the studybuddies namespace.
Name the release webserver, and make sure the Service is of type NodePort.


## Kustomize

you should know how to use it, but only at a practical, basic level. You're not expected to master advanced overlays or plugin systems.

1. What Kustomize Is
A tool built into kubectl (kubectl apply -k) for customizing Kubernetes YAML without modifying the originals.

It works by combining base YAML files and applying patches, name prefixes, labels, etc.

2. Basic Concepts You Must Understand
Directory structure (typical):

my-app/
├── deployment.yaml
├── service.yaml
└── kustomization.yaml


kustomization.yaml example:

resources:
  - deployment.yaml
  - service.yaml

namePrefix: studybuddies-
commonLabels:
  app: myapp


What this does:
Includes deployment.yaml and service.yaml

Adds a name prefix like studybuddies-deployment

Adds a label app=myapp to all objects


3. What CKAD Might Ask You to Do
Create or modify a kustomization.yaml

Deploy resources using:
kubectl apply -k ./my-app
Add a label or namePrefix using Kustomize

Understand how patches or environment-specific configs are applied


 What You Do Not Need to Know
No need for advanced overlays or generators

No need to write strategic merge patches or JSON6902 patches

No need to install Kustomize separately (it's built into kubectl)


Summary Table
Topic	Required for CKAD
Understand kustomization.yaml	✅ Yes
Use kubectl apply -k	✅ Yes
Add labels, prefixes	✅ Yes
Use overlays or advanced patches	❌ No
Understand Kustomize structure	✅ Yes
