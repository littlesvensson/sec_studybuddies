Let's create the pod first:

```bash
k create deploy lunchserver --image=littlesvensson/lunchserver:v2 -n studybuddies 
```
Now, we will create the loadbalancer service:

```bash
k create svc loadbalancer lunchserver -n studybuddies --tcp=80:8080
```     

This will generate and create the following service definition:

```yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: lunchserver
  name: lunchserver
  namespace: studybuddies
spec:
  ports:
  - name: 80-8080
    port: 80
    protocol: TCP
    targetPort: 8080
  selector:
    app: lunchserver
  type: LoadBalancer
status:
  loadBalancer: {}
```
Now, we can check if the service is running and is of type LoadBalancer:

```bash
k get svc lunchserver -n studybuddies

NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
lunchserver   LoadBalancer   10.96.12.214   <pending>     80:31108/TCP   18s

```
If we were testing this in a cloud environment, we would see an external IP assigned to the service. However, in a local environment, it will show `<pending>`.

Let's try to access the service:

```bash
k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

curl 10.96.12.214:80          # Adjust the IP to match your service's Cluster IP
   (\_/)
  ( •_•)
 / >🌮 Looking forward to lunch?

curl lunchserver:80
   (\_/)
  ( •_•)
 / >🌮 Looking forward to lunch?

exit
```

If you will try to reach the server from a different namespace with the testing pod, you would need to write the full dns name for the service: `curl lunchserver.studybuddies.svc.cluster.local:80` 

```bash
k run -it --rm tester --image=curlimages/curl  --restart=Never -- sh

curl lunchserver.studybuddies.svc.cluster.local:80
   (\_/)
  ( •_•)
 / >🌮 Looking forward to lunch?

```

Congrats! You were just served a delicious taco from the lunch server!