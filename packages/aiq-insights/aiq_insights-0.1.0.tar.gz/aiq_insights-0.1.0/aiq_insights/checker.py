from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
from typing import List, Optional


class MCQ:
    """Class representing a multiple-choice question."""

    def __init__(self, question_text: str, options: List[str], correct_option_index: int):
        self.question_text = question_text
        self.options = options
        self.correct_option_index = correct_option_index


class MCQChecker:
    """Class for analyzing MCQs for common errors and duplicates."""

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        # Load a pre-trained Sentence-BERT model for encoding sentences
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def get_embeddings(self, text: str):
        # Tokenize and encode text into embeddings
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings.squeeze().numpy()

    # Check #1: Ambiguous Wording
    def check_ambiguity(self, question_text: str) -> str:
        vague_words = ["sometimes", "often", "may", "could", "usually"]
        if any(word in question_text for word in vague_words):
            return "Ensure the question is clear, concise, and straightforward. Avoid double negatives or overly complex language."
        return "ok"

    # Check #2: "All of the Above" and "None of the Above" Options
    def check_all_none_above(self, options: List[str]) -> str:
        problematic_phrases = ["all of the above", "none of the above"]
        if any(phrase in opt.lower() for opt in options for phrase in problematic_phrases):
            return "Use these options sparingly and only when they genuinely add value to the question."
        return "ok"

    # Check #3: Unequal Option Lengths
    def check_option_length(self, options: List[str], tolerance: float = 0.5) -> str:
        avg_length = sum(len(opt) for opt in options) / len(options)
        if any(abs(len(opt) - avg_length) > avg_length * tolerance for opt in options):
            return "Keep options similar in length and style to avoid inadvertently cueing the answer."
        return "ok"

    # Check #4: Clues in the Question Stem or Options
    def check_clues(self, question_text: str, options: List[str], threshold: float = 0.5) -> str:
        question_embedding = self.get_embeddings(question_text)
        for option in options:
            option_embedding = self.get_embeddings(option)
            similarity = 1 - cosine(question_embedding, option_embedding)
            if similarity > threshold:
                return "Avoid repetitive language between the question stem and options, and ensure each option is unique."
        return "ok"

    # Check #5: Using Absolutes
    def check_absolute_terms(self, options: List[str]) -> str:
        absolute_terms = ["always", "never", "only"]
        if any(term in opt.lower() for opt in options for term in absolute_terms):
            return "Use qualifiers sparingly, and avoid absolute terms unless the statement is definitively true or false."
        return "ok"

    # Check #6: Negative Questions
    def check_negative_phrasing(self, question_text: str) -> str:
        negative_words = ["not", "except"]
        if any(word in question_text.lower() for word in negative_words):
            return 'Use negative phrasing sparingly and highlight the negative words ("not," "except") if necessary.'
        return "ok"

    # Check #7: Duplicate Options
    def check_duplicate_options(self, options: List[str]) -> str:
        if len(set(options)) != len(options):
            return "Duplicate options detected. Ensure each option is unique."
        return "ok"

    # Check #8: Duplicate Questions in Set
    def check_duplicates_in_set(self, questions: List[MCQ], threshold: float = 0.85) -> List[str]:
        duplicates = []
        embeddings = [self.get_embeddings(q.question_text) for q in questions]

        for i, emb1 in enumerate(embeddings):
            for j in range(i + 1, len(embeddings)):
                emb2 = embeddings[j]
                similarity = 1 - cosine(emb1, emb2)
                if similarity >= threshold:
                    duplicates.append(f"Duplicate detected between question {i + 1} and question {j + 1}")

        return duplicates if duplicates else ["ok"]

    def analyze_question(self, mcq: MCQ) -> dict:
        """Analyzes an individual question for various errors."""
        return {
            "ambiguity": self.check_ambiguity(mcq.question_text),
            "all_none_above": self.check_all_none_above(mcq.options),
            "unequal_length": self.check_option_length(mcq.options),
            "clues": self.check_clues(mcq.question_text, mcq.options),
            "absolute_terms": self.check_absolute_terms(mcq.options),
            "negative_phrasing": self.check_negative_phrasing(mcq.question_text),
            "duplicate_options": self.check_duplicate_options(mcq.options),
        }

    def analyze_question_set(self, question_list: List[MCQ]) -> dict:
        """Analyzes a set of questions for duplicates."""
        duplicates = self.check_duplicates_in_set(question_list)

        return {
            "duplicates": duplicates,
        }
