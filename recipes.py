import requests
from bs4 import BeautifulSoup

def scrape_recipes():
    response = requests.get("https://pinchofyum.com/recipes/instant-pot")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    recipes = []
    #print(soup.text)
    for recipe_div in soup.find_all("article", class_="carousel-cell"):  # Update selectors
        title_tag = recipe_div.find("h3", class_="font-domaine")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled Recipe" 
        print(title)
        link_tag = recipe_div.find("a", href=True)
        if link_tag:
            recipe_url = link_tag["href"]
            print(recipe_url)
        img_tag = recipe_div.find("img", {"data-pin-description": True})
        if img_tag:
            description = img_tag["data-pin-description"]
            print(description)
        recipe_response = requests.get(recipe_url)
        recipe_response.raise_for_status()
        recipe_soup = BeautifulSoup(recipe_response.text, "html.parser")    
        information = recipe_soup.text

        '''ingredients_tag = recipe_div.find("ul", class_="ingredients")
        ingredients = ", ".join([li.get_text(strip=True) for li in ingredients_tag.find_all("li")]) if ingredients_tag else "N/A"

        instructions_tag = recipe_div.find("div", class_="instructions")
        instructions = instructions_tag.get_text(" ", strip=True) if instructions_tag else "N/A"

        cooking_time_tag = recipe_div.find("span", class_="cooking-time")
        cooking_time = cooking_time_tag.get_text(strip=True) if cooking_time_tag else "N/A"

        diet_tag = recipe_div.find("span", class_="diet")
        diet = diet_tag.get_text(strip=True) if diet_tag else "N/A"

        recipes.append({
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "cooking_time": cooking_time,
            "diet": diet
        })
    return recipes'''

scrape_recipes()