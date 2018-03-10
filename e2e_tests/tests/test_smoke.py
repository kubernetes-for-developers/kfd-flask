import kubernetes
import pytest
import yaml
import time
import subprocess

# in a larger example, this section could easily be in conftest.py
@pytest.fixture
def kube_v1_client():
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    return v1

@pytest.fixture
def kubectl_proxy():
    # establish proxy for kubectl communications
    # https://docs.python.org/2/library/subprocess.html#subprocess-replacements
    proxy = subprocess.Popen("kubectl proxy", stdout=subprocess.PIPE, shell=True)
    yield 
    # terminate the proxy
    proxy.kill()

@pytest.mark.dependency()
def test_kubernetes_components_healthy(kube_v1_client):
    # iterates through the core kuberneters components to verify the cluster is reporting healthy
    ret = kube_v1_client.list_component_status()
    for item in ret.items:
        assert item.conditions[0].type == "Healthy"
        print("%s: %s" % (item.metadata.name, item.conditions[0].type))

@pytest.mark.dependency(depends=["test_kubernetes_components_healthy"])
def test_deployment():
    # https://docs.python.org/3/library/subprocess.html#subprocess.run
    # using check=True will throw an exception if a non-zero exit code is returned, saving us the need to assert
    # using timeout=10 will throw an exception if the process doesn't return within 10 seconds
    # Enables the deployment
    process_result = subprocess.run('kubectl apply -f ../deploy/', check=True, shell=True, timeout=10)

@pytest.mark.dependency(depends=["test_deployment"])
def test_list_pods(kube_v1_client):
    ret = kube_v1_client.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

@pytest.mark.dependency(depends=["test_deployment"])
def test_deployment_ready(kube_v1_client):
    TOTAL_TIMEOUT_SECONDS = 300
    DELAY_BETWEEN_REQUESTS_SECONDS = 5
    REQUEST_TIMEOUT_SECONDS=2
    apps_client = kubernetes.client.AppsV1beta2Api()
    now = time.time()
    while (time.time() < now+TOTAL_TIMEOUT_SECONDS):
        api_response = apps_client.list_namespaced_deployment("default", 
            include_uninitialized=True, 
            timeout_seconds=REQUEST_TIMEOUT_SECONDS)
        print("name\tavail\tready")
        for i in api_response.items:
            print("%s\t%s\t%s" %
                (i.metadata.name, i.status.available_replicas, i.status.ready_replicas))
            if i.metadata.name == 'flask':
                if i.status and i.status.ready_replicas:
                    return 
        time.sleep(DELAY_BETWEEN_REQUESTS_SECONDS)
    assert False

@pytest.mark.dependency(depends=["test_deployment_ready"])
def test_pods_running(kube_v1_client):
    pod_list = kube_v1_client.list_namespaced_pod("default")
    print("name\tphase\tcondition\tstatus")
    for pod in pod_list.items:
        for condition in pod.status.conditions:
            print("%s\t%s\t%s\t%s" % (pod.metadata.name, pod.status.phase, condition.type, condition.status))
            if condition.type == 'Ready':
                assert condition.status == 'True'
        assert pod.status.phase == "Running"

@pytest.mark.dependency(depends=["test_deployment_ready"])
def test_contexts(kube_v1_client, kubectl_proxy):
    # contexts, active_context = kubernetes.config.list_kube_config_contexts()
    # print("%s\t%s" % (contexts, active_context))
    # print(kube_v1_client.list_node())
    # print("-----------------------------------------------------------------")
    # print(kube_v1_client.list_service_for_all_namespaces())
    # print(kubernetes.config)
    print("hi")

