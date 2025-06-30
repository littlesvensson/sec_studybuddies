At first, you will need to create a Pod with the name `juchjuch` and the image `nginx:latest`. The fastest way is to use the imperative approach:

```bash
k run juchjuch --image=nginx:latest
```
You can check the pod was created successfully by running:

```bash
k get po juchjuch
```
and the image used by the Pod:

```bash
k describe po juchjuch
```
or

```bash
k get po juchjuch -oyaml
```

Next, you will need to export the Pod's YAML manifest, edit it to change the image to `nginx:1.23`, and then apply the changes. You can do this in two ways:

1. Export the Pod's YAML manifest, edit it, and then apply it:

```bash
k get po juchjuch -o yaml > juchjuch.yaml
```
Edit the `juchjuch.yaml` file to change the image to `nginx:1.23`. You will need to remove some fields that are not editable, such as `status`, `metadata.creationTimestamp`, and `metadata.resourceVersion`. After editing, apply the changes:

```bash
k apply -f juchjuch.yaml
```
Note: you cannot use k create, because the Pod already exists. You need to use k apply or k replace to update/replace the existing Pod.

2. Use the `--dry-run=client -o yaml` option to generate the YAML manifest of the resource you are creating, tweak it and then apply it:

```bash
k run juchjuch --image=nginx:1.23 --dry-run=client -oyaml > juchjuch.yaml
```
and then apply it:

```bash
k apply -f juchjuch.yaml
```
If you want to be superfast, you can do it all in one command:

```bash
k run juchjuch --image=nginx:1.23 --dry-run=client -oyaml | k apply -f -
```
This command will create the Pod with the name `juchjuch` and the image `nginx:1.23` in one go.