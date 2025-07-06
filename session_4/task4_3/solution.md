At first, let's create the deployment "base" imperatively:

```bash
k create deploy -n studybuddies log-writer --image=busybox --replicas=1 --dry-run=client -oyaml > log-writer.yaml
```
```bash
cat log-writer.yaml
```
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: log-writer
  name: log-writer
  namespace: studybuddies
spec:
  replicas: 1
  selector:
    matchLabels:
      app: log-writer
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: log-writer
    spec:
      containers:
      - image: busybox
        name: busybox
        resources: {}
status: {}
```
Now, let's edit the `log-writer.yaml` file to have the log writer and reader containers, as well as the shared volume. Easiest way is to use the [examples from the official documentation in the volumes section](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-configuration-example).

```bash
vim log-writer.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: log-writer
  name: log-writer
  namespace: studybuddies
spec:
  replicas: 1
  selector:
    matchLabels:
      app: log-writer
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: log-writer
    spec:
      containers:
      - image: busybox
        name: log-writer
        command: ["sh", "-c", "while true; do echo \"Just another boring log... $(date)\" >> /shared/log.txt; sleep 5; done"]                                                                            # Added command
        volumeMounts:                                                                     # Added volumeMounts section for log-writer container
        - mountPath: /shared                                                              # Added volumeMounts section for log-writer container
          name: shared-logs                                                               # Added volumeMounts section for log-writer container
      - image: busybox                                                                    # Added log-reader container
        name: log-reader                                                                  # Added log-reader container
        command: ["sh", "-c", "while true; do cat /shared/log.txt; sleep 5; done"]        # Added command
        volumeMounts:                                                                     # Added volumeMounts section for log-reader container
        - mountPath: /shared                                                              # Added volumeMounts section for log-reader container
          name: shared-logs                                                               # Added volumeMounts section for log-reader container
      volumes:                                                                            # Added volumes section
      - name: shared-logs                                                                 # Added volumes section
        emptyDir: {}                                                                      # Added volumes section. If there is no special configuration for it, use curly braces: `{}`.
status: {}
```
Now, let's apply the changes:

```bash
k apply -f log-writer.yaml
```
Let's check the status of the deployment:

```bash
k get deploy -n studybuddies log-writer

NAME         READY   UP-TO-DATE   AVAILABLE   AGE
log-writer   1/1     1            1           2m
```

```bash
k get pods -n studybuddies -l app=log-writer 

NAME                          READY   STATUS    RESTARTS   AGE
log-writer-5b46db6dfb-jb7g8   2/2     Running   0          2m   # your pod suffix will be different
```
Now, let's check the logs of the log-reader container:

```bash
k logs -n studybuddies log-writer-5b46db6dfbjb7g8 -c log-reader -f # your pod suffix will be different

Just another boring log... Sun Jul  6 15:18:14 UTC 2025
Just another boring log... Sun Jul  6 15:18:14 UTC 2025
Just another boring log... Sun Jul  6 15:18:19 UTC 2025
Just another boring log... Sun Jul  6 15:18:14 UTC 2025
Just another boring log... Sun Jul  6 15:18:19 UTC 2025
Just another boring log... Sun Jul  6 15:18:24 UTC 2025
Just another boring log... Sun Jul  6 15:18:14 UTC 2025
Just another boring log... Sun Jul  6 15:18:19 UTC 2025
Just another boring log... Sun Jul  6 15:18:24 UTC 2025
Just another boring log... Sun Jul  6 15:18:29 UTC 2025
... and so on
```

With -f flag, the command will run in the foreground and you will see the logs in real-time.
With -c flag, you specify the container you want to see the logs from. In this case, we want to see the logs from the log-reader container.


Hooray! You have successfully finished the task! :)
