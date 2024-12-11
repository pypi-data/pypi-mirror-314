import argparse
from typing import Union
import requests
from .apis_handling import fact, animal, quote, celebrity, superhero
from .configuration import load_api_key, configure_api_key
from .constants import console
from .interactive_cli import interactive_mode
from .utils import parse_multiple_types

def main_entery():
    parser = argparse.ArgumentParser(
                        prog='fun_apis.py',
                        description='Playing with some APIs',
                        epilog='Enjoy it!',
                        allow_abbrev=False)

    parser.add_argument("-c","--config", help="Launch API configuring process.", action='store_true')
    parser.add_argument("-i","--interactive", help="Displays a random fact.", action='store_true')
    parser.add_argument("-f","--fact", help="Displays a random fact.", action='store_true')
    parser.add_argument("-a","--animal",metavar="animal_name", help="Displays animal(s) information.", nargs="+",type=str)
    parser.add_argument("-q","--quote", metavar="quote_topic" ,help="Displays a random quote.", type=str)
    parser.add_argument("-sc","--search-celebrity",metavar="celebrity_name", help="Displays a celebrity information.", nargs="+",type=str)
    parser.add_argument("-ss","--search-superhero",metavar="sup_name", help="Displays a superhero information.", nargs="+",type=parse_multiple_types)

    args = parser.parse_args()

    if args.config:
        configure_api_key() 
    if args.interactive:
        interactive_mode()
    elif args.fact:
        fact(api_key=load_api_key(which_api_key="ninjas_api_key"))  
    elif args.animal:
        animal(api_key=load_api_key(which_api_key="ninjas_api_key"),animal_name=" ".join(args.animal))
    elif args.quote:
        quote(api_key=load_api_key(which_api_key="ninjas_api_key"),category=args.quote)  
    elif args.search_celebrity :
        celebrity(api_key=load_api_key(which_api_key="ninjas_api_key"),celeb_name=" ".join(args.search_celebrity))
    elif args.search_superhero :
        reference : Union[str, int] = args.search_superhero[0]
        if isinstance(reference, str):
            superhero(api_key=load_api_key(which_api_key="superhero_api_key"),
                    superhero_id_or_name=" ".join(args.search_superhero))
        elif isinstance(reference, int):
            superhero(api_key=load_api_key(which_api_key="superhero_api_key"),
                    superhero_id_or_name=reference)

if __name__ == "__main__":
    main_entery()