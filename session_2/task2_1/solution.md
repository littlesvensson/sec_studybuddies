We will export the manifest with the help of the `--dry-run=client -oyaml` option:

```bash
k run almostfunny --image=busybox --dry-run=client -oyaml -- curl -s https://icanhazdadjoke.com/ > almostfunny.yaml

```

This will be your output:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: almostfunny
  name: almostfunny
spec:
  containers:
  - args:
    - curl
    - -s
    - https://icanhazdadjoke.com/
    image: busybox
    name: almostfunny
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
Now we can edit the manifest in Vim. Open the file `almostfunny.yaml` (or whatever name you chose) in Vim:

```bash
vim almostfunny.yaml
```
and edit the image to `curlimages/curl`. You can do this by navigating to the line with the image and changing it. In Vim, you can press `i` to enter insert mode, make your changes, and then press `Esc` to exit insert mode. Finally, save and exit Vim by typing `:x`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: almostfunny
  name: almostfunny
spec:
  containers:
  - args:
    - curl
    - -s
    - https://icanhazdadjoke.com/
    image: curlimages/curl # Changed from busybox to curlimages/curl
    name: almostfunny
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

and then apply it:

```bash
k apply -f almostfunny.yaml
```

We can check the pod with:

```bash
k get po almostfunny
```

The log of the pod will show you a dad joke:

```bash
k logs almostfunny
```