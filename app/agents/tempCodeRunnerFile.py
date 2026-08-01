def evaluate_candidate_answer(candidate_answer, question):
    """ takes the candidate answer and question and evaluate it 
    """
    core_components = {
        "clarity": 8,
        "accuracy": 9,
        "depth": 7.5,
        "communication": 6
    }

    overall_score = sum(core_components.values()) / len(core_components)

    evaluation_result = {
        "question_id": "Q04",
        "question": "what is your experience with python programming?",
        "answer": "i have been working with python for 5 years and have experience in web development, data analysis, and machine learning.",
        "overall_score": overall_score,
        "recommendation": "study advanced data structured",
    }
    return evaluation_result


class ConversationMemory:
    # store and retrieve history

    def __init__(self):
        self.conversation_history = []

    def add_to_memory(self, question, answer, evaluation):

        entry = {
            "question": question,
            "answer": answer,
            "evaluation": evaluation
        }  
        self.conversation_history.append(entry)

    def get_context(self, num_recent=3):
        return self.conversation_history[-num_recent:]

    def get_score_summary(self):

        scores= [entry['evaluation']['overall_score']
                 for entry in self.conversation_history]

        average_scores=sum(scores)/len(scores) if scores else 0

        return

