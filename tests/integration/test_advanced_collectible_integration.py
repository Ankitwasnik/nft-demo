from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
import pytest
from scripts.advanced_collectible.deploy_advanced_collectible import deploy
import time


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    advanced_collectible, creation_tx = deploy()

    time.sleep(180)
    assert advanced_collectible.counter() == 1
