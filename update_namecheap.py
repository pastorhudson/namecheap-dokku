import requests
import configparser
import sys


def load_config():
    """Load API credentials and subdomain configurations from config.ini."""
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_user = config.get("NamecheapAPI", "api_user")
    api_key = config.get("NamecheapAPI", "api_key")
    username = config.get("NamecheapAPI", "username")
    client_ip = config.get("NamecheapAPI", "client_ip")

    # Parse subdomains from config
    subdomains = config.get("Domains", "subdomains").split(",")
    subdomains_dict = {}
    for subdomain_entry in subdomains:
        subdomain_entry = subdomain_entry.strip()
        if ":" in subdomain_entry:
            subdomain, domain = subdomain_entry.split(":")
            subdomains_dict[subdomain.strip()] = domain.strip()
        else:
            print(f"Warning: Invalid subdomain entry '{subdomain_entry}' in config.ini. Skipping...")

    return api_user, api_key, username, client_ip, subdomains_dict


def fetch_existing_records(api_user, api_key, username, client_ip, domain):
    """Fetch existing DNS records for the given domain."""
    payload = {
        "ApiUser": api_user,
        "ApiKey": api_key,
        "UserName": username,
        "Command": "namecheap.domains.dns.getHosts",
        "ClientIp": client_ip,
        "SLD": domain.split('.')[0],
        "TLD": domain.split('.')[1],
    }
    response = requests.post("https://api.namecheap.com/xml.response", data=payload)
    response.raise_for_status()
    return response.text


import xml.etree.ElementTree as ET


def update_dns_record(api_user, api_key, username, client_ip, subdomain, domain, new_ip):
    """Update or add a specific subdomain record."""
    # Step 1: Fetch existing records
    existing_records_xml = fetch_existing_records(api_user, api_key, username, client_ip, domain)
    root = ET.fromstring(existing_records_xml)

    # Step 2: Define the namespace and parse existing DNS records
    namespace = {"ns": "http://api.namecheap.com/xml.response"}
    records = []
    for host in root.findall(".//ns:host", namespace):
        records.append({
            "HostName": host.attrib["Name"],
            "RecordType": host.attrib["Type"],
            "Address": host.attrib["Address"],
            "TTL": host.attrib.get("TTL", "60"),
        })

    # Step 3: Update or add the subdomain record
    updated = False
    for record in records:
        if record["HostName"] == subdomain:
            record["Address"] = new_ip
            updated = True

    if not updated:
        # Add the subdomain if it doesn't exist
        records.append({
            "HostName": subdomain,
            "RecordType": "A",
            "Address": new_ip,
            "TTL": "60",
        })

    # Step 4: Submit the updated records
    payload = {
        "ApiUser": api_user,
        "ApiKey": api_key,
        "UserName": username,
        "Command": "namecheap.domains.dns.setHosts",
        "ClientIp": client_ip,
        "SLD": domain.split('.')[0],
        "TLD": domain.split('.')[1],
    }

    # Add records to the payload
    for i, record in enumerate(records, start=1):
        payload[f"HostName{i}"] = record["HostName"]
        payload[f"RecordType{i}"] = record["RecordType"]
        payload[f"Address{i}"] = record["Address"]
        payload[f"TTL{i}"] = record["TTL"]
    response = requests.post("https://api.namecheap.com/xml.response", data=payload)
    response.raise_for_status()

    # Parse the response XML to check for success
    response_xml = ET.fromstring(response.text)
    success_element = response_xml.find(".//ns:DomainDNSSetHostsResult", namespace)
    errors_element = response_xml.find(".//ns:Errors", namespace)

    if success_element is not None and success_element.attrib.get("IsSuccess") == "true":
        print(f"DNS record updated successfully for {subdomain}.{domain}.")
    else:
        print(f"Failed to update DNS record for {subdomain}.{domain}.")
        if errors_element is not None:
            errors = [error.text for error in errors_element.findall(".//ns:Error", namespace)]
            print("Errors:", errors)
        print(response.text)


def main():
    """Main script execution."""
    if len(sys.argv) != 2:
        print("Usage: python script.py <new_ip_address>")
        sys.exit(1)

    new_ip = sys.argv[1]
    api_user, api_key, username, client_ip, subdomains_dict = load_config()
    for subdomain, domain in subdomains_dict.items():
        update_dns_record(api_user, api_key, username, client_ip, subdomain, domain, new_ip)


if __name__ == "__main__":
    main()
