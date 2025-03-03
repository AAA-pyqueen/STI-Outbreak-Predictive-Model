import requests
import pandas as pd

# Fetch genomic metadata from NCBI
from ncbi_api import fetch_ncbi_data

def load_data():
    pathogens = ["Syphilis", "HPV", "HSV", "HIV"]
    
    genomic_data = []
    metadata = []
    
    for pathogen in pathogens:
        data = fetch_ncbi_data(pathogen)
        if data:
            for genome in data.get("genomes", []):
                genomic_data.append(genome.get("sequence"))
                metadata.append({
                    "pathogen": pathogen,
                    "host": genome.get("host"),
                    "collection_date": genome.get("collection_date"),
                    "location": genome.get("location")
                })
    
    genomic_df = pd.DataFrame(genomic_data, columns=["genomic_sequence"])
    metadata_df = pd.DataFrame(metadata)
    return pd.concat([genomic_df, metadata_df], axis=1)

if __name__ == "__main__":
    data = fetch_ncbi_data()
    print(data.head())  # Test output
