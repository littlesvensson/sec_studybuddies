For both Role and RoleBinding, the most efficient way how to create them during the exam is to use imperative commands. This is the solution for the given task:

```bash
k create role loyal-role --namespace=studybuddies --verb=get,list --resource=pods
```

```bash
k create rolebinding loyal-role-binding --namespace=studybuddies --role=loyal-role --serviceaccount=studybuddies:loyalservant
```

It's as easy as that! You can also use the `--dry-run=client` flag to test your command before actually creating the resources to see what the manifest would look like:

```bash
k create role loyal-role --namespace=studybuddies --verb=get,list --resource=pods --dry-run=client -o yaml
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: null
  name: loyal-role
  namespace: studybuddies
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
```

```bash
k create rolebinding loyal-role-binding --namespace=studybuddies --role=loyal-role --serviceaccount=studybuddies:loyalservant --dry-run=client -oyaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: loyal-role-binding
  namespace: studybuddies
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: loyal-role
subjects:
- kind: ServiceAccount
  name: loyalservant
  namespace: studybuddies
```

