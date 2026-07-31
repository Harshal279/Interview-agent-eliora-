from groq import Groq
client= Groq(api_key="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")

print("chatbot(Groq streaming):Type 'quit','exit' or 'bye' to stop\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit','exit','bye']:
        print("chatbot: Goodbye!")
        break
    
    print("chatbot: ", end="", flush=True)

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[ {"role": "system","content": "you are a helpful assistant."},
           {"role": "user","content": user_input}
         ],
         stream=True  # enable streaming
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()   # new line after the response
    