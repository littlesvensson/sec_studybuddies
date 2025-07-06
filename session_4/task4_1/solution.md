Lets generate the base for our deployment manifest using the `k create deploy` command with the `--dry-run=client -o yaml` flags:

```bash
k create deploy nostalgic -n studybuddies --image=busybox --replicas=3 --dry-run=client -oyaml -- sh -c 'echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600' > nostalgic.yaml
```
This will be your generated output:

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
  replicas: 3
  selector:
    matchLabels:
      app: nostalgic
  strategy: {}
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nostalgic
  name: nostalgic
  namespace: studybuddies
spec:
  replicas: 3
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
        - echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600
        image: busybox
        name: busybox
        resources: {}
status: {}

```
Let's add the environment variable from the `holyConfig` ConfigMap:

```bash
vim nostalgic.yaml
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
  replicas: 3
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
        - echo Best chapter in the world is $BESTCHAPTERINTHEWORLD && sleep 3600
        image: busybox
        name: busybox
        resources: {}
        env:                                     # Added
          - name: BESTCHAPTERINTHEWORLD          # Added
            valueFrom:                           # Added
              configMapKeyRef:                   # Added
                name: holyconfig                 # Added
                key: BESTCHAPTERINTHEWORLD       # Added

status: {}
```

And now we can apply the manifest:

```bash
k apply -f nostalgic.yaml
```
Let's check the logs!

```bash
k logs -l app=nostalgic -n studybuddies # This will show the logs of all pods with the label app=nostalgic in the studybuddies namespace.
```
              