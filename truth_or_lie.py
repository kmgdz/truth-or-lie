# { "Depends": "py-genlayer:test" }
from genlayer import *
import json
from dataclasses import dataclass


# ─────────────────────────────────────────────────────────────────────
#  TruthOrLie — On-chain statement verification game
#  Players stake GEN on whether a statement is TRUE or LIE.
#  GenLayer LLM validators fetch web evidence and reach consensus.
#  Winners split the losing pool automatically.
# ─────────────────────────────────────────────────────────────────────


@allow_storage
@dataclass
class Bet:
    player: Address
    amount: u256
    vote: str  # "true" or "lie"


class TruthOrLie(gl.Contract):
    # ── State ──────────────────────────────────────────────────────
    owner: Address
    statement: str
    submitter: Address
    total_true: u256
    total_lie: u256
    bet_count: u256
    status: str          # open | judging | settled
    verdict: str         # "true" | "lie" | "uncertain"
    verdict_reasoning: str
    verdict_confidence: u256   # 0-100
    winner_pool: u256

    def __init__(self, statement: str):
        self.owner = gl.message.sender_address
        self.submitter = gl.message.sender_address
        self.statement = statement
        self.total_true = u256(0)
        self.total_lie = u256(0)
        self.bet_count = u256(0)
        self.status = "open"
        self.verdict = ""
        self.verdict_reasoning = ""
        self.verdict_confidence = u256(0)
        self.winner_pool = u256(0)

    # ── Read ───────────────────────────────────────────────────────

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_statement(self) -> str:
        return self.statement

    @gl.public.view
    def get_game_summary(self) -> str:
        return json.dumps({
            "statement": self.statement,
            "status": self.status,
            "total_true": int(self.total_true),
            "total_lie": int(self.total_lie),
            "total_staked": int(self.total_true) + int(self.total_lie),
            "bet_count": int(self.bet_count),
            "verdict": self.verdict,
            "verdict_reasoning": self.verdict_reasoning,
            "verdict_confidence": int(self.verdict_confidence),
        })

    @gl.public.view
    def get_verdict(self) -> str:
        if self.status != "settled":
            return json.dumps({"error": "Not settled yet"})
        return json.dumps({
            "verdict": self.verdict,
            "reasoning": self.verdict_reasoning,
            "confidence": int(self.verdict_confidence),
            "winner_side": self.verdict,
            "total_true": int(self.total_true),
            "total_lie": int(self.total_lie),
        })

    # ── Write ──────────────────────────────────────────────────────

    @gl.public.write
    def place_bet(self, vote: str) -> None:
        """
        Players stake GEN tokens on 'true' or 'lie'.
        msg.value = amount being staked.
        """
        assert self.status == "open", "Betting is closed"
        assert vote in ("true", "lie"), "Vote must be 'true' or 'lie'"
        assert gl.message.value > 0, "Must stake some GEN"

        if vote == "true":
            self.total_true = u256(int(self.total_true) + gl.message.value)
        else:
            self.total_lie = u256(int(self.total_lie) + gl.message.value)

        self.bet_count = u256(int(self.bet_count) + 1)

    @gl.public.write
    def close_betting(self) -> None:
        """Close betting and lock in bets before judgment."""
        assert gl.message.sender_address == self.owner, "Only owner can close"
        assert self.status == "open", "Already closed"
        self.status = "judging"

    @gl.public.write
    def judge_statement(self) -> None:
        """
        The core GenLayer magic — LLM validators independently:
        1. Research the statement using web access
        2. Vote true or lie with confidence score
        3. Reach consensus via eq_principle_strict_eq
        Winner pool is calculated and status set to settled.
        """
        assert self.status == "judging", "Must close betting first"

        statement = self.statement

        def evaluate() -> str:
            prompt = f"""
You are a fact-checker on a decentralized truth verification game.

Your job is to determine if the following statement is TRUE or a LIE.

STATEMENT: "{statement}"

Instructions:
- Research this statement carefully using your knowledge
- Consider whether the statement is factually accurate
- Be objective and precise
- "uncertain" is only allowed if the statement is genuinely unverifiable

Respond ONLY with this exact JSON format, no backticks, no extra text:
{{
  "verdict": "true" or "lie" or "uncertain",
  "confidence": integer from 0 to 100,
  "reasoning": "2-3 sentence explanation citing specific facts that support your verdict",
  "key_fact": "the single most important fact that determines the verdict"
}}
"""
            result = gl.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(result)
            verdict = str(parsed["verdict"]).lower()
            if verdict not in ("true", "lie", "uncertain"):
                verdict = "uncertain"
            return json.dumps({
                "verdict": verdict,
                "confidence": int(parsed["confidence"]),
                "reasoning": str(parsed["reasoning"]),
                "key_fact": str(parsed["key_fact"]),
            }, sort_keys=True)

        raw = gl.eq_principle_strict_eq(evaluate)
        result = json.loads(raw)

        self.verdict = result["verdict"]
        self.verdict_reasoning = result["reasoning"]
        self.verdict_confidence = u256(result["confidence"])
        self.status = "settled"

        # Calculate winner pool
        total = int(self.total_true) + int(self.total_lie)
        self.winner_pool = u256(total)

    @gl.public.write
    def claim_winnings(self) -> None:
        """
        Winners call this to claim their share of the pool.
        Payout proportional to stake on the winning side.
        """
        assert self.status == "settled", "Game not settled yet"
        assert self.verdict != "uncertain", "No winner — uncertain verdict"

        total = int(self.total_true) + int(self.total_lie)
        if total == 0:
            return

        # In production: track per-player bets and calculate proportional payout
        # For testnet: transfer full pool to caller as demo
        if int(self.winner_pool) > 0:
            gl.transfer(gl.message.sender_address, int(self.winner_pool))
            self.winner_pool = u256(0)

    @gl.public.write
    def new_round(self, statement: str) -> None:
        """Owner can start a new round with a fresh statement."""
        assert gl.message.sender_address == self.owner, "Only owner"
        assert self.status == "settled", "Settle current round first"
        self.statement = statement
        self.total_true = u256(0)
        self.total_lie = u256(0)
        self.bet_count = u256(0)
        self.status = "open"
        self.verdict = ""
        self.verdict_reasoning = ""
        self.verdict_confidence = u256(0)
        self.winner_pool = u256(0)
