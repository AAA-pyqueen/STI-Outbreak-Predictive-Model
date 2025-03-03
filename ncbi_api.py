import yaml
import requests

# Load OpenAPI spec
def load_openapi_spec(filepath="openapi3.docs.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

# Get base URL from the OpenAPI spec
def get_ncbi_base_url():
    spec = load_openapi_spec()
    return spec["servers"][0]["url"] if "servers" in spec else None

# Fetch genomic data using OpenAPI
def fetch_ncbi_data(pathogen):
    base_url = get_ncbi_base_url()
    if not base_url:
        raise ValueError("Base URL not found in OpenAPI spec")

    endpoint = f"{base_url}/genome/accession/{pathogen}"
    headers = {"Accept": "application/json"}

    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
