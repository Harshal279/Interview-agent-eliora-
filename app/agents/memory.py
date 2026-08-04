from collections import Counter


class InterviewMemory:

    def __init__(self):
        self.memory = {
            "candidate_profile": {
                "overall_average": 0,
                "questions_answered": 0,
                "strong_topics": [],
                "weak_topics": [],
                "strengths": [],
                "weaknesses": [],
                "covered_topics": [],
                "covered_followups": []
            },

            "history": {}
        }

    ##########################################################

    def add_evaluation(self, question_id: str, evaluation: dict):

        self.memory["history"][question_id] = evaluation

        self._update_profile()

    ##########################################################

    def _update_profile(self):

        history = self.memory["history"]

        if not history:
            return

        total_score = 0

        strengths = []

        weaknesses = []

        topics = []

        followups = []

        topic_scores = {}

        for qid, item in history.items():

            total_score += item.get("overall_score", 0)

            strengths.extend(item.get("strengths", []))

            weaknesses.extend(item.get("weaknesses", []))

            topic = item.get("topic")

            if topic:

                topics.append(topic)

                topic_scores.setdefault(topic, [])

                topic_scores[topic].append(item.get("overall_score", 0))

            followups.extend(item.get("followup_topics", []))

        avg = round(total_score / len(history), 2)

        strong_topics = []

        weak_topics = []

        for topic, scores in topic_scores.items():

            score = sum(scores) / len(scores)

            if score >= 8:
                strong_topics.append(topic)

            elif score <= 5:
                weak_topics.append(topic)

        self.memory["candidate_profile"] = {

            "overall_average": avg,

            "questions_answered": len(history),

            "strong_topics": strong_topics,

            "weak_topics": weak_topics,

            "strengths": Counter(strengths).most_common(),

            "weaknesses": Counter(weaknesses).most_common(),

            "covered_topics": list(set(topics)),

            "covered_followups": list(set(followups))
        }

    ##########################################################

    def get_profile(self):

        return self.memory["candidate_profile"]

    ##########################################################

    def get_history(self):

        return self.memory["history"]

    ##########################################################

    def export(self):

        return self.memory