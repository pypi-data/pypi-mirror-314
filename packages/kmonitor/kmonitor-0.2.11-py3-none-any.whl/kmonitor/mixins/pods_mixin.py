import json

from collections import OrderedDict


import kubernetes

from ..utils.consts import KCt, POD_STATUS




class _PodsMixin:
  """
  Mixin class for pod-related operations. It assumes the `self.api` is initialized by the main class.
  """
  def __init__(self):
    super(_PodsMixin, self).__init__()
    return
  
  def __get_pod_transition_time(self, pod_info):
    """
    Get the elapsed time since the pod transitioned to its current phase.
    """
    start_time = pod_info.status.conditions[-1].last_transition_time
    transition_time = self._get_elapsed(start_time)
    return transition_time
  
 
  
  def __get_pod_status(self, pod_name, namespace):
    try:
      pod = self.api.read_namespaced_pod(name=pod_name, namespace=namespace)
    except Exception as exc:
      self._handle_exception(exc)
      return None
    return self._check_pod_health(pod)
  
  
  def __list_pods(self, namespace=None):
    try:
      if namespace is None:
        ret = self.api.list_pod_for_all_namespaces(watch=False)
      else:
        ret = self.api.list_namespaced_pod(namespace, watch=False)
    except Exception as exc:
      self._handle_exception(exc)
      return None
    return ret.items
  
  
  def _check_pod_health(self, pod : kubernetes.client.models.v1_pod.V1Pod):
    try:
      # Fetch the specified pod      
      health_status = OrderedDict({
        POD_STATUS.KEY_POD_NAME: pod.metadata.name,
        POD_STATUS.KEY_STATUS: POD_STATUS.OK, 
        POD_STATUS.KEY_NAMESPACE: pod.metadata.namespace,
        POD_STATUS.KEY_MESSAGES: []
      })
      # Determine if the pod is in a loading or initializing state
      if pod.status.phase in [POD_STATUS.STATUS_PENDING]:
        initializing_status = False
        for condition in pod.status.conditions or []:
          if condition.type == POD_STATUS.STATUS_SCHEDULED and condition.status != "True":
            health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.LOADING
            health_status[POD_STATUS.KEY_MESSAGES].append("Pod is scheduled but not running yet.")
            initializing_status = True
          elif condition.type in [POD_STATUS.STATUS_INITIALIZED, "ContainersReady"] and condition.status != "True":
            health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.INITIALIZING
            health_status[POD_STATUS.KEY_MESSAGES].append(f"Pod is initializing: {condition.type} is {condition.status}.")
            initializing_status = True
          #end if condition
        #end for condition
        if not initializing_status:
          # If the pod is pending but no specific initializing status was detected,
          # it could be waiting for resources or other conditions.
          health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.LOADING
          health_status[POD_STATUS.KEY_MESSAGES].append("Pod is pending, waiting for resources/conditions.")
        #end if initializing_status
        if self.__get_pod_transition_time(pod) > KCt.MAX_PENDING_TIME:
          health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.WARNING
          health_status[POD_STATUS.KEY_MESSAGES].append(f"Pod has been pending for more than 5 minutes.")
        #end if transition time          
      #end if pod is pending
      elif pod.status.phase not in [POD_STATUS.STATUS_RUNNING, "Succeeded"]:
        health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.CRITICAL
        health_status[POD_STATUS.KEY_MESSAGES].append(f"Pod is in {pod.status.phase} phase.")
      # end if pod is not running or succeeded
      
      # Check container statuses if pod phase is Running
      if pod.status.phase == POD_STATUS.STATUS_RUNNING:
        health_status[POD_STATUS.KEY_CONTAINERS] = {}
        for container_status in pod.status.container_statuses or []:
          container_name = container_status.name
          dct_container = {}
          # Check if container is ready 
          if not container_status.ready:
            health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.WARNING
            health_status[POD_STATUS.KEY_MESSAGES].append(f"Container {container_status.name} is not ready.")
          # Check if container has restarted
          if container_status.restart_count > 0:
            health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.WARNING
            health_status[POD_STATUS.KEY_MESSAGES].append(f"Container {container_status.name} restarted {container_status.restart_count} times.")
          # now compute running time for this pod containers                   
          run_info = container_status.state.running                  
          running_time = self._get_elapsed(run_info.started_at)
          hours, rem = divmod(running_time, 3600)
          minutes, seconds = divmod(rem, 60)
          # format elapsed time as a string        
          dct_container[POD_STATUS.KEY_STARTED] = run_info.started_at.strftime("%Y-%m-%d %H:%M:%S")
          dct_container[POD_STATUS.KEY_RUNNING] = "{:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds))
          if running_time < KCt.MIN_RUNNING_TIME:
            health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.LOW_WARNING
            health_status[POD_STATUS.KEY_MESSAGES].append(f"Low running time: Container {container_status.name} run-time {dct_container['running_time']}.")
          else:
            health_status[POD_STATUS.KEY_STATUS] = POD_STATUS.OK
            health_status[POD_STATUS.KEY_MESSAGES].append(f"Container {container_status.name} run-time {dct_container['running_time']}.")  
          #end if running time
          health_status[POD_STATUS.KEY_CONTAINERS][container_name] = dct_container
        #end for container status
      #end if pod is running
    except Exception as e:
      health_status = {
        **health_status,
        POD_STATUS.KEY_STATUS: "Error", POD_STATUS.KEY_MESSAGES: [str(e)]
      }
      self.P(f"An error occurred: {e}", color='r') # if you want to see datils check in the payloads
    #end try
    return health_status  
  
  
  def __get_pod_by_name(self, pod_name):
    assert isinstance(pod_name, str), "`pod_name` must be a string"
    
    pods = self.list_pods()
    if pods is None:
      health_status = {POD_STATUS.KEY_STATUS: "Error", POD_STATUS.KEY_MESSAGES: ["Unable to get pods"]}
    else:      
      found = None
      for p in pods:
        if p.metadata.name.startswith(pod_name):
          found = p
          break        
    return found
  
  
################################################################################################
# Public methods
################################################################################################
  

  def check_pod(self, namespace, pod_name):
    """
    Check the health of a pod by its name and namespace.
    
    Parameters
    ----------
    namespace : str
        The namespace where the pod is located.
    pod_name : str
        The name of the pod to check.
    
    Returns
    -------
      dict
        The health status of the pod.
    """
    return self.__get_pod_status(pod_name=pod_name, namespace=namespace)
  
  
  def check_pod_by_name(self, pod_name):
    """
    Check the health of a pod by its name.
    
    Parameters
    ----------
    pod_name : str
        The name of the pod to check.
    
    Returns
    -------
      dict
    """
    
    found_pod = self.__get_pod_by_name(pod_name)
    if found_pod is None:
      health_status = {POD_STATUS.KEY_STATUS: "Error", POD_STATUS.KEY_MESSAGES: [f"Pod '{pod_name}' not found"]}
    else:
      health_status = self._check_pod_health(found_pod)
      #end if found
    return health_status
  
  
  def check_pods_by_names(self, lst_pod_names):
    """
    Check the health of a list of pods by their names.
    
    Parameters
    ----------
    lst_pod_names : list
        A list of pod names to check.
        
    Returns
    -------
      list
    """
    result = []
    for pod_name in lst_pod_names:
      status = self.check_pod_by_name(pod_name)
      result.append(status)
    return result
  
    
  def get_all_pods(self, namespace=None):
    """
    Get all pods in all namespaces.
    """
    lst_pods = self.__list_pods(namespace=namespace)
    return lst_pods


  def list_pods(self):
    """Get all pods in all namespaces."""
    return self.get_all_pods()
  


  def get_pods_by_namespace(self, namespace):
    """
    Get all pods in a specific namespace.
    """
    lst_pods = self.__list_pods(namespace=namespace)
    return lst_pods
  
  
  def get_all_pods_health(self, namespace=None):
    """
    Get the health status of all pods in all namespaces.
    """
    lst_pods = self.get_all_pods(namespace=namespace)
    result = []
    for pod in lst_pods:
      status = self._check_pod_health(pod)
      result.append(status)
    return result
  
  
  def delete_pods_from_namespace(self, base_name : str, namespace : str):
    """
    Delete all pods in a namespace that start with a specific name.
    
    Parameters
    ----------
    base_name : str
        The base name of the pods to delete.
    namespace : str
        The namespace where the pods are located.
    """
    assert isinstance(base_name, str), "`base_name` must be a string"
    assert isinstance(namespace, str), "`namespace` must be a string"
    
    pods = self.get_pods_by_namespace(namespace)
    if pods is None:
      self.P("No pods found in namespace {}".format(namespace)) 
      return
    #end if pods is None
    for pod in pods:
      if pod.metadata.name.startswith(base_name):
        self.P(f"Deleting pod {pod.metadata.name} in namespace {namespace}")
        res = self.api.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)
        if res is not None:
          creation_date = res.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
          delete_date = res.metadata.deletion_timestamp.strftime("%Y-%m-%d %H:%M:%S")
          delta = res.metadata.deletion_timestamp - res.metadata.creation_timestamp
          lifetime_sec = (delta).total_seconds()
          elapsed_time = str(delta)
          msg = f"Pod {pod.metadata.name} deleted. Created: {creation_date}, Deleted: {delete_date}, Lifetime: {elapsed_time}."
          self.P(msg)
    #end for pod
    return
      