"""
SSH Client for RunPod
Core connectivity and basic operations
"""
import paramiko
import shlex
from pathlib import Path
from typing import Tuple


class SSHClient:
    """Client for SSH connections to RunPod pods"""
    
    def __init__(self, ssh_key_path: str = "~/.ssh/id_ed25519"):
        self.ssh_key_path = Path(ssh_key_path).expanduser()
        self.client = None
        self.connected_host = None
    
    def connect(self, host_id: str) -> bool:
        """Connect to a RunPod pod via SSH"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Load private key
            key = paramiko.Ed25519Key.from_private_key_file(str(self.ssh_key_path))
            
            # Connect
            hostname = "ssh.runpod.io"
            username = host_id
            
            self.client.connect(
                hostname=hostname,
                username=username,
                pkey=key,
                timeout=10
            )
            
            self.connected_host = host_id
            return True
            
        except Exception as e:
            print(f"SSH connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            self.client = None
            self.connected_host = None
    
    def upload_file(self, local_path: str, remote_path: str) -> Tuple[bool, str]:
        """
        Upload a file to the remote pod using base64 encoding over SSH
        More reliable than SFTP for RunPod
        
        Args:
            local_path: Local file path
            remote_path: Remote destination path
            
        Returns:
            (success: bool, error_message: str)
        """
        if not self.client:
            return (False, "Not connected")
        
        try:
            import base64
            
            # Read and encode file
            with open(local_path, 'rb') as f:
                file_data = f.read()
            
            encoded = base64.b64encode(file_data).decode('ascii')
            
            # Ensure remote directory exists
            remote_dir = str(Path(remote_path).parent)
            self.execute_command(f"mkdir -p {remote_dir}")
            
            # Upload in chunks to avoid command length limits
            chunk_size = 50000  # Safe chunk size for SSH commands
            
            # Clear/create file
            self.execute_command(f"rm -f {remote_path}")
            
            for i in range(0, len(encoded), chunk_size):
                chunk = encoded[i:i + chunk_size]
                # Append chunk to file
                cmd = f'echo "{chunk}" | base64 -d >> {remote_path}'
                exit_code, stdout, stderr = self.execute_command(cmd, timeout=60)
                
                if exit_code != 0:
                    return (False, f"Failed to write chunk: {stderr}")
            
            return (True, "")
            
        except Exception as e:
            return (False, str(e))
    
    def download_file(self, remote_path: str, local_path: str) -> Tuple[bool, str]:
        """
        Download a file from the remote pod using base64 encoding over SSH
        
        Args:
            remote_path: Remote file path
            local_path: Local destination path
            
        Returns:
            (success: bool, error_message: str)
        """
        if not self.client:
            return (False, "Not connected")
        
        try:
            import base64
            
            # Read file as base64
            exit_code, stdout, stderr = self.execute_command(
                f"base64 {remote_path}", timeout=120
            )
            
            if exit_code != 0:
                return (False, f"Failed to read remote file: {stderr}")
            
            # Decode and write locally
            file_data = base64.b64decode(stdout.strip())
            
            local_file = Path(local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_file, 'wb') as f:
                f.write(file_data)
            
            return (True, "")
            
        except Exception as e:
            return (False, str(e))
    
    def execute_command(self, command: str, timeout: int = 30) -> Tuple[int, str, str]:
        """
        Execute a command on the remote pod
        Returns: (exit_code, stdout, stderr)
        """
        if not self.client:
            return (-1, "", "Not connected")
        
        try:
            # Wrap command in bash -c to ensure shell expansion of wildcards
            shell_command = f'bash -c {shlex.quote(command)}'
            stdin, stdout, stderr = self.client.exec_command(shell_command, timeout=timeout, get_pty=False)
            
            # IMPORTANT: Read stdout/stderr BEFORE getting exit status
            stdout_text = stdout.read().decode('utf-8')
            stderr_text = stderr.read().decode('utf-8')
            
            # Get exit code AFTER reading output
            exit_code = stdout.channel.recv_exit_status()
            
            # Filter out RunPod PTY noise
            stderr_text = self._filter_pty_errors(stderr_text)
            stdout_text = self._filter_pty_errors(stdout_text)
            
            return (exit_code, stdout_text, stderr_text)
            
        except Exception as e:
            return (-1, "", str(e))
    
    def _filter_pty_errors(self, text: str) -> str:
        """Filter out RunPod PTY warnings that aren't real errors"""
        if not text:
            return text
        
        pty_patterns = [
            "Error: Your SSH client doesn't support PTY",
            "PTY allocation request failed",
            "stdin: is not a tty",
        ]
        
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            if any(pattern in line for pattern in pty_patterns):
                continue
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def get_disk_usage(self) -> dict:
        """Get disk usage information from the pod"""
        exit_code, stdout, stderr = self.execute_command("df -h /workspace")
        
        if exit_code != 0:
            return {"error": stderr}
        
        lines = stdout.strip().split('\n')
        if len(lines) < 2:
            return {"error": "Unexpected df output"}
        
        parts = lines[1].split()
        
        return {
            'filesystem': parts[0],
            'size': parts[1],
            'used': parts[2],
            'available': parts[3],
            'use_percent': parts[4],
            'mounted_on': parts[5] if len(parts) > 5 else '/workspace'
        }
    
    def get_gpu_info(self) -> dict:
        """Get GPU information using nvidia-smi"""
        exit_code, stdout, stderr = self.execute_command(
            "nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader"
        )
        
        if exit_code != 0:
            return {"error": stderr}
        
        parts = stdout.strip().split(',')
        if len(parts) < 4:
            return {"error": "Unexpected nvidia-smi output"}
        
        return {
            'name': parts[0].strip(),
            'memory_total': parts[1].strip(),
            'memory_used': parts[2].strip(),
            'memory_free': parts[3].strip()
        }
    
    def check_service_running(self, port: int) -> bool:
        """Check if a service is running on a given port"""
        exit_code, stdout, stderr = self.execute_command(f"lsof -i:{port}")
        return exit_code == 0 and len(stdout.strip()) > 0
    
    def list_directory(self, path: str) -> list:
        """List contents of a directory"""
        exit_code, stdout, stderr = self.execute_command(f"ls -la {path}")
        
        if exit_code != 0:
            return []
        
        return [line for line in stdout.strip().split('\n') if line.strip()]
    
    def file_exists(self, path: str) -> bool:
        """Check if a file exists on the remote pod"""
        exit_code, _, _ = self.execute_command(f"test -f {path}")
        return exit_code == 0
    
    def directory_exists(self, path: str) -> bool:
        """Check if a directory exists on the remote pod"""
        exit_code, _, _ = self.execute_command(f"test -d {path}")
        return exit_code == 0
