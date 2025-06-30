### Create the base imperatively with using dry-run

In this case, the easiest way would be to use the example from official documentation in the init containers section as base:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app.kubernetes.io/name: MyApp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', "until nslookup myservice.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for myservice; sleep 2; done"]
  - name: init-mydb
    image: busybox:1.28
    command: ['sh', '-c', "until nslookup mydb.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for mydb; sleep 2; done"]
```
mytask2.yaml:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: president # changed
  labels:
    app.kubernetes.io/name: president # changed
spec:
  containers:
  - name: president # changed
    image: nginx # changed
  - name: heartbeat # added
    image: busybox # added
    command: ['sh', '-c', 'while true; do echo "Im still alive $(date), time to go to bed for 10 seconds!"; sleep 10; done'] # changed
  initContainers:
  - name: waiter # changed
    image: busybox # changed
    command: ['sh', '-c', 'echo "Initializing..." && sleep 5'] # changed

```bash
k apply -f mytask2.yaml # You can also use `k create -f president.yaml` if you prefer
```

```bash
k get po # Check if the pod is running
```

```bash
k logs po superpod -c heartbeat # Check the logs of the sidecar container
```
