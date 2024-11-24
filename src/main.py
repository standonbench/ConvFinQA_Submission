from utils.evaluation import evaluate_dataset

def main():
    """Main entry point."""
    results = evaluate_dataset("src/data/train.json", num_samples=5)

if __name__ == "__main__":
    main()