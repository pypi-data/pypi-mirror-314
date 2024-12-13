import numpy as np
try:
  from src.kmonitor import KubeMonitor, safe_jsonify
except:
  from kmonitor import KubeMonitor, safe_jsonify
# end try imports from local project or from deployed package


if __name__ == '__main__':
  km = KubeMonitor()
  pods = km.list_pods()
  if pods is not None:
    for pod in pods:
      print(f"Pod: {pod.metadata.name} in namespace {pod.metadata.namespace} is in phase {pod.status.phase}")
  else:
    print("Failed to get pods")

  namespaces = km.list_namespaces()
  if namespaces is not None:
    for ns in namespaces:
      print(f"Namespace: {ns.metadata.name}")
  else:
    print("Failed to get namespaces")
  
  nr_pods = len(pods)
  idx = np.random.randint(0, nr_pods)
  example_pod_name = "basic-test" # pods[idx].metadata.name
  print("Checking pod status for pod {}".format(example_pod_name))
  status = km.check_pod_by_name(example_pod_name)
  print(safe_jsonify(status, indent=2))

  example_pod_names = [
    # "nvidia", 
    # "calico-node", 
    # "emqx",
    "redis",
    "ee-super"
  ]
  print("Checking pod status for pods {}".format(example_pod_names))
  status = km.check_pods_by_names(example_pod_names)
  print(safe_jsonify(status, indent=2))
  
  
  # km.delete_pods_from_namespace("redis", "hyfy")
  

  namespace = "hyfy"
  lst_pods = km.get_all_pods(namespace=namespace)
  print(f"Found {len(lst_pods)} pods in namespace {namespace}")
  
  print(lst_pods[0].metadata.namespace)
  