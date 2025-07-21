(FINAL) SESSION 10, 21.7.2025 
========================

* Network Policies
* Helm  
* Kustomize
* Last Tips 


## Network Policies pt. 2

To understan Network Policies OR/AND syntax better, I highly recommend experimenting with the [Network Policy Editor by Isovalent] (https://editor.networkpolicy.io/). Just make sure to play within the Kubernetes Network Policy Tab and not the Cilium Network Policy Tab.

### TASK! (#1)

For the following task, please use the [Killercoda playground](https://killercoda.com/playgrounds/scenario/kubernetes), as with Kind we do not have any CNI for NetworkPolicies in place.

- Create a new namespace called mystery.
- In the folder [task9_3](task9_3), you have manifest definitions for two Deployments, one Service and a NetworkPolicy. Apply them to the `mystery` namespace.
- It seems something is wrong with this setup. Why? Try to fix the issue by **keeping NetworkPolicy without changes**. You can check if the change is or is not working by running the following commands:

```bash
k exec -n mystery deploy/frontend -- curl backend
```

## Helm

Helm is a Kubernetes package manager that simplifies deploying, upgrading, and managing applications using reusable, versioned templates called charts. You should know how to use Helm to deploy applications, but only at a **basic user level**.

#### Install and Use a Chart

```bash
helm repo add <name it how you like> <repository URL>
```

#### Update the Helm repo with the latest charts:
```bash
helm repo update
```

#### Install a Chart to create a release
```bash
helm install <name> <chart>
```

#### Upgrade a Release
```bash
helm upgrade <release> <chart> --set replicaCount=3
```

#### Upgrade a Release with custom values
```bash
helm upgrade <release> <chart> --set replicaCount=3
```

```bash
helm show values <chart>
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

### TASK! (#4)

- create a new namespace called `ingress`
- in the newly created namespace, install the Bitnami NGINX Helm chart. The url to the chart is https://charts.bitnami.com/bitnami. Use the latest version of the chart.
- name the release webserver



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