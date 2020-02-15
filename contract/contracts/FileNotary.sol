pragma solidity ^0.5.0;

contract FileNotary {
    mapping(string => bytes32) hashes;
    address owner;

    event HashSet(string indexed fileId, bytes32 hash);

    constructor() public {
      owner = msg.sender;
    }

    function getFileHash(string memory fileId) public view returns (bytes32) {
      return hashes[fileId];
    }

    function setFileHash(string memory fileId, bytes32 hash) public {
      require(msg.sender == owner, "Only owner can set hashes");
      require(hashes[fileId] == 0, "You cannot mutate already set hash");

      hashes[fileId] = hash;
      emit HashSet(fileId, hash);
    }
}
