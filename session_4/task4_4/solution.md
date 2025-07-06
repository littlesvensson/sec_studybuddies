Let's create the service account at first:

```bash
k create sa -n studybuddies loyalservant
```

Then, we will create a base for our yaml manifest:

```bash
k create deploy -n studybuddies bossdeploy --image=busybox --replicas=3 --dry-run=client -oyaml -- sh -c "echo 'I am loyal' && sleep 3600" > bossdeploy.yaml
```
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: bossdeploy
  name: bossdeploy
  namespace: studybuddies
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bossdeploy
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: bossdeploy
    spec:
      containers:
      - command:
        - sh
        - -c
        - echo 'I am loyal' && sleep 3600
        image: busybox
        name: busybox
        resources: {}
status: {}

```
Lets connect our loyal ServiceAccount to the bossdeploy.yaml by adding the `spec.serviceAccountName`:

```bash
vim bossdeploy.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: bossdeploy
  name: bossdeploy
  namespace: studybuddies
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bossdeploy
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: bossdeploy
    spec:
      serviceAccountName: loyalservant # This line connects the ServiceAccount to the deployment. Otherwise, the deployment would use the default ServiceAccount.
      containers:
      - command:
        - sh
        - -c
        - echo 'I am loyal' && sleep 3600
        image: busybox
        name: busybox
        resources: {}
status: {}

```

Let's apply the manifest:

```bash
k apply -f bossdeploy.yaml
```
We can check if the ServiceAccount is connected to the deployment by checking the deployment:

```bash
k get deploy -n studybuddies bossdeploy -oyaml | grep serviceAccountName

    {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"app":"bossdeploy"},"name":"bossdeploy","namespace":"studybuddies"},"spec":{"replicas":3,"selector":{"matchLabels":{"app":"bossdeploy"}},"strategy":{},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"bossdeploy"}},"spec":{"containers":[{"command":["sh","-c","echo 'I am loyal' \u0026\u0026 sleep 3600"],"image":"busybox","name":"busybox","resources":{}}],"serviceAccountName":"loyalservant"}}},"status":{}}
    serviceAccountName: loyalservant
```
As we dit not forbid mounting of the ServiceAccount token, we can check it inside of the pod:

```
k exec -it -n studybuddies bossdeploy-67655696f6-42fq5 -- sh # the suffix of the pod name will be different in your case

/ # cat /var/run/secrets/kubernetes.io/serviceaccount/token

eyJhbGciOiJSUzI1NiIsImtpZCI6ImFLVEVncFQxVzNDbTVfOGxlMm44bnpUeWpOeHN0bTA2d0NTTjlTa1dXMUkifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzgzMjc0NjYyLCJpYXQiOjE3NTE3Mzg2NjIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJzdHVkeWJ1ZGRpZXMiLCJwb2QiOnsibmFtZSI6ImJvc3NkZXBsb3ktNjc2NTU2OTZmNi00MmZxNSIsInVpZCI6IjRhNzhlNmM5LTNmNjEtNDQ5ZC1hYTkwLTNkZGJjNjdiY2IwZSJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoibG95YWxzZXJ2YW50IiwidWlkIjoiMGU4NzFmNTgtODQ4ZC00YmE3LWE1ODgtMmI0N2ZlMGI3NzA5In0sIndhcm5hZnRlciI6MTc1MTc0MjI2OX0sIm5iZiI6MTc1MTczODY2Miwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OnN0dWR5YnVkZGllczpsb3lhbHNlcnZhbnQifQ.c7dr63OJRvlVUhEMFBQjFOFGzOhHt63iXOjHLeZXm8nODG4d9SEbuVRvKNFoWbMqbfL2clVJSsXZPdjPN_dhRqb5WeAzUuSPvWJ7ksbdatrFj1rv4sk96z4vfEjJqEauFejs27-_RLLQ8_iwkVb958VBuP6ZK5vs0Lpzrcxm8ZZLpCO6BbRZIXG_1BqL_mpB24lt1D4p_2HWoxfF_fSKaqlha0s5bwWNO7ds5zglhN_KtaC2ctDtP5QayTqHLU0Oprc10lrst8eceZbSUWV16OFYkFFQG4cGnoTEvpg2M-Hz0uErDZPn-anmdwBUTtwWdoNHEKfW0006rYrxma2y9w/
```



