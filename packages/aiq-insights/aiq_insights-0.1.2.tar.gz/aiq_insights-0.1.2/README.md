# AI Q Insights

This library checks for common errors in multiple-choice questions (MCQs), including ambiguity, unequal option lengths, and duplicate questions.

## Installation

You can install the library via pip:

```bash
pip install aiq_insight

# import
from aiq_insights import MCQ, MCQChecker

# Sample MCQs
mcq1 = MCQ(
    question_text="What is the capital of France?",
    options=["Paris", "London", "Berlin", "Rome"],
    correct_option_index=0
)

mcq2 = MCQ(
    question_text="Paris is the capital of which country?",
    options=["France", "Germany", "Italy", "Italy"],
    correct_option_index=0
)

# Initialize checker
aiq_insights = MCQChecker()

# Analyze individual questions
result1 = aiq_insights.analyze_question(mcq1)
result2 = aiq_insights.analyze_question(mcq2)
print("Question 1 Analysis:", result1)
print("Question 2 Analysis:", result2)

# Analyze question set for duplicates
result_set = aiq_insights.analyze_question_set([mcq1, mcq2])
print("Question Set Analysis:", result_set)
