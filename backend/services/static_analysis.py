def run_static_analysis(code: str) -> dict:
    bugs = []

    # Detect TODOs
    if "TODO" in code:
        bugs.append("TODO found — unfinished implementation.")

    # Detect dangerous eval usage
    if "eval(" in code:
        bugs.append("Use of eval() detected — potential security risk.")

    return {
        "bugs": bugs
    }
