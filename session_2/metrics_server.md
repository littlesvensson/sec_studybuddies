Metrics server can be install through the following manifest:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Sometimes in kind or other local clusters, the metrics-server needs extra flags due to certificate issues. You may need to edit the deployment like this:

```bash
 k edit deploy -n kube-system metrics-server
```

```yaml
containers:
- name: metrics-server
  args:
    - --kubelet-insecure-tls
``` 
