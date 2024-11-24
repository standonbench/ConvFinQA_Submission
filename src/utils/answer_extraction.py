from typing import Optional
import re


def extract_final_answer(response: str) -> Optional[float]:
    """Extract the final numerical answer from the model's response with improved parsing."""
    # Clean the response string
    response = response.replace('\\', '').strip()
    
    # Look for explicit FINAL_ANSWER format (case insensitive)
    patterns = [
        r'FINAL_?ANSWER:\s*(-?\d+\.?\d*%?)',
        r'\\boxed{([^}]+)}',
        r'answer(?:\s+is)?:\s*(-?\d+\.?\d*%?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            # Get the last group that matched (handles different capture group counts)
            answer_str = match.group(match.lastindex).strip()
            try:
                # Remove any remaining special characters and convert
                answer_str = answer_str.replace('$', '').replace(',', '').strip()
                if '%' in answer_str:
                    return float(answer_str.rstrip('%')) / 100
                return float(answer_str)
            except ValueError:
                continue
    
    # Fallback: look for the last numerical value in the response
    lines = response.split('\n')
    for line in reversed(lines):
        # Skip lines that are clearly not final answers
        if re.search(r'step|calculate|formula|let|=', line.lower()):
            continue
        
        # Try to find percentage values first
        percent_matches = re.findall(r'-?\d+\.?\d*%', line)
        if percent_matches:
            try:
                return float(percent_matches[-1].rstrip('%')) / 100
            except ValueError:
                continue
        
        # Try to find plain numbers
        num_matches = re.findall(r'-?\d+\.?\d*', line)
        if num_matches:
            try:
                return float(num_matches[-1])
            except ValueError:
                continue
    
    return None

def standardize_percentage(value: float) -> str:
    """Consistently format percentage values."""
    if value is None:
        return "N/A"
    # Convert to percentage form if not already
    if abs(value) < 1:  # If it's already in decimal form
        value = value * 100
    return f"{value:.1f}%"

def compare_answers(calculated: float, expected: str) -> dict:
    """Compare calculated and expected answers with flexible precision."""
    if calculated is None:
        return {
            "is_correct": False,
            "exact_match": False,
            "close_match": False,
            "error": None
        }
    
    # Clean expected answer string
    expected = expected.strip().replace('$', '').replace(',', '').replace('\\', '')
    is_percentage = '%' in expected
    
    try:
        # Convert expected to float
        expected_val = float(expected.rstrip('%')) / 100 if is_percentage else float(expected)
        
        # If it's a percentage question, ensure comparison is done in same format
        if is_percentage:
            calculated = calculated if calculated < 1 else calculated / 100
        
        # Calculate error
        error = abs(calculated - expected_val)
        
        # Different levels of matching
        exact_match = error < 0.0001
        close_match = error < 0.01  # 1% tolerance
        
        return {
            "is_correct": exact_match or close_match,
            "exact_match": exact_match,
            "close_match": close_match,
            "error": error
        }
    except ValueError as e:
        print(f"Error comparing answers: {str(e)}")
        return {
            "is_correct": False,
            "exact_match": False,
            "close_match": False,
            "error": None
        }
