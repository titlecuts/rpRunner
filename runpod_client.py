"""
RunPod API Client
Wrapper for interacting with RunPod's GraphQL API
"""
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime


class RunPodClient:
    """Client for interacting with RunPod API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.runpod.io/graphql"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def _make_request(self, query: str, debug: bool = False) -> Dict:
        """Make a GraphQL request to RunPod API"""
        url = f"{self.base_url}?api_key={self.api_key}"
        
        payload = {"query": query}
        
        if debug:
            print(f"[DEBUG] Sending query:\n{query}\n")
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            # Try to get JSON response even on error
            try:
                result = response.json()
            except:
                result = {"error": f"HTTP {response.status_code}: {response.text}"}
            
            if debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response: {json.dumps(result, indent=2)}\n")
            
            # Raise for 4xx/5xx status codes, but after we've captured the response
            response.raise_for_status()
            
            return result
            
        except requests.exceptions.RequestException as e:
            # If we got a result with GraphQL errors, return that instead
            if 'result' in locals() and isinstance(result, dict):
                if 'errors' in result or 'data' in result:
                    return result
            
            error_response = {"error": str(e)}
            if debug:
                print(f"[DEBUG] Request failed: {error_response}")
            return error_response
    
    def get_all_pods(self) -> List[Dict]:
        """Get all pods associated with the account"""
        query = """
        query {
            myself {
                pods {
                    id
                    name
                    desiredStatus
                    imageName
                    lastStatusChange
                    gpuCount
                    costPerHr
                    containerDiskInGb
                    volumeInGb
                    volumeMountPath
                    runtime {
                        uptimeInSeconds
                        ports {
                            ip
                            isIpPublic
                            privatePort
                            publicPort
                            type
                        }
                    }
                    machine {
                        podHostId
                        gpuTypeId
                    }
                }
            }
        }
        """
        
        result = self._make_request(query)
        
        if "error" in result:
            return []
        
        try:
            return result.get('data', {}).get('myself', {}).get('pods', [])
        except (KeyError, TypeError):
            return []
    
    def get_pod_by_id(self, pod_id: str) -> Optional[Dict]:
        """Get specific pod by ID"""
        pods = self.get_all_pods()
        for pod in pods:
            if pod.get('id') == pod_id:
                return pod
        return None
    
    def get_running_pods(self) -> List[Dict]:
        """Get all currently running pods"""
        all_pods = self.get_all_pods()
        return [pod for pod in all_pods if pod.get('desiredStatus') == 'RUNNING']
    
    def stop_pod(self, pod_id: str) -> Dict:
        """Stop a running pod"""
        query = f"""
        mutation {{
            podStop(input: {{podId: "{pod_id}"}}) {{
                id
                desiredStatus
            }}
        }}
        """
        return self._make_request(query)
    
    def start_pod(self, pod_id: str) -> Dict:
        """Start a stopped pod"""
        query = f"""
        mutation {{
            podResume(input: {{podId: "{pod_id}", gpuCount: 1}}) {{
                id
                desiredStatus
            }}
        }}
        """
        return self._make_request(query)
    
    def terminate_pod(self, pod_id: str) -> Dict:
        """Terminate (delete) a pod - USE WITH CAUTION"""
        query = f"""
        mutation {{
            podTerminate(input: {{podId: "{pod_id}"}}) {{
                id
            }}
        }}
        """
        return self._make_request(query)
    
    def create_pod(
        self,
        gpu_type: str = "NVIDIA RTX 4090",
        template_id: str = "st18mlieee",
        volume_id: str = "glr3kp77sk",
        container_disk_gb: int = 100,
        gpu_count: int = 1,
        name: Optional[str] = None,
        datacenter_id: Optional[str] = None,
        country_code: Optional[str] = None
    ) -> Dict:
        """Create a new pod with specified configuration
        
        Args:
            datacenter_id: Specific datacenter (e.g., "US-CA-2", "US-TX-3", "EU-RO-1")
            country_code: Country code for region filtering (e.g., "US", "CA", "GB")
        """
        
        # Map common GPU names to RunPod's GPU type IDs
        gpu_type_map = {
            "NVIDIA RTX 4090": "NVIDIA GeForce RTX 4090",
            "NVIDIA RTX 5090": "NVIDIA GeForce RTX 5090",
            "NVIDIA RTX A6000": "NVIDIA RTX A6000",
            "NVIDIA RTX 5000 Ada": "NVIDIA RTX 5000 Ada Generation",
            "NVIDIA L40": "NVIDIA L40",
            "NVIDIA A100 80GB PCIe": "NVIDIA A100 80GB PCIe",
            "NVIDIA A100-SXM4-80GB": "NVIDIA A100-SXM4-80GB",
            "NVIDIA A40": "NVIDIA A40",
            # Add both formats so it works either way
            "NVIDIA GeForce RTX 4090": "NVIDIA GeForce RTX 4090",
            "NVIDIA GeForce RTX 5090": "NVIDIA GeForce RTX 5090",
        }
        
        # Use mapped GPU type if available, otherwise use as-is
        gpu_type_id = gpu_type_map.get(gpu_type, gpu_type)
        
        # Build datacenter filter if specified
        datacenter_filter = ""
        if datacenter_id:
            datacenter_filter = f', datacenterId: "{datacenter_id}"'
        elif country_code:
            datacenter_filter = f', countryCode: "{country_code}"'
        
        # Build mutation query
        # Note: cloudType ALL enables global networking (searches all datacenters)
        mutation = f"""
        mutation {{
            podFindAndDeployOnDemand(input: {{
                cloudType: ALL,
                gpuTypeId: "{gpu_type_id}",
                templateId: "{template_id}",
                networkVolumeId: "{volume_id}",
                minVcpuCount: 8,
                minMemoryInGb: 32,
                gpuCount: {gpu_count},
                containerDiskInGb: {container_disk_gb},
                ports: "8188/http,8888/http",
                volumeMountPath: "/workspace"
                {datacenter_filter}
                {f', name: "{name}"' if name else ''}
            }}) {{
                id
                imageName
                machineId
                machine {{
                    podHostId
                }}
            }}
        }}
        """
        
        # Always use debug mode for pod creation to see actual errors
        result = self._make_request(mutation, debug=True)
        
        # If there's an error, try to extract useful information
        if "errors" in result:
            print(f"\n[ERROR] GraphQL errors from RunPod API:")
            for error in result.get("errors", []):
                print(f"  - {error.get('message', error)}")
        
        return result
    
    def get_pod_metrics(self, pod_id: str) -> Dict:
        """Get resource usage metrics for a pod"""
        # This requires the pod to be running and accessible
        # Returns basic info from the API
        pod = self.get_pod_by_id(pod_id)
        
        if not pod:
            return {"error": "Pod not found"}
        
        metrics = {
            "pod_id": pod_id,
            "status": pod.get('desiredStatus'),
            "gpu_type": pod.get('machine', {}).get('gpuTypeId'),
            "gpu_count": pod.get('gpuCount'),
            "uptime_seconds": pod.get('runtime', {}).get('uptimeInSeconds', 0),
            "cost_per_hr": pod.get('costPerHr'),
            "disk_size_gb": pod.get('containerDiskInGb'),
            "volume_size_gb": pod.get('volumeInGb'),
        }
        
        # Calculate uptime in human-readable format
        uptime = metrics['uptime_seconds']
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        metrics['uptime_formatted'] = f"{hours}h {minutes}m"
        
        return metrics
    
    def get_pod_urls(self, pod_id: str) -> Dict[str, str]:
        """Get service URLs for a pod (common ports)"""
        pod = self.get_pod_by_id(pod_id)
        
        if not pod:
            return {}
        
        urls = {
            'port_8188': f"https://{pod_id}-8188.proxy.runpod.net",  # Common web UI port
            'port_8888': f"https://{pod_id}-8888.proxy.runpod.net",  # Jupyter default
        }
        
        # Get SSH connection string
        host_id = pod.get('machine', {}).get('podHostId')
        if host_id:
            urls['ssh'] = f"ssh {host_id}@ssh.runpod.io -i ~/.ssh/id_ed25519"
        
        return urls
    
    def format_pod_status(self, pod: Dict) -> str:
        """Format pod information for display"""
        status = pod.get('desiredStatus', 'UNKNOWN')
        pod_id = pod.get('id', 'unknown')
        name = pod.get('name', 'unnamed')
        gpu = pod.get('machine', {}).get('gpuTypeId', 'unknown')
        uptime = pod.get('runtime', {}).get('uptimeInSeconds', 0)
        
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        
        status_emoji = "✅" if status == "RUNNING" else "⏸️" if status == "STOPPED" else "❓"
        
        return (
            f"{status_emoji} {name} ({pod_id})\n"
            f"   GPU: {gpu}\n"
            f"   Status: {status}\n"
            f"   Uptime: {hours}h {minutes}m\n"
        )

