import os
import json
from typing import Union, Optional, List, Dict, TypedDict
from rich.console import Console
from rich.table import Table
from platformdirs import user_config_dir

console = Console()

CONFIG_FILE_PATH : os.PathLike = os.path.join(
    user_config_dir(appname="Fun_APIs_CLI", ensure_exists=True) ,'config.json'
    )
SUPERHEROES_JSON_FILE_PATH : os.PathLike = os.path.join(
    os.path.dirname(__file__), 
        'heroes_ids_names.json'
)

valid_apis_keys = ["ninjas_api_key", "superhero_api_key"]
valid_options = valid_apis_keys.copy()
valid_options.append("all")
valid_options_string = f"{"; ".join(valid_options)}"

categories = ["age", "alone", "amazing", "anger", "architecture", "art", "attitude", "beauty", "best", "birthday", "business", "car", "change", "communication", "computers", "cool", "courage", "dad", "dating", "death", "design", "dreams", "education", "environmental", "equality", "experience", "failure", "faith", "family", "famous", "fear", "fitness", "food", "forgiveness", "freedom", "friendship", "funny", "future", "god", "good", "government", "graduation", "great", "happiness", "health", "history", "home", "hope", "humor", "imagination", "inspirational", "intelligence", "jealousy", "knowledge", "leadership", "learning", "legal", "life", "love", "marriage", "medical", "men", "mom", "money", "morning", "movies", "success"]

categories_noun = {
    "alone": "loneliness",
    "amazing": "amazement",
    "best": "excellence",
    "cool": "coolness",
    "famous": "fame",
    "funny": "humor",
    "good": "goodness",
    "great": "greatness",
    "inspirational": "inspiration",
    "legal": "legality",
    "medical": "medicine",
}

SUPERHEROES_IDS_NAMES_TABLE = Table(title="SuperHeroes IDs and Names", )
SUPERHEROES_IDS_NAMES_TABLE.add_column("[green]Names", style="red", no_wrap=True)
SUPERHEROES_IDS_NAMES_TABLE.add_column("[green]IDs", style="blue", no_wrap=True)

with open(SUPERHEROES_JSON_FILE_PATH, 'r') as ref_file:
    heroes_json : Dict = json.load(ref_file)
for Name, Id in heroes_json.items():
    SUPERHEROES_IDS_NAMES_TABLE.add_row(Name,str(Id))
