import kubernetes
import pytest

# in a larger example, this section could easily be in conftest.py
@pytest.fixture
def kube_v1_client():
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    return v1

def test_noop(kube_v1_client):
    assert 1
    kube_v1_client.list_pod_for_all_namespaces(watch=False)
    assert 1
