#!/usr/bin/env python3
"""
rpRunner Core - Basic RunPod Connection Example

This is a minimal example showing how to connect to a RunPod pod
and check ComfyUI status. It's the foundation that the full rpRunner
pipeline builds upon.

Requirements:
    pip install runpod requests

Usage:
    export RUNPOD_API_KEY="your_key_here"
    python basic_pod_connect.py
    
For the full production pipeline with 15+ video models, voice synthesis,
batch processing, and 259 templates, contact Allan @ TitleCuts.
"""

import os
import requests
from typing import Optional

def get_pods(api_key: str) -> list:
    """List all your RunPod pods."""
    response = requests.get(
        "https://api.runpod.io/graphql",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "query": """
                query {
                    myself {
                        pods {
                            id
                            name
                            runtime { gpus { id gpuUtilPercent memoryUtilPercent } }
                            desiredStatus
                            machine { gpuDisplayName }
                        }
                    }
                }
            """
        }
    )
    data = response.json()
    return data.get("data", {}).get("myself", {}).get("pods", [])


def check_comfyui(pod_id: str) -> Optional[dict]:
    """Check if ComfyUI is running on a pod."""
    proxy_url = f"https://{pod_id}-8188.proxy.runpod.net"
    try:
        response = requests.get(f"{proxy_url}/system_stats", timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return None


def main():
    api_key = os.environ.get("RUNPOD_API_KEY")
    if not api_key:
        print("❌ Set RUNPOD_API_KEY environment variable")
        print("   export RUNPOD_API_KEY='your_key_here'")
        return
    
    print("🔍 Fetching your RunPod pods...\n")
    pods = get_pods(api_key)
    
    if not pods:
        print("No pods found. Create one at https://runpod.io")
        return
    
    for pod in pods:
        status = "✅" if pod["desiredStatus"] == "RUNNING" else "⏸️"
        gpu = pod.get("machine", {}).get("gpuDisplayName", "Unknown GPU")
        print(f"{status} {pod['name']} ({pod['id']})")
        print(f"   GPU: {gpu}")
        print(f"   Status: {pod['desiredStatus']}")
        
        if pod["desiredStatus"] == "RUNNING":
            comfy = check_comfyui(pod["id"])
            if comfy:
                vram = comfy.get("devices", [{}])[0]
                vram_used = vram.get("vram_total", 0) - vram.get("vram_free", 0)
                vram_total = vram.get("vram_total", 1)
                print(f"   ComfyUI: ✅ Running ({vram_used/1e9:.1f}/{vram_total/1e9:.1f} GB VRAM)")
            else:
                print(f"   ComfyUI: ❌ Not responding")
        print()
    
    print("---")
    print("This is the basic foundation. The full rpRunner suite adds:")
    print("  • 15+ video models (Veo, Kling, Luma, Minimax, etc.)")
    print("  • Voice synthesis with emotion control")
    print("  • Sound effects generation")
    print("  • 259 ComfyUI templates")
    print("  • Batch processing with resume")
    print("  • And much more...")
    print()
    print("📧 Contact: allan@titlecuts.com")


if __name__ == "__main__":
    main()
