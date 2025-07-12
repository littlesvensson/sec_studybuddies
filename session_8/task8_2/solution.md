helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update


helm install webserver bitnami/nginx \
  --namespace studybuddies \
  --create-namespace \
  --set service.type=NodePort


kubectl get svc -n studybuddies
helm list -n studybuddies
