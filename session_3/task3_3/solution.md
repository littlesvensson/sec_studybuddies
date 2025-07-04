Create a deployment:

```bash
k create deploy mylittledeploy --image=nginx --replicas=3
```

Scale the deployment to 5 replicas

```bash
k scale deploy mylittledeploy --replicas=5 
```

Set the image of the deployment to `busybox`:

```bash
k set image deploy/mylittledeploy nginx=busybox
```
You can always check if the deployment works and has the proper image:

```bash
k get deploy mylittledeploy -o yaml

or

k describe deploy mylittledeploy
``` 

Now you can undo the last change to the deployment:

```bash
k rollout undo deploy/mylittledeploy
```
You can also check the history of the deployment:

```bash
k rollout history deploy/mylittledeploy
```
You can also check the status of the deployment rollout:

```bash
k rollout status deploy/mylittledeploy
```
