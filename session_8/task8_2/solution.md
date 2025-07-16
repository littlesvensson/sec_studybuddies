At first, we will deploy the manifest within the folder:

```bash
k apply -f task8_2/deployments.yaml -n studybuddies
```
Then we will expose the blue version of the app (version: blue) by creating a Service with name `green-blue` that selects the blue version of the app.

```bash
k expose -n studybuddies deploy blue-deployment --name green-blue
```



