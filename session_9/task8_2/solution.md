There is no way to do this imperatively :( But! It's easy to create the NetworkPolicy manifest by tweaking the example from the official documentation.

The manifest should look like this:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: studybuddies
spec:
  podSelector:
    matchLabels:
      app: backend                 # This policy applies to backend pods only
  policyTypes:
    - Ingress                      # We're only restricting incoming traffic
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend        # Only allow traffic from frontend pods
      ports:
        - protocol: TCP
          port: 8080                 # Only allow traffic to port 80
```

Now, let's apply this manifest to create the NetworkPolicy:

```bash
k apply -f allow-frontend-to-backend.yaml
```

Lets verify that the NetworkPolicy has been created successfully:

```bash
k get netpol -n studybuddies
```

kubectl run test --rm -it --image=curlimages/curl -n studybuddies -- sh
# Inside the shell:
curl http://backend:80

kubectl exec -n studybuddies deploy/frontend -- curl http://backend:80


