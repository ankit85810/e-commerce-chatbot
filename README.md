# E-commerce Chatbot 🛒🤖

This project implements an **AI-powered E-commerce Chatbot** capable of answering frequently asked questions (FAQs), handling small talk (chit-chat), and generating SQL queries for product-related data stored in a database.  
It integrates **Groq API**, **Streamlit UI**, **ChromaDB**, and **SQLite** for seamless conversational AI with product database connectivity.

---
## Code Workflow


```
                   ┌───────────────────────────┐
                   │       User Interface       │
                   │     (Streamlit Frontend)   │
                   └──────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │       router.py           │
                    │ (Semantic Intent Router)  │
                    └──────────────┬─────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
 ┌────────────────┐       ┌──────────────────┐       ┌─────────────────┐
 │   faq.py       │       │   chit_chat.py   │       │     sql.py      │
 │  (FAQ Engine)  │       │(Chit-Chat Module)│       │(SQL Query Gen.) │
 └────────────────┘       └──────────────────┘       └─────────────────┘
          │                        │                        │
          ▼                        ▼                        ▼
 ┌────────────────┐       ┌──────────────────┐       ┌──────────────────────────┐
 │ ChromaDB Index │       │   Groq API (LLM) │       │ SQLite Database (db.sqlite) │
 │ (Embeddings)   │       │ (Conversational) │       │  via Groq Query Generator │
 └────────────────┘       └──────────────────┘       └──────────────────────────┘
          │                        │                        │
          └───────────────┬────────┴────────┬───────────────┘
                          │                 │
                          ▼                 ▼
                 ┌────────────────────────────────┐
                 │         main.py                │
                 │ Collects + Displays Responses  │
                 │  (Streamlit Chat UI)           │
                 └────────────────────────────────┘

```
## 📁 Project Structure

```
E-commerce-chatbot/
│
├── app/
│   ├── main.py                # Streamlit app entry point
│   ├── chit_chat.py           # Handles general user conversations using Groq API
│   ├── faq.py                 # Handles FAQ retrieval using embeddings and ChromaDB
│   ├──.env                    # Environment variables (not uploaded to GitHub)
│   ├── router.py              # Semantic routing between FAQ, chit-chat, and SQL query handling
│   ├── sql.py                 # Handles SQL generation and database interactions using Groq API
│   └── resources/
│       └── faq_data.csv       # FAQ dataset used by the chatbot
│
└──  web-scraping/
    ├── flipkart_data_extraction.ipynb  # Jupyter notebook for scraping product data
    ├── csv_to_sqlite.py       # Converts scraped CSV data into SQLite format
    ├── db.sqlite              # SQLite database containing product data
    ├── flipkart_product_data.csv
    ├── flipkart_product_links.csv
    ├── duplicate_products.csv
    └── unavailable_products.csv
 
                      
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/E-commerce-chatbot.git
cd E-commerce-chatbot
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate       # On Windows
source venv/bin/activate      # On macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Environment Variables

Create a `.env` file inside the **app/** directory:

```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-70b-8192
```

---

## 🚀 Run the Chatbot

```bash
cd app
streamlit run main.py
```

The app will launch on **http://localhost:8501**

---

## 🧠 Features

| Feature | Description |
|----------|-------------|
| 💬 **Chit-Chat** | Engages in general conversation using the Groq API |
| ❓ **FAQ Handling** | Retrieves answers to predefined questions using ChromaDB embeddings |
| 🧾 **SQL Querying** | Converts natural language questions into SQL queries using Groq |
| 🗂️ **Web Scraping Module** | Extracts real product data from Flipkart and stores it into a SQLite database |

---

## 🧩 Technologies Used

- **Python 3.10+**
- **Streamlit** – Web UI
- **Groq API** – LLM-based response generation
- **ChromaDB** – Semantic search for FAQ handling
- **Semantic Router** – Intent routing between modules
- **SQLite** – Database for product data
- **Pandas** – Data manipulation
- **dotenv** – Environment variable management

---

## 🧑‍💻 Author

**Ankit Kumar**  
Data Science Enthusiast | AI Developer  

---

## 📄 License

This project is open-source and available under the **MIT License**.
