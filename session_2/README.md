SESSION 2, 2.7.2025 
========================

## Content of the session:

**Application Design and Build**
* Imperative vs declarative approach
* Understand multi-container Pod design patterns (e.g. sidecar, init and others)
* Learn about Kubernetes cluster, nodes and namespaces
* Choose and use the right workload resource 
  * Deployment
  * ReplicaSet
  * DaemonSet
  * StatefulSet
  * Job
  * Cronjob

**Application Deployment**
* Understand Deployments and how to perform rolling updates
* Implement probes and health checks

**Application Environment, Configuration and Security**
* Understand ConfigMaps
* Understand Secrets

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

You can get a yaml file also from an existing resource with `k get <resource type> <<resource name>> -o yaml > <name your file to edit>.yaml` and then edit it in your favorite editor (e.g. Vim) and apply it using `kubectl apply -f <file name>.yaml`.

### TASK! (#1)
* Export a manifest for pod with name 'almostfunny', image 'busybox' and command `curl -s https://icanhazdadjoke.com/` with help of `--dry-run=client -oyaml` and save the manifest to a file called 'almostfunny.yaml'
* Oh no! The manifest has wrong image in it. Edit the pod's manifest in *VIM* and change the image to 'curlimages/curl'
* Create the pod using the edited manifest file
* Check the logs of the pod with `k logs almostfunny` and paste you joke into the chat. Let's see if at least one of them will be funny

> Note: command always needs to go as the last one. `--dry-run=client -oyaml` needs to be before the command, otherwise it will not work.

Time CAP: 2 minutes

Don't forget to use some of the VIM shorcuts you learned in this session, such as `i` to enter insert mode, `x` to delete characters, `dw` to delete words etc...

Stuck on the way? No worries, you can check the solution in the [./task2_2/solution.md](./task2_2/solution.md) file.

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

In the exam, there is a high chance that you will need to create a workload resource (like Deployment, DaemonSet, or CronJob) that uses multi-container Pods. You will need to understand how to define the containers, their images, and how they interact with each other. This is something you cannot do just with the `kubectl run` command, as it is not suitable for creating complex resources with multiple containers.

Instead, you will need to use the `kubectl create` / `kubectl apply` command with help of the `--dry-run=client -o yaml` option to generate the YAML manifest of the resource you are creating, tweak it a bit and then apply it using `kubectl apply -f <file.yaml>` or just by tweaking the YAML copied from the docs.

### TASK! (#2)

Create a Pod with Init, Main, and Sidecar Containers. You can use Kubernetes documentation or/and `--dry-run=client -o yaml` + adjust values to create the manifest. 

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

