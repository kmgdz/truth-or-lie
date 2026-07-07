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

This contract is deployed and finalized on **GenLayer Studionet** — verified via constructor SUCCESS on the [Explorer](https://explorer-studio.genlayer.com/address/0xF27FE2B440626F9A32F53c11eb9C0717BB710e60). This deployment also fixes a permission bug in the previous version: `close_betting()` no longer requires the caller to be the original deployer — any wallet can now advance the game through the full bet → close → judge → claim flow. Check the Explorer link for live, current transaction history rather than relying on any snapshot here.

**🚀 Play Now:** [https://truth-or-lie-six.vercel.app/](https://truth-or-lie-six.vercel.app/)

**🎮 Deployed Contract Address:**  
`0xF27FE2B440626F9A32F53c11eb9C0717BB710e60`  
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

## 🧪 How To Test This Contribution

For reviewers/devs verifying this submission — the full flow end-to-end.

### Quick test (using the pre-deployed contract)

1. **Open the live app:** [https://truth-or-lie-six.vercel.app/](https://truth-or-lie-six.vercel.app/)
2. **Connect your wallet** (top right) — MetaMask or similar, and make sure you're on **GenLayer Studionet**. If the network isn't added yet, the app will prompt you to add/switch to it automatically.
3. **Get test GEN** if you don't have any — use the built-in faucet (💧 button in the account selector on `studio.genlayer.com`).
4. **Load the contract:** the address `0xF27FE2B440626F9A32F53c11eb9C0717BB710e60` is pre-filled in the "Contract Address" field. Click **LOAD GAME**. The statement should display, along with current TRUE/LIE pool totals.
5. **Place a bet:** click **TRUE** or **LIE**, enter an amount (e.g. `1`), click the stake button, and confirm in your wallet. The pool totals should update after the transaction confirms (a few seconds).
6. **Trigger judgment:** click **⚡ TRIGGER AI JUDGMENT**. This calls `close_betting()` then `judge_statement()`, sequentially. Confirm both wallet prompts. **Any wallet can do this step** — it's no longer restricted to whoever originally deployed the contract (see "Permission fix" below).
7. **Wait for the verdict:** the page polls automatically every few seconds. GenLayer's LLM validators need to reach consensus via the Equivalence Principle, which typically takes **30–90 seconds**. When it resolves, a verdict (TRUE/LIE), confidence score, and reasoning will appear.
8. **Claim winnings** (only relevant if you bet on the winning side): once settled, a **🏆 CLAIM WINNINGS** button appears — click it to receive your stake back plus a proportional share of the losing pool.

### Deploy a fresh contract with your own example statement

Rather than reuse the pre-deployed one, you can deploy a brand-new instance and pick your own test case:

1. Open `truth_or_lie.py` in [GenLayer Studio](https://studio.genlayer.com)
2. Deploy with a constructor argument — pick one of these ready-made examples, or write your own:

   | Example statement | Expected verdict |
   |---|---|
   | `"The Eiffel Tower is located in London, England"` | LIE (clearly false, easy to sanity-check) |
   | `"Water boils at 100 degrees Celsius at sea level"` | TRUE (clearly true, easy to sanity-check) |
   | `"Bitcoin's block time is approximately 10 minutes"` | TRUE (verifiable technical fact) |
   | `"The Great Wall of China is visible from space with the naked eye"` | LIE (common myth — good test of real research, not just pattern-matching) |

3. Paste the new contract address into the app's "Contract Address" field and click **LOAD GAME**

### Permission fix — testing with a second wallet

An earlier version of this contract restricted `close_betting()` to only the wallet that originally deployed it — meaning anyone else testing the app got stuck with a permission error and could never reach the judgment step. **This is now fixed**: any connected wallet can call `close_betting()`. To specifically verify this:

1. Have Wallet A place a bet and **not** trigger judgment
2. Switch to a different wallet (Wallet B) in MetaMask, reconnect
3. Wallet B should be able to click **⚡ TRIGGER AI JUDGMENT** successfully — no "Only the owner can close betting" error

### What to check for a valid pass

- Statement loads without a JSON-parsing error (this was the original bug — a missing CORS proxy)
- Placing a bet doesn't throw a "no verdict" or "execution failed" error
- **A wallet other than the contract's deployer can trigger judgment** (the permission bug fix)
- The judgment step actually resolves to a real verdict, not stuck indefinitely on "judging"
- Pool amounts display as plain GEN (e.g. "5 GEN"), not scaled by 10¹⁸

---

## 📖 Overview

**Truth or Lie** is a revolutionary decentralized betting game built on [GenLayer](https://genlayer.com), the first Intelligent Blockchain. Utilizing GenLayer's native **Intelligent Contracts** (written in Python), the game allows players to bet on the validity of any real-world statement. 

Instead of relying on centralized oracles or human judges, "Truth or Lie" delegates the resolution to GenLayer's decentralized network of LLM validators. These AI nodes fetch internet data, reason through the evidence, reach consensus, and autonomously distribute the losing pool to the winners.

---

## ✨ Features

- **🧠 AI-Powered Settlement:** Uses native LLM execution at the protocol level to parse web evidence and verify statements.
- **🔗 Intelligent Contracts:** Written purely in Python using the `py-genlayer` SDK. No Solidity required!
- **💸 Proportional Payouts:** Once the AI verdict settles the game, winners call `claim_winnings()` to receive their original stake plus a proportional share of the losing side's pool.
- **📜 Transparent Reasoning:** The blockchain permanently records the AI's confidence score and reasoning alongside the final verdict.

---

## ⚙️ How It Works

1. **The Claim:** A smart contract is initialized with a statement (e.g., *"Bitcoin hit $100k in 2024"*).
2. **The Stake:** Players interact with the `place_bet(vote)` function, sending $GEN tokens to stake on either `"true"` or `"lie"`.
3. **The Lock:** Betting is closed via `close_betting()`, securing the pool.
4. **The Verdict:** The `judge_statement()` function triggers GenLayer's LLM validators (after `close_betting()` has moved the game into "judging" state). The validators connect to the web, gather context, and reach consensus on the truth via the Equivalence Principle.
5. **The Reward:** Once settled, each winning bettor calls `claim_winnings()` to receive their original stake back plus a proportional share of the losing side's pool. If the statement is deemed a "lie", the "lie" bettors split the "true" bettors' stakes (and vice-versa).

---

## 🛠️ Built With GenLayer

This project showcases the unique paradigm of **GenLayer Intelligent Contracts**. 

### Key GenLayer Integrations:
- **Pythonic State Management:** Utilizing standard Python types to manage decentralized state.
- **Native AI Consensus:** GenLayer nodes inherently run LLMs. The contract doesn't call an external web2 API; the GenLayer network *is* the AI.
- **Deterministic Off-Chain Data:** By fetching web pages during validator execution, GenLayer reaches a deterministic consensus on non-deterministic real-world events.

*Sample from `truth_or_lie.py`:*
```python
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
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
- A wallet (e.g. MetaMask) connected to GenLayer Studionet, or the [`genlayer-cli`](https://docs.genlayer.com/api-references/genlayer-cli) installed
- Python 3.10+ (only needed if deploying via CLI rather than the browser-based [GenLayer Studio](https://studio.genlayer.com))

### Installation & Deployment
1. Clone the repository:
   ```bash
   git clone https://github.com/kmgdz/truth-or-lie.git
   cd truth-or-lie
   ```
2. Set your network (or select interactively):
   ```bash
   genlayer network set studionet
   ```
3. Deploy to the GenLayer Studionet, passing the statement as a constructor arg:
   ```bash
   genlayer deploy --contract truth_or_lie.py --args "The Earth is flat"
   ```
   This was also tested by deploying directly through the browser-based
   [GenLayer Studio](https://studio.genlayer.com) IDE, which doesn't require the CLI at all.

### Frontend
To run the front-end interface locally (including the `/api/rpc` proxy), use the Vercel CLI:
```bash
npm i -g vercel
vercel dev
```
`npx serve .` alone will **not** work — it only serves static files and has no
way to run `api/rpc.js`, so the wallet-connected views (Explore/statement
loading) will fail with a JSON parsing error locally, even though the
deployed Vercel site works fine.

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
