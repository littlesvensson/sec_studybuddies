SESSION 2, 3.7.2025 
========================

## Content of the session:

**Application Design and Build**
* Imperative vs declarative approach
* Understand multi-container Pod design patterns (e.g. sidecar, init)
* Learn about Kubernetes cluster, nodes and namespaces
* Understand ReplicaSets and how to scale them

**wrap up, homework, next steps**

### Imperative vs declarative approach

During the exam, you will mostly use the imperative approach, which means you will use commands to create and manage resources directly. 

```bash
k run <pod name> --image=<image name>
```

This is different from the declarative approach, where you define resources in YAML files and apply them using `kubectl apply`. Often, you will need to use the `--dry-run=client -oyaml` option to generate the YAML manifest of the resource you are creating, tweak it a bit and then apply it using `kubectl apply -f <file.yaml>`. 

```bash
k run <pod name> --image=<image name> --dry-run=client -oyaml
``` 

```bash
k run <pod name> --image=<image name> --dry-run=client -oyaml > <name your file to edit>.yaml
k apply -f <name your file to edit>.yaml
``` 

In the above case, applying the dry run manifest will create the same pod as the `k run` command, but it allows you to edit the manifest before applying it.

You can get a yaml file also from an existing resource with `k get <resource type> <resource name> -o yaml > <file name>.yaml` and then edit it in your favorite editor (e.g. Vim) and apply it using `kubectl apply -f <file name>.yaml`.

### TASK! (#1)
* Export a manifest for pod with name 'almostfunny', image 'busybox' and command `curl -s https://icanhazdadjoke.com/` with help of `--dry-run=client -oyaml` and save the manifest to a file called 'almostfunny.yaml'
* Oh no! The manifest has wrong image in it. Edit the pod's manifest in *VIM* and change the image to 'curlimages/curl'
* Create the pod using the edited manifest file
* Check the logs of the pod with `k logs almostfunny` and paste you joke into the chat. Let's see if at least one of them will be funny

> Note: command always needs to go as the last one. `--dry-run=client -oyaml` needs to be before the command, otherwise it will not work.

Time CAP: 2 minutes

Don't forget to use some of the VIM shorcuts you learned in this session, such as `i` to enter insert mode, `x` to delete characters, `dw` to delete words etc...

Stuck on the way? No worries, you can check the solution in the [./task2_1/solution.md](./task2_1/solution.md) file.

#### Useful commands for getting information about Pods

**k get po**:	List all Pods in the current namespace <br>
**k get po <pod name> -o wide**:  Get more details about the Pod (node, IP, etc.) <br>
**k describe po <pod name>**:	Detailed info about the Pod (events, conditions, etc.) <br>
**k get po <pod name> -o yaml**:	Get full YAML manifest of the Pod <br>
**k logs po <pod name>**:  Get logs from the Pod's main container <br>
**k logs po <pod name> -c <container name>**:  Get logs from a specific container in the Pod <br>

### Multi-container Pod design patterns (e.g. sidecar, init and others)

If there are multiple containers in a Pod?
They:
* Run on the same node
* Share the same IP address
* Can talk to each other using localhost
* Can share storage/volumes
* Are co-located and scheduled together

You use multi-container Pods when containers need to work closely together, often in tightly-coupled roles.

#### 1. Sidecar Pattern
**Purpose**: Add capabilities to the main container <br>
**Typical Use Case**: Log shipping, proxying, configuration reloaders <br>
**Example**: A web server (main container) + a Fluentd container (sidecar) to forward logs.

```yaml
containers:
- name: app
  image: my-app
- name: fluentd
  image: fluentd
  volumeMounts:
  - name: logs
    mountPath: /var/log/app
```

#### 2. Init Container Pattern
**Purpose**: Run setup logic before main containers start <br>
**Typical Use Case**: Downloading code, waiting for dependencies, setting up databases <br>
**Key Feature**: They always run sequentially and must complete successfully before main containers start.

