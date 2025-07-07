We will create holyconfig ConfigMap with usage of --from-literal option:

```bash
k create cm holyconfig -n studybuddies --from-literal=BESTCHAPTERINTHEWORLD=security
```
The second task will use the --from-file option as we want to create a ConfigMap from a file. The path will depend on your current working directory, so make sure to adjust it accordingly. The command will look like this in case you are in the session_3 directory:

```bash
k create cm holyconfig2 -n studybuddies --from-env-file=task3_4/config
```

We can check their existence:

```bash
k get cm -n studybuddies

k get cm -n studybuddies
NAME               DATA   AGE
holyconfig         1      44h
holyconfig2        1      4s
```


We can also check the content of the ConfigMap:

```bash
k get cm -n studybuddies -o yaml

apiVersion: v1
items:
- apiVersion: v1
  data:
    BESTCHAPTERINTHEWORLD: security
  kind: ConfigMap
  metadata:
    creationTimestamp: "2025-07-05T18:49:52Z"
    name: holyconfig
    namespace: studybuddies
    resourceVersion: "25381"
    uid: f622437b-c9f3-4ca0-87fb-9f8fee979130
- apiVersion: v1
  data:
    BEST_CHAPTER_IN_THE_WORLD_IN_CASE_SECURITY_CHAPTER_DOES_NOT_EXIST: security will
      still be in our hearts and common its the best chapter no matter what
  kind: ConfigMap
  metadata:
    creationTimestamp: "2025-07-07T15:17:02Z"
    name: holyconfig2
    namespace: studybuddies
    resourceVersion: "121591"
    uid: bede84b6-f72e-4288-a48f-c2712128a8a5
```