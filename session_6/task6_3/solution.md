At first, will create our deployment base imperatively:

```bash
k create deploy -n studybuddies secure-joke --image=curlimages/curl --dry-run=client -oyaml -- curl -s https://icanhazdadjoke.com/ > secure-joke.yaml
```
```bash
cat secure-joke.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: secure-joke
  name: secure-joke
  namespace: studybuddies
spec:
  replicas: 1
  selector:
    matchLabels:
      app: secure-joke
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: secure-joke
    spec:
      containers:
      - command:
        - curl
        - -s
        - https://icanhazdadjoke.com/
        image: curlimages/curl
        name: curl
        resources: {}
status: {}
```

Then, we will add the security context to our deployment:

```bash
vim secure-joke.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: secure-joke
  name: secure-joke
  namespace: studybuddies
spec:
  replicas: 1
  selector:
    matchLabels:
      app: secure-joke
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: secure-joke
    spec:
      containers:
      - name: curl-container
        image: curlimages/curl
        command:
        - curl
        - -s
        - https://icanhazdadjoke.com/
        securityContext:                      # Added security context for the container
          runAsUser: 1000                     # Added security context for the container
          readOnlyRootFilesystem: true        # Added security context for the container
        resources: {}
status: {}
```

Finally, we will apply our deployment:

```bash
k apply -f secure-joke.yaml
```

Tadaaaa! Our secure-joke deployment is ready to go!

```bash

