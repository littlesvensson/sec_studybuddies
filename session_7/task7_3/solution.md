At first, we will wait until the playground is ready. Then, we will create a new namespace called `studybuddies`.

```bash
k create namespace studybuddies
```
Next, we will apply the [manifest definition](deployment.yaml).

Then, we will expose the Deployment as a NodePort Service named `my-beautiful-nodeport-service` that targets Pods with label `app=my-beautiful-nodeport-app` and forwards traffic from port 80 to container port 8080:

```bash
k expose deployment my-beautiful-nodeport-app --type=NodePort --name=my-beautiful-nodeport-service --port=80 --target-port=8080 -n studybuddies
```
Now, we can check if the Service is created successfully:

```bash
k get svc -n studybuddies

 
NAME                            TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
my-beautiful-nodeport-service   NodePort   10.99.220.77   <none>        80:31832/TCP   5s
```

You should see the `my-beautiful-nodeport-service` listed with a `NodePort` type and an assigned port.

Now, let's check the IP address of our node:

```bash
k get no -owide
NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
controlplane   Ready    control-plane   20d   v1.33.2   172.30.1.2    <none>        Ubuntu 24.04.1 LTS   6.8.0-51-generic   containerd://1.7.27
node01         Ready    <none>          20d   v1.33.2   172.30.2.2    <none>        Ubuntu 24.04.1 LTS   6.8.0-51-generic   containerd://1.7.27
```

Now, let's test the Service by running a curl command in the pod, trying to connect through the IP address of the node and the NodePort assigned to the Service:

```bash
k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

curl 172.30.1.2:31832
Hello from your fancy beautiful nodeport app!
```
Success! The pod has responded to you with the expected message.