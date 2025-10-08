from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.routers import SemanticRouter

faq = Route(
    name="faq",
    utterances=[
    "How do I track my order on Flipkart?",
    "What is Flipkart's return policy?",
    "How can I cancel my order?",
    "What payment methods does Flipkart accept?",
    "How do I contact Flipkart customer support?",
    "What is Flipkart Plus and how does it work?",
    "How do I return an item to Flipkart?",
    "What are Flipkart's delivery charges?",
    "How do I change my delivery address after placing an order?",
    "What is Flipkart's refund policy?",
    "How do I create a Flipkart account?",
    "What is Cash on Delivery (COD)?",
    "How do I use Flipkart Gift Cards?",
    "What is Flipkart's EMI option?",
    "How do I check my order status?",
    "What if I receive a damaged or wrong product?",
    "How does Flipkart's replacement policy work?",
    "What is Flipkart Assured?",
    "How do I cancel a return request?",
    "What are Flipkart's exchange offers?",
    "How do I become a Flipkart seller?",
    "What is Supercoins in Flipkart?",
    "How do I update my profile information?",
    "What is Flipkart's price protection policy?",
    "How do I report a seller or product issue?",
    "What are the different delivery options available?",
    "How do I remove items from my wishlist?",
    "What is Flipkart's Green Delivery initiative?",
    "How do I apply coupon codes on Flipkart?",
    "What should I do if my payment fails?",
    "What is the return policy of the products?",
    "Do I get discount with the HDFC credit card?",
    "How can I track my order?",
    "What payment methods are accepted?",
    "How long does it take to process a refund?",
    "Are there any ongoing sales or promotions?",
    "Can I cancel or modify my order after placing it?",
    "Do you offer international shipping?",
    "What should I do if I receive a damaged product?",
    "How do I use a promo code during checkout?"
]

)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes that have 50% disscount",
        "are there any shoes under 2000 rs",
        "what is the price of puma shoes",
        "show me all the products from adidas",
        "do you have formal shoe of size 9",
        "i want to buy a red color t-shirt",
        "show me all the products under 1000 rs",
        "list all the products from reebok",
        "Show me puma shoes with rating above 4 stars",
        "find me nike shoes under 3000 rs"
    ]
)

chit_chat = Route(
    name="chit_chat",
    utterances=[
        "Hello",
        "Hi there",
        "How are you?",
        "What's your name?",
        "Tell me a joke",
        "What can you do?",
        "Goodbye",
        "See you later",
        "Thank you",
        "You're welcome",
        "How are you?"
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
        "Can you help me?",
        "Tell me something interesting.",
        "Do you have any hobbies?",
        "What is the meaning of life?",
        "can you help me with something?",
        "What is the weather like today?"
    ]
)
router = SemanticRouter(
    routes=[faq, sql, chit_chat],
    encoder=HuggingFaceEncoder(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    auto_sync="local"
)


if __name__ == "__main__":
    print(router("What is your policy on defective products?").name)
    print(router("Pink puma shoes under 3000 rs").name)