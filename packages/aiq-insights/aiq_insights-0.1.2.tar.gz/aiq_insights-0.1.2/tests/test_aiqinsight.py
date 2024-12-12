

from aiq_insights.checker import MCQChecker, MCQ

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
from timeit import default_timer as timer

# Measure time for analyzing question 1
start = timer()
result1 = aiq_insights.analyze_question(mcq1)
end = timer()
print("Question 1 Analysis:", result1)
print("Time taken for Question 1 Analysis:", end - start, "seconds")

# Measure time for analyzing question 2
start = timer()
result2 = aiq_insights.analyze_question(mcq2)
end = timer()
print("Question 2 Analysis:", result2)
print("Time taken for Question 2 Analysis:", end - start, "seconds")

# Measure time for analyzing the question set
start = timer()
result_set = aiq_insights.analyze_question_set([mcq1, mcq2])
end = timer()
print("Question Set Analysis:", result_set)
print("Time taken for Question Set Analysis:", end - start, "seconds")
