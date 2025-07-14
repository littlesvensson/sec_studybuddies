At first, we will deploy the deployment from the `my-beautiful-app.yaml` file:

```bash
k apply -f my-beautiful-app.yaml
``` 
Then we will expose the deployment using the ClusterIP service type. The easiest way is to do it imperatively:

```bash
k expose deployment my-beautiful-app --type=ClusterIP --name=my-beautiful-service --port=80 --target-port=8080 -n studybuddies
```
We do not need to specify the selector, as it is automatically set to match the labels of the Pods created by the deployment. Also, there is no need to specify the `ClusterIP` service type, as it is the default type. The `--port` flag specifies the port on which the service will be exposed, and the `--target-port` flag specifies the port on which the application is running inside the Pods. We have to specify `--target-port` even though it is not the mandatory field, because otherwise the service would assign it the same number as the `--port` flag, which is not what we want in this case. It the task, there is written that the name of the service should be `my-beautiful-service`, therefore we need to specify it. Otherwise, the service would be named `my-beautiful-app` by default, which is not what we want.

Great! The task is done. Let's check the service:

```bash
k get svc -n studybuddies
k get svc my-beautiful-service -n studybuddies -o yaml
```

Can we reach the application? Yes, we can! We can use the `kubectl port-forward` command to forward the service port to our local machine:

```bash
k port-forward svc/my-beautiful-service 8080:80 -n studybuddies
```
Now we can access the application in our browser at `http://localhost:8080`.

Or, we can reach it from the cluster using the `curl` command:

```bash
k run -it --rm debug --image=curlimages/curl -n studybuddies --restart=Never -- sh

~ $ curl http://my-beautiful-service:80
Hello from my-beautiful-app
```



