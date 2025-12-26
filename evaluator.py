import json

class Evaluator:
    def __init__(self):
        self.results = []
    
    def evaluate_answer(self, question, answer, question_type="answerable", notes=""):
        evaluation = {
            "question": question,
            "answer": answer,
            "question_type": question_type,
            "accuracy": self.check_accuracy(answer),
            "hallucination": self.check_hallucination(answer),
            "clarity": self.check_clarity(answer),
            "completeness": self.check_completeness(answer),
            "notes": notes
        }
        self.results.append(evaluation)
        return evaluation
    
    def check_accuracy(self, answer):
        if "error" in answer.lower() or "not covered" in answer.lower():
            return "partial"
        if "i don't know" in answer.lower() or "unable to" in answer.lower():
            return "partial"
        return "good"
    
    def check_hallucination(self, answer):
        if "error" in answer.lower():
            return "error"
        return "good"
    
    def check_clarity(self, answer):
        if len(answer) < 10:
            return "poor"
        return "good"
    
    def check_completeness(self, answer):
        if len(answer) < 20:
            return "poor"
        return "good"
    
    def save_results(self, filename="eval_results.json"):
        summary = {
            "total_questions": len(self.results),
            "results": self.results
        }
        
        with open(filename, "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"Results saved to {filename}")
