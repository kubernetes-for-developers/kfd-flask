# ab testing container image

 ... for generating simple web-based load


## To build this image

    docker build -t quay.io/kubernetes-for-developers/ab:1.0.0 .
    docker push quay.io/kubernetes-for-developers/ab

## to run a shell with this image

    kubectl run -it --rm --restart=Never --image-pull-policy=Always \
    --image=quay.io/kubernetes-for-developers/ab:1.0.0 quicktest -- sh
