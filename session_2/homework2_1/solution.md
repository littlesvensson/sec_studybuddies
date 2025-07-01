At first, lets create the base for the deployment with the help of `dry-run=client -oyaml`:
\
```bash
k create deploy probeofmylife --image=nginxdemos/hello:0.2 --replicas=2 -n studybuddies --dry-run=client -o yaml > probeofmylife.yaml
```
This will create a file `probeofmylife.yaml` with the following base manifest:

```bash
cat probeofmylife.yaml
```

```yaml
cat probeofmylife.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: probeofmylife
  name: probeofmylife
  namespace: studybuddies
spec:
  replicas: 2
  selector:
    matchLabels:
      app: probeofmylife
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: probeofmylife
    spec:
      containers:
      - image: nginxdemos/hello:0.2
        name: hello
        resources: {}
status: {}
```

Now it's best to check what the docmentation says about the probes. Let's copy the probe sections and tweak them for the needs of this homework:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: probeofmylife
  name: probeofmylife
  namespace: studybuddies
spec:
  replicas: 2
  selector:
    matchLabels:
      app: probeofmylife
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: probeofmylife
    spec:
      containers:
      - image: nginxdemos/hello:0.2
        name: hello
        resources: {} 
        startupProbe:             # Added
          httpGet:                # Added
            path: /               # Added
            port: 80              # Added
          failureThreshold: 15    # Added
          periodSeconds: 2        # Added
        readinessProbe:           # Added
          httpGet:                # Added
            path: /               # Added
            port: 80              # Added
          initialDelaySeconds: 5  # Added
          periodSeconds: 5        # Added
        livenessProbe:            # Added
          httpGet:                # Added
            path: /               # Added
            port: 80              # Added
          initialDelaySeconds: 10 # Added
          periodSeconds: 10       # Added
