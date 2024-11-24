
def create_prompt(context: str, question: str) -> str:
    """Create a more structured prompt with explicit percentage handling."""
    return f"""You are a financial analysis assistant. Follow these EXACT rules:

1. Carefully read and analyze the numerical data in the context
2. Show your calculation steps clearly using basic arithmetic
3. IMPORTANT FORMAT RULES:
   - If calculating a PERCENTAGE:
     * First calculate to 4 decimal places for accuracy
     * Then convert to decimal form (e.g., 0.147 not 14.7)
     * Your final answer must be in decimal form
   - If calculating a regular number:
     * Calculate to 4 decimal places first
     * Round to 2 decimal places for final answer
4. Your final answer must ALWAYS be in this exact format:
   - For percentages: "FINAL_ANSWER: 0.147"  (not 14.7%)
   - For regular numbers: "FINAL_ANSWER: 1234.56"

Context:
{context}

Question: {question}

Let's solve this step by step:"""
