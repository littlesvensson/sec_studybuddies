### Create the base imperatively with using dry-run

```bash
kubectl run president --dry-run=client -oyaml > president.yaml
```
```bash
cat president.yaml
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: president
  name: president
spec:
  containers:
  - image: nginx:1.25
    name: president
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Now we can have a look in the docs [how the examples for sidecar containers and init containers look like](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/#init-containers-in-use) so we can steal the code from there and adjust appropriately.

Alternatively, we do not need to do any dry run, copy the whole [example](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/#sidecar-example) from the docs and adjust it to our needs.

```bash
vim superpod.yaml
```


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: president
  labels:
    app.kubernetes.io/name: president
spec:
  containers:
  - name: president
    image: nginx
  - name: heartbeat
    image: busybox
    command: ['sh', '-c', 'echo "Initializing..." && sleep 5']
  initContainers:
  - name: waiter
    image: busybox
    command: ['sh', '-c', 'while true; do echo "Im still alive $(date), time to go to bed for 10 seconds!"; sleep 10; done']
```

```bash
k apply -f superpod.yaml # You can also use `k create -f president.yaml` if you prefer
```

```bash
k get po # Check if the pod is running
```

```bash
k logs po superpod -c heartbeat # Check the logs of the sidecar container
```
