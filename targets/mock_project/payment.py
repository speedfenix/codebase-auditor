def process_transaction(amount, currency):
    print(f"Initiating payment of {amount} {currency}...")
    
    # BUG: Dangerous blind exception handling that silences severe errors
    try:
        result = 100 / amount  # Will crash if amount is 0
        return {"status": "success", "id": result}
    except Exception:
        # Silently failing without logging or raising the issue!
        pass
