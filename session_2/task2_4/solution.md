Imperatively:

```bash
k create cj almostfunny --image=curlimages/curl --schedule="*/5 * * * *" -- curl -s https://icanhazdadjoke.com/
```

Or declaratively:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  creationTimestamp: null
  name: almostfunny
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: almostfunny
    spec:
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - command:
            - curl
            - -s
            - https://icanhazdadjoke.com/
            image: curlimages/curl
            name: almostfunny
            resources: {}
          restartPolicy: OnFailure
  schedule: '*/5 * * * *'
status: {}
```