from enum import Enum


class CronosEvm(str, Enum):
    """
    Chain IDs for Cronos EVM (Mainnet and Testnet).
    """
    MAINNET = "25"
    TESTNET = "338"

    def __str__(self):
        return self.value


class CronosZkEvm(str, Enum):
    """
    Chain IDs for Cronos ZK EVM (Mainnet and Testnet).
    """
    MAINNET = "388"
    TESTNET = "240"

    def __str__(self):
        return self.value
