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

```yaml