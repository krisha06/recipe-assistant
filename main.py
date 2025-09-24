import sys
from db import create_db, add_recipe
from recipes import scrape_recipes
from rag import query_recipe
from app import app  # Flask app

def run_scraper(url: str):
    """Scrape recipes from a URL and save to DB."""
    create_db()
    recipes = scrape_recipes(url)
    for r in recipes:
        add_recipe(r, source_url=url)
        print(f"  Added recipe: {r['title']}")

def ask_question():
    """Ask a question to the RAG pipeline from terminal."""
    from rag import query_recipe
    query = input("Ask a recipe question: ")
    answer = query_recipe(query)
    print("🤖 Answer:", answer)

def run_web():
    """Run the Flask web app."""
    app.run(debug=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg.startswith("http"):  
            # Example: python main.py https://allrecipes.com/recipes
            run_scraper(arg)

        elif arg == "web":
            # Example: python main.py web
            run_web()

        elif arg == "ask":
            # Example: python main.py ask
            ask_question()
        elif arg == "initdb":
            create_db()
            print("Database initialized")

        else:
            print("   Unknown command. Use:")
            print("   python main.py <URL>   # scrape recipes")
            print("   python main.py ask     # query recipes")
            print("   python main.py web     # launch Flask app")
    else:
        print("ℹ  Usage:")
        print("   python main.py <URL>   # scrape recipes")
        print("   python main.py ask     # query recipes")
        print("   python main.py web     # launch Flask app")
