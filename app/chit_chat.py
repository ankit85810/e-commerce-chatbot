from groq import Groq
from dotenv import load_dotenv
import os


if "GROQ_API_KEY" in os.environ:
    api_key = os.environ["GROQ_API_KEY"]
else:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

def generate_answer(query):
    client = Groq(api_key=api_key)
    prompt = f"""You are a helpful assistant for an E-commerce website. This is just a chit-chat conversation with the user. Be polite and courteous. Keep your answers short and precise."""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.5,
        model=os.getenv("GROQ_MODEL"),
        max_tokens=500
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    query = "Hello, how are you?"
    answer = generate_answer(query)
    print(answer)