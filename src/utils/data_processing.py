import json
import pandas as pd
from typing import Dict, List, Any

def load_dataset(filepath: str) -> List[Dict[str, Any]]:
    """Load and parse the ConvFinQA dataset."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def format_table(table_data: List[List[str]]) -> str:
    """Convert table data into a readable string format."""
    df = pd.DataFrame(table_data)
    table_str = df.to_string(index=False, header=False)
    return f"Table data:\n{table_str}"

def prepare_context(entry: Dict[str, Any]) -> str:
    """Prepare the context by combining pre-text, table, and post-text."""
    pre_text = " ".join(entry.get("pre_text", []))
    post_text = " ".join(entry.get("post_text", []))
    table = format_table(entry.get("table", []))
    
    return f"""Context:
    Pre-text: {pre_text}
    
    {table}
    
    Post-text: {post_text}"""

def get_qa_from_entry(entry: Dict) -> Dict:
    """Extract QA data from entry regardless of structure."""
    if "qa" in entry:
        return entry["qa"]
    for key in ["qa_0", "qa_1", "qa_2"]:
        if key in entry:
            return entry[key]
    raise KeyError("No QA data found in entry")