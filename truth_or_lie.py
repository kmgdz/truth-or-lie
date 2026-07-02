# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


@gl.evm.contract_interface
class _Recipient:
    class View:
        pass
    class Write:
        pass


class TruthOrLie(gl.Contract):

    owner:      Address
    statement:  str
    status:     str          # open, judging, settled
    verdict:    str
    total_true: u256
    total_lie:  u256
    pool_true:  TreeMap[str, u256]
    pool_lie:   TreeMap[str, u256]
    confidence: u256
    reasoning:  str

    def __init__(self, statement: str) -> None:
        self.owner      = gl.message.sender_address
        self.statement  = statement
        self.status     = "open"
        self.verdict    = "uncertain"
        self.total_true = u256(0)
        self.total_lie  = u256(0)
        self.pool_true  = TreeMap()
        self.pool_lie   = TreeMap()
        self.confidence = u256(0)
        self.reasoning  = ""

    # ── place_bet ─────────────────────────────────────────────
    @gl.public.write.payable
    def place_bet(self, vote: str) -> None:
        if self.status != "open":
            raise Exception("Betting is no longer open")

        amount = gl.message.value
        if amount == u256(0):
            raise Exception("Bet amount must be greater than 0")

        voter = str(gl.message.sender_address)
        if vote == "true":
            self.total_true = self.total_true + amount
            self.pool_true[voter] = self.pool_true.get(voter, u256(0)) + amount
        elif vote == "lie":
            self.total_lie = self.total_lie + amount
            self.pool_lie[voter] = self.pool_lie.get(voter, u256(0)) + amount
        else:
            raise Exception("Vote must be 'true' or 'lie'")

    # ── close_betting ─────────────────────────────────────────
    @gl.public.write
    def close_betting(self) -> None:
        if str(gl.message.sender_address) != str(self.owner):
            raise Exception("Only the owner can close betting")
        if self.status != "open":
            raise Exception("Betting is not open")
        self.status = "judging"

    # ── judge_statement ───────────────────────────────────────
    @gl.public.write
    def judge_statement(self) -> None:
        if self.status != "judging":
            raise Exception("Game is not in judging state")

        statement = self.statement

        def evaluate():
            prompt = f"""You are an impartial fact-checker.

Evaluate the following statement: "{statement}"
Is this statement literally TRUE or a LIE? Research using the web if needed.

Return ONLY a JSON object. No markdown. No text outside JSON.
{{"verdict": "true" | "lie", "confidence": 0-100, "reasoning": "<one sentence>"}}"""

            result = gl.nondet.exec_prompt(prompt)
            return result.replace("```json", "").replace("```", "").strip()

        # Non-deterministic LLM calls must run through the Equivalence
        # Principle so validators can reach consensus on the verdict.
        raw = gl.eq_principle.prompt_comparative(
            evaluate,
            'The "verdict" field must be the same in both responses'
        )

        try:
            parsed = json.loads(raw)
            verdict = str(parsed.get("verdict", "uncertain")).strip().lower()
            confidence = int(parsed.get("confidence", 0))
            reasoning = str(parsed.get("reasoning", ""))[:300]
        except Exception:
            verdict = "uncertain"
            confidence = 0
            reasoning = "Failed to parse LLM response"

        if verdict not in ("true", "lie"):
            verdict = "uncertain"
        if confidence < 0:
            confidence = 0
        if confidence > 100:
            confidence = 100

        self.verdict    = verdict
        self.confidence = u256(confidence)
        self.reasoning  = reasoning
        self.status     = "settled"

    # ── claim_winnings ────────────────────────────────────────
    @gl.public.write
    def claim_winnings(self) -> None:
        if self.status != "settled":
            raise Exception("Game is not settled yet")
        if self.verdict not in ("true", "lie"):
            raise Exception("Verdict is uncertain, no winnings can be calculated")

        claimer = str(gl.message.sender_address)
        amount_won = u256(0)

        if self.verdict == "true":
            if claimer not in self.pool_true:
                raise Exception("You have no winning bets")
            staked = self.pool_true[claimer]
            amount_won = staked + (self.total_lie * staked) // self.total_true
            del self.pool_true[claimer]

        elif self.verdict == "lie":
            if claimer not in self.pool_lie:
                raise Exception("You have no winning bets")
            staked = self.pool_lie[claimer]
            amount_won = staked + (self.total_true * staked) // self.total_lie
            del self.pool_lie[claimer]

        if amount_won > u256(0):
            _Recipient(Address(claimer)).emit_transfer(value=amount_won)

    # ── views ─────────────────────────────────────────────────
    @gl.public.view
    def get_game_summary(self) -> str:
        return json.dumps({
            "statement":  self.statement,
            "status":     self.status,
            "total_true": str(self.total_true),
            "total_lie":  str(self.total_lie),
        })

    @gl.public.view
    def get_verdict(self) -> str:
        return json.dumps({
            "verdict":    self.verdict,
            "confidence": int(self.confidence),
            "reasoning":  self.reasoning,
            "total_true": str(self.total_true),
            "total_lie":  str(self.total_lie),
        })
