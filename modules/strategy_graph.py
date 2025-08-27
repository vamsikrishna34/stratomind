import modules.genai_agent as genai_agent

def run_strategy_pipeline(domain, query, docs, prediction):
    """
    Coordinates strategy generation using a multi-agent approach.
    Stub version — will be replaced by LangGraph orchestration.
    """
    genai_output = genai_agent.generate_strategy(docs, query)
    return f"[Domain: {domain}] {genai_output} | Prediction: {prediction}"