![Kubernetes Nodes](../assets/kubernetes_nodes.png)
Image source: [expertflow.com](https://docs.expertflow.com/cx/4.3/kubernetes-deployment-getting-started)

#### Commands to check nodes
```bash
k get no # list nodes
k get no --show-labels # list nodes with labels
k get no -owide # list nodes with more details
k top no # show resource usage of nodes
```

> Note: If you want to get the command k top no to work, you need to have the metrics server installed in your cluster otherwise you will get an error message `error: Metrics API not available`. More info for getting this work in Kind and Minikube is to be found in [metrics_server.md](https://github.com/littlesvensson/sec_studybuddies/blob/main/session_2/metrics_server.md) file. If you will need the command during the exam, metrics server would be preinstalled for you already. 

### Homework(#1)
* Install the metrics server in your local cluster. You can use the [metrics_server.md](https://github.com/littlesvensson/sec_studybuddies/blob/main/session_2/metrics_server.md) file as a guide.
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
k get ns --show-labels # list nodes with labels
k get ns -owide # list nodes with more details
k delete ns <namespace name> # show resource usage of nodes
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
  namespace: studybuddies
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

### Daemonsets

Daemonsets ensure that a copy of a specific pod is running on all (or a subset of) nodes in the cluster. They are typically used for background tasks that need to run on every node, such as logging agents or monitoring tools.

> Note: Daemonset cannot be created imperatively. But can be deleted, edited..

### TASK! (#5, together)

Let's try to apply the [Daemonset from the docs example](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#create-a-daemonset).

```bash
vim ds.yaml
```
copy the manifest:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      # these tolerations are to have the daemonset runnable on control plane nodes
      # remove them if your control plane nodes should not run pods
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: quay.io/fluentd_elasticsearch/fluentd:v2.5.2
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      # it may be desirable to set a high priority class to ensure that a DaemonSet Pod
      # preempts running Pods
      # priorityClassName: important
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```
Apply it:

```bash
k apply -f ds.yaml
```

Check the pods in all namespaces:
```
k get po -A -owide | grep fluentd-elasticsearch
```
The pods will be created on all nodes (each pod in different node), and all of them will be within the kube-system namespace.

Delete the daemonset

```bash
k delete ds fluentd-elasticsearch -n kube-system
```
### Jobs

A Job is a Kubernetes controller that is designed for short-lived, one-time tasks. It ensures a pod runs to completion, and if the pod fails, the Job will retry it (based on backoffLimit). Once the task is complete, the Job exits successfully.

```bash
kubectl create job hello --image=busybox -- echo "Hello from Kubernetes"
```

```bash
k get job
k describe job hello
k get job hello -oyaml
```

Let's check a simple job from the official documentation that calculates the value of pi:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

> Note: Jobs and their pods will be listed also after they are completed unless you either delete them or define .spec.ttlSecondsAfterFinished in the manifest related to the job. In that case the job and its pods will be deleted automatically after the specified time in seconds.

### CronJobs

Cronjobs are used to run jobs on a scheduled basis, similar to the cron utility in Unix/Linux systems. They allow you to specify a time-based schedule for running jobs, such as daily, weekly, or monthly. Otherwise they are basically the same as Jobs.

You can create a cronjob imperatively using the `k create cronjob --image=<image name> --schedule="<schedule>"` command. For example, to create a cronjob that runs every minute and prints the current date and a message:

```bash
k create cj iscreamfor --image=busybox --schedule="* * * * *" -- /bin/sh -c "echo icecream"
``` 
Need to adjust details? Save as yaml file, edit what you need and apply it:
```bash
k create cj iscreamfor --image=busybox --schedule="* * * * *" --dry-run=client -oyaml > cj.yaml -- /bin/sh -c "echo icecream"
```

```bash
cat cj.yaml
```

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  creationTimestamp: null
  name: iscreamfor
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: iscreamfor
    spec:
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - command:
            - /bin/sh
            - -c
            - echo icecream
            image: busybox
            name: iscreamfor
            resources: {}
          restartPolicy: OnFailure
  schedule: '* * * * *'
status: {}
```

More options including cron syntax can be found in the [official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).

### TASK! (#6)

Create a cronjob:
- name of the cronjob: fortuneteller
- name of image: curlimages/curl
- should run every 5 minutes
- command: `curl https://helloacm.com/api/fortune/

Time CAP: 3 minutes.

Stuck on the way? Check the solution in the [./task2_6/solution.md](./task2_6/solution.md) file.

### StatefulSets

StatefulSets are used for managing stateful applications, which require stable, unique network identifiers and persistent storage. They provide guarantees about the ordering and uniqueness of pods, making them suitable for applications like databases or distributed systems.

We cannot create statefulsets imperatively, but we can scale them using the `k scale sts <statefulset name> --replicas=<number of replicas>` command. Also, we can delete and edit stateful sets.

Let's check a [simple statefulset from the official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#components)

We will wait with task for a statefulset until we get to some other necessary concepts like headless service and volume claims. For now, what you need to know is that they are useful for managing stateful application and are ordered.

### Deployments + Rolling updates

Deployments are a higher-level abstraction that manages the lifecycle of pods and replicasets. They provide features like rolling updates, rollbacks, and scaling. Deployments ensure that the desired state of the application is maintained, and they automatically handle updates to the application.

Under the hood, a deployment creates a replicaset that manages the pods. When you update a deployment, it creates a new replicaset with the updated pod template and gradually scales down the old replicaset while scaling up the new one. With deployments, you can perform nice rolling updates that allow you to update your application without downtime. You can also rollback to a previous version if something goes wrong.

![Deployment](../assets/deploy_rs_po.png)
Image source: [kubernetes.io](https://kubernetes.io/docs/concepts/workloads/controllers)

#### Basic commands connected to deployment management:
```bash
k create deploy <deployment name> --image=<image name> --replicas=<number of replicas>
k edit deploy <deployment name>
k scale deploy <deployment name> --replicas=<number of replicas> 
k set image deployment/<name> <container name>=<new image name>

Let's try:

k create deploy importantsession --image=nginx --replicas=3 
k get deploy --watch
k edit deploy importantsession # change the image to busybox, save and exit
k get po --watch
k rollout status deploy/importantsession
k get deploy importantsession -o yaml # check the manifest and image
k scale deploy importantsession --replicas=5 
k set image deploy/importantsession nginx=curlimages/curl # nginx because that is the name of the container in the deployment
```

The amazing feature of deployments is their ability to rollback through history.
```bash
k rollout status deploy/<deployment name> # check the status of the deployment rollout
k rollout undo deploy/<deployment name>
k rollout history deploy/<deployment name>
k rollout undo deploy <deployment name> --to-revision=<revision number>"
```

### TASK! (#7)

* Create a deployment with the following specifications:
  - name: mylittledeploy
  - image: nginx
  - replicas: 3

* When done, scale the deployment to 5 replicas using the imperative approach
* Change the image of the deployment to `busybox` just with command
* Undo the last change

Time CAP: 3 minutes <br>
Stuck on the way? Check the solution in the [./task2_7/solution.md](./task2_7/solution.md) file.

### Implement probes and health checks

#### What Are Probes?
Kubernetes uses probes to check the health of containers. These are automated checks that determine whether to:

- Restart the container (Liveness Probe)
- Send traffic to the container (Readiness Probe)
- Wait before running other probes (Startup Probe)

#### Liveness probe
Checks if the app is alive. If it fails, Kubernetes restarts the container.

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

#### Readiness probe

Checks if the app is ready to receive traffic.
If it fails, the pod is removed from service endpoints but not restarted.

```yaml
readinessProbe:
  tcpSocket:
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```
Readiness and liveness probes can be used in parallel for the same container. Using both can ensure that traffic does not reach a container that is not ready for it, and that containers are restarted when they fail.

####  Startup Probe 
Used when your app takes a while to start.
Only runs during startup, and disables liveness/readiness during that time.

```yaml
startupProbe:
  exec:
    command: ["cat", "/tmp/healthy"]
  failureThreshold: 30
  periodSeconds: 5
```
Startup Probe tells Kubernetes when your container has finished starting up. <br>
Until this probe succeeds:

- Liveness and readiness probes are disabled
- Kubernetes will wait patiently, even if the app is not yet responding

This prevents Kubernetes from killing your container too early just because it takes a while to become ready.


### HOMEWORK! (#1)

Create a deployment with the following specifications:

- *Name*: probeofmylife
- *Namespace*: studybuddies
- *Replicas*: 2
- *Image*: nginxdemos/hello:0.2

*Probes*:
*StartupProbe*
- Use a HTTP GET to /
- *Port*: 80
- *Delay*: Allow up to 30 seconds for the app to start
- *FailureThreshold*: 15
- *PeriodSeconds*: 2

*ReadinessProbe*
- Use HTTP GET to /
- *Port*: 80
- *InitialDelaySeconds*: 5
- *PeriodSeconds*: 5

*LivenessProbe*
- Use HTTP GET to /
- *Port*: 80
- *InitialDelaySeconds*: 10
- *PeriodSeconds*: 10

Use VIM for editing the manifest file. Pay attention to indentation and syntax.

Hint: Create the base with `--dry-run=client -oyaml` option to generate the YAML manifest of the deployment, edit it in VIM and apply it using `kubectl apply -f <file.yaml>`.
Hint 2: Docs are your friend. Copy parts of the code you need for probes!

Stuck on the way? Check the solution in the [./homework2_1/solution.md](./task2_1/solution.md) file.


### Configmaps

ConfigMaps are used to store non-sensitive configuration data in key-value pairs. They allow you to decouple configuration from application code, making it easier to manage and update configurations without changing the application image.

#### Create a ConfigMap
You can create a ConfigMap using a YAML file or imperatively with the `k create cm` command.

```bash
k create configmap <configmap name> --from-literal=key1=value1 --from-literal=key2=value2
``` 

```bash
  kubectl create configmap <configmap name> --from-env-file=path/to/foo.env --from-env-file=path/to/bar.env
```
If you use env-file, the keys within the file will be the names of the variables in the file and the values will be the values of the variables.


```bash
  kubectl create configmap <configmap name> --from-file=key1=/path/to/bar/file1.txt --from-file=key2=/path/to/bar/file2.txt
``` 
In the example above, keys are directly defined.

```bash
kubectl create configmap <configmap name> --from-env-file=path/to/foo.env --from-env-file=path/to/bar.env
``` 

### TASK! (#7)

Create two configmaps:
1. `holyconfig` with two key-value pairs: `BESTCHAPTERINTHEWORLD=security` 
2. `holyconfig2` from a file `config.txt` within the [task2_7/](./task2_7/) folder. 

#### How to use ConfigMaps in Pods
You can use ConfigMaps in your pods by mounting them as volumes or using them as environment variables. <br>
Mounting ConfigMaps as volumes in Kubernetes means making the data stored in a ConfigMap available to a container as files inside the container's filesystem. <br>
We will get to the volumes in one of the following sessions.


Let's check an example [with both methods from the official documentation](https://kubernetes.io/docs/concepts/configuration/configmap/#configmaps-and-pods)


### TASK! (#8)

Create a deployment with 3 replicas within the studybuddies namespace with the name `nostalgic` that uses the `BESTCHAPTERINTHEWORLD` value from the `holyconfig` ConfigMap as an environment variable. 
- deployment name: nostalgic
- replicas: 3
- namespace: studybuddies
- image: busybox
- command: `sh -c "echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600"`
- environment variable: `BESTCHAPTERINTHEWORLD` from the `holyConfig` ConfigMap
- volume mount: `/config` from the `holyConfig2` ConfigMap

Hint: You can design the deployment imperatively using the `k create deploy <name of deployment> -n <namespace name> --replicas=<number of replicas>` -- 'sh -c "echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600"' command, but with the `--dry-run=client -o yaml` flags to generate the YAML manifest. Then you can edit the manifest (add env from configmap) and apply it.

Time CAP: 5 minutes.

```bash

Stuck on the way? Check the solution in the [./task2_8/solution.md](./task2_8/solution.md) file.

### Secrets

Secrets are used to store sensitive information, such as passwords, tokens, or SSH keys. They are similar to ConfigMaps but are designed to handle sensitive data securely. Secrets can be created from literal values, files, or directories. They are stored base64-encoded, not encrypted by default (unless encryption-at-rest is enabled). The topic of encryption-at-rest is a topic of of CKAD exam, but you will encounter it in the CKA. For now, you need to know what secret is, how to create one and how to use it for your workloads.

````bash
k create secret -h

k create secret <typeofsecret> <secret name> [--from-literal=<key>=<value>] [--from-file=<key>=<path>] [--from-env-file=<path>] [--dry-run=client -o yaml] [-n <namespace name>]
```

You can create a secret using a YAML file or imperatively with the `kubectl create secret` command.

```bash
k create secret generic moodoftheday --from-literal=ifeel=euphoric
```
```bash
k create secret generic  --from-file=ssh-privatekey=/path/to/private/key 
```
When using from file, the file name will be used as the key in the secret. If you want to specify a different key name, you can use the `--from-file=<key>=<path>` option.

```bash
k create secret generic my-secret --from-env-file=path/to/secret.env
``` 
With env file, the keys within the file will be the names of the variables in the file and the values will be the values of the variables.

### TASK! (#9)

Create a secret in the namespace `studybuddies` with the name `mydirtysecret` that contains the following key-value pairs:

- key: thebestlecturerever
- value: jaja

When finished, write to the channel "I am a pro." (If doing outside of the session, tell out loud: "I AM A PRO!")

## Wrap up
Congratulations on completing the second session of the Study Buddies series!

Today, we have learned:
* Imperative vs declarative approaches in Kubernetes
* Multi-container Pods and design patterns like sidecar and init containers
* Basic concepts of Kubernetes, including clusters, nodes, and namespaces
* Different workload resources in Kubernetes, such as Deployments, ReplicaSets, DaemonSets, StatefulSets, Jobs, and CronJobs
* How to perform rolling updates and manage application deployments
* ConfigMaps and Secrets for managing configuration and sensitive data
* How to use probes and health checks to ensure the reliability of your applications


I truly hope this session gave you some knowledge and inspiration. Please let me know your feedback and any improvement suggestions, this should help us all with preparation and the right feedback would make this serie more efficient.



## TODO
- Add homework for the session
- Secrets
- explanation for creating configmaps types in command line













