import typer
import requests
from rich import print
import os
from dotenv import load_dotenv

app = typer.Typer()

load_dotenv(dotenv_path="./typercli/.env")
BASE_URL_ZAP = os.getenv("BASE_URL_ZAP", "http://127.0.0.1:8000/ZAP")
BASE_URL_NMAP = os.getenv("BASE_URL_NMAP", "http://127.0.0.1:8000/nmap")


@app.command("zap")
def zap_scan(domains: str):
    """
    Perform ZAP spider scan. Required input format:
    "example1.com, example2.com"
    """
    try:
        domain_list = [domain.strip() for domain in domains.split(",")]

        url = f"{BASE_URL_ZAP}/scan/multipleDomains" 
    
        response = requests.post(url, json={"domains": domain_list})
        if response.status_code == 200:
            results = response.json()
            display_zap_vulnerabilities(results)        
        else:
            print(f"[red]Failed to call ZAP API: {response.status_code} - {response.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")


@app.command("nmap_script_common_ports")
def nmap_script_common_ports(ips: str, script: str):
    """
    Perform Nmap Script engine scan. Required input format:
    "example1.com, example2.com" "Script"
    """
    ip_list = [ip.strip() for ip in ips.split(",")]

    url = f"{BASE_URL_NMAP}/script/commonPorts/multipleDomains" 
    
    try:
        response = requests.post(url, json={"ips": ip_list, "script": script})
        if response.status_code == 200:
            results = response.json()
            display_nmap_vulnerabilities(results)         
        else:
            print(f"[red]Failed to call Nmap API: {response.status_code} - {response.text}[/red]")
    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")


@app.command("nmap_without_ping")
def nmap_without_ping(ips: str):
    """
    Perform Nmap SYN scan without PING. Required input format:
    "example1.com, example2.com"
    """
    try:
        ip_list = [ip.strip() for ip in ips.split(",")]

        url = f"{BASE_URL_NMAP}/scanWithoutPing/multipleDomains" 
    
        response = requests.post(url, json={"ips": ip_list})
        if response.status_code == 200:
            results = response.json()
            display_nmap_results(results)  
                    
        else:
            print(f"[red]Failed to call Nmap API: {response.status_code} - {response.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")


@app.command("nmap_with_ping")
def nmap_with_ping(ips: str):
    """
    Perform Nmap SYN scan with PING. Required input format:
    "example1.com, example2.com"
    """
    try:
        ip_list = [ip.strip() for ip in ips.split(",")]

        url = f"{BASE_URL_NMAP}/scanWithPing/multipleDomains" 
    
        response = requests.post(url, json={"ips": ip_list})
        if response.status_code == 200:
            results = response.json()
            display_nmap_results(results)           
        else:
            print(f"[red]Failed to call Nmap API: {response.status_code} - {response.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")


@app.command("vulnerability")
def vulnerability_scan(targets: str, script: str):
    """
    Perform ZAP and Nmap Script Scans for vulnerabilities. Required input format:
    "example1.com, example2.com" "Nmap script"

    """
    try:
        target_list = [target.strip() for target in targets.split(",")]

        # Run ZAP Scan first
        print("\n[bold green]Starting ZAP Scan...[/bold green]")
    
        url_zap = f"{BASE_URL_ZAP}/scan/multipleDomains"
        response_zap = requests.post(url_zap, json={"domains": target_list})
        if response_zap.status_code == 200:
            result_zap = response_zap.json()
            display_zap_vulnerabilities(result_zap)
        else:
            print(f"[red]Failed to call ZAP Scan API: {response_zap.status_code} - {response_zap.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred during ZAP Scan: {str(e)}[/red]")

    # Run Nmap Script Scan 
    print("\n[bold green]Starting Nmap Script Scan on Common Ports...[/bold green]")
    try:
        url_script = f"{BASE_URL_NMAP}/script/commonPorts/multipleDomains"
        response_script = requests.post(url_script, json={"ips": target_list, "script": script})
        if response_script.status_code == 200:
            result_script = response_script.json()
            display_nmap_vulnerabilities(result_script)
        else:
            print(f"[red]Failed to call Nmap Script Scan API: {response_script.status_code} - {response_script.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred during Nmap Script Scan: {str(e)}[/red]")


def display_zap_vulnerabilities(results):
    """
    Display vulnerability results from ZAP scans
    """
    print("\n[bold green]ZAP Scan Results:[/bold green]")
    if isinstance(results, str):
        print(f"[red]Error: {results}[/red]")
    else:
        for domain, alerts in results.items():
            print(f"\n[bold white]Domain:[/bold white] [bold green]{domain}[/bold green]")
            
            if isinstance(alerts, dict) and "message" in alerts:
                print("  [bold white]No vulnerabilities found.[/bold white]")
            elif isinstance(alerts, dict) and "error" in alerts:
                print(f"  [red]Error: {alerts['error']}[/red]")
            else:
                for alert in alerts:
                    print(f"\n[bold white]Alert:[/bold white] [italic]{alert.get('alert', 'N/A')}[/italic]")
                    print(f"[bold white]URL:[/bold white] [italic]{alert.get('url', 'N/A')}[/italic]")
                    print(f"[bold white]Risk:[/bold white] [italic]{alert.get('risk', 'N/A')}[/italic]")
                    print(f"[bold white]Confidence:[/bold white] [italic]{alert.get('confidence', 'N/A')}[/italic]")
                    print(f"[bold white]Parameter:[/bold white] [italic]{alert.get('param', 'N/A')}[/italic]")
                    print(f"[bold white]Attack:[/bold white] [italic]{alert.get('attack', 'N/A')}[/italic]")
                    print(f"[bold white]Evidence:[/bold white] \n[italic]{alert.get('evidence', 'N/A')}[/italic]")
                    print(f"[bold white]CWE ID:[/bold white] [italic]{alert.get('cweid', 'N/A')}[/italic]")
                    print(f"[bold white]WASC ID:[/bold white] [italic]{alert.get('wascid', 'N/A')}[/italic]")
                    print(f"[bold white]Source:[/bold white] [italic]{alert.get('source', 'N/A')}[/italic]")
                    print(f"[bold white]Alert Reference:[/bold white] [italic]{alert.get('alert_reference', 'N/A')}[/italic]")
                    print(f"[bold white]Input Vector:[/bold white] [italic]{alert.get('input_vector', 'N/A')}[/italic]")
                    print("\n[bold white]Description:[/bold white]")
                    print(f"  [italic]{alert.get('description', 'N/A')}[/italic]")
                    print("\n[bold white]Solution:[/bold white]")
                    print(f"  [italic]{alert.get('solution', 'N/A')}[/italic]")
                    print("\n[bold white]References:[/bold white]")

                    references = alert.get("reference", "N/A")
                    if isinstance(references, str):
                        print(f"  [italic]{references}[/italic]")
                    else:
                        for ref in references:
                            print(f"  [italic]{ref}[/italic]")

                    tags = alert.get("tags", {})
                    if tags:
                        print("\n[bold white]Alert Tags:[/bold white]")
                        for tag_key, tag_url in tags.items():
                            print(f"  [bold white]{tag_key}:[/bold white] [italic]{tag_url}[/italic]")
                    print(" ")
                    print("-" * 40)

