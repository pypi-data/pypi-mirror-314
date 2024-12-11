import requests
from typing import List, Dict, Optional
from ..constants import AnimalsInfo, console
from ..utils import requests_error_handler

@requests_error_handler
def fetch_animal_info(name : str, api_key : str) -> Optional[List[AnimalsInfo]]:
    api_url = f'https://api.api-ninjas.com/v1/animals?name={name}'

    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        console.print(f"[red]Error: {response.status_code} {response.text}")
        return None

def display_animal_info(animals_data: List[AnimalsInfo]) -> None:
    if not animals_data:
        return 
    for data_dict in animals_data:
        console.print("[green]\n=== Animal Information ===")
        
        console.print(f"[red]\nName:[/red] {data_dict['name']}")
        
        console.print("[cyan]\nTaxonomy:")
        for key, value in data_dict['taxonomy'].items():
            console.print(f"  [cyan i]{key.title().replace("_"," ")}:[/cyan i] {value}")
    
        console.print("[yellow]\nLocations:", ", ".join(data_dict['locations']))
        
        console.print("[blue]\nCharacteristics:")
        for key, value in data_dict['characteristics'].items():
            formatted_key = key.replace('_', ' ').title()
            console.print(f"   [red i]{formatted_key}:[/red i] [white]{value}[/white]")

def animal(api_key : str, animal_name : str = None) -> None:
    if not animal_name:
        console.print("[yellow] Please provide an animal name.")
        return
    with console.status("Looking around...", spinner="monkey"):
        display_animal_info(fetch_animal_info(animal_name, api_key))

