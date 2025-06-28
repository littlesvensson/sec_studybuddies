### Create the base imperatively with using dry-run

```bash
kubectl run superpod --dry-run=client -oyaml > superpod.yaml
```
```bash
cat superpod.yaml
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: superpod
  name: superpod
spec:
  containers:
  - image: nginx:1.25
    name: superpod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Now we can have a look in the docs [how the examples for sidecar containers and init containers look like](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/#init-containers-in-use) so we can steal the code from there and adjust appropriately.

```bash
vim superpod.yaml
```


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: superpod
spec:
  initContainers:  # Added line for init container
  - name: wait-init # Added line for init container
    image: busybox:1.28 # Added line for init container
    command: ['sh', '-c', 'echo "Initializing..." && sleep 5'] # Added line for init container

  containers:
  - name: superpod 
    image: nginx:1.25

  - name: heartbeat # Added line for sidecar container
    image: busybox:1.28 # Added line for sidecar container
    command: ['sh', '-c', 'while true; do echo "Sidecar alive at $(date)"; sleep 10; done'] # Added line for sidecar container
    ```
```bash
k apply -f superpod.yaml # You can also use `k create -f superpod.yaml` if you prefer
```

```bash
k get po # Check if the pod is running
```

```bash
k logs po superpod -c heartbeat # Check the logs of the sidecar container
```
