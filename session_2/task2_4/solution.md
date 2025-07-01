Apply the manifest in the studybuddies namespace:

```bash
k apply -f mylovelyllamaset.yaml -n studybuddies
```
Scale the replicaset to 5 replicas:

```bash
k scale rs mylovelyllamaset --replicas=5 -n studybuddies
```
