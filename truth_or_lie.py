# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

class TruthOrLie(gl.Contract):
    owner: Address
    statement: str
    status: str
    verdict: str
    total_true: int
    total_lie: int
    pool_true: dict
    pool_lie: dict
    confidence: int
    reasoning: str

    def __init__(self, statement: str):
        self.owner = msg.sender
        self.statement = statement
        self.status = "open"  # open, judging, settled
        self.verdict = "uncertain"
        self.total_true = 0
        self.total_lie = 0
        self.pool_true = {}
        self.pool_lie = {}
        self.confidence = 0
        self.reasoning = ""

    def place_bet(self, vote: str):
        if self.status != "open":
            raise Exception("Betting is no longer open")
        
        amount = msg.value
        if amount <= 0:
            raise Exception("Bet amount must be greater than 0")

        voter = msg.sender
        if vote == "true":
            self.total_true += amount
            if voter in self.pool_true:
                self.pool_true[voter] += amount
            else:
                self.pool_true[voter] = amount
        elif vote == "lie":
            self.total_lie += amount
            if voter in self.pool_lie:
                self.pool_lie[voter] += amount
            else:
                self.pool_lie[voter] = amount
        else:
            raise Exception("Vote must be 'true' or 'lie'")

    def close_betting(self):
        if msg.sender != self.owner:
            raise Exception("Only the owner can close betting")
        self.status = "judging"

    def judge_statement(self):
        if self.status != "judging":
            raise Exception("Game is not in judging state")

        # In a real GenLayer contract, we use gl.exec_prompt to ask validators.
        # This is a basic implementation of reaching out to LLM.
        prompt = f"""
        Evaluate the following statement: "{self.statement}"
        Is this statement literally TRUE or a LIE?
        Research using the web if necessary.
        You must output JSON exactly in this format:
        {{"verdict": "true" | "lie", "confidence": 0-100, "reasoning": "brief explanation"}}
        """
        
        response_str = gl.exec_prompt(prompt)
        try:
            result = json.loads(response_str)
            self.verdict = result.get("verdict", "uncertain").lower()
            self.confidence = result.get("confidence", 0)
            self.reasoning = result.get("reasoning", "")
        except:
            self.verdict = "uncertain"
            self.confidence = 0
            self.reasoning = "Failed to parse LLM response"
            
        self.status = "settled"

    def claim_winnings(self):
        if self.status != "settled":
            raise Exception("Game is not settled yet")
        if self.verdict not in ["true", "lie"]:
            raise Exception("Verdict is uncertain, no winnings can be calculated")

        claimer = msg.sender
        amount_won = 0

        if self.verdict == "true":
            if claimer not in self.pool_true:
                raise Exception("You have no winning bets")
            staked = self.pool_true[claimer]
            # Calculate proportion of the losing pool
            share = staked / self.total_true
            amount_won = staked + int(self.total_lie * share)
            # Remove from pool to prevent double-claiming
            del self.pool_true[claimer]
            
        elif self.verdict == "lie":
            if claimer not in self.pool_lie:
                raise Exception("You have no winning bets")
            staked = self.pool_lie[claimer]
            # Calculate proportion of the losing pool
            share = staked / self.total_lie
            amount_won = staked + int(self.total_true * share)
            # Remove from pool to prevent double-claiming
            del self.pool_lie[claimer]

        if amount_won > 0:
            gl.transfer(claimer, amount_won)

    def get_game_summary(self) -> str:
        return json.dumps({
            "statement": self.statement,
            "status": self.status,
            "total_true": str(self.total_true),
            "total_lie": str(self.total_lie)
        })

    def get_verdict(self) -> str:
        return json.dumps({
            "verdict": self.verdict,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "total_true": str(self.total_true),
            "total_lie": str(self.total_lie)
        })
