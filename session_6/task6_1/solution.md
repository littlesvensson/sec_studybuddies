At first, we will try to apply the manifest as it is, but we will get an error:

```bash
k apply -f sickcronjob.yaml
error: resource mapping not found for name: "fortune" namespace: "" from "sickcronjob.yaml": no matches for kind "CronJob" in version "v1"
ensure CRDs are installed first
```
As the error suggests, the current Kubernetes version does not have a CronJob resource with the version `v1`. We need to use one that is available in the cluster.

```bash
k api-resources | grep cron
cronjobs                          cj           batch/v1                               true         CronJob
```
BINGO! We see that the apiVersion in the manifest is missing the group prefix `batch/`. Let's fix that:

```yaml
apiVersion: batch/v1 # Corrected apiVersion with the right group prefix
kind: CronJob
metadata:
  name: sadcronjob
spec:
  jobTemplate:
    metadata:
      name: sadcronjob
    spec:
      template:
        spec:
          containers:
          - command:
            - curl
            - https://helloacm.com/api/fortune/
            image: curlimages/curl
            name: fortune
            resources: {}
          restartPolicy: OnFailure
  schedule: '*/5 * * * *'
status: {}
```

Now we can apply the manifest successfully:

```bashk apply -f sickcronjob.yaml
cronjob.batch/sadcronjob created
```






