# kfd-flask

A sample (and simple) Python/flask application for Kubernetes for Developers

## to rebuild all the images

(this may need to be done to resolve any underlying image issues, such
as security updates or vulnerabilities found and resolved in Alpine)

The container images associated with this repo are available for review at
https://quay.io/repository/kubernetes-for-developers/flask?tab=tags

    git checkout 0.1.1
    docker build -t quay.io/kubernetes-for-developers/flask:0.1.1 .
    git checkout 0.2.0
    docker build -t quay.io/kubernetes-for-developers/flask:0.2.0 .
    git checkout 0.3.0
    docker build -t quay.io/kubernetes-for-developers/flask:0.3.0 .
    git checkout 0.4.0
    docker build -t quay.io/kubernetes-for-developers/flask:0.4.0 .
    git checkout master
    docker build -t quay.io/kubernetes-for-developers/flask:latest .
    docker push quay.io/kubernetes-for-developers/flask

