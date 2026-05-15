<div align="center">

# 🎭 Truth or Lie
**The World's First On-Chain AI Fact-Verification Game**

[![Play Now](https://img.shields.io/badge/Play_Now-Live-success?style=for-the-badge)](https://truth-or-lie-six.vercel.app/)
[![Powered by Genlayer](https://img.shields.io/badge/Powered_by-Genlayer-black?style=for-the-badge&logo=python)](https://genlayer.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-gold.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Studionet](https://img.shields.io/badge/Network-Studionet-blue?style=for-the-badge)](https://explorer-studio.genlayer.com)

*Stake $GEN tokens. Let decentralized AI validators judge the facts. Winners take the pool.*

</div>

---

## 🌍 Live on Studionet

The logic is live! The game is currently deployed and fully playable on **GenLayer Studionet**. 

**🚀 Play Now:** [https://truth-or-lie-six.vercel.app/](https://truth-or-lie-six.vercel.app/)

**🎮 Deployed Contract Address:**  
`0x155c991fEdb92e50056B34EC639934be793375E4`  
*(View on the [GenLayer Explorer](https://explorer-studio.genlayer.com/))*

### Network Setup

To connect your wallet and interact with the game, add Studionet to your Web3 wallet:

| Field | Value |
| :--- | :--- |
| **Network Name** | GenLayer Studionet |
| **Chain ID** | `61999` (Hex: `0xF22F`) |
| **GenLayer Chain RPC** | `https://studio.genlayer.com/api` |
| **Currency Symbol** | `GEN` |
| **Block Explorer** | [explorer-studio.genlayer.com](https://explorer-studio.genlayer.com) |

💧 **Need tokens to play?**  
Before placing your first bet, make sure to claim your testing tokens from the **Built-in faucet (use the 💧 button in the account selector)**!

---

## 📖 Overview

**Truth or Lie** is a revolutionary decentralized betting game built on [GenLayer](https://genlayer.com), the first Intelligent Blockchain. Utilizing GenLayer's native **Intelligent Contracts** (written in Python), the game allows players to bet on the validity of any real-world statement. 

Instead of relying on centralized oracles or human judges, "Truth or Lie" delegates the resolution to GenLayer's decentralized network of LLM validators. These AI nodes fetch internet data, reason through the evidence, reach consensus, and autonomously distribute the losing pool to the winners.

---

## ✨ Features

- **🧠 AI-Powered Settlement:** Uses native LLM execution at the protocol level to parse web evidence and verify statements.
- **🔗 Intelligent Contracts:** Written purely in Python using the `py-genlayer` SDK. No Solidity required!
- **💸 Automated Payouts:** Winners automatically split the staked $GEN tokens from the losing side based on AI consensus.
- **📜 Transparent Reasoning:** The blockchain permanently records the AI's confidence score and reasoning alongside the final verdict.

---

## ⚙️ How It Works

1. **The Claim:** A smart contract is initialized with a statement (e.g., *"Bitcoin hit $100k in 2024"*).
2. **The Stake:** Players interact with the `place_bet(vote)` function, sending $GEN tokens to stake on either `"true"` or `"lie"`.
3. **The Lock:** Betting is closed via `close_betting()`, securing the pool.
4. **The Verdict:** The `resolve_verdict()` function triggers GenLayer's LLM validators. The validators connect to the web, gather context, and reach a Byzantine Fault Tolerant consensus on the truth.
5. **The Reward:** The smart contract natively parses the result. If the statement is deemed a "lie", the "true" bettors' stakes are distributed proportionally to the "lie" bettors (and vice-versa).

---

## 🛠️ Built With GenLayer

This project showcases the unique paradigm of **GenLayer Intelligent Contracts**. 

### Key GenLayer Integrations:
- **Pythonic State Management:** Utilizing standard Python types to manage decentralized state.
- **Native AI Consensus:** GenLayer nodes inherently run LLMs. The contract doesn't call an external web2 API; the GenLayer network *is* the AI.
- **Deterministic Off-Chain Data:** By fetching web pages during validator execution, GenLayer reaches a deterministic consensus on non-deterministic real-world events.

*Sample from `truth_or_lie.py`:*
```python
# { "Depends": "py-genlayer:test" }
from genlayer import *

class TruthOrLie(gl.Contract):
    # State variables managed natively by Genlayer!
    owner: Address
    statement: str
    status: str
    verdict: str
```

---

## 🚀 Getting Started

### Prerequisites
- Access to a GenLayer Studionet/validator node (or connecting to the public RPC).
- Python 3.10+
- GenLayer Simulator / CLI installed.

### Installation & Deployment
1. Clone the repository:
   ```bash
   git clone https://github.com/kmgdz/truth-or-lie.git
   cd truth-or-lie
   ```
2. Run the file locally using the GenLayer Simulator:
   ```bash
   genlayer simulate truth_or_lie.py
   ```
3. Deploy to the GenLayer Studionet:
   ```bash
   genlayer deploy truth_or_lie.py --init "['The Earth is flat']"
   ```

### Frontend
To run the front-end interface, simply serve the index file (or use Vercel as configured in `vercel.json`):
```bash
npx serve .
```
Access the dark-mode cinematic interface at `localhost:3000`.

---

## 📚 Resources & Documentation

Want to learn more about Intelligent Contracts and how to build your own AI-powered dApps? 

- 📖 **[GenLayer Official Documentation](https://docs.genlayer.com/)** - Dive into the architecture, learn the Python SDK, and start building.
- 🌐 **[GenLayer Protocol](https://genlayer.com)** - The official homepage of the intelligent blockchain.

---

## 🌐 The Frontier of Smart Contracts

Traditional smart contracts are blind to the real world. They execute `if X then Y`, but they cannot answer *"Is X true?"* without centralized oracles. 

**Truth or Lie** demonstrates how GenLayer eliminates the oracle problem. By giving blockchains an "intellect" and a connection to the web, we can create markets, games, and autonomous organizations around complex, qualitative real-world data.

*Are you ready to risk your $GEN on the truth?*

---
<div align="center">
  <i>Created for the GenLayer ecosystem.</i>
</div>
