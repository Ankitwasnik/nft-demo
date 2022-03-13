from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
import pytest
from scripts.advanced_collectible.deploy_advanced_collectible import deploy


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy()
    request_id = creation_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, random_number, advanced_collectible.address, {"from": get_account()})
    assert advanced_collectible.counter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
