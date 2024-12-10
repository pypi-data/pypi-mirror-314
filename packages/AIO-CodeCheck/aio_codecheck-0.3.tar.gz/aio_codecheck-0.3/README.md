
# Python Code Evaluation Tool

A lightweight Python-based tool designed to evaluate the quality of Python scripts based on correctness, coding style, and syntax validity. 

## Features
- **Test Case Execution:** Automatically runs predefined test cases and checks for correctness.
- **Style Evaluation:** Analyzes variable naming conventions and line lengths to ensure compliance with Python style guidelines (PEP-8).
- **Syntax Checking:** Ensures the provided code is syntactically correct.
- **Score Calculation:** Provides a detailed report with scores for correctness, style, and syntax, along with a final evaluation.
- **Feedback Output:** Generates a comprehensive evaluation report as a `.txt` file.

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd python-code-evaluation-tool
   ```

2. **Install Requirements** (if applicable)
   No external libraries are required; the tool uses Python's built-in modules.

## Usage

Run the tool from the command line using the following syntax:

```bash
python evaluator.py -f <path-to-your-script> [-o <output-feedback-path>]
```

### Arguments
- `-f, --file`: **(Required)** Path to the Python file to evaluate.
- `-o, --output`: **(Optional)** Path to save the evaluation report as a `.txt` file.

### Example
```bash
python evaluator.py -f sample_script.py -o feedback.txt
```

## Scoring
The final evaluation score is computed using the following weights:
- **Correctness:** 70%
- **Style:** 20%
- **Syntax:** 10%

A score of **90% or higher** results in code approval.

## Output
The tool provides a summary in the terminal and optionally saves a detailed `.txt` report. The report includes:
- Correctness, style, and syntax scores.
- A list of style issues (if any).
- Final evaluation status (ACCEPTED/REJECTED).

## Sample Output

### Terminal Output:
```
Evaluating your code...
...

Summary:
Correctness: 100%
Style: 80%
Syntax: 100%
Final Score: 94%
Result: Your code passed the evaluation ✅
```

### Feedback Report:
```text
========================================
Code Evaluation Report
========================================

Scores:
- Correctness: 100%
- Style: 80%
- Syntax: 100%
- Final Score: 94%

Evaluation Summary:
Your code is ACCEPTED ✅

Style Issues:
  - Variable 'TestVariable' is not in snake_case.
  - Line 12 exceeds 79 characters.

========================================
Detailed Feedback:
- Variable 'TestVariable' is not in snake_case.
- Line 12 exceeds 79 characters.
```

## Contributing
Feel free to open issues or submit pull requests for additional features or improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
