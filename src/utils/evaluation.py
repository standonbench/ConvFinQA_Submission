from ollama import Client 
from tqdm import tqdm
import time
from pathlib import Path
import json
from .data_processing import load_dataset, prepare_context, get_qa_from_entry
from .prompt_engineering import create_prompt
from .answer_extraction import extract_final_answer, compare_answers, standardize_percentage



def evaluate_dataset(dataset_path: str, num_samples: int = None):
    """Evaluate with running accuracy scores."""
    client = Client()
    dataset = load_dataset(dataset_path)
    
    if num_samples:
        dataset = dataset[:num_samples]
    
    results = []
    running_stats = {
        "processed": 0,
        "exact_matches": 0,
        "close_matches": 0
    }
    
    print(f"Evaluating {len(dataset)} questions...")
    
    for i, entry in enumerate(tqdm(dataset)):
        try:
            qa_data = get_qa_from_entry(entry)
            question = qa_data["question"]
            expected = qa_data["answer"]
            
            # Get model response
            context = prepare_context(entry)
            prompt = create_prompt(context, question)
            response = client.generate(
                model="qwen2-math",
                prompt=prompt,
                stream=False,
                options={"temperature": 0.1}
            )
            
            calculated = extract_final_answer(response['response'])
            comparison = compare_answers(calculated, expected)
            
            # Update running statistics
            running_stats["processed"] += 1
            if comparison["exact_match"]:
                running_stats["exact_matches"] += 1
            elif comparison["close_match"]:
                running_stats["close_matches"] += 1
            
            # Store result
            result = {
                "question": question,
                "expected": expected,
                "calculated": calculated,
                "comparison": comparison,
                "response": response['response']
            }
            results.append(result)
            
            # Print running accuracy after each question
            total_correct = running_stats["exact_matches"] + running_stats["close_matches"]
            print(f"\nRunning Accuracy ({i+1}/{len(dataset)}):")
            print(f"Exact Matches: {running_stats['exact_matches']}/{running_stats['processed']} ({running_stats['exact_matches']/running_stats['processed']:.1%})")
            print(f"Close Matches: {running_stats['close_matches']}/{running_stats['processed']} ({running_stats['close_matches']/running_stats['processed']:.1%})")
            print(f"Total Correct: {total_correct}/{running_stats['processed']} ({total_correct/running_stats['processed']:.1%})")
            
            # Print details for non-exact matches
            if not comparison["exact_match"]:
                print(f"\nQuestion {i+1}:")
                print(f"Q: {question}")
                print(f"Expected: {expected}")
                print(f"Got: {standardize_percentage(calculated) if '%' in expected else calculated}")
                if comparison["close_match"]:
                    print("Note: Close match (within tolerance)")
                if comparison["error"] is not None:
                    print(f"Error margin: {comparison['error']:.4f}")
                print("-" * 50)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"\nError processing entry {i+1}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {str(e)}")
            print("Entry structure:", json.dumps(entry, indent=2)[:200] + "...")
            continue
    
   # Final statistics
    total = len(results)
    print(f"\n=== Final Results ===")
    print(f"Total Questions: {total}")
    print(f"Exact Matches: {running_stats['exact_matches']} ({running_stats['exact_matches']/total:.1%})")
    print(f"Close Matches: {running_stats['close_matches']} ({running_stats['close_matches']/total:.1%})")
    total_correct = running_stats["exact_matches"] + running_stats["close_matches"]
    print(f"Total Correct: {total_correct} ({total_correct/total:.1%})")
    
    # save results
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    save_path = Path("results")
    save_path.mkdir(exist_ok=True)
    
    # Save detailed results and statistics
    with open(save_path / f"evaluation_results_{timestamp}.json", "w") as f:
        json.dump({
            "total_questions": total,
            "exact_matches": running_stats['exact_matches'],
            "close_matches": running_stats['close_matches'],
            "total_correct": total_correct,
            "accuracy": total_correct/total,
            "detailed_results": results  # This contains all individual question results
        }, f, indent=2)
    
    return results