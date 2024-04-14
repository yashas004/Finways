// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract MainnetBridge is Ownable {
    using ECDSA for bytes32;

    IERC20 public token;
    address public validator;

    event TokensLocked(address indexed sender, uint256 amount, address indexed sidechainDestination);
    event TokensUnlocked(address indexed receiver, uint256 amount);

    constructor(address _token) {
        token = IERC20(_token);
    }

    function setValidator(address _validator) external onlyOwner {
        validator = _validator;
    }

    function lockTokens(uint256 amount, address sidechainDestination) external {
        require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        emit TokensLocked(msg.sender, amount, sidechainDestination);
    }

    function unlockTokens(address to, uint256 amount, bytes memory signature) external {
        require(_verify(_hash(to, amount), signature), "Invalid signature");
        require(token.transfer(to, amount), "Transfer failed");
        emit TokensUnlocked(to, amount);
    }

    function _hash(address to, uint256 amount) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked(to, amount));
    }

    function _verify(bytes32 hash, bytes memory signature) internal view returns (bool) {
        return validator == hash.toEthSignedMessageHash().recover(signature);
    }
}
