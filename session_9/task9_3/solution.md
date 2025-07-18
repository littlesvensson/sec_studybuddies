There is no way to do this imperatively :( But! It's easy to create the NetworkPolicy manifest by tweaking the example from the official documentation.

At first, we will deploy the manifests in the manifests.yaml file in this folder.

```bash
k apply -f manifests.yaml
```

Currently, there are no NetworkPolicies in the `studybuddies` namespace, so all pods can communicate with each other. We can check this by running the following commands:

1.) Trying to reach the backend service from the temporary random curl pod:

```bash
k run test --rm -it --image=curlimages/curl -n studybuddies -- curl backend
Hello from Backend
pod "test" deleted
```
2.) Trying to reach the backend service from the frontend deployment:

```bash
k exec -n studybuddies deploy/frontend -- curl backend
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0Hello from Backend
100    19  100    19    0     0   4078      0 --:--:-- --:--:-- --:--:--  4750
```


The manifest for our networkpolicy should look like this:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: studybuddies
spec:
  podSelector:
    matchLabels:
      app: backend                    # This policy applies to backend pods only
  policyTypes:
    - Ingress                         # We're only restricting incoming traffic
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend           # Only allow traffic from frontend pods
      ports:
        - protocol: TCP
          port: 8080                  # Only allow traffic to port 80
```

Now, let's apply this manifest to create the NetworkPolicy:

```bash
k apply -f allow-frontend-to-backend.yaml
```

Lets verify that the NetworkPolicy has been created successfully:

1.) Trying to reach the backend service from the temporary random curl pod:

```bash
k run test --rm -it --image=curlimages/curl -n studybuddies -- curl backend




...nothing happening, no response
```
2.) Trying to reach the backend service from the frontend deployment:

```bash
k exec -n studybuddies deploy/frontend -- curl backend
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0Hello from Backend
100    19  100    19    0     0   6333      0 --:--:-- --:--:-- --:--:--  6333
```

As we can see, the NetworkPolicy is working as expected. The frontend deployment can access the backend service, while the temporary curl pod cannot.