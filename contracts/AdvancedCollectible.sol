// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBase {
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public counter;
    mapping(bytes32 => address) requestIdToSender;
    mapping(uint256 => Breed) tokenIdToBreed;

    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        ERC721("Dogie", "DOG")
        VRFConsumerBase(_vrfCoordinator, _linkToken)
    {
        keyHash = _keyHash;
        fee = _fee;
        counter = 0;
    }

    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    function createCollectible() public returns (uint256) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        uint256 tokenId = counter;
        Breed selectedBreed = Breed(randomNumber % 3);
        tokenIdToBreed[tokenId] = selectedBreed;
        emit breedAssigned(tokenId, selectedBreed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, tokenId);
        counter = counter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: Caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
