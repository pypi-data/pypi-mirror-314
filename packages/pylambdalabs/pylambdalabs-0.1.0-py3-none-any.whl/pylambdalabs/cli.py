#!/usr/bin/env python3

"""
Lambda Cloud CLI - A professional command-line interface for Lambda Labs GPU cloud.

This CLI tool provides a seamless interface for managing GPU instances on Lambda Cloud,
including listing available instances, starting/stopping instances, and managing file systems.
"""

import os
import time
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import re
import json
import random

import click
import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich import print as rprint
from dotenv import load_dotenv
import textwrap

# Initialize Rich console
console = Console()

# API Configuration
BASE_URL = "https://cloud.lambdalabs.com/api/v1"
load_dotenv()

@dataclass
class InstanceSpecs:
    vcpus: int
    memory_gib: int
    storage_gib: int
    gpus: int

@dataclass
class InstanceType:
    name: str
    description: str
    gpu_description: str
    price_cents_per_hour: int
    specs: InstanceSpecs

@dataclass
class Region:
    name: str
    description: str

@dataclass
class InstanceTypeResponse:
    instance_type: InstanceType
    regions_with_capacity_available: List[Region]

@dataclass
class Instance:
    """Instance details matching OpenAPI schema."""
    id: str
    name: Optional[str]
    ip: Optional[str]
    status: str
    jupyter_url: Optional[str]
    is_reserved: bool
    ssh_key_names: List[str]
    file_system_names: Optional[List[str]]
    region: Dict[str, str]  # {name: str, description: str}
    instance_type: Dict[str, Any]  # Matches instanceType schema

@dataclass
class FileSystem:
    """File system details matching OpenAPI schema."""
    id: str
    name: str
    created: str  # ISO 8601 datetime
    created_by: Dict[str, str]  # user object
    mount_point: str
    region: Dict[str, str]
    is_in_use: bool
    bytes_used: Optional[int]

class LambdaAPIError(Exception):
    """Custom exception for Lambda API errors matching OpenAPI spec."""
    def __init__(self, code: str, message: str, suggestion: str = None, field_errors: Dict = None):
        self.code = code  # Must be one of the enum values from components.schemas.errorCode
        self.message = message
        self.suggestion = suggestion
        self.field_errors = field_errors or {}
        super().__init__(self.message)

class LambdaCloudAPI:
    """Handler for Lambda Cloud API interactions."""
    
    def __init__(self, api_key: str):
        """Initialize API handler with authentication."""
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
    def _make_request(self, method: str, endpoint: str, json: Dict = None) -> Dict:
        """Make an authenticated request to the Lambda Cloud API."""
        url = f"{BASE_URL}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method, url, headers=self.headers, json=json, timeout=30)
            
            if not response.ok:
                error_data = response.json().get("error", {})
                raise LambdaAPIError(
                    code=error_data.get("code", "global/unknown"),
                    message=error_data.get("message", "Unknown error occurred"),
                    suggestion=error_data.get("suggestion"),
                    field_errors=response.json().get("field_errors", {})
                )
            
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise click.ClickException(f"Invalid response from API. Status code: {response.status_code}, Response text: {response.text}")
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"Request failed: {str(e)}")

    def validate_api_key(self) -> bool:
        """Validate the API key by making a test request."""
        try:
            self._make_request("GET", "/instances")
            return True
        except requests.exceptions.HTTPError:
            return False

    def list_instances(self) -> Dict:
        """Get available instance types and their details."""
        return self._make_request("GET", "/instance-types")

    def list_running_instances(self) -> Dict:
        """Get currently running instances."""
        return self._make_request("GET", "/instances")

    def start_instance(self, instance_type: str, ssh_key: str, region: str, 
                      filesystem: Optional[str] = None, name: Optional[str] = None) -> Dict:
        """Launch instance matching OpenAPI launch schema."""
        payload = {
            "region_name": region,
            "instance_type_name": instance_type,
            "ssh_key_names": [ssh_key],  # API requires exactly one
            "quantity": 1  # API requires exactly one
        }
        
        if filesystem:
            payload["file_system_names"] = [filesystem]  # API allows max one
        if name:
            payload["name"] = name
            
        return self._make_request("POST", "/instance-operations/launch", json=payload)

    def stop_instance(self, instance_id: str) -> Dict:
        """Terminate instance matching OpenAPI terminate schema."""
        payload = {"instance_ids": [instance_id]}
        response = self._make_request("POST", "/instance-operations/terminate", json=payload)
        return response["data"]["terminated_instances"][0]

    def get_instance_details(self, instance_id: str) -> Dict:
        """Get details for a specific instance matching OpenAPI getInstance schema."""
        return self._make_request("GET", f"/instances/{instance_id}")

    def list_file_systems(self) -> Dict:
        """Get available file systems."""
        return self._make_request("GET", "/file-systems")

    def get_instance_type_response(self, gpu: str) -> Optional[InstanceTypeResponse]:
        """Get instance type details matching Rust implementation."""
        response = self._make_request("GET", "/instance-types")
        return response["data"].get(gpu)

    def list_ssh_keys(self) -> Dict:
        """Get available SSH keys matching OpenAPI listSSHKeys operation."""
        return self._make_request("GET", "/ssh-keys")

    def add_ssh_key(self, name: str, public_key: Optional[str] = None) -> Dict:
        """Add an SSH key matching OpenAPI addSSHKey operation."""
        payload = {"name": name}
        if public_key:
            payload["public_key"] = public_key
        return self._make_request("POST", "/ssh-keys", json=payload)

    def delete_ssh_key(self, key_id: str) -> None:
        """Delete an SSH key matching OpenAPI deleteSSHKey operation."""
        self._make_request("DELETE", f"/ssh-keys/{key_id}")

    def restart_instance(self, instance_id: str) -> Dict:
        """Restart instance matching OpenAPI restart schema."""
        payload = {"instance_ids": [instance_id]}
        response = self._make_request("POST", "/instance-operations/restart", json=payload)
        return response["data"]["restarted_instances"][0]

    def validate_ssh_key(self, key_name: str) -> bool:
        """Validate that an SSH key exists."""
        try:
            response = self.list_ssh_keys()
            return any(key["name"] == key_name for key in response["data"])
        except LambdaAPIError as e:
            raise click.ClickException(f"Failed to validate SSH key: {e.message}")

