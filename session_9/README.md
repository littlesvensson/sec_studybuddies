SESSION 9, 18.7.2025 
========================

* Network Policies
* Helm (just basics for CKAD)
* Kustomize (just basics for CKAD)
* Recap and last tips before the exam

## Ingress

An Ingress resource in Kubernetes manages external access to services within a cluster, typically via HTTP or HTTPS. It defines rules for routing traffic based on the request's host or path to the appropriate backend services.

The rules specified within by the ingress object are interpreted by an **Ingress Controller** which is a Kubernetes component that watches Ingress resources and manages the actual routing of external HTTP/HTTPS traffic to the appropriate services inside the cluster. The Ingress Controller does not come by default; you need to deploy one, such as the NGINX Ingress Controller or Traefik. <br>

In the context of CKAD, you should be able to create an Ingress resource, understand its basic structure, and know that an Ingress Controller is required for it to function. However, you are not expected to install or configure an Ingress Controller in the exam environment.

Let's have a look at the basic structure of an Ingress resource from the documentation:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx-example                   # Define the Ingress Controller to use
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix                            # Request path based on a prefix match
        backend:
          service:
            name: test
            port:
              number: 80
```
**nginx.ingress.kubernetes.io/rewrite-target: /** : rewrite the matched request path to / before forwarding it to the backend service. If your Ingress rule matches /testpath as in the example, and a client requests /testpath/home, the path sent to the backend will be rewritten to /home <br>
**ingressClassName**: Specify the Ingress Controller you want to use. You can get the name of the Ingress Controller by running `k get ingressclass`. <br>
**pathType**: Defines how the path is matched. Common values are `Prefix` (matches all paths starting with the specified path) and `Exact` (matches only the exact path) <br>
**service.name**: The name of the service to route traffic to <br>
**service.port.number**: The port on the service to route traffic to <br>
**backend**: Defines the backend service to route traffic to based on the specified rules. It's a combination of the service name and port. <br>

> Note: It is possible to define a default backend service that will handle requests that do not match any of the specified rules. This is done by adding a `defaultBackend` section in the `spec` of the Ingress resource. However, this is [usually setup on the level of the Ingress Controller](https://kubernetes.github.io/ingress-nginx/examples/customization/custom-errors/), not in the Ingress resource itself.

Common Ingress Tasks in CKAD:

- Create an Ingress to expose a service
- Route multiple paths or hostnames
- Fix an Ingress that's misconfigured (e.g., wrong pathType, wrong service name)

> Note:TLS Support - You’re not required to deeply configure TLS, but should recognize a TLS block:

```yaml
tls:
- hosts:
  - myapp.example.com
  secretName: tls-secret
```

### Task! (#4)

This time, the task is awaiting you in the [Killercoda: Ingress create section].(https://killercoda.com/killer-shell-ckad/scenario/ingress-create). Once you will get the last check successfully, please do not close the scenario, just express your happiness in the chat, we will do some check together.

The check:

```bash
curl -H "Host: world.universe.mine" http://localhost:<ingress controller node port>/europe  
curl -H "Host: world.universe.mine" http://localhost:<ingress controller node port>/asia
```
You're sending the request to the node port, which is the NodePort exposed by the NGINX Ingress Controller. This internally forwards the request to port 80 of the Ingress controller pod. In Killercoda, localhost works because you're testing from the controlplane node, which runs the ingress controller. The part -H "Host: world.universe.mine" is crucial because it tells the Ingress controller which host to match against the rules defined in the Ingress resource. The Ingress rule matches by Host. We are imitating a real-world scenario where you would access the service via a domain name (world.universe.mine) instead of an IP address.



## Network Policies

## Helm

Helm is a Kubernetes package manager that simplifies deploying, upgrading, and managing applications using reusable, versioned templates called charts. You should know how to use Helm to deploy applications, but only at a **basic user level**.

#### Install and Use a Chart

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-nginx bitnami/nginx
```

#### Upgrade a Release
```bash
helm upgrade my-nginx bitnami/nginx --set replicaCount=3
```

#### Uninstall a Release
```bash
helm uninstall my-nginx
```

#### View Installed Releases
```bash
helm list
helm list --all-namespaces
helm list -n <namespace>
```

#### Inspect a Chart or Values
```bash
helm show values bitnami/nginx
```

### TASK! (#2)

Install the Bitnami NGINX Helm chart in the studybuddies namespace.
Name the release webserver, and make sure the Service is of type NodePort.

## Kustomize

Kustomize is a tool built into kubectl (kubectl apply -k) for customizing Kubernetes YAML without modifying the originals. You should know how to use it, but only at a practical, basic level. You're not expected to master advanced overlays or plugin systems.

It works by combining base YAML files and applying patches, name prefixes, labels, etc.

#### Basic Concepts 
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
- Includes deployment.yaml and service.yaml
- Adds a name prefix like studybuddies-deployment
- Adds a label app=myapp to all objects

#### What CKAD Might Ask You to Do
- Create or modify a kustomization.yaml
- Deploy resources using:
- k apply -k ./my-app
- Add a label or namePrefix using Kustomize

#### What You Do Not Need to Know
- No need for advanced overlays or generators
- No need to write strategic merge patches or JSON6902 patches
- No need to install Kustomize separately (it's built into kubectl)