def display_nmap_vulnerabilities(results):
    """
    Display vulnerability results from Nmap
    """
    print("\n[bold green]Nmap Script Scan Results:[/bold green]")
    if isinstance(results, str):
        print(f"[red]Error: {results}[/red]")
    else:
        for ip, details in results.items():
            print(f"\n[bold white]IP:[/bold white] [bold green]{ip}[/bold green]\n")

            # Check for errors
            if "error" in details:
                print(f"  [red]Error: {details['error']}[/red]")
                continue

            if "hostnames" in details:
                print("  [bold white]Hostnames:[/bold white]")
                for hostname in details.get("hostnames", []):
                    print(f"    - [bold white]Name:[/bold white] [italic]{hostname.get('name', 'N/A')}[/italic] [bold white](Type: {hostname.get('type', 'N/A')})[/bold white]")

            if "addresses" in details:
                print("\n  [bold white]Addresses:[/bold white]")
                for addr_type, addr in details["addresses"].items():
                    print(f"    - [bold white]{addr_type}:[/bold white] [italic]{addr}[/italic]")

            if "status" in details:
                print("\n  [bold white]Status:[/bold white]")
                print(f"    - [bold white]State:[/bold white] [italic]{details['status'].get('state', 'N/A')}[/italic]")
                print(f"    - [bold white]Reason:[/bold white] [italic]{details['status'].get('reason', 'N/A')}[/italic]")

            if "tcp" in details:
                print("\n  [bold white]TCP Ports:[/bold white]")
                for port, port_details in details["tcp"].items():
                    print(f"    - [bold white]Port:[/bold white] [italic]{port}[/italic]")
                    print(f"      - [bold white]State:[/bold white] [italic]{port_details.get('state', 'N/A')}[/italic]")
                    print(f"      - [bold white]Reason:[/bold white] [italic]{port_details.get('reason', 'N/A')}[/italic]")
                    print(f"      - [bold white]Service Name:[/bold white] [italic]{port_details.get('name', 'N/A')}[/italic]")
                    print(f"      - [bold white]Product:[/bold white] [italic]{port_details.get('product', 'N/A')}[/italic]")
                    print(f"      - [bold white]Version:[/bold white] [italic]{port_details.get('version', 'N/A')}[/italic]")
                    print(f"      - [bold white]Extra Info:[/bold white] [italic]{port_details.get('extrainfo', 'N/A')}[/italic]")
                    print(f"      - [bold white]Confidence Level:[/bold white] [italic]{port_details.get('conf', 'N/A')}[/italic]")
                    print(f"      - [bold white]CPE:[/bold white] [italic]{port_details.get('cpe', 'N/A')}[/italic]")

                    if "script" in port_details:
                        print("\n      - [bold white]Script Results:[/bold white]")
                        for script_name, script_result in port_details["script"].items():
                            display_script_results(script_name, script_result)
                    print(" ")
            print("-" * 40)

def display_script_results(script_name: str, script_result: str):
    print(f"        * [bold white]{script_name}:[/bold white]")
    script_result = script_result.strip()

    if not script_result:  # If the result is empty
        print("          [red]No results found.[/red]")
        return

    if '\n' not in script_result:
        print(f"          [bold white]Result:[/bold white] [italic]{script_result}[/italic]")
    else:
        # Split the result into lines
        lines = script_result.split('\n')
        print("          [bold white]Results:[/bold white]")
        for line in lines:
            if line.strip():
                print(f"            - [italic]{line.strip()}[/italic]")

def display_nmap_results(results):
    """
    Display results from Nmap port scan
    """
    print("[bold green]Nmap Port Scan Results:[/bold green]")
    if isinstance(results, str):
        print(f"[red]Error: {results}[/red]")
    else:
        for ip, details in results.items():
            print(f"\n[bold white]IP:[/bold white] [bold green]{ip}[/bold green]\n")

            # Check for errors
            if "error" in details:
                print(f"  [red]Error: {details['error']}[/red]")
                continue

            if "hostnames" in details:
                print("  [bold white]Hostnames:[/bold white]")
                for hostname in details.get("hostnames", []):
                    print(f"    -[bold white] Name:[/bold white] [italic]{hostname.get('name', 'N/A')}[/italic] [bold white](Type: {hostname.get('type', 'N/A')})[/bold white]")

            if "addresses" in details:
                print("\n  [bold white]Addresses:[/bold white]")
                for addr_type, addr in details["addresses"].items():
                    print(f"    - [bold white]{addr_type}:[/bold white] [italic]{addr}[/italic]")

            if "vendor" in details and details["vendor"]:
                print("\n  [bold white]Vendor Information:[/bold white]")
                for mac, vendor_name in details["vendor"].items():
                    print(f"    - [bold white]MAC:[/bold white] [italic]{mac}[/italic], [bold white]Vendor:[/bold white] [italic]{vendor_name}[/italic]")
            else:
                print("\n  [bold white]Vendor Information: No vendor information available.[/bold white]")

            if "status" in details:
                print("\n  [bold white]Status:[/bold white]")
                print(f"    - [bold white]State:[/bold white] [italic]{details['status'].get('state', 'N/A')}[/italic]")
                print(f"    - [bold white]Reason:[/bold white] [italic]{details['status'].get('reason', 'N/A')}[/italic]")

            if "tcp" in details:
                print("\n  [bold white]TCP Ports:[/bold white]")
                for port, port_details in details["tcp"].items():
                    print(f"    - [bold white]Port:[/bold white] [italic]{port}[/italic]")
                    print(f"      - [bold white]State:[/bold white] [italic]{port_details.get('state', 'N/A')}[/italic]")
                    print(f"      - [bold white]Reason:[/bold white] [italic]{port_details.get('reason', 'N/A')}[/italic]")
                    print(f"      - [bold white]Service Name:[/bold white] [italic]{port_details.get('name', 'N/A')}[/italic]")
                    print(f"      - [bold white]Product:[/bold white] [italic]{port_details.get('product', 'N/A')}[/italic]")
                    print(f"      - [bold white]Version:[/bold white] [italic]{port_details.get('version', 'N/A')}[/italic]")
                    print(f"      - [bold white]Extra Info:[/bold white] [italic]{port_details.get('extrainfo', 'N/A')}[/italic]")
                    print(f"      - [bold white]Confidence Level:[/bold white] [italic]{port_details.get('conf', 'N/A')}[/italic]")
                    print(f"      - [bold white]CPE:[/bold white] [italic]{port_details.get('cpe', 'N/A')}[/italic]")
                    print(" ")
            
            if "portused" in details:
                print("\n  [bold white]Ports Used:[/bold white]")
                for port_info in details.get("portused", []):
                    print(f"    - [bold white]Port:[/bold white] [italic]{port_info.get('portid', 'N/A')} ({port_info.get('proto', 'N/A')})[/italic]")
                    print(f"      - [bold white]State:[/bold white] [italic]{port_info.get('state', 'N/A')}[/italic]")
            
            if "osmatch" in details:
                print("\n  [bold white]OS Matches:[/bold white]")
                for os_match in details.get("osmatch", []):
                    print(f"    - [bold white]OS Name:[/bold white] [italic]{os_match.get('name', 'N/A')}[/italic] [bold white](Accuracy: {os_match.get('accuracy', 'N/A')}%)[/bold white]")
                    for os_class in os_match.get("osclass", []):
                        print(f"      - [bold white]OS Type:[/bold white] [italic]{os_class.get('type', 'N/A')}[/italic]")
                        print(f"      - [bold white]Vendor:[/bold white] [italic]{os_class.get('vendor', 'N/A')}[/italic]")
                        print(f"      - [bold white]OS Family:[/bold white] [italic]{os_class.get('osfamily', 'N/A')}[/italic]")
                        print(f"      - [bold white]OS Generation:[/bold white] [italic]{os_class.get('osgen', 'N/A')}[/italic]")
                        print(f"      - [bold white]CPE:[/bold white] [italic]{', '.join(os_class.get('cpe', []))}[/italic]")
                        print(" ")
            print("-" * 40)
