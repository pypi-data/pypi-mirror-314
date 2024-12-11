import os
from ..apis_handling import fact, animal, quote, celebrity, superhero
from ..configuration import load_api_key, configure_api_key
from ..constants import welcome_message, quote_topics, help_message, console, static_options, AVAILABLE_QUOTE_TOPICS
from ..utils import cli_errors_handler, clear_screen
from prompt_toolkit import prompt, HTML
from prompt_toolkit.completion import WordCompleter

def display_help_message() -> None:
    console.print(f"[green]{help_message}")

def exit_script() -> None:
    console.print("[bright_yellow]Have a good day!")
    exit()

def invalid_option(option : str) -> None:
    if option.strip() == "":
        console.print(f"[orange_red1]Input cannot be empty, run 'help' to check the available commands.")
    else:
        console.print(f"[orange_red1]{option} is invalid, run 'help' to check the available commands.")

@cli_errors_handler
def prompt_animal(api_key : str) -> None:
    animal_name = prompt(HTML("<ansibrightblue>Which Animal are you looking for?</ansibrightblue> "))
    animal(api_key , animal_name)

@cli_errors_handler
def prompt_quote(api_key : str) -> None:
    console.print(quote_topics)
    quote_prompt_completer = WordCompleter(AVAILABLE_QUOTE_TOPICS, ignore_case=True)
    quote_category = prompt(HTML("<ansimagenta>You want a quote about what ?</ansimagenta> <i><ansiblue>[Leave blank for a random topic]</ansiblue></i> "), completer=quote_prompt_completer)
    quote(api_key,quote_category)

@cli_errors_handler
def prompt_celebrity(api_key : str) -> None:
    celebrity_name = prompt(HTML("<ansimagenta>Who are you looking for ?</ansimagenta> "))
    celebrity(api_key, celebrity_name)

@cli_errors_handler
def prompt_superhero(api_key : str) -> None:
    superhero_id_or_name = prompt(HTML("<ansimagenta>Which sup are looking for ?</ansimagenta> "))
    superhero(api_key, superhero_id_or_name)

options = {
    "1" : display_help_message,
    "help" : display_help_message,
    "2" : configure_api_key,
    "configure" : configure_api_key,
    "3" : clear_screen,
    "clear" : clear_screen,
    "4" : exit_script,
    "exit" : exit_script,
    # STATIC OPTIONS |^|
    "5" : fact,
    "fact" : fact,
    "6" : prompt_animal,
    "animal" : prompt_animal,
    "7" : prompt_quote,
    "quote" : prompt_quote,
    "8" : prompt_celebrity,
    "celebrity" : prompt_celebrity,
    "9" : prompt_superhero,
    "superhero" : prompt_superhero
}

def launch_interactive(option : str) -> None:
    choice = options.get(option.strip().lower(), None)
    if not choice:
        invalid_option(option)
    elif option.lower().strip() in static_options:
        choice()
    else:
        if option.lower().strip() in list(options.keys())[8:16]:
            api_key = load_api_key(which_api_key="ninjas_api_key")
            if choice is fact:
                choice(api_key)
            else:
                choice(api_key=api_key) 
        elif option.lower().strip() in ["9","superhero"]:
            api_key = load_api_key(which_api_key="superhero_api_key")
            choice(api_key)

@cli_errors_handler
def interactive_mode() -> None:
    console.print(f"[green bold]{welcome_message}[/green bold]")
    while True:
        cli_prompt_completer = WordCompleter(list(options.keys()))
        option = prompt(HTML(f"<ansibrightcyan>What would you like to do? Select an option by its <u>number</u> or <u>name</u>: </ansibrightcyan>"), completer=cli_prompt_completer) 
        launch_interactive(option)
