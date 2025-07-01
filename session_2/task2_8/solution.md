At first, create the base with the command:

```bash
k create deploy nostalgic -n studybuddies --image=busybox --replicas=2 --dry-run=client -oyaml -- sh -c 'echo "Best chapter in the world is $BESTCHAPTERINTHEWORLD" && sleep 3600' > nostalgic.yaml
```

You will get the following YAML manifest:

```bash
cat nostalgic.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nostalgic
  name: nostalgic
  namespace: studybuddies
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nostalgic
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nostalgic
    spec:
      containers:
      - command:
        - sh
        - -c
        - echo "Best chapter in the world is $BESTCHAPTERINTHEWORLD" && sleep 3600
        image: busybox
        name: busybox
        resources: {}
status: {}
```
Now, you can [check the docs](https://kubernetes.io/docs/concepts/configuration/configmap/#configmaps-and-pods) and add the environment variable `BESTCHAPTERINTHEWORLD` from the `holyconfig` ConfigMap inspired by the examples that you can find there.


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nostalgic
  namespace: studybuddies
  labels:
    app: nostalgic
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nostalgic
  template:
    metadata:
      labels:
        app: nostalgic
    spec:
      containers:
      - name: busybox
        image: busybox
        command:
        - sh
        - -c
        - echo "Best chapter in the world is $BESTCHAPTERINTHEWORLD" && sleep 3600
        env:
        - name: BESTCHAPTERINTHEWORLD
          valueFrom:
            configMapKeyRef:
              name: holyconfig
              key: BESTCHAPTERINTHEWORLD
```
