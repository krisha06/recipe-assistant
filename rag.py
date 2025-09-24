from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import sqlite3

DB_PATH = "recipes.db"

# Load recipes from DB
def load_recipes_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, ingredients, instructions, cooking_time, diet FROM recipes")
    rows = cursor.fetchall()
    conn.close()
    texts = []
    for r in rows:
        text = f"Title: {r[0]}\nIngredients: {r[1]}\nInstructions: {r[2]}\nCooking Time: {r[3]}\nDiet: {r[4]}"
        texts.append(text)
    return texts


def get_qa_chain():
    texts = load_recipes_from_db()
    if not texts:
        return None  # Handle empty DB case gracefully

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="./chroma_recipes",
        collection_name="recipes"
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model="llama3")

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
def query_recipe(user_query: str) -> str:
    qa_chain = get_qa_chain()
    if not qa_chain:
        return "⚠️ No recipes found in the database. Please scrape some recipes first."
    return qa_chain.run(user_query)

