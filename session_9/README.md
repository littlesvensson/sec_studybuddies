SESSION 9, 18.7.2025 
========================

* Network Policies
* Helm (just basics for CKAD)
* Kustomize (just basics for CKAD)
* Recap and last tips before the exam


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
