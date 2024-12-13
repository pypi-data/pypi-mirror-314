import re
import typer
import requests
from rich import print
import os
from dotenv import load_dotenv

app = typer.Typer()

load_dotenv(dotenv_path="./typercli/.env")
BASE_URL_WAPPALYZER = os.getenv("BASE_URL_WAPPALYZER", "http://127.0.0.1:8000/Wappalyzer")
BASE_URL_THEHARVESTER = os.getenv("BASE_URL_THEHARVESTER", "http://127.0.0.1:8000/theHarvester")
BASE_URL_WHOISXML = os.getenv("BASE_URL_WHOISXML", "http://127.0.0.1:8000/Whoisxml")


@app.command("wappalyzer")
def wappalyzer_scan(domains: str):
    """
    Analyze technologies of target domain. Required input format:
    "example1.com, example2.com"
    """
    domain_list = [domain.strip() for domain in domains.split(",")]

    url = f"{BASE_URL_WAPPALYZER}/analyze/multipleDomains"
    
    try:
        response = requests.post(url, json={"domains": domain_list})
        if response.status_code == 200:
            results = response.json()
            display_results_wappalyzer(results)
                    
        else:
            typer.echo(f"Failed to call Wappalyzer API: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")


@app.command("whois")
def whois_scan(domains: str):
    """
    Perform WHOIS scan. Required input format:
    "example1.com, example2.com"
    """
    domain_list = [domain.strip() for domain in domains.split(",")]

    try:
        response = requests.post(f"{BASE_URL_WHOISXML}/lookup/multipleDomains", json={"domains": domain_list})
        
        if response.status_code == 200:
            results = response.json()
            display_results_whois(results)
                    
        else:
            typer.echo(f"Failed to call WhoisXML API: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")


@app.command("theharvester")
def theharvester_scan_all(domains: str):
    """
    Perform theHarvester scan to gather subdomains and emails. Required input format:
    "example1.com, example2.com"
    """
  
    domain_list = [domain.strip() for domain in domains.split(",")]

    # Send the POST request to the FastAPI backend
    try:
        response = requests.post(f"{BASE_URL_THEHARVESTER}/scan/multipleDomains", json={"domains": domain_list, "data_type": "all"})
        
        if response.status_code == 200:
            results = response.json()
            display_results_theHarvester(results)
                    
        else:
            typer.echo(f"Failed to call theHarvester API: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")

@app.command("theharvester-subdomains")
def theharvester_scan_subdomains(domains: str):
    """
    Perform theHarvester scan to gather subdomains only. Required input format:
    "example1.com, example2.com"
    """
    domain_list = [domain.strip() for domain in domains.split(",")]

    # Send the POST request to the FastAPI backend
    try:
        response = requests.post(f"{BASE_URL_THEHARVESTER}/scan/multipleDomains", json={"domains": domain_list, "data_type": "subdomains"})
        
        if response.status_code == 200:
            results = response.json()
            display_results_theHarvester(results)
        else:
            typer.echo(f"Failed to call theHarvester API: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")

@app.command("theharvester-emails")
def theharvester_scan_emails(domains: str):
    """
    Perform theHarvester scan to gather emails only. Required input format:
    "example1.com, example2.com"
    """
    domain_list = [domain.strip() for domain in domains.split(",")]

    # Send the POST request to the FastAPI backend
    try:
        response = requests.post(f"{BASE_URL_THEHARVESTER}/scan/multipleDomains", json={"domains": domain_list, "data_type": "emails"})
        
        if response.status_code == 200:
            results = response.json()
            display_results_theHarvester(results)
        else:
            typer.echo(f"Failed to call theHarvester API: {response.status_code} - {response.text}")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")


@app.command("all")
def all_passive_scans(domains: str):
    """
    Run Wappalyzer, WhoisXML, and theHarvester for the provided domains. Required input format:
    "example1.com, example2.com"
    """
    domain_list = [domain.strip() for domain in domains.split(",")]

    # Run WhoisXML
    print(f"\n[bold green]Running WhoisXML scan...[/bold green]\n")
    try:
        response = requests.post(f"{BASE_URL_WHOISXML}/lookup/multipleDomains", json={"domains": domain_list})
        
        if response.status_code == 200:
            results = response.json()
            display_results_whois(results)
                    
        else:
            print(f"[red]Failed to call WhoisXML API: {response.status_code} - {response.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")

    # Run theHarvester
    print(f"\n[bold green]Running theHarvester scan...[/bold green]\n")
    try:
        response = requests.post(f"{BASE_URL_THEHARVESTER}/scan/multipleDomains", json={"domains": domain_list})
        
        if response.status_code == 200:
            results = response.json()
            display_results_theHarvester(results)

        else:
            print(f"[red]Failed to call theHarvester API: {response.status_code} - {response.text}[/red]")

    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[red]")
    
     # Run Wappalyzer
    print(f"[bold green]Running Wappalyzer scan...[/bold green]\n")
    try:
        response = requests.post(f"{BASE_URL_WAPPALYZER}/analyze/multipleDomains", json={"domains": domain_list})
        if response.status_code == 200:
            results = response.json()
            display_results_wappalyzer(results)
                    
        else:
            print(f"[red]Failed to call Wappalyzer API: {response.status_code} - {response.text}[/red]")
            
    except KeyboardInterrupt:
        print("\n[bold red]Exiting the session...[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")

def display_results_whois(results):

    print("[bold green]Results for domains:[/bold green]")
    
    for domain, info in results.items():
        print(f"\n[bold white]* Domain:[/bold white] [bold green]{domain}[/bold green]\n")
        if "error" in info:
            print(f"  [red]Error: {info['error']}[/red]")
        else:
            print(f"  [bold white]Domain Name:[/bold white] [italic]{info.get('domain_name', 'N/A')}[/italic]")
            print(f"  [bold white]Created Date:[/bold white] [italic]{info.get('created_date', 'N/A')}[/italic]")
            print(f"  [bold white]Updated Date:[/bold white] [italic]{info.get('updated_date', 'N/A')}[/italic]")
            print(f"  [bold white]Expiration Date:[/bold white] [italic]{info.get('expiration_date', 'N/A')}[/italic]")
            print(f"  [bold white]Estimated Domain Age:[/bold white] [italic]{info.get('estimated_domain_age', 'N/A')}[/italic]")
            print(f"  [bold white]Registrar Name:[/bold white] [italic]{info.get('registrar_name', 'N/A')}[/italic]\n")

            if "name_servers" in info and info["name_servers"]:
                print("  [bold white]Name Servers:[/bold white]")
                for ns in info["name_servers"].get("host_names", []):
                    print(f"    - [italic]{ns}[/italic]")
                print("")
        
            if "contact_email" in info:
                print(f"  [bold white]Contact Email:[/bold white] [italic]{info['contact_email']}[/italic]\n")

            for contact_type in ["registrant", "administrative_contact", "technical_contact"]:
                contact_info = info.get(contact_type)
                if contact_info:
                    print(f"  [bold white]{contact_type.replace('_', ' ').capitalize()} Contact:[/bold white]")
                    for sub_key, sub_value in contact_info.items():
                        print(f"    [bold white]{sub_key.replace('_', ' ').capitalize()}:[/bold white] [italic]{sub_value}[/italic]")
                    print("")  

def display_results_wappalyzer(results):
    print("[bold green]Results for domains:[/bold green]")
    for domain, info in results.items():
        print(f"\n[bold white]* Domain:[/bold white] [bold green]{domain}[/bold green]\n")
        if "error" in info:
            print(f"  [red]Error: {info['error']}[/red]")
        elif not info:
            print("  [bold white]No results found.[/bold white]")
        else:
            for tech, details in info.items():
                print(f"  [bold white]Technology:[/bold white] [italic]{tech}[/italic]")

                if isinstance(details, dict):
            
                    categories = details.get("categories", [])
                    categories_str = ", ".join(categories) if categories else "[italic]No categories[/italic]"
                    print(f"    [bold white]Categories:[/bold white] [italic]{categories_str}[/italic]")

                    versions = details.get("versions", [])
                    versions_str = ", ".join(versions) if versions else "[italic]No versions[/italic]"
                    print(f"    [bold white]Versions:[/bold white] [italic]{versions_str}[/italic]\n")
                else:
                    error_message = get_error_message_wappalyzer(details)
                    print(f"    [bold white]Details:[/bold white] [red]{error_message}[/red]")


def get_error_message_wappalyzer(message: str) -> str:
    """
    Extract the relevant portion of the error message if it matches a known pattern.
    """
    match = re.search(r"No connection could be made because the target machine actively refused it", message)
    if match:
        return match.group(0)
    else:
        return "An error occurred during the connection attempt"

def display_results_theHarvester(results):
    # Display the results in a readable format
    print("[bold green]Results for domains:[/bold green]")
    for domain, info in results.items():
        print(f"\n[bold white]* Domain:[/bold white] [bold green]{domain}[/bold green]")
        if "error" in info:
            print(f"  [red]Error: {info['error']}[/red]")
        else:   
            for source, details in info.items():
                print(f"    [bold white]Source:\n     {source.capitalize()}[/bold white]\n")
                
                if isinstance(details, dict):
                    for key, value in details.items():
                        if value:
                            print(f"      [bold white]{key.capitalize()}:[/bold white]")
                            
                            if isinstance(value, list):
                                for item in value:
                                    print(f"      - [italic]{item}[/italic]")
                            else:
                                print(f"      [italic]{value}[/italic]")
                            print(" ")
                else:
                    print(f"      [bold white]{details}[/bold white]\n")