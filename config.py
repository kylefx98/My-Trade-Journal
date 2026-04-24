"""
======================== CONFIGURATION FILE ========================

This file stores all fixed values used by the app.

SECTIONS:
1. Network → Connects to Ethereum Sepolia
2. Contract → Address + ABI (how we talk to the smart contract)
3. Branding → UI text
4. Labels → Converts blockchain codes into human-readable text

IMPORTANT:
- This file contains NO logic
- ABI must be a Python list (not a string)
====================================================================
"""

# ---------------------- NETWORK CONFIG ----------------------
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CHAIN_ID = 11155111  # Sepolia Network


# ---------------------- CONTRACT DETAILS ----------------------
CONTRACT_ADDRESS = "0x2FdB8536D27B71413FC1Cc570Bb184072d24f52B"

CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "tradeId", "type": "uint256"},
            {"indexed": False, "internalType": "int256", "name": "result", "type": "int256"}
        ],
        "name": "TradeClosed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "tradeId", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "pair", "type": "string"},
            {"indexed": False, "internalType": "uint8", "name": "risk", "type": "uint8"}
        ],
        "name": "TradeLogged",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_tradeId", "type": "uint256"},
            {"internalType": "int256", "name": "_pipResult", "type": "int256"},
            {"internalType": "string", "name": "_lessons", "type": "string"}
        ],
        "name": "closeTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_tradeId", "type": "uint256"}
        ],
        "name": "getTrade",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "string", "name": "pair", "type": "string"},
                    {"internalType": "string", "name": "setupNotes", "type": "string"},
                    {"internalType": "uint256", "name": "confluenceCount", "type": "uint256"},
                    {"internalType": "int256", "name": "pipResult", "type": "int256"},
                    {"internalType": "string", "name": "lessonsLearned", "type": "string"},
                    {"internalType": "uint8", "name": "status", "type": "uint8"},
                    {"internalType": "uint8", "name": "risk", "type": "uint8"},
                    {"internalType": "address", "name": "trader", "type": "address"}
                ],
                "internalType": "tuple",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_pair", "type": "string"},
            {"internalType": "string", "name": "_notes", "type": "string"},
            {"internalType": "uint256", "name": "_confluences", "type": "uint256"}
        ],
        "name": "logNewTrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tradeCount",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


# ---------------------- APP BRANDING ----------------------
APP_NAME = "Falcon Forex Journal"
APP_TAGLINE = "Track Every Trade. Trust Every Record."
APP_DESCRIPTION = "A blockchain-powered journal for logging forex trades before and after execution."


# ---------------------- HUMAN READABLE LABELS ----------------------
TRADE_STATUS = {
    0: "Setup Phase",
    1: "Active Trade",
    2: "Closed Trade"
}

RISK_LEVEL = {
    0: "Low Risk",
    1: "Medium Risk",
    2: "High Risk"
}