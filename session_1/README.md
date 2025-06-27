SESSION 1, 30.6.2025 
========================

## Content of the session:

* Welcome to the Study Buddies POC (theme CKAD)
    * intro, principles, concepts, difference between CKA & CKAD
    * most important hints - kubectl shortcuts, docs usage, ALIASes…

* VIM shortcuts intro

* **Application Design and Build (20%)**
    * Define, build and modify container images
    * Choose and use the right workload resource (Deployment, DaemonSet, CronJob, etc.)
    * Understand multi-container Pod design patterns (e.g. sidecar, init and others)
    * Utilize persistent and ephemeral volumes


## Concepts of the sessions in general:

This experiments theme is CKAD, the Kubernetes Application Developer certification. The sessions are designed to be interactive, with a focus on hands-on practice and real-world scenarios. Each session will cover specific topics related to the CKAD exam objectives, with a mix of theory and practical exercises.

Please bear in mind that the sessions are not a supercomplete replacement for the official training with lots of theory and deep-dive insights, but rather a practical approach to the exam objectives. The goal is to focus on the most important aspects of the exam, with providing useful resources to additional knowledge gathering and practice in YOUR free time.

### CKAD vs CKA

The CKAD (Certified Kubernetes Application Developer) certification is focused on the skills required to design, build, and run applications on Kubernetes. It emphasizes application development, deployment, and a bit of basic troubleshooting within a Kubernetes environment. The CKA (Certified Kubernetes Administrator) certification, on the other hand, is more focused on the skills required to administer and manage Kubernetes clusters.

In other words, the CKAD is more about the application side of Kubernetes, while the CKA is more about the infrastructure and operational side. The CKAD exam tests your ability to work with Kubernetes resources, understand application design patterns, and utilize Kubernetes features to build and deploy applications effectively. As a CKAD test maker, you are in the position of being a developer who just needs to make sure his or her apps run smoothly on Kubernetes, while the CKA test maker is more focused on the operational aspects of managing the Kubernetes cluster itself.

### Hints before the exam:

* Go throught the exam scenarios:
    * Killershell (available through the purchased course)
    * Killercoda scenarios for CKAD (https://killercoda.com/scenarios/ckad)

### Hints for the exam in general:

#### Time management

The exam is time-limited, so practice managing your time effectively. Use shortcuts and aliases to speed your workflow. If you get stuck on a question, move on and come back to it later if time allows. The exam environment allows you to flag the questions you want to revisit, so use that feature wisely.



I highly recommend the following ALIASes to speed up your exam flow:

```bash

export do=“--dry-run=client -o yaml”  # usage example: k create deploy nginx --image=nginx $do
export now=“--force --grace-period 0” # usage example: k delete pod x $now
```
* It is highly beneficial to use shortcuts for resources definitions (po, rs, sts, k...) 
```bash

k api-resources

configmaps                        cm           v1                                     true         ConfigMap
endpoints                         ep           v1                                     true         Endpoints
events                            ev           v1                                     true         Event
limitranges                       limits       v1                                     true         LimitRange
namespaces                        ns           v1                                     false        Namespace
nodes                             no           v1                                     false        Node
persistentvolumeclaims            pvc          v1                                     true         PersistentVolumeClaim
persistentvolumes                 pv           v1                                     false        PersistentVolume
pods                              po           v1                                     true         Pod
replicationcontrollers            rc           v1                                     true         ReplicationController
resourcequotas                    quota        v1                                     true         ResourceQuota
serviceaccounts                   sa           v1                                     true         ServiceAccount
customresourcedefinitions         crd,crds     apiextensions.k8s.io/v1                false        CustomResourceDefinition
daemonsets                        ds           apps/v1                                true         DaemonSet
deployments                       deploy       apps/v1                                true         Deployment
replicasets                       rs           apps/v1                                true         ReplicaSet
statefulsets                      sts          apps/v1                                true         StatefulSet
horizontalpodautoscalers          hpa          autoscaling/v2                         true         HorizontalPodAutoscaler
cronjobs                          cj           batch/v1                               true         CronJob
certificatesigningrequests        csr          certificates.k8s.io/v1                 false        CertificateSigningRequest
events                            ev           events.k8s.io/v1                       true         Event
ingresses                         ing          networking.k8s.io/v1                   true         Ingress
networkpolicies                   netpol       networking.k8s.io/v1                   true         NetworkPolicy
priorityclasses                   pc           scheduling.k8s.io/v1                   false        PriorityClass
storageclasses                    sc           storage.k8s.io/v1                      false        StorageClass
...

```

* Imperative commands is the way to go, as you will not have time to write YAML files during the exam. This is a bit different from the real world scenarios, where gitops and YAML files are the best practice.
* Docs are your friend, especially because of the example yaml files. During the exam, you can use the official Kubernetes documentation as well as Kubernetes blog although that one is not very useful.

## VIM shortcuts intro

Vim is a powerful text editor that is often used in the Kubernetes ecosystem. You will need to be familiar with basic Vim commands to navigate and edit files during the exam. Here are some essential Vim shortcuts:

Basic Movement: **h j k l** <br>
Moving with words: **w e b** <br>
Insert Mode: **i a** <br>
Insert at Line Ends: **I O** <br>
Opening Lines: **o O** <br>
Deleting: **x dd dw** <br>
Copying and Pasting: **y p** <br>
Select more lines: **v** <br>

During hands-on tasks, it would be good to practice these shortcuts. You can use the Vim Hero website to practice Vim shortcuts interactively.

And now, time for the first game!

GAME: [Bug Squasher](https://www.vim-hero.com/lessons/basics-review)

**How to play:**
* 1: Eliminate bugs by jumping over them with the word motions w, e, and b.
* 2: Use insert mode to restore the characters devoured by bugs.
* Time cap: 5 minutes

Other sources for Vim practice:
* Vimtutor - just write 'vimtutor' in your terminal
* [ThePrimeagen](https://www.youtube.com/watch?v=X6AR2RMB5tE&t=360s) really nice intro to Vim
* most important - practice, practice, practice on real files


## DOCKER magic

Dockerfile is a text file that contains instructions on how to build a Docker image. It defines the base image, the commands to run, and the files to include in the image. The Dockerfile is used to create a Docker image that can be run as a container. We need it to build our application image that we will run in Kubernetes.

There is a simple Dockerfile example in the `session_1` directory, which you can use to build your first Docker image. The Dockerfile is a simple Python application that prints a message to the console.

```dockerfile
# Image from which we are starting
FROM python:3.13-slim

# Seting working directory
WORKDIR /app

# Copy of a beautiful script into the container
COPY miaumiau.py .
ENV IFEELLIKEA="FRISBEE"

# Running the script on container start
CMD ["python", "miaumiau.py"]
```

In the CKAD exam, it is not necessary to have too much deep knowledge of Dockerfile syntax and the docs about this topic are 
not available during the exam. It is enough to have some basic knowledge of how to build a Docker image and run it in a container.

**Task time**: 
* clone the repo if you haven't done it yet
* go to the `session_1` directory
* make sure you have Docker or Podman installed
* How do you feel today? Change the `IFEELLIKEA` environment variable in the Dockerfile to something else than "FRISBEE" (e.g. "STUDY BUDDY", "KUBERNETES SUPERSTAR", "DOCKERNINJA", etc.)
* build the Docker image with the command: docker build -t miaumiau&lt;&lt;yourname&gt;&gt;:1h .
* run the Docker image with the command: docker run --rm miaumiau&lt;&lt;yourname&gt;&gt;:1h
* push ttl.sh image registry: docker push ttl.sh/miaumiau&lt;&lt;yourname&gt;&gt;:1h
* If you don't have a Docker Hub account, you can use Podman to run the image locally without pushing it to a registry.
* Run the image with Podman using the command: podman run --rm miaumiau:1.0



> Note:
> [ttl.sh](https://ttl.sh/) is a supercool, free, temporary container image registry provided by Replicated. It allows you to:
> * Push container images using Docker or Podman
> * Set a Time To Live (TTL) after which the image is automatically deleted
> * Use it without creating an account
> In other words, a beautiful tool for demos, testing and study sessions like this one!


For additional information on Dockerfile syntax, you can refer to the [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).
More on building images via [docker](https://docs.docker.com/get-started/docker-concepts/building-images/) and [podman](https://docs.podman.io/en/latest/Commands.html) can be found in their respective sections.
Dockerfile best practices can be found in the [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) documentation.

Homework! 
Killercoda will be your friend through the whole (not only) CKAD journey. Feel free to explore the scenarios dediacated to the Dockerfile and image building:
* [Dockerfile](https://killercoda.com/scenarios/dockerfile)
When working on exercises, try to use at least some of the VIM shortcuts you learned in this session :)

## PODS playground

### What the hell are pods?
Pods are the smallest deployable units in Kubernetes and can contain one or more containers. These containers share the same network namespace and can communicate with each other using localhost.

What is the Pod resource for?
The Pod resource tells Kubernetes:

What container(s) to run (like Docker images)

How to run them (CPU, memory, ports, etc.)

Where they should live (on which node)

How they connect to the network

What to do if the container crashes

Why not just run containers directly?
Because Kubernetes manages containers through Pods, not directly.

If you run a container in Kubernetes, it always wraps it in a Pod.

Even a single container needs to live in a Pod.

 If there are multiple containers in a Pod?
They:

Run on the same machine

Share the same IP address

Can talk to each other using localhost

Can share storage

This is great for helper containers, like:

A web server + a log collector

A main app + a sidecar

In most Pods, there's usually one main container, and that's the one doing the "real work" (like running your app).

What can we "do" with resources in general?

create
edit
describe
delete
replace
apply
scale
rollout
label
annotate
expose
logs

A pod example


TASK!

Create and run a temporary Kubernetes pod that:

* Uses the wernight/funbox container image
* Name of the pod is meowmaster
* Runs the *nyancat* command
* Launches in *interactive mode*
* Cleans itself up automatically after exit (no leftover pod)



```bash
kubectl run meowww -it --rm --restart=Never --image=wernight/funbox -- nyancat






kubectl get pods	List all Pods in the current namespace
kubectl get pods -A	List all Pods in all namespaces
kubectl describe pod <pod-name>	Detailed info about the Pod (events, conditions, etc.)
kubectl get pod <pod-name> -o yaml	Get full YAML manifest of the Pod
kubectl get pod <pod-name> -o wide

k run 
