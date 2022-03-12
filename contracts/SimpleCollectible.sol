// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract SimpleCollectible is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor() ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 tokenId = tokenCounter;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return tokenId;
    }
}
