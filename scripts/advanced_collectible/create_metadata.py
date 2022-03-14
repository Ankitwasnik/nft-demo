
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path


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
        print(collectible_metadata)
