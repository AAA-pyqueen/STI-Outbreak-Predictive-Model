import requests
import pandas as pd

# Function to fetch genomic metadata from NCBI
def fetch_ncbi_data():
    base_url = "https://api.ncbi.nlm.nih.gov/datasets/v1/genome/accession/"
    pathogens = ["Syphilis", "HPV", "HSV", "HIV"]
    
    genomic_data = []
    metadata = []
    
    for pathogen in pathogens:
        try:
            response = requests.get(f"{base_url}{pathogen}")
            response.raise_for_status()  # Raise an error for bad responses
            
            data = response.json()
            for genome in data.get("genomes", []):
                genomic_data.append(genome.get("sequence", "N/A"))
                metadata.append({
                    "pathogen": pathogen,
                    "host": genome.get("host", "Unknown"),
                    "collection_date": genome.get("collection_date", "Unknown"),
                    "location": genome.get("location", "Unknown")
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {pathogen}: {e}")

    # Convert to DataFrame
    genomic_df = pd.DataFrame(genomic_data, columns=["genomic_sequence"])
    metadata_df = pd.DataFrame(metadata)
    
    return pd.concat([genomic_df, metadata_df], axis=1)

if __name__ == "__main__":
    data = fetch_ncbi_data()
    print(data.head())  # Test output
