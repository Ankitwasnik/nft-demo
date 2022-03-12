import pytest
from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.simple_collectible.deploy import deploy


def test_create_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy()
    assert simple_collectible.ownerOf(0) == get_account()
