import json
import random
from typing import Union, List, TypedDict, Optional
import requests
from ..constants import console, categories, categories_noun, Quote
from ..utils import requests_error_handler

@requests_error_handler
def fetch_quote(api_key : str , category : Optional[str] = None) -> Optional[List[Quote]]:
    if not category or category == "random":
        category = random.choice(categories)
    else:
        category = {v: k for k, v in categories_noun.items()}.get(category.lower(), category.lower())
        if category not in categories:
            console.print(f"[red]Invalid category '{category}'. Falling back to random choice![/red]")
            category = random.choice(categories)
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'

    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        console.print(f"[red]Error: {response.status_code} {response.text}")
        return None

def display_quote(quote : Union[List[Quote], int]) -> None:
    if not quote:
        return 
    quote = quote[0]
    topic = categories_noun.get(quote['category'],quote['category']).capitalize()
    console.print(f'''
    [green bold]"{quote['quote']}"[/green bold]
    said by [cyan i]{quote['author']}[/cyan i] about [red]{topic}[/red]
    ''')

def quote(api_key : str , category : Optional[str] = None) -> None:
    with console.status("Fetching a quote...", spinner="earth"):
        display_quote(quote=fetch_quote(api_key,category))

