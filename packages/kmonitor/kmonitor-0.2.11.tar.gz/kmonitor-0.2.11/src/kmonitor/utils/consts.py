class POD_STATUS:
  OK = "Success"
  LOADING = "Loading"
  INITIALIZING = "Initializing"
  LOW_WARNING = "Low warning"
  WARNING = "Warning"
  CRITICAL = "Critical"
  
  KEY_STATUS = "status"
  KEY_MESSAGES ="messages"
  KEY_CONTAINERS = "containers"
  KEY_POD_NAME = "pod_name"
  KEY_NAMESPACE = "namespace"
  KEY_STARTED = "started"
  KEY_RUNNING = "running_time"
  
  STATUS_RUNNING = "Running"
  STATUS_INITIALIZED = "Initialized"
  STATUS_PENDING = "Pending"
  STATUS_SCHEDULED = "PodScheduled"
  

class KCt:
  MAX_PENDING_TIME = 300
  MIN_RUNNING_TIME = 3600
