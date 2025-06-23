Порядок сборки манифестов

Сначала запускаем докер image

```
cd docker-compose-template

docker-compose up -d
```

Затем идем в папку kubernettes

```
cd kubernettes

minikube start

minikube ssh

docker images

minikube ip

kubectl apply -f namespace.yaml

kubectl apply -f backend-pod.yaml

kubectl apply -f frontend-pod.yaml

kubectl apply -f postgres-pod.yaml

kubectl apply -f service-kub.yaml

kubectl get svc -n kub-app

kubectl get pod -n kub-app

minikube addons enable ingress

kubectl apply -f ingress.yaml

kubectl get ingress -n kub-app

curl kub.local
```
