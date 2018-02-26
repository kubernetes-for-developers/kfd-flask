import kubernetes
import pytest

# in a larger example, this section could easily be in conftest.py
@pytest.fixture
def kube_v1_client():
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    return v1

def test_contexts(kube_v1_client):
    contexts, active_context = kubernetes.config.list_kube_config_contexts()
    #print("%s\t%s" % (contexts, active_context))
    #print(kube_v1_client.list_node())
    #print("-----------------------------------------------------------------")
    print(kube_v1_client.list_service_for_all_namespaces())
    print(kubernetes.config)

def test_component_status(kube_v1_client):
    ret = kube_v1_client.list_component_status()
    for item in ret.items:
        assert item.conditions[0].type == "Healthy"
        print("%s: %s" % (item.metadata.name, item.conditions[0].type))

def test_noop(kube_v1_client):
    assert 1
    ret = kube_v1_client.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    assert 1
