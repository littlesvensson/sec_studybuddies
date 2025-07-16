At first, we will apply the manifest for the two deployments in the `task8_3` folder:

```bash
k apply -f deployments.yaml -n studybuddies             # path depends on the folder you are in right now

deployment.apps/v1-deployment created
deployment.apps/canary-deployment created
```
Next, we will create the ClusterIP service for the `v1-deployment`:

```bash
 k expose deploy -n studybuddies v1-deployment --name canary-service --port 80 --target-port 8080
```
As we want to reach both deployments through the same service, we will patch the `canary-service` to include the `v1-deployment` as well:

```bash
k edit svc -n studybuddies canary-service
```
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2025-07-16T06:32:06Z"
  name: canary-service
  namespace: studybuddies
  resourceVersion: "439677"
  uid: 63a26200-af0a-4ce2-b317-f03b8c44f7c6
spec:
  clusterIP: 10.96.221.223
  clusterIPs:
  - 10.96.221.223
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - port: 80
    protocol: TCP
    targetPort: 8080
  selector:
    app: mycanaryapp
#    version: v1                                              # Delete this label
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```
Now, the `canary-service` will route traffic to both the `v1-deployment` and the `canary-deployment`, because the app: mycanaryapp label is shared between them.

Let's verify that the service is working correctly by sending a request to it:

```bash
k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

If you don't see a command prompt, try pressing enter.
~ $ while true; do curl canary-service; sleep 1; done
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
Greetings from the v1!
^C
~ $ exit
pod "tester" deleted

```

We see the response from the `v1-deployment`, which is expected since it is the only deployment currently running with some replicas.

Let's scale the `canary-deployment` to 3 replicas and check the responses again:

```bash
k scale deploy -n studybuddies canary-deployment --replicas=3
deployment.apps/canary-deployment scaled

k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

If you don't see a command prompt, try pressing enter.
~ $ while true; do curl canary-service; sleep 1; done
Greetings from the v1!
Greetings from the canary!
Greetings from the canary!
Greetings from the canary!
Greetings from the v1!
Greetings from the canary!
Greetings from the canary!
Greetings from the canary!
```
Let's scale the `v1` to 0 replicas and check the responses again:

```bash
k scale deploy -n studybuddies v1-deployment --replicas=0
deployment.apps/v1-deployment scaled

k scale deploy -n studybuddies v1-deployment --replicas=0
deployment.apps/v1-deployment scaled

k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

If you don't see a command prompt, try pressing enter.
~ $ while true; do curl canary-service; sleep 1; done
Greetings from the canary!
Greetings from the canary!
Greetings from the canary!
Greetings from the canary!
Greetings from the canary!
^C
~ $
```

Wohooo! We successfully imitated the canary deployment strategy.








