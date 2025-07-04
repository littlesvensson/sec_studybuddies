SESSION 3, 4.7.2025 
========================

## Content of the session:

* Choose and use the right workload resource (continue after replicasets)
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

### Daemonsets

Daemonsets ensure that a copy of a specific pod is running on all (or a subset of) nodes in the cluster. They are typically used for background tasks that need to run on every node, such as logging agents or monitoring tools.

> Note: Daemonset cannot be created imperatively. But can be deleted, edited..

What can you do with Daemonsets with help of kubectl?
```bash
k edit ds <daemonset name>
k delete ds <daemonset name>
k get ds <daemonset name>
k get ds -A # get all daemonsets in all namespaces
k get ds <daemonset name> -o yaml # get the manifest of the daemonset
k rollout restart ds <daemonset name> # restart the daemonset
k rollout status ds <daemonset name> # check the status of the daemonset rollout
k describe ds <daemonset name> # describe the daemonset
```
Rollout restart is useful when you want to restart the daemonset pods without changing the manifest. The reason could be for example that you have updated a configmap or secret that is connected to the daemonset, so the pod needs to be restarted in order to mount to the new configmap/secret. It will trigger a rolling update of the daemonset, which will restart all pods managed by the daemonset. 


### TASK! (#1, together)

Let's try to apply the [Daemonset from the docs example](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#create-a-daemonset).

```bash
vim ds.yaml
```
Copy the manifest:

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

With daemonsets, as well as with statefulsets or deployments, we can use the `k rollout` command to manage the rollout of the daemonset. For example, we can restart the daemonset to apply changes or to ensure that the pods are running with the latest configuration.

```bash
k rollout restart ds -n kube-system fluentd-elasticsearch 
```
The default rollout strategy for daemonsets is `RollingUpdate`, which means that the pods will be updated one by one, ensuring that there is always at least one pod running on each node. At first, the pod on a node will be terminated, and then a new pod will be created on the same node. 

Unlike with Deployments, which we will see in a while, DaemonSets are built on the principle of one Pod per node.

```bash
k rollout status ds fluentd-elasticsearch -n kube-system
```

Delete the DaemonSet

```bash
k delete ds fluentd-elasticsearch -n kube-system
```
### Jobs

A Job is a Kubernetes controller that is designed for short-lived, one-time tasks. It ensures a pod runs to completion, and if the pod fails, the Job will retry it (based on backoffLimit). Once the task is complete, the Job exits successfully.

```bash
k create job hello --image=busybox --dry-run=client -oyaml -- echo "Hello dear studybuddies"
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

```bash
k explain job.spec
k explain job.metadata --recursive
```


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

### TASK! (#2)

Create a cronjob:
- name of the cronjob: fortuneteller
- namespace: studybuddies
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
```

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

If you want to add the change of the changed-cause to the history, this is being done with the annotation:
```yaml
metadata:
  annotations:
    kubernetes.io/change-cause: "Updated image to v2.0"
```

### TASK! (#3)

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

## HOMEWORK(#2)

If you have not done some of the tasks during the session, you can do them at home :)
Also, there are some additional tasks for you to practice at Killercoda CKAD section:
- [VIM Setup](https://killercoda.com/killer-shell-ckad/scenario/vim-setup)
- [SSH Basics](https://killercoda.com/killer-shell-ckad/scenario/ssh-basics)
- [Configmap Access in Pods](https://killercoda.com/killer-shell-ckad/scenario/configmap-pod-access)
- [Readiness Probe](https://killercoda.com/killer-shell-ckad/scenario/readiness-probe)
- [Build and Run a Container](https://killercoda.com/killer-shell-ckad/scenario/container-build)
- [Rollout Rolling](https://killercoda.com/killer-shell-ckad/scenario/rollout-rolling)


* Different workload resources in Kubernetes, such as Deployments, ReplicaSets, DaemonSets, StatefulSets, Jobs, and CronJobs
* How to perform rolling updates and manage application deployments
* ConfigMaps and Secrets for managing configuration and sensitive data
* How to use probes and health checks to ensure the reliability of your applications