We will export the manifest with the help of the `--dry-run=client -oyaml` option:

```bash
k run juchjuch --image=busybox --dry-run=client -oyaml -- curl -s https://icanhazdadjoke.com/ > juchjuch.yaml

```

This will be your output:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: juchjuch
  name: juchjuch
spec:
  containers:
  - args:
    - curl
    - -s
    - https://icanhazdadjoke.com/
    image: busybox
    name: juchjuch
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
Now we can edit the manifest in Vim. Open the file `juchjuch.yaml` (or whatever name you chose) in Vim:

```bash
vim juchjuch.yaml
```
and edit the image to `curlimages/curl`. You can do this by navigating to the line with the image and changing it. In Vim, you can press `i` to enter insert mode, make your changes, and then press `Esc` to exit insert mode. Finally, save and exit Vim by typing `:x`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: juchjuch
  name: juchjuch
spec:
  containers:
  - args:
    - curl
    - -s
    - https://icanhazdadjoke.com/
    image: curlimages/curl # Changed from busybox to curlimages/curl
    name: juchjuch
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

and then apply it:

```bash
k apply -f juchjuch.yaml
```

We can check the pod with:

```bash
k get po juchjuch
```

The log of the pod will show you a dad joke:

```bash
k logs juchjuch
```