from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PerformanceTrend(Enum):
    """Performance trend categories"""
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"

@dataclass
class EvaluationResult:
    """Structured evaluation result"""
    question_id: str
    question: str
    answer: str
    overall_score: float
    feedback: str
    

class CandidateEvaluator:
    """Evaluates candidate answers based on multiple criteria."""
    
    # Configurable scoring weights
    DEFAULT_criteria = {
        "clarity": 7,
        "accuracy": 6,
        "depth": 5,
        "communication": 4
    }
    
    def __init__(self, criteria: Optional[Dict[str, float]] = None):
        """
        Initialize evaluator with scoring criteria.
        
       """
        self.criteria = criteria or self.DEFAULT_criteria
        
        score_sum = sum(self.criteria.values())
        if not (score_sum > 0):  
            raise ValueError("allowed criteria weights must sum to a positive value.")

    def candidate_evaluate_answer(
        self,
        question_id: str,
        question: str,
        candidate_answer: str
    ) -> EvaluationResult:
        """Candidate answer evaluation based on predefined criteria"""
        # validate inputs
        if not candidate_answer or not isinstance(candidate_answer, str):
            raise ValueError("Invalid candidate answer must be a non-empty string.")
        if not question or not isinstance(question, str):
            raise ValueError("Invalid question must be a non-empty string.")

        scores = self._calculate_score(candidate_answer, question)
        overall_score = self._calculate_overall_score(scores)
        feedback = self.generate_feedback(scores, overall_score)
        
        return EvaluationResult(
            question_id=question_id,
            question=question,
            answer=candidate_answer,
            overall_score=overall_score,
            feedback=feedback
        )
    
    def _calculate_score(self, answer: str, question: str) -> Dict[str, float]:
        """Calculate individual scores for each criterion"""
        scores = {}
        answer_length = len(answer.split())
        
        # Clarity: based on sentence structure
        scores["clarity"] = min(10.0, (answer_length / 50) * 10)
        
        # Accuracy: simplified keyword matching
        scores["accuracy"] = self._calculate_accuracy(answer, question)
        
        # Depth: based on answer length and detail
        scores["depth"] = min(10.0, (answer_length / 100) * 10)
        
        # Communication: based on punctuation and structure
        scores["communication"] = self._calculate_communication_score(answer)
        
        return scores
    
    def _calculate_accuracy(self, answer: str, question: str) -> float:
        """Calculate accuracy score based on keyword matching"""
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        
        if not question_words:
            return 5.0
        
        overlap = len(question_words & answer_words)
        accuracy_score = (overlap / len(question_words)) * 10
        return min(10.0, max(0.0, accuracy_score))
    
    def _calculate_communication_score(self, answer: str) -> float:
        """Calculate communication score based on sentence structure"""
        sentences = answer.split('.')
        sentence_count = len([s for s in sentences if s.strip()])
        
        if sentence_count == 0:
            return 3.0
        
        avg_sentence_length = len(answer.split()) / max(sentence_count, 1)
        
        # Good communication: 10-20 words per sentence
        if 10 <= avg_sentence_length <= 20:
            return 9.0
        elif 5 <= avg_sentence_length < 10 or 20 < avg_sentence_length <= 30:
            return 7.0
        else:
            return 5.0
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_weighted_score = 0.0
        total_weight = sum(self.criteria.values())
        
        for criterion, weight in self.criteria.items():
            score = scores.get(criterion, 0.0)
            total_weighted_score += score * weight
        
        overall = total_weighted_score / total_weight if total_weight > 0 else 0.0
        return round(overall, 2)
    
    def generate_feedback(self, scores: Dict[str, float], overall_score: float) -> str:
        """Generate feedback based on scores"""
        feedback_parts = []
        
        for criterion, score in scores.items():
            if score >= 8:
                status = "excellent"
            elif score >= 6:
                status = "good"
            elif score >= 4:
                status = "acceptable"
            else:
                status = "needs improvement"
            
            feedback_parts.append(f"{criterion.capitalize()}: {status} ({score:.1f}/10)")
        
        feedback_parts.append(f"\nOverall: {overall_score}/10")
        return " | ".join(feedback_parts)

        

    