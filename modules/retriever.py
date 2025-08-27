import os

def get_relevant_docs(domain: str, strategy: str):
    """
    Retrieves domain-specific strategy documentation.
    Currently a stub — will be replaced with LangChain RAG pipeline.
    """
    docs_dir = "assets/strategy_docs"
    domain_map = {
        "EdTech": "edtech_strategies.py",
        "FinTech": "fintech_strategies.py",
        "SaaS": "saas_strategies.py"
    }
    file_path = os.path.join(docs_dir, domain_map.get(domain, ""))
    try:
        with open(file_path, "r") as f:
            return [f.read()]
    except FileNotFoundError:
        return [f"No strategies found for {domain}."]