```yaml
initContainers:
- name: init-db
  image: busybox
  command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
```

Lets have a look what documentation examples show regarding the topic:
* [PODs in general](https://kubernetes.io/docs/concepts/workloads/pods/)
* [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
* [sidecar containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)

In the exam, there is a high chance that you will need to create a workload resource (like Deployment, DaemonSet, or CronJob) that uses multi-container Pods. You will need to understand how to define the containers, their images, and how they interact with each other. This is something you cannot do just with the `k run` command, as it is not suitable for creating complex resources with multiple containers.

Instead, you will need to use the `k create` / `k apply` command with help of the `--dry-run=client -o yaml` option to generate the YAML manifest of the resource you are creating, tweak it a bit and then apply it using `k apply -f <file.yaml>` or just by tweaking the YAML copied from the docs.

### TASK! (#2)

Create a Pod with name `president` with Init, Main, and Sidecar Containers. You can use Kubernetes documentation or/and `--dry-run=client -o yaml` + adjust values to create the manifest. 

##### 1. Init Container
**Container name**: waiter <br>
**Image**: busybox <br>
**Command**: Simulate a wait using: ['sh', '-c', 'echo "Initializing..." && sleep 5'] <br>

##### 2. Main Container (also pod name)
**Name**: president <br>
**Image**: nginx <br>

##### 3. Sidecar Container
**Name**: heartbeat <br>
**Image**: busybox <br>
**Command**: Print a heartbeat message every 10 seconds: ['sh', '-c', 'while true; do echo "Im still alive $(date), time to go to bed for 10 seconds!"; sleep 10; done'] <br>

*Do the file changes in VIM.* Once done, write "I am happy" to the chat. Or you can say it to the micropohone :)

Time CAP: 4 minutes

Hint: Kubernetes docs is your friend. Try to find a similar example and change the values appropriately. 

Hint2: Not found any nice example? I guess a good base for the manifest can be found in the official documentation in the init containers section: [Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/#init-containers-in-use).

Stuck on the way? No worries, you can check the solution in the [./task2_2/solution2_2.md](./task2_2/solution.md) file.

## Kubernetes Cluster, Nodes and Namespaces

Before we will continue with the pods and their parents, let's clarify three other terms in Kubernetes: Cluster, Namespace and Node.

#### Cluster
A cluster is a set of nodes (machines) that run containerized applications. Or basically its a playground you get access to from the CAAS team where you can do some Kubernetes magic. It consists of a control plane that manages the cluster and worker nodes that run the applications. The control plane makes decisions about the cluster, such as scheduling applications, maintaining their desired state, scaling them up or down, and rolling out updates.

#### Node 
A node is a physical or virtual machine that runs your application workloads. It is part of the Kubernetes cluster and hosts pods, which are the smallest deployable units in Kubernetes.

![Kubernetes Nodes](../assets/kubernetes_nodes.png) <br>
Image source: [expertflow.com](https://docs.expertflow.com/cx/4.3/kubernetes-deployment-getting-started)

#### Commands to check nodes
```bash
k get no # list nodes
k get no --show-labels # list nodes with labels
k get no -owide # list nodes with more details
k top no # show resource usage of nodes
```

> Note: If you want to get the command k top no to work, you need to have the metrics server installed in your cluster otherwise you will get an error message `error: Metrics API not available`. More info for getting this work in Kind and Minikube is to be found in [metrics_server.md](./metrics_server.md) file. If you will need the command during the exam, metrics server would be preinstalled for you already. 

### Homework(#1)
* Install the metrics server in your local cluster. You can use the [metrics_server.md](./metrics_server.md) file as a guide.
* Check the CPU and memory of nodes in your cluster using the `k top no` command.
* Check the CPU and memory of all pods in your cluster using the `k top po` command.

#### Namespace
A namespace is a way to divide cluster resources according to a specific logic - defined by you/admin/owner of the cluster. It acts like a virtual cluster within the Kubernetes cluster, helping organize and isolate resources (like pods, services, etc.) for different teams or projects.

![Kubernetes Namespaces](../assets/kubernetes_namespaces.png) <br>
Image source: [devopssec.fr](https://www.devopssec.fr/article/environnements-ephemeres-kubernetes)

Very simply said, pods deployed within one namespace cannot access resources in another namespace unless explicitly allowed. (Depending on the cluster configuration, RBAC, Network Policies, etc.). Pods deployed in the same namespace can be from various nodes, but they can communicate with each other without any issues.

#### Basic commands for working with namespaces
```bash
k create ns <namespace name> # create namespace
k get ns # list namespaces
k get ns --show-labels # list namespaces with their respective labels
k delete ns <namespace name> # delete namespace
k edit ns <namespace name> # edit namespace
k label ns <namespace name> <label name>=<label value> # add label to namespace
k label ns <namespace name> <label name>- # remove label from namespace
```
In the exam, you will often get task in combination with a particular namespace. It is crucial not to forget to specify the namespace in your commands, otherwise you might end up creating resources in the default namespace and lose all the points for the task. 

Imperatively:
```bash
k create deploy <deployment name> --image=<image name> --replicas=<number of replicas> -n <namespace name>
```
Let's see it through manifest file:

```bash
k create deploy cutedeployment --image=nginx -n studybuddies --dry-run=client -oyaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: cutedeployment
  name: cutedeployment
  namespace: studybuddies # namespace where the deployment will be created defined here under metadata
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cutedeployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: cutedeployment
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
status: {}
```

### TASK! (#3)

- Create a namespace called `studybuddies`
- Label the namespace with `team=studybuddies`
- Check all namespaces and their labels `k get <resource name> --show-labels`

Time CAP: 2 minutes.
Stuck on the way? Check the solution in the [./task2_3/solution.md](./task2_3/solution.md) file.

## PODS PARENTS

Pods are the smallest deployable units in Kubernetes, but they are often managed by higher-level abstractions that provide additional features like scaling, rolling updates, and self-healing. These abstractions are known as **controllers**.

### Replicasets

A replicaset ensures that a specified number of pod replicas are running at any given time. It can be used to scale applications up or down and provides self-healing capabilities by replacing failed pods.

#### Features:
- Replication:	Maintains a stable set of running pods
- Self-healing:	Recreates pods if they crash or are deleted
- Label selector support:	Matches pods using labels to manage them
- Scaling: We can scale the number of pod replicas up or down by changing the `replicas` field in the replicaset configuration

> Note: Replicasets are most often used indirectly through Deployments, which manage the lifecycle of replicasets and provide additional features like rolling updates. Also, it is not possible to create them imperatively using `k create rs...`

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: mylovelyllamaset
  namespace: studybuddies
spec:
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
```
We cannot create replicaset imperatively using `k create rs...`, but we can scale the number of replicas in an existing replicaset using the command:

```bash
k scale rs mylovelyllamaset --replicas=5 -n studybuddies
```
### TASK! (#4)
- Create / apply the yaml file in the [task2_4/ folder](./task2_4/) to create a replicaset called `mylovelyllamaset` in the `studybuddies` namespace.
- Scale the replicaset to 5 replicas using **imperative** approach (with command).

Time CAP: 2 minutes.
Stuck on the way? Check the solution in the [./task2_4/solution.md](./task2_4/solution.md) file.

## Wrap up
Congratulations on completing the second session of the Study Buddies series!

Today, we have learned:
* Imperative vs declarative approaches in Kubernetes
* Multi-container Pods and design patterns like sidecar and init containers
* Basics of clusters, nodes, and namespaces
* How to work with ReplicaSets and scale them 

I truly hope this session gave you some knowledge and inspiration. Please let me know your feedback and any improvement suggestions, this should help us all with preparation and the right feedback would make this serie more efficient.















