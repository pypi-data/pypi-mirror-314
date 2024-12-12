from typing import Union, Optional, Dict, List
import json
import requests
from ..constants import console, SuperHeroInfo
from ..utils import requests_error_handler, verify_superhero, create_powerstats_barplot

@requests_error_handler
def fetch_superhero_info(api_key : str , superhero_id_or_name : Union[int, str]) -> Optional[SuperHeroInfo] :
    is_valid_arg, superhero_id = verify_superhero(superhero_id_or_name)
    if is_valid_arg:
        api_url = f"https://superheroapi.com/api/{api_key}/{superhero_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            json_response : Optional[SuperHeroInfo] = response.json()
            if json_response.get('response') == 'error' and json_response.get('error') == 'access denied':
                console.print(f"[red]Access denied. Please check your API key.[/red]")
                return None

            return json_response
        else:
            console.print(f"[red]Failed to fetch superhero info. HTTP Status: {response.status_code}")
            return None
    else:
        console.print(f"[yellow]Invalid superhero identifier: {superhero_id_or_name}")
        return None

def display_superhero_info(superhero_info: Optional[Dict[str, Union[str, Dict]]]) -> None:
    if not superhero_info:
        return 
    superhero_name : str = superhero_info['name']
    console.print(f"[bold green underline]Superhero Name:[/bold green underline] [white]{superhero_name}[/white]")
    console.print("[bright_yellow i]'-' refers to Unknown or None ")
    # Appearance Section
    appearance_section: Dict[str, Union[str, list]] = superhero_info['appearance']
    eye_color: str = appearance_section['eye-color'].title()
    gender: str = appearance_section['gender']
    hair_color: str = appearance_section['hair-color'].title()
    height_us, height_metric = appearance_section['height'][0], appearance_section['height'][1]
    race = appearance_section['race']
    weight_us, weight_metric = appearance_section['weight'][0], appearance_section['weight'][1]

    console.print(f'''[bold blue]Appearance:[/bold blue]
    [italic yellow]Eye Color:[/italic yellow] [white]{eye_color}[/white]
    [italic yellow]Gender:[/italic yellow] [white]{gender}[/white]
    [italic yellow]Hair Color:[/italic yellow] [white]{hair_color}[/white]
    [italic yellow]Height:[/italic yellow] [white]{height_us} / {height_metric}[/white]
    [italic yellow]Race:[/italic yellow] [white]{race}[/white]
    [italic yellow]Weight:[/italic yellow] [white]{weight_us} / {weight_metric}[/white]
    ''')

    # Biography Section
    biography_section: Dict[str, Union[str, list]] = superhero_info['biography']
    full_name: str = biography_section['full-name']
    birthplace: str = biography_section['place-of-birth']
    personas: str = ", ".join(biography_section['aliases'])
    alternate_personas: str = biography_section['alter-egos']
    side: str = biography_section['alignment']
    universe: str = biography_section['publisher']
    first_appearance: str = biography_section['first-appearance']
    work_info: Dict[str, str] = superhero_info['work']
    work_bases: str = work_info['base']
    occupation: str = work_info['occupation']

    console.print(f'''[bold magenta]Biography:[/bold magenta]
    [italic cyan]Full Name:[/italic cyan] [white]{full_name}[/white]
    [italic cyan]Birthplace:[/italic cyan] [white]{birthplace}[/white]
    [italic cyan]Occupation:[/italic cyan] [white]{occupation}[/white]
    [italic cyan]Work Bases:[/italic cyan] [white]{work_bases}[/white]
    [italic cyan]Personas:[/italic cyan] [white]{personas}[/white]
    [italic cyan]Alternate personas:[/italic cyan] [white]{alternate_personas}[/white]
    [italic cyan]Side:[/italic cyan] [white]{side.title()}[/white]
    [italic cyan]Universe:[/italic cyan] [white]{universe}[/white]
    [italic cyan]First Appearance:[/italic cyan] [white]{first_appearance}[/white]
    ''')

    # Powerstats Section
    powerstats_section: Dict[str, str] = {power:(int(stat) if stat != 'null' else 0) for power,stat in superhero_info['powerstats'].items()}
    combat: int = powerstats_section['combat']
    intelligence: int = powerstats_section['intelligence']
    power: int = powerstats_section['power']
    speed: int = powerstats_section['speed']
    strength: int = powerstats_section['strength']
    overall: float = (combat + intelligence + power + speed + strength) / 5

    console.print(f'''[bold red]Powerstats:[/bold red]
    [italic green]Combat:[/italic green] [white]{combat}[/white]
    [italic green]Intelligence:[/italic green] [white]{intelligence}[/white]
    [italic green]Power:[/italic green] [white]{power}[/white]
    [italic green]Speed:[/italic green] [white]{speed}[/white]
    [italic green]Strength:[/italic green] [white]{strength}[/white]
    [italic green]Overall:[/italic green] [white]{overall:.2f}[/white]
    ''')
    create_powerstats_barplot(combat, intelligence, power, speed, strength,superhero_name)

    # Connections Section
    connections_section: Dict[str, str] = superhero_info['connections']
    alliances: str = connections_section['group-affiliation']
    relatives: str = connections_section['relatives']

    console.print(f'''\n[bold yellow]Connections:[/bold yellow]
    [italic blue]Alliances:[/italic blue] [white]{alliances}[/white]
    [italic blue]Relatives:[/italic blue] [white]{relatives}[/white]
    ''')

def superhero(api_key : str , superhero_id_or_name : Union[int, str]) -> None:
    display_superhero_info(fetch_superhero_info(api_key, superhero_id_or_name))