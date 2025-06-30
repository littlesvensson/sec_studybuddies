### Sidecar containers pattern

```yaml
containers:
- name: app
  image: my-app
- name: fluentd
  image: fluentd
  volumeMounts:
  - name: logs
    mountPath: /var/log/app
```

### Init containers pattern

```yaml
initContainers:
- name: init-db
  image: busybox
  command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
```
