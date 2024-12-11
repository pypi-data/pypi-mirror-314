import os
import json
from json import JSONDecodeError
from functools import wraps
from typing import Callable, Union, Any, Optional
from requests import ConnectionError
from ..constants import console, SUPERHEROES_JSON_FILE_PATH
import plotext as plt

def requests_error_handler(func: Callable[..., Any]) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            console.print("[red]No internet connection! Please check your network and try again.[/red]")
            return None
        except Exception as error:
            console.print(f"[red]An error has occured:[/red]\n{error}")
            return None
    return wrapper

def cli_errors_handler(func: Callable[..., Any]) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except (EOFError, KeyboardInterrupt):
            print("Exiting...")
            exit("Have a good day!")
    return wrapper

def meters_to_freedom_units(meters : Union[int, float]) -> str:
    total_feet = meters * 3.28084  
    feet = int(total_feet)         
    inches = (total_feet - feet) * 12  
    return f"{feet}'{round(inches)}\""

def verify_superhero (superhero_id_or_name : Union[int, str]):
    try:
        with open(SUPERHEROES_JSON_FILE_PATH, "r") as ref_file:
            ref = json.load(ref_file)

        if isinstance(superhero_id_or_name,int) and superhero_id_or_name in ref.values():
            return True, superhero_id_or_name
        elif isinstance(superhero_id_or_name, str) and superhero_id_or_name.title() in ref.keys():
            return True, ref.get(superhero_id_or_name.title())
        else:
            return False, None
    except JSONDecodeError as err:
        console.print(f"[red]Broken or invalid JSON file:\"{SUPERHEROES_JSON_FILE_PATH}\"\n{err}")
        return False, None

def clear_screen() -> None:
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def create_powerstats_barplot(combat : int, intelligence: int, power: int, speed: int, strength: int, sup_name : str) -> None:
    powerstats = ["Combat", "Intelligence", "Power", "Speed", "Strength"]
    powerstats_percentages = [combat, intelligence, power, speed, strength]
    plt.simple_bar(powerstats, powerstats_percentages, width = 50,color="green", title = plt.colorize(f'{sup_name} Powerstats Chart', "magenta"))
    plt.show()

# A function for fun_apis.py
def parse_multiple_types(value):
    try:
        return int(value)
    except ValueError:
        return value

