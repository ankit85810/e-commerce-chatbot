import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os


if "GROQ_API_KEY" in os.environ:
    api_key = os.environ["GROQ_API_KEY"]
else:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")


faqs_path = Path(__file__).parent / "resources" / "faq_data.csv"

chroma_client = chromadb.Client()
collection_name = "faq_collection"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def ingest_faq_data(path):
    if collection_name not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data...")
        collection = chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=ef
            )

        df = pd.read_csv(path) 
        docs = df['question'].tolist()
        metadata = [{'answer': ans} for ans in df['answer'].tolist()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )

        print(f"Ingested {len(docs)} FAQ entries into the collection.")
    else:
        print("Collection already exists. Skipping ingestion.")

def get_relevant_faqs(query):
    collection = chroma_client.get_collection(name=collection_name, embedding_function=ef)

    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results

def faq_chain(query):
    result = get_relevant_faqs(query)
    context = ' '.join([r.get('answer') for r in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer

def generate_answer(query, context):
    prompt = f'''    
    You are a helpful assistant. Based on the following context, answer the user's question concisely.if you don't know the answer, just say "I don't know". Do not try to make up an answer.Just do not make things up.

    Context:
    {context}

    User's Question:
    {query}

    Answer:
    '''
    groq_client = Groq(api_key=api_key)

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.2,
        model=os.getenv("GROQ_MODEL")
    )
    return chat_completion.choices[0].message.content
if __name__ == "__main__":

    ingest_faq_data(faqs_path)

    test_query = "i do not want this product, how can i return it?"
    # faqs = get_relevant_faqs(test_query)
    ans = faq_chain(test_query)
    print(ans)