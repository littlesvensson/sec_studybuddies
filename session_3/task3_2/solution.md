Imperatively:

```bash
k create cj fortuneteller -n studybuddies --image=curlimages/curl --schedule="*/5 * * * *" -- curl https://helloacm.com/api/fortune/
```

If you wanted to see the generated manifest with `k create cj fortuneteller -n studybuddies --image=curlimages/curl --schedule="*/5 * * * *" --dry-run=client -oyaml -- curl https://helloacm.com/api/fortune/`, you would get an output like this:


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
> Note that the `creationTimestamp` is set to `null` because the cronjob has not been created yet. Also, when writing the command for the main container imperatively, you ALWAYS have to write the command as the last argument, otherwise it will be interpreted as a flag for the `k create` command. Also the `--dry-run=client -oyaml` needs to be before the container command.

Five minutes later, you can check in logs what awaits you in the future :) Or if you want to see the output immediately, you can create a job from the cronjob template:

```bash
k create job --from=cronjob/fortuneteller fortuneteller-now
k logs job/fortuneteller-now
```
