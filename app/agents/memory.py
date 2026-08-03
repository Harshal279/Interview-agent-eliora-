<<<<<<< Updated upstream
=======
#from agents import evaluation

memory = {

    "question_1" : {
        "question" : "Define what is RAG?",
        "candidate_answer": "Um, okay. So, RAG... uh, RAG stands for Retrieval-Augmented Generation. And, basically, what it does is... sorry, let me rephrase. Its a framework used to improve the accuracy ofLLMs.So, instead of just relying on the model's internal weights you know, what it learned during pre-training\u2014it, um, it actually hooks up the LLM to an external database. Like, a vector database.Uh, how it actually works step-by-step is... well, there are three main parts. First is the retrieval phase. When a user asks a question\u2014the query\u2014the system converts that text into an embedding. Um, using an embedding model. Then it does a similarity search... wait, sorry, a semantic search inside the vector database to find chunks of textthat match the user's intent.Then comes the... the augmentation part.This is where the system takes those retrieved chunks\u2014the context\u2014and sort of glues them together with the original user prompt. It creates a new, bigger prompt.And finally, the... the generation phase. The LLM reads this whole combined prompt\u2014so it\u2019s basically like an open-book exam for the AI\u2014and it generates an answer based only on that specific data.Um, as for why you\u2019d use it over fine-tuning... wow, my mind just went blank for a second, sorry. Right, fine-tuning. Fine-tuning actually changes the model's weights, whichis super expensive and takes a long time. Plus, if your data changes every day, you can't keep fine-tuning it. RAG is way better for dynamic data because you just update the database, not the whole model. And... um, yeah, it also really helps stop hallucinations because the model is forced to stick to the facts you give it. I think... yeah, I think that covers the main points.",
        "scores": {
            "technical": 8,
            "communication": 6,
            "problem_solving": 7,
            "confidence": 5,
            "relevance": 9
        },
        "overall_score": 7,
        "strengths": [
            "Ability to explain complex concepts",
            "Knowledge of RAG framework",
            "Understanding of the benefits of RAG over fine-tuning"
        ],
        "weaknesses": [
            "Lack of confidence in answering",
            "Tendency to hesitate and use filler words",
            "Could improve in providing a clear and concise explanation"
        ],
        "feedback": "The candidate demonstrates a good understanding of the RAG framework and its benefits. However, they could improve in providing a clear and concise explanation, and showing more confidence in their answer.",
        "difficulty": "Medium",
        "topic": "Natural Language Processing",
        "followup_topics": [
            "LLM fine-tuning",
            "Vector databases",
            "Semantic search"
        ]
    },
}


print 
    
>>>>>>> Stashed changes
