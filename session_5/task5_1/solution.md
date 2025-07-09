At first, we will create the persistent volume resource. Persistent volumes are cluster-wide, so we don't need to specify a namespace for it.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mycoolpv
spec:
  capacity:
    storage: 2Mi
  accessModes:
    - ReadWriteOnce 
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data
```
>Note: <br>
>- ReadWriteOnce means that the volume can be mounted as read-write by a single node.
>- Retain means that when the PersistentVolumeClaim is deleted, the PersistentVolume will not be deleted and will remain in the cluster.
>- hostPath means that the volume is backed by a directory on the host node's filesystem.

Then, we will create a PersistentVolumeClaim in the `studybuddies` namespace that requests 2Mi of storage and uses the ReadWriteOnce access mode.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: evencoolerpvc
  namespace: studybuddies
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Mi
  storageClassName: ""
```

If we done everything correctly, the PVC should bind to the PV we created earlier. You can check the status of the PVC by running:

```bash
k get pvc -n studybuddies

NAME            STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
evencoolerpvc   Bound    mycoolpv   2Mi        RWO                           4s
```
Finally, we will create a Deployment that uses this PVC. 

To create the base:

```bash
k create deploy lookinggood -n studybuddies --image=docker/whalesay --dry-run=client -oyaml > lookinggood.yaml -- sh -c 'cowsay "CKAD is fun and I am looking good" >> /data/whalesay && sleep 3600'
```

```bash
cat lookinggood.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: lookinggood
  name: lookinggood
  namespace: studybuddies
spec:
  replicas: 1
  selector:
    matchLabels:
      app: lookinggood
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: lookinggood
    spec:
      containers:
      - command:
        - sh
        - -c
        - cowsay "CKAD is fun and I am looking good" >> /data/whalesay && sleep 3600
        image: docker/whalesay
        name: whalesay
        resources: {}
status: {}
```

Then, we will edit the `lookinggood.yaml` file to add the volume and volumeMounts:

```bash
vim lookinggood.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: lookinggood
  name: lookinggood
  namespace: studybuddies
spec:
  replicas: 1
  selector:
    matchLabels:
      app: lookinggood
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: lookinggood
    spec:
      containers:
      - command:
        - sh
        - -c
        - 'cowsay "CKAD is fun and I am looking good" >> /data/whalesay && sleep 3600'
        image: docker/whalesay
        volumeMounts:                        # Added volumeMounts section
        - mountPath: "/data"                 # Added volumeMounts section
          name: evencoolerpvc                # Added volumeMounts section
        name: whalesay
        resources: {}
      volumes:                               # Added volumes section
        - name: evencoolerpvc                # Added volumes section
          persistentVolumeClaim:             # Added volumes section
            claimName: evencoolerpvc         # Added volumes section
status: {}
```

Finally, we will apply the `lookinggood.yaml` file to create the Deployment:

```bash
k apply -f lookinggood.yaml
```

Now, we can check the pod an the mounted volume:

```bash
k get po -n studybuddies

NAME                           READY   STATUS    RESTARTS      AGE
lookinggood-5d88f9f655-2xrbp   1/1     Running   0             4m12s
```

```bash
k exec -it lookinggood-5d88f9f655-2xrbp -n studybuddies -- cat /data/whalesay # Suffi for your pod will be different

 ___________________________________
< CKAD is fun and I am looking good >
 -----------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

We can also check the contents of the mounted volume from a different pod:

```bash
k apply -f deployment-inspector.yaml -- cat tralala/whalesay
```

```bash
k exec -it deployment-inspector-5d88f9f655-2xrbp -n studybuddies -- cat /tralala/whalesay # Suffi for your pod will be different
 ___________________________________
< CKAD is fun and I am looking good >
 -----------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

