import google.generativeai as genai
from dotenv import load_dotenv
import os


if "GOOGLE_API_KEY" in os.environ:
    api_key = os.environ["GOOGLE_API_KEY"]
else:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

def generate_answer(query):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    prompt = f"""You are a helpful assistant for an E-commerce website. This is just a chit-chat conversation with the user. Be polite and courteous. Keep your answers short and precise."""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.5,
            "max_output_tokens": 500
        }
    )

    return response.text.strip() if response.text else "No response generated."


if __name__ == "__main__":
    query = "Hello, how are you?"
    answer = generate_answer(query)
    print(answer)