from collections import OrderedDict

from ..utils.consts import KCt

class _NodesMixin:
  def __init__(self):
    super(_NodesMixin, self).__init__()
    return


  def get_all_nodes(self):
    """
    Retrieves all nodes in the cluster along with their status.

    Returns
    -------
    list
        A list of nodes and their statuses.
    """
    node_infos = {}
    try:
      nodes = self.api.list_node()
      for node in nodes.items:
        memory = node.status.capacity['memory']
        str_cpu = self.to_number_str(node.status.capacity['cpu'])
        cpu = int(str_cpu)
        memory_bytes = self.convert_memory_to_bytes(memory)
        conditions = {
          condition.type: condition.status for condition in node.status.conditions
        }
        node_infos[node.metadata.name] = {
          'status': 'Ready' if conditions.get('Ready') == 'True' else 'Not Ready',
          'conditions': conditions,
          'memory_gib': round(memory_bytes / (1024**3), 2),
          'cpu_cores': cpu,            
        }
    except Exception as exc:
      self._handle_exception(exc)
      node_infos = {}
    return node_infos


  def get_nodes_metrics(self):
    """
    Fetches metrics for all nodes and converts them to readable units.

    Returns
    -------
    list
        A list of nodes with their CPU (in millicores) and memory usage (in GiB).
    """
    metrics_list = []    
    nodes_capacity = self.get_all_nodes()
    if len(nodes_capacity) > 0:
      try:      
        node_metrics = self.custom_api.list_cluster_custom_object(
          group="metrics.k8s.io",
          version="v1beta1",
          plural="nodes"
        )
        metrics_list = []
        for node in node_metrics.get('items', []):
          node_name = node['metadata']['name']
          str_cpu = self.to_number_str(node['usage']['cpu'])
          str_mem = self.to_number_str(node['usage']['memory'])
          cpu_usage_millicores = int(str_cpu) / 1e6  # Convert nanocores to millicores
          memory_usage_gib = int(str_mem) / (1024**2)  # Convert KiB to GiB
          total_memory_gib = nodes_capacity[node_name]['memory_gib']
          total_cpu_cores = nodes_capacity[node_name]['cpu_cores']
          metrics_list.append({
            'name': node_name,
            'status': nodes_capacity[node_name]['status'],
            'conditions': nodes_capacity[node_name]['conditions'],
            'cpu_usage_mili': int(cpu_usage_millicores),
            'memory_usage_gib': round(memory_usage_gib, 2),
            'total_memory_gib': total_memory_gib,
            'total_cpu_cores': total_cpu_cores,
            'memory_load': '{:.1f}%'.format(round((memory_usage_gib / total_memory_gib) * 100, 2)),
            'cpu_load': '{:.1f}%'.format(round((cpu_usage_millicores / (total_cpu_cores * 1000)) * 100, 2)),
          })
      except Exception as exc:
        self._handle_exception(exc)
        metrics_list = []
    return metrics_list  

