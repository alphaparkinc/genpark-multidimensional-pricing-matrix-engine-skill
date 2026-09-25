import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import MultidimensionalPricingMatrixEngineClient

def main():
    client = MultidimensionalPricingMatrixEngineClient()
    res = client.evaluate_dimensional_rate()
    print("=== Multi-Dimensional Pricing Matrix Engine Output ===")
    print(f"Model: {res['model']} | Region: {res['region']} | SLA: {res['sla_tier']}")
    print(f"Volume: {res['volume_consumed_millions']}M tokens (Committed: {res['committed_volume_millions']}M)")
    print(f"Committed Cost: ${res['committed_cost_usd']:,.2f} (@ ${res['effective_committed_rate_per_1k']}/1k)")
    print(f"Overage Cost:   ${res['overage_cost_usd']:,.2f} (@ ${res['overage_rate_per_1k']}/1k)")
    print(f"Total Billing:  ${res['total_billing_usd']:,.2f}")
    print(f"Blended Rate:   ${res['blended_effective_rate_per_1k']}/1k tokens")
    print(f"Status: {res['pricing_matrix_status']}")

if __name__ == '__main__':
    main()
