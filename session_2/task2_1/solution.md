We will export the manifest with the help of the `--dry-run=client -oyaml` option:

```bash
k run juchjuch --image=curlimages/curl --dry-run=client -oyaml -- curl -s https://icanhazdadjoke.com/ > juchjuch.yaml

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