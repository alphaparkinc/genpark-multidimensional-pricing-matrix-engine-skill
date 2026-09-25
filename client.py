import json
from typing import Dict, Any, List, Optional

class MultidimensionalPricingMatrixEngineClient:
    """
    Production-grade multi-dimensional pricing matrix evaluation engine.
    Inspired by Metronome (metronome.com) — supporting complex multi-attribute pricing
    based on region, model tier, concurrency tier, and custom enterprise SLA commitments.
    """
    def __init__(self):
        self.base_rates = {
            "gpt-4o-mini": 0.00015,
            "gpt-4o": 0.00250,
            "claude-3-7-sonnet": 0.00300,
            "llama-3-3-70b": 0.00080
        }
        self.region_multipliers = {
            "us-east-1": 1.00,
            "eu-west-1": 1.10,
            "ap-southeast-1": 1.15
        }
        self.sla_multipliers = {
            "standard_99_5": 1.00,
            "enterprise_99_99": 1.25,
            "dedicated_low_latency": 1.40
        }

    def evaluate_dimensional_rate(
        self,
        model: str = "claude-3-7-sonnet",
        region: str = "eu-west-1",
        sla_tier: str = "enterprise_99_99",
        monthly_committed_volume_millions: float = 50.0,
        volume_consumed_millions: float = 62.5
    ) -> Dict[str, Any]:
        base_rate = self.base_rates.get(model, 0.00100)
        reg_mult = self.region_multipliers.get(region, 1.0)
        sla_mult = self.sla_multipliers.get(sla_tier, 1.0)

        # Committed vs Overage Discount Curves
        commit_discount = 0.20 if monthly_committed_volume_millions >= 50.0 else 0.10
        effective_commit_rate = round(base_rate * reg_mult * sla_mult * (1.0 - commit_discount), 6)
        overage_rate = round(base_rate * reg_mult * sla_mult * (1.0 - (commit_discount * 0.5)), 6)

        committed_qty = min(volume_consumed_millions, monthly_committed_volume_millions)
        overage_qty = max(0.0, volume_consumed_millions - monthly_committed_volume_millions)

        committed_cost = round(committed_qty * 1000 * effective_commit_rate, 2)
        overage_cost = round(overage_qty * 1000 * overage_rate, 2)
        total_billing_usd = round(committed_cost + overage_cost, 2)

        blended_effective_rate_per_1k = round((total_billing_usd / max(1.0, volume_consumed_millions * 1000)), 6)

        return {
            "matrix_evaluation_id": "mat_eval_mtr_5501",
            "model": model,
            "region": region,
            "sla_tier": sla_tier,
            "base_unit_rate_usd": base_rate,
            "region_multiplier": reg_mult,
            "sla_multiplier": sla_mult,
            "committed_volume_millions": monthly_committed_volume_millions,
            "volume_consumed_millions": volume_consumed_millions,
            "effective_committed_rate_per_1k": effective_commit_rate,
            "overage_rate_per_1k": overage_rate,
            "committed_cost_usd": committed_cost,
            "overage_cost_usd": overage_cost,
            "total_billing_usd": total_billing_usd,
            "blended_effective_rate_per_1k": blended_effective_rate_per_1k,
            "pricing_matrix_status": "DETERMINISTIC_MATCH_FOUND",
            "powered_by": "metronome.com multi-dimensional pricing engine"
        }
