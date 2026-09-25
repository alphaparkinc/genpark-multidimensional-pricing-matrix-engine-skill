import json, sys
from client import MultidimensionalPricingMatrixEngineClient

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "multidimensional-pricing-matrix", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "evaluate_dimensional_rate", "description": "Evaluates complex multi-dimensional pricing matrices across model, region, SLA tier, and volume commitments."}]}}
    elif method == "tools/call":
        client = MultidimensionalPricingMatrixEngineClient()
        res = client.evaluate_dimensional_rate()
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ACTIVE"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_mcp_request({"method": "tools/list"})))
    else:
        client = MultidimensionalPricingMatrixEngineClient()
        print(json.dumps(client.evaluate_dimensional_rate(), indent=2))
