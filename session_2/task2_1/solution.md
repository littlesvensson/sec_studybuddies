Creating a namespace called `studybuddies`:

```bash
k create ns studybuddies
```

Labeling the namespace with `team=studybuddies`:

```bash
k label ns studybuddies team=studybuddies
```
Check the namespaces and their respective labels:

```bash
k get ns --show-labels
```