def display_instance_types_table(instances_data: Dict) -> None:
    """Display available instance types in a formatted table."""
    table = Table(title="Available Instance Types")
    table.add_column("Instance Type", style="green")
    table.add_column("Description")
    table.add_column("Price/Hour", style="yellow")
    table.add_column("vCPUs")
    table.add_column("Memory (GB)")
    table.add_column("Storage (GB)")
    table.add_column("Available Regions", style="blue")

    for instance_type, data in instances_data["data"].items():
        specs = data["instance_type"]["specs"]
        regions = [f"{r['name']} ({r['description']})" 
                  for r in data["regions_with_capacity_available"]]
        
        if regions:  # Only show instances that are available
            table.add_row(
                instance_type,
                data["instance_type"]["description"],
                f"${data['instance_type']['price_cents_per_hour']/100:.2f}",
                str(specs["vcpus"]),
                str(specs["memory_gib"]),
                str(specs["storage_gib"]),
                "\n".join(regions)
            )

    console.print(table)

@click.group()
def cli():
    """Lambda Cloud CLI - Professional command-line interface for Lambda Labs GPU cloud."""
    pass

@cli.command()
def validate():
    """Validate the configured API key."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    with console.status("[bold green]Validating API key..."):
        if api.validate_api_key():
            console.print("[green]✓[/green] API key is valid")
        else:
            console.print("[red]✗[/red] Invalid API key")

@cli.command()
def list():
    """List all available GPU instances and their specifications."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold green]Fetching available instances..."):
        response = api.list_instances()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Instance Type", style="green")
    table.add_column("Description")
    table.add_column("Price/Hour", style="yellow")
    table.add_column("vCPUs", justify="right")
    table.add_column("Memory (GB)", justify="right")
    table.add_column("Storage (GB)", justify="right")
    table.add_column("Available Regions", style="blue")
    
    for name, data in response["data"].items():
        instance = data["instance_type"]
        regions = [f"{r['name']} ({r['description']})" for r in data["regions_with_capacity_available"]]
        
        if regions:  # Only show instances that are available
            table.add_row(
                name,
                instance["description"],
                f"${instance['price_cents_per_hour']/100:.2f}",
                str(instance["specs"]["vcpus"]),
                str(instance["specs"]["memory_gib"]),
                str(instance["specs"]["storage_gib"]),
                "\n".join(regions)
            )
    
    console.print(table)

@cli.command()
def running():
    """List running instances."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold green]Fetching running instances..."):
        response = api.list_running_instances()
    
    table = Table()
    table.add_column("Instance ID", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("IP Address", style="blue")
    table.add_column("SSH Key Names", style="purple")
    
    for instance in response["data"]:
        table.add_row(
            instance.get("id", "N/A"),
            instance.get("status", "N/A"),
            instance.get("ip", "N/A"),
            ", ".join(instance.get("ssh_key_names", ["N/A"]))
        )
    
    console.print(table)

@cli.command()
@click.option("--gpu", "-g", required=True, help="GPU instance type to start")
@click.option("--ssh", "-s", required=True, help="SSH key name to use")
@click.option("--filesystem", "-f", help="File system to attach")
def start(gpu: str, ssh: str, filesystem: str = None):
    """Start a new GPU instance."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    # Validate SSH key exists before attempting to start instance
    with console.status("[bold green]Validating SSH key..."):
        if not api.validate_ssh_key(ssh):
            raise click.ClickException(f"SSH key '{ssh}' not found. Use 'lambda keys' to list available keys.")
    
    with console.status("[bold green]Checking instance availability..."):
        instance_type = api.get_instance_type_response(gpu)
        if not instance_type or not instance_type["regions_with_capacity_available"]:
            raise click.ClickException(f"Instance type {gpu} not found or not available")
        
        region = instance_type["regions_with_capacity_available"][0]["name"]
    
    with console.status("[bold green]Starting instance...") as status:
        try:
            response = api.start_instance(gpu, ssh, region, filesystem)
            instance_id = response["data"]["instance_ids"][0]
            
            status.update(f"[bold green]Instance {instance_id} started in region {region}. Waiting for it to become active...")
            
            # Match Rust's behavior: wait for 120 seconds
            time.sleep(120)
            
            instance = api.get_instance_details(instance_id)["data"]
            if instance.get("ip"):
                console.print(f"[green]Instance is active. SSH IP:[/green] {instance['ip']}")
            else:
                console.print("[yellow]Instance is active, but IP address is not available yet.[/yellow]")
            
        except LambdaAPIError as e:
            if e.code == "instance-operations/launch/insufficient-capacity":
                raise click.ClickException("No capacity available in the selected region")
            elif e.code == "global/quota-exceeded":
                raise click.ClickException("Account quota exceeded")
            raise click.ClickException(f"Failed to start instance: {e.message}")

@cli.command()
@click.option("--id", "-i", required=True, help="Instance ID to stop")
def stop(id: str):
    """Stop a running instance."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold red]Stopping instance..."):
        try:
            api.stop_instance(id)
            console.print(f"[green]Instance {id} stopped[/green]")
        except LambdaAPIError as e:
            if e.code == "global/object-does-not-exist":
                raise click.ClickException(f"Instance {id} not found")
            raise click.ClickException(f"Failed to stop instance: {e.message}")

@cli.command()
def filesystems():
    """List available file systems."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold green]Fetching file systems..."):
        response = api.list_file_systems()
    
    table = Table(title="File Systems")
    table.add_column("Name", style="green")
    table.add_column("ID")
    table.add_column("Region", style="blue")
    table.add_column("Mount Point")
    table.add_column("Status", style="yellow")
    table.add_column("Size", justify="right")
    
    for fs in response["data"]:
        table.add_row(
            fs["name"],
            fs["id"],
            f"{fs['region']['name']} ({fs['region']['description']})",
            fs["mount_point"],
            "[green]In Use[/green]" if fs["is_in_use"] else "[blue]Available[/blue]",
            f"{fs.get('bytes_used', 0) / (1024**3):.1f} GB" if fs.get("bytes_used") else "N/A"
        )
    
    console.print(table)

def wait_for_instance(api: LambdaCloudAPI, instance_id: str, timeout: int = 300) -> Dict:
    """Wait for instance to become active with timeout and status updates."""
    start_time = time.time()
    status_map = {
        "pending": "[yellow]⋯[/yellow]",
        "active": "[green]✓[/green]",
        "terminated": "[red]✗[/red]",
        "failed": "[red]✗[/red]"
    }
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("Waiting for instance to start...", total=None)
        
        while True:
            if time.time() - start_time > timeout:
                raise click.ClickException(f"Timeout waiting for instance {instance_id} to become active")
            
            try:
                instance = api.get_instance_details(instance_id)["data"]
                status = instance.get("status", "unknown")
                progress.update(task, description=f"Instance status: {status_map.get(status, '?')} {status}")
                
                if status == "active":
                    return instance
                elif status in ["terminated", "failed"]:
                    raise click.ClickException(f"Instance failed to start: {status}")
                
                time.sleep(5)
            except Exception as e:
                progress.stop()
                raise click.ClickException(f"Error checking instance status: {str(e)}")

@cli.command()
@click.option("--gpu", "-g", help="Specific GPU instance type to find (optional)")
@click.option("--ssh", "-s", help="SSH key name to use (required if --launch is specified)")
@click.option("--region", "-r", help="Preferred region")
@click.option("--cores", "-c", type=int, help="Minimum CPU cores required")
@click.option("--storage", "-d", type=int, help="Minimum storage in GB required")
@click.option("--gpus", "-n", type=int, help="Minimum number of GPUs required")
@click.option("--vram", "-v", type=int, help="Minimum VRAM per GPU in GB required")
@click.option("--filesystem", "-f", help="Existing filesystem ID to use")
@click.option("--interval", "-i", default=10, help="Check interval in seconds", type=int)
@click.option("--timeout", "-t", default=3600, help="Total timeout in seconds", type=int)
@click.option("--launch/--no-launch", default=False, help="Launch instance if found")
def find(gpu: str, ssh: str, region: str, cores: int, storage: int, 
         gpus: int, vram: int, filesystem: str, interval: int, timeout: int, launch: bool):
    """Monitor for available GPU instances matching specified criteria."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    start_time = time.time()
    retry_interval = interval
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Last Check")
    table.add_column("Status")
    table.add_column("Available Regions")
    table.add_column("Next Check")
    
    with Live(table, refresh_per_second=1) as live:
        while True:
            try:
                response = api.list_instances()
                retry_interval = interval
                
                # Debug: Print first instance's data structure
                first_instance = next(iter(response["data"].items()))
                print("Instance data structure:")
                print(json.dumps(first_instance[1], indent=2))
                
                matching_instances = []
                for instance_type, instance_data in response["data"].items():
                    # Filter regions based on criteria
                    available_regions = instance_data["regions_with_capacity_available"]
                    if region:
                        available_regions = [r for r in available_regions if r["name"] == region]
                    
                    if not available_regions:
                        continue
                        
                    # Check all requirements
                    specs = instance_data["instance_type"]["specs"]
                    gpu_description = instance_data["instance_type"]["gpu_description"]
                    
                    # Get GPU count directly from specs
                    gpu_count = specs["gpus"]
                    
                    # Get VRAM from gpu_description (e.g., "GH200 (96 GB)" -> 96)
                    vram_match = re.search(r'\((\d+)\s*GB', gpu_description, re.IGNORECASE)
                    gpu_vram = int(vram_match.group(1)) if vram_match else 0
                    
                    print(f"Checking {instance_type}:")
                    print(f"  Found: {gpu_count} GPUs with {gpu_vram}GB VRAM each")
                    
                    # Apply all filters
                    if cores and specs["vcpus"] < cores:
                        print(f"  Skipping: cores {specs['vcpus']} < {cores}")
                        continue
                    if storage and specs["storage_gib"] < storage:
                        print(f"  Skipping: storage {specs['storage_gib']} < {storage}")
                        continue
                    if gpus and gpu_count < gpus:
                        print(f"  Skipping: GPUs {gpu_count} < {gpus}")
                        continue
                    if vram and gpu_vram < vram:
                        print(f"  Skipping: VRAM {gpu_vram} < {vram}")
                        continue
                    
                    print(f"  Matched!")
                    matching_instances.append((instance_type, available_regions))
                
                if matching_instances:
                    table.add_row(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        f"[green]Found {len(matching_instances)} matching instance types![/green]",
                        "\n".join(
                            f"{instance_type}: {', '.join(r['name'] + ' (' + r['description'] + ')' for r in regions)}"
                            for instance_type, regions in matching_instances
                        ),
                        "[green]✓[/green]"
                    )
                    
                    if launch:
                        if len(matching_instances) > 1:
                            # Sort instances by price, memory, and random factor
                            sorted_instances = []
                            for instance_type, regions in matching_instances:
                                instance_data = response["data"][instance_type]
                                price = instance_data["instance_type"]["price_cents_per_hour"] / 100.0
                                memory = instance_data["instance_type"]["specs"]["memory_gib"]
                                sorted_instances.append((instance_type, regions, price, memory))
                            
                            # Sort by price (ascending), then memory (descending), then randomly
                            sorted_instances.sort(key=lambda x: (x[2], -x[3], random.random()))
                            
                            # Show options to user
                            console.print("\n[yellow]Multiple instance types available:[/yellow]")
                            for i, (instance_type, regions, price, memory) in enumerate(sorted_instances, 1):
                                console.print(f"{i}. {instance_type}")
                                console.print(f"   Price: ${price:.2f}/hour")
                                console.print(f"   Memory: {memory} GB")
                                console.print(f"   Regions: {', '.join(r['name'] for r in regions)}")
                            
                            # Select the cheapest option
                            selected = sorted_instances[0]
                            console.print(f"\n[green]Selected {selected[0]} (cheapest option at ${selected[2]:.2f}/hour)[/green]")
                            
                            instance_type, available_regions = selected[0], selected[1]
                        else:
                            instance_type, available_regions = matching_instances[0]
                        
                        selected_region = available_regions[0]["name"]
                        console.print(f"\n[yellow]Launching instance {instance_type} in {selected_region}...[/yellow]")
                        
                        try:
                            response = api.start_instance(instance_type, ssh, selected_region, filesystem)
                            instance_id = response["data"]["instance_ids"][0]
                            
                            with console.status("[bold green]Waiting for instance to become active...") as status:
                                instance = wait_for_instance(api, instance_id)
                                console.print("\n[green]Instance launched successfully![/green]")
                                if instance.get("jupyter_url"):
                                    console.print(f"[blue]Jupyter URL:[/blue] {instance['jupyter_url']}")
                                console.print(f"[green]SSH command:[/green] ssh -i {ssh}.pem ubuntu@{instance.get('ip', 'N/A')}")
                        except LambdaAPIError as e:
                            handle_api_error(e)
                        return
                    else:
                        return
                
                table.add_row(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "[red]No matching instances available[/red]",
                    "",
                    f"[yellow]{retry_interval}s[/yellow]"
                )
                
                time.sleep(retry_interval)
                
            except Exception as e:
                if "429" in str(e):
                    retry_interval = min(retry_interval * 2, 300)
                    status = f"[yellow]Rate limited. Backing off for {retry_interval}s[/yellow]"
                else:
                    status = f"[red]Error: {str(e)}[/red]"
                
                table.add_row(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status,
                    "",
                    f"[yellow]{retry_interval}s[/yellow]"
                )
                
                time.sleep(retry_interval)

def handle_api_error(e: LambdaAPIError):
    """Handle API errors based on OpenAPI error codes."""
    error_messages = {
        "global/unknown": "An unknown error occurred",
        "global/invalid-api-key": "Invalid API key",
        "global/account-inactive": "Account is inactive",
        "global/invalid-address": "Invalid address provided",
        "global/invalid-parameters": "Invalid parameters provided",
        "global/object-does-not-exist": "Requested resource does not exist",
        "global/quota-exceeded": "Account quota exceeded",
        "instance-operations/launch/insufficient-capacity": "No capacity available",
        "instance-operations/launch/file-system-in-wrong-region": "File system is in wrong region",
        "ssh-keys/key-in-use": "SSH key is in use"
    }
    
    message = error_messages.get(e.code, e.message)
    if e.suggestion:
        message = f"{message}\nSuggestion: {e.suggestion}"
    if e.field_errors:
        message = f"{message}\nField errors: {e.field_errors}"
    raise click.ClickException(message)

@cli.command()
@click.argument("key-name")
@click.option("--public-key", "-k", help="Public key content. If not provided, a new key pair will be generated.")
def add_key(key_name: str, public_key: Optional[str]):
    """Add an SSH key to your account."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold green]Adding SSH key..."):
        response = api.add_ssh_key(key_name, public_key)
        key_data = response["data"]
        
        if "private_key" in key_data:
            # New key pair was generated
            private_key_path = f"{key_name}.pem"
            with open(private_key_path, "w") as f:
                f.write(key_data["private_key"])
            os.chmod(private_key_path, 0o400)
            console.print(f"[green]✓[/green] New key pair generated and saved to {private_key_path}")
        else:
            console.print(f"[green]✓[/green] Public key added successfully")

@cli.command()
def keys():
    """List all SSH keys."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold green]Fetching SSH keys..."):
        response = api.list_ssh_keys()
    
    table = Table(title="SSH Keys")
    table.add_column("Name", style="green")
    table.add_column("ID")
    table.add_column("Public Key", style="blue")
    
    for key in response["data"]:
        table.add_row(
            key["name"],
            key["id"],
            textwrap.shorten(key["public_key"], width=50, placeholder="...")
        )
    
    console.print(table)

@cli.command()
@click.argument("instance-id")
def restart(instance_id: str):
    """Restart a running instance."""
    api = LambdaCloudAPI(os.getenv("LAMBDA_API_KEY"))
    
    with console.status("[bold green]Restarting instance..."):
        try:
            instance = api.restart_instance(instance_id)
            console.print(f"[green]Instance {instance_id} restarted successfully[/green]")
            if instance.get("jupyter_url"):
                console.print(f"\n[blue]Jupyter URL:[/blue] {instance['jupyter_url']}")
            console.print(f"[green]SSH command:[/green] ssh ubuntu@{instance.get('ip', 'N/A')}")
        except LambdaAPIError as e:
            handle_api_error(e)

if __name__ == "__main__":
    cli()
