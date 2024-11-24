# Financial QA System

## Setup
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure Ollama is installed https://ollama.com/

3. Pull the Qwen2-Math model
    ```bash
    ollama pull qwen2-math
    ```

4. Run the evaluation:
    ```bash
    python src/main.py
    ```

## Project Structure

### Main Components

#### `src/main.py`
- Entry point of the application
- Runs the evaluation on the financial QA dataset

#### `src/utils/data_processing.py`
- Handles loading and preprocessing of financial data
- Functions for:
  * Loading JSON dataset
  * Formatting financial tables
  * Preparing context for the model
  * Extracting QA pairs from data

#### `src/utils/prompt_engineering.py`
- Contains prompt templates for the model
- Ensures consistent formatting of questions
- Specialized prompts for financial calculations

#### `src/utils/answer_extraction.py`
- Extracts numerical answers from model responses
- Handles percentage calculations
- Compares predicted vs actual answers
- Manages different formats (percentages, decimals, etc.)

#### `src/utils/evaluation.py`
- Main evaluation logic
- Tracks accuracy metrics
- Generates detailed performance reports
- Handles error cases and edge conditions

### Data
- Place your financial QA dataset in the `data/` folder
- Expected format: JSON with pre-text, post-text, tables, and QA pairs

## How It Works
1. **Data Loading**: System reads financial reports with tables and text
2. **Context Preparation**: Combines relevant text and tables for each question
3. **Question Processing**: Sends formatted questions to Qwen2-Math model
4. **Answer Extraction**: Processes model responses to get numerical answers
5. **Evaluation**: Compares answers with ground truth and calculates accuracy

## Model Details
- **Model**: Qwen2-Math (via Ollama)
- **Features**:
  * Specialized for mathematical calculations
  * Handles complex financial metrics
  * Provides step-by-step reasoning

Please Note - the code has been optimised for my laptop, an M2 mac.

Pierre Muletier