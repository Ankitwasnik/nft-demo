
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.counter()
    print(f"You have created {number_of_advanced_collectible} collectibles")
    for token_id in range(number_of_advanced_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_filename)

        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists. Delete it to override")
        else:
            print(f"Creating metdata file: {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            print(collectible_metadata)
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                upload_to_ipfs(metadata_filename)    


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url+endpoint, files={"file":image_binary})    
        ipfs_hash = response.json()["Hash"]
        # "./img/PUG.png" --> PUG.png
        filename = filepath.split("/")[-1:][0]
        image_url = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        # "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
        print(image_url)
        return image_url
