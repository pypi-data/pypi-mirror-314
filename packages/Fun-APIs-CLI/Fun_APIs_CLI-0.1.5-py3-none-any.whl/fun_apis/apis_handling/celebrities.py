import requests
from typing import Union, List, Dict, Optional
import pycountry
from ..constants import console, CelebrityInfo
from ..utils import requests_error_handler, meters_to_freedom_units

@requests_error_handler
def fetch_celebrity_info(api_key: str , celeb_name : str) -> Optional[List[CelebrityInfo]]:
    api_url = f'https://api.api-ninjas.com/v1/celebrity?name={celeb_name}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        console.print(f"[red]Error: {response.status_code} {response.text}")
        return None

def display_celebrity_info(celeb_info : Optional[List[CelebrityInfo]]) -> None:
    if not celeb_info:
        console.print("[red bold]No celebrity information founded.[/red bold]")
        return 

    console.print(f"Found {len(celeb_info)} results.")
    for celebrity_info in celeb_info:
        console.print("[spring_green2 bold]\n*** Celebrity Information ***\n[/spring_green2 bold]")
        
        console.print(f"[cyan]Name:[/cyan] [white]{celebrity_info['name'].title()}[/white]")

        age : Optional[int] = celebrity_info.get('age', None)
        birthday : Optional[str] = celebrity_info.get('birthday', None)
        if age and birthday:
            console.print(f"[bright_blue]Age & Birthday:[/bright_blue] [white]{age} years old[/white], [magenta]{birthday}[/magenta]")

        height : Optional[int] = celebrity_info.get('height')
        if height:
            console.print(f"[yellow]Height:[/yellow] [white]{height} m[/white] / ~ [light_slate_blue]{meters_to_freedom_units(float(height))}[/light_slate_blue]")

        gender : Optional[str] = celebrity_info.get('gender', None)
        if gender:
            console.print(f"[orange3]Gender:[/orange3] [white]{gender.capitalize()}[/white]")

        nationality : Optional[str] = celebrity_info.get('nationality', None)
        if nationality:
            country = pycountry.countries.get(alpha_2=nationality.upper()).name
            console.print(f"[green]Nationality:[/green] [white]{country}[/white]")

        net_worth : Optional[int] = celebrity_info.get('net_worth', None)
        if net_worth:
            console.print(f"[gold3]Net Worth:[/gold3] [green i]{net_worth:,} $[/green i]")

        occupation : Optional[List[str]] = celebrity_info.get('occupation', [])
        if occupation:
            formatted_occupations : str = ', '.join([occupation.capitalize().replace('_', ' ') for occupation in occupation])
            console.print(f"[purple]Occupation:[/purple] [white]{formatted_occupations}[/white]")

def celebrity(api_key: str , celeb_name : str) -> None:
    with console.status("Fetching celebrity info...", spinner="star"):
        display_celebrity_info(fetch_celebrity_info(api_key = api_key , celeb_name = celeb_name))

