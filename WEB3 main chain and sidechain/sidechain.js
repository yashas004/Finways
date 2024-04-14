// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

contract SidechainBridge is Ownable {
    ERC20Burnable public token;
    address public validator;

    event TokensMinted(address indexed receiver, uint256 amount);
    event TokensBurned(address indexed sender, uint256 amount);

    constructor(address _token) {
        token = ERC20Burnable(_token);
    }

    function setValidator(address _validator) external onlyOwner {
        validator = _validator;
    }

    function mintTokens(address to, uint256 amount, bytes memory signature) external {
        require(_verify(_hash(to, amount), signature), "Invalid signature");
        token.mint(to, amount);
        emit TokensMinted(to, amount);
    }

    function burnTokens(uint256 amount) external {
        token.burn(amount);
        emit TokensBurned(msg.sender, amount);
    }

    function _hash(address to, uint256 amount) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked(to, amount));
    }

    function _verify(bytes32 hash, bytes memory signature) internal view returns (bool) {
        return validator == hash.toEthSignedMessageHash().recover(signature);
    }
}

