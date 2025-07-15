SESSION 9, 18.7.2025 
========================

* Network Policies
* Helm (just basics for CKAD)
* Kustomize (just basics for CKAD)
* Recap and last tips before the exam


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
