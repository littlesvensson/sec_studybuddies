Both resource types can be created imperatively:

```bash
k create role loyal-role --verb=get,list --resource=pods --namespace=studybuddies
```

This command would apply the following YAML in the background:

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
k create rolebinding loyal-rolebinding --role=loyal-role --serviceaccount=studybuddies:loyalservant --namespace=studybuddies
```

would apply the following YAML in the background:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: loyal-rolebinding
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

Let's check the permissions of the `loyalservant` service account:

```bash
k auth can-i get pods --as=system:serviceaccount:studybuddies:loyalservant --namespace=studybuddies

yes
``` 

```bash
k auth can-i get pods --as=system:serviceaccount:studybuddies:loyalservant --namespace=default

no
``` 
