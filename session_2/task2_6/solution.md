Imperatively:

```bash
k create cj fortuneteller --image=curlimages/curl --schedule="*/5 * * * *" -- curl https://helloacm.com/api/fortune/
```

If you wanted to see the generated manifest with `k create cj fortuneteller --image=curlimages/curl --schedule="*/5 * * * *" --dry-run=client -oyaml -- curl https://helloacm.com/api/fortune/`, you would get an output like this:


```yaml
kind: CronJob
metadata:
  creationTimestamp: null
  name: fortuneteller
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: fortuneteller
    spec:
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - command:
            - curl
            - https://helloacm.com/api/fortune/
            image: curlimages/curl
            name: fortuneteller
            resources: {}
          restartPolicy: OnFailure
  schedule: '*/5 * * * *'
status: {}

```
