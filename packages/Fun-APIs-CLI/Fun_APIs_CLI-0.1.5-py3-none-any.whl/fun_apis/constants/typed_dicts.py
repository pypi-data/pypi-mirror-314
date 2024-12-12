from typing import Union, Optional, List, Dict, TypedDict

class Fact(TypedDict):
    fact: str

class Quote(TypedDict):
    quote : str
    author : str
    category : str

class AnimalsInfo(TypedDict):
    name : str
    taxonomy : Dict[str, str]
    locations : List[str]
    characteristics : Dict[str, str]

class CelebrityInfo(TypedDict):
    name : str
    net_worth : Optional[int]
    gender : Optional[str]
    nationality : Optional[str]
    occupation : Optional[List[str]]
    height : Optional[float]
    birthday : Optional[str]

class SuperHeroInfo(TypedDict):
    appearence : Dict[str, Union[str, List[str]]]
    biography : Dict[str, Union[str, List[str]]]
    connections : Dict[str,str]
    id : str
    image : Dict[str,str]
    name : str
    powerstats : Dict[str,str]
    response: str
    work : Dict[str,str]