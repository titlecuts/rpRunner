#!/usr/bin/env python3
"""
rpRunner™ - Zero-touch CLI for RunPod GPU management

Core pod management functionality only.
For ComfyUI automation, see rpComfy add-on.
For multi-provider AI, see rpAPI add-on.
"""
import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table

try:
    from config import AgentConfig
except ImportError:
    print("⚠️  config.py not found. Copy config.py.example to config.py and configure.")
    sys.exit(1)

from ssh_client import SSHClient
from runpod_client import RunPodClient


class RPRunner:
    """Core RunPod runner for pod management"""
    
    def __init__(self):
        self.console = Console()
        self.config = AgentConfig()
        
        if not self.config.runpod_api_key:
            self.console.print("[red]✗ RUNPOD_API_KEY not set[/red]")
            self.console.print("  Set environment variable or add to config.py")
            sys.exit(1)
        
        self.runpod_client = RunPodClient(self.config.runpod_api_key)
        self.ssh_client = SSHClient(str(self.config.ssh_key_path))
        self.connected_pod = None
    
    def list_pods(self):
        """List all pods"""
        self.console.print("\n[bold]Your RunPod Instances:[/bold]\n")
        
        pods = self.runpod_client.get_pods()
        if not pods:
            self.console.print("[yellow]No pods found[/yellow]")
            return
        
        table = Table()
        table.add_column("Pod ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("GPU", style="magenta")
        
        for pod in pods:
            status_color = "green" if pod.get('desiredStatus') == 'RUNNING' else "red"
            table.add_row(
                pod.get('id', 'N/A')[:12],
                pod.get('name', 'N/A'),
                f"[{status_color}]{pod.get('desiredStatus', 'UNKNOWN')}[/{status_color}]",
                pod.get('machine', {}).get('gpuDisplayName', 'N/A')
            )
        
        self.console.print(table)
    
    def connect_pod(self, pod_id):
        """Connect to a pod"""
        self.console.print(f"\n[bold]Connecting to pod {pod_id}...[/bold]\n")
        
        # Get pod details from API
        self.console.print("📡 Fetching pod details from RunPod API...")
        pod_info = self.runpod_client.get_pod(pod_id)
        
        if not pod_info:
            self.console.print("[red]✗ Pod not found[/red]")
            return False
        
        pod_name = pod_info.get('name', pod_id)
        runtime = pod_info.get('runtime', {})
        ports = runtime.get('ports', [])
        
        # Extract SSH connection info
        ssh_port = None
        for port in ports:
            if port.get('privatePort') == 22:
                ssh_port = port.get('publicPort')
                break
        
        if not ssh_port:
            self.console.print("[red]✗ No SSH port found for this pod[/red]")
            return False
        
        # Build SSH connection string
        pod_host = runtime.get('podHostId', '')
        ssh_connection = f"{pod_host}-{ssh_port}"
        
        self.console.print(f"✓ Pod found: {pod_name}")
        self.console.print(f"✓ SSH connection: {ssh_connection}")
        
        # Save pod state
        self.config.set_current_pod(pod_id, pod_name, pod_host)
        
        # Test SSH connection
        self.console.print("\n🔌 Testing SSH connection...")
        if self.ssh_client.connect(f"{pod_host}-{ssh_port}.proxy.runpod.net"):
            self.console.print("[green]✓ SSH connection successful![/green]")
            self.connected_pod = pod_id
            
            # Run health check
            self.console.print("\n💊 Running health check...")
            exit_code, stdout, stderr = self.ssh_client.execute_command("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader")
            if exit_code == 0 and stdout:
                self.console.print(f"[green]✓ GPU: {stdout.strip()}[/green]")
            
            self.console.print(f"\n[bold green]✅ Connected to {pod_name}[/bold green]")
            return True
        else:
            self.console.print("[red]✗ SSH connection failed[/red]")
            return False
    
    def check_pod(self):
        """Health check current pod"""
        pod_id = self.config.get_pod_id()
        if not pod_id:
            self.console.print("[yellow]No pod connected. Use 'rpconnect <pod_id>' first.[/yellow]")
            return
        
        self.console.print(f"\n[bold]Health Check: {self.config.get_pod_name()}[/bold]\n")
        
        # Reconnect if needed
        pod_host = self.config.get_pod_host()
        if not self.ssh_client.client or not self.ssh_client.is_connected():
            self.console.print("🔌 Reconnecting...")
            if not self.ssh_client.connect(f"{pod_host}.proxy.runpod.net"):
                self.console.print("[red]✗ Connection failed[/red]")
                return
        
        # GPU check
        self.console.print("🎮 Checking GPU...")
        exit_code, stdout, stderr = self.ssh_client.execute_command("nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader")
        if exit_code == 0 and stdout:
            self.console.print(f"[green]✓ {stdout.strip()}[/green]")
        else:
            self.console.print("[red]✗ GPU check failed[/red]")
        
        # Disk space
        self.console.print("\n💾 Checking disk space...")
        exit_code, stdout, stderr = self.ssh_client.execute_command("df -h /workspace | tail -1")
        if exit_code == 0 and stdout:
            self.console.print(f"[green]✓ {stdout.strip()}[/green]")
        
        self.console.print("\n[bold green]✅ Health check complete[/bold green]")
    
    def start_pod(self, pod_id):
        """Start a stopped pod"""
        self.console.print(f"\n[bold]Starting pod {pod_id}...[/bold]\n")
        
        success = self.runpod_client.start_pod(pod_id)
        if success:
            self.console.print("[green]✓ Pod start initiated[/green]")
            self.console.print("  Wait 30-60 seconds, then use 'rpconnect' to connect")
        else:
            self.console.print("[red]✗ Failed to start pod[/red]")
    
    def stop_pod(self, pod_id=None):
        """Stop a running pod"""
        if not pod_id:
            pod_id = self.config.get_pod_id()
        
        if not pod_id:
            self.console.print("[yellow]No pod specified. Use 'rpstop <pod_id>'[/yellow]")
            return
        
        self.console.print(f"\n[bold]Stopping pod {pod_id}...[/bold]\n")
        
        success = self.runpod_client.stop_pod(pod_id)
        if success:
            self.console.print("[green]✓ Pod stop initiated[/green]")
        else:
            self.console.print("[red]✗ Failed to stop pod[/red]")
    
    def upload_file(self, local_path, remote_path="/workspace/"):
        """Upload file to pod"""
        pod_id = self.config.get_pod_id()
        if not pod_id:
            self.console.print("[yellow]No pod connected. Use 'rpconnect <pod_id>' first.[/yellow]")
            return
        
        self.console.print(f"\n[bold]Uploading {local_path} to pod...[/bold]\n")
        
        # Reconnect if needed
        pod_host = self.config.get_pod_host()
        if not self.ssh_client.client or not self.ssh_client.is_connected():
            if not self.ssh_client.connect(f"{pod_host}.proxy.runpod.net"):
                self.console.print("[red]✗ Connection failed[/red]")
                return
        
        success, error = self.ssh_client.upload_file(local_path, remote_path)
        if success:
            self.console.print(f"[green]✓ Uploaded to {remote_path}[/green]")
        else:
            self.console.print(f"[red]✗ Upload failed: {error}[/red]")
    
    def download_file(self, remote_path, local_path):
        """Download file from pod"""
        pod_id = self.config.get_pod_id()
        if not pod_id:
            self.console.print("[yellow]No pod connected. Use 'rpconnect <pod_id>' first.[/yellow]")
            return
        
        self.console.print(f"\n[bold]Downloading {remote_path} from pod...[/bold]\n")
        
        # Reconnect if needed
        pod_host = self.config.get_pod_host()
        if not self.ssh_client.client or not self.ssh_client.is_connected():
            if not self.ssh_client.connect(f"{pod_host}.proxy.runpod.net"):
                self.console.print("[red]✗ Connection failed[/red]")
                return
        
        success, error = self.ssh_client.download_file(remote_path, local_path)
        if success:
            self.console.print(f"[green]✓ Downloaded to {local_path}[/green]")
        else:
            self.console.print(f"[red]✗ Download failed: {error}[/red]")
    
    def show_status(self):
        """Show current pod status"""
        pod_id = self.config.get_pod_id()
        if not pod_id:
            self.console.print("[yellow]No pod connected. Use 'rpconnect <pod_id>' first.[/yellow]")
            return
        
        self.console.print("\n[bold]Current Pod Configuration:[/bold]\n")
        self.console.print(f"  Pod ID: {pod_id}")
        self.console.print(f"  Pod Name: {self.config.get_pod_name()}")
        self.console.print(f"  SSH Host: {self.config.get_pod_host()}")
        self.console.print(f"  SSH Command: {self.config.get_ssh_command()}")
        self.console.print()
    
    def verify_keys(self):
        """Verify API key configuration"""
        self.console.print("\n[bold]API Key Verification:[/bold]\n")
        
        if self.config.runpod_api_key:
            self.console.print(f"[green]✓ RUNPOD_API_KEY configured ({self.config.runpod_api_key[:8]}...)[/green]")
            
            # Test API
            pods = self.runpod_client.get_pods()
            if pods is not None:
                self.console.print(f"[green]✓ RunPod API accessible ({len(pods)} pods found)[/green]")
            else:
                self.console.print("[red]✗ RunPod API test failed[/red]")
        else:
            self.console.print("[red]✗ RUNPOD_API_KEY not configured[/red]")
        
        self.console.print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="rpRunner™ - Zero-touch CLI for RunPod GPU management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rprunner.py pods                     # List all pods
  rprunner.py connect abc123xyz        # Connect to pod
  rprunner.py check                    # Health check current pod
  rprunner.py start abc123xyz          # Start a pod
  rprunner.py stop                     # Stop current pod
  rprunner.py upload file.txt          # Upload file
  rprunner.py download /workspace/out.png ./local.png
  rprunner.py status                   # Show current pod info
  rprunner.py keys                     # Verify API keys

Add-ons:
  rpComfy - ComfyUI workflow automation
  rpAPI - Multi-provider AI orchestration
  rpPipe - Production tracking
  rpStore - Storage optimization
        """
    )
    
    parser.add_argument('command', help='Command to run')
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    
    # Initialize runner
    runner = RPRunner()
    
    # Route commands
    cmd = args.command.lower()
    
    if cmd in ['pods', 'list', 'rpp']:
        runner.list_pods()
    
    elif cmd in ['connect', 'rpconnect']:
        if not args.args:
            print("Usage: rprunner.py connect <pod_id>")
            sys.exit(1)
        runner.connect_pod(args.args[0])
    
    elif cmd in ['check', 'rpcheck', 'health']:
        runner.check_pod()
    
    elif cmd in ['start', 'rpstart']:
        if not args.args:
            print("Usage: rprunner.py start <pod_id>")
            sys.exit(1)
        runner.start_pod(args.args[0])
    
    elif cmd in ['stop', 'rpstop']:
        pod_id = args.args[0] if args.args else None
        runner.stop_pod(pod_id)
    
    elif cmd in ['upload', 'rpupload']:
        if not args.args:
            print("Usage: rprunner.py upload <local_file> [remote_path]")
            sys.exit(1)
        local_path = args.args[0]
        remote_path = args.args[1] if len(args.args) > 1 else "/workspace/"
        runner.upload_file(local_path, remote_path)
    
    elif cmd in ['download', 'rpdownload']:
        if len(args.args) < 2:
            print("Usage: rprunner.py download <remote_path> <local_path>")
            sys.exit(1)
        runner.download_file(args.args[0], args.args[1])
    
    elif cmd in ['status', 'rpstatus']:
        runner.show_status()
    
    elif cmd in ['keys', 'rpkeys', 'verify']:
        runner.verify_keys()
    
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'rprunner.py --help' for usage")
        sys.exit(1)


if __name__ == '__main__':
    main()

