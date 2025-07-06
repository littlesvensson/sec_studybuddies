At first, lets create the deployment base:

```
 k create deploy secretholder -n studybuddies --replicas 2 --image=littlesvensson/dirtysecret --dry-run=client -oyaml > secretholder.yaml

```

The base manifest looks like this:

```bash
cat secretholder.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: secretholder
  name: secretholder
  namespace: studybuddies
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secretholder
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: secretholder
    spec:
      containers:
      - image: littlesvensson/dirtysecret
        name: dirtysecret
        resources: {}
status: {}
```

Then, we check the docs to see how to mount a secret as a volume. We copy the parts we need, paste them in the right sections and modify some values to fit the task requirements:

```bash
vim secretholder.yaml
```

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: secretholder
  name: secretholder
  namespace: studybuddies
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secretholder
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: secretholder
    spec:
      containers:
      - image: littlesvensson/dirtysecret
        name: mydirtysecret
        volumeMounts:                         # Added volumeMounts section within the container spec
        - name: secretinfo                    # Name of the volume to mount
          mountPath: "/etc/secretinfo"        # Mount path where the secret will be available
      volumes:                                # Added volume section at the pod spec level
      - name: secretinfo                      # Added volume section at the pod spec level
        secret:                               # Added secret type
          secretName: mydirtysecret           # Reference to the secret created in the previous step
status: {}
```

Now we can create the deployment:

```bash
k apply -f secretholder.yaml
``` 

Finally, we can check logs of one of the pods created by the deployment to see if the secret was mounted correctly:

```bash
k logs -n studybuddies secretholder-564f785dd5-2lxn5 # Suffix will be different for you
```

```python
jaja is so proud of you <3.

          |
            \     (      /
       `.    \     )    /    .'
         `.   \   (    /   .'
           `.  .-''''-.  .'
     `~._    .'/_    _\`.    _.~'
         `~ /  / \  / \  \ ~'
    _ _ _ _|  _\O/  \O/_  |_ _ _ _
           | (_)  /\  (_) |
        _.~ \  \      /  / ~._
     .~'     `. `.__.' .'     `~.
           .'  `-,,,,-'  `.
         .'   /    )   \   `.
       .'    /    (     \    `.
            /      )     \
```