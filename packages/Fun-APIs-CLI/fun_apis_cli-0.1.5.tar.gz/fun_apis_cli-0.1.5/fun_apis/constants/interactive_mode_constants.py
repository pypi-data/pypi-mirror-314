import textwrap

AVAILABLE_QUOTE_TOPICS = ['age', 'loneliness', 'amazement', 'anger', 'architecture', 'art', 'attitude', 'beauty', 'excellence', 'birthday', 'business', 'car', 'change', 'communication', 'computers', 'coolness', 'courage', 'dad', 'dating', 'death', 'design', 'dreams', 'education', 'environmental', 'equality', 'experience', 'failure', 'faith', 'family', 'fame', 'fear', 'fitness', 'food', 'forgiveness', 'freedom', 'friendship', 'humor', 'future', 'god', 'goodness', 'government', 'graduation', 'greatness', 'happiness', 'health', 'history', 'home', 'hope', 'humor', 'imagination', 'inspiration', 'intelligence', 'jealousy', 'knowledge', 'leadership', 'learning', 'legality', 'life', 'love', 'marriage', 'medicine', 'men', 'mom', 'money', 'morning', 'movies', 'success', 'random']

columns = 4
max_topic_length = max(len(topic) for topic in AVAILABLE_QUOTE_TOPICS)
formatted_topics = [
    "  ".join(
        topic.capitalize().ljust(max_topic_length) 
        for topic in AVAILABLE_QUOTE_TOPICS[i:i + columns]
    )
    for i in range(0, len(AVAILABLE_QUOTE_TOPICS), columns)
]

quote_topics = f"""
[yellow i]Available topics are:[/yellow i]
[bright_cyan bold]
{textwrap.indent("\n".join(formatted_topics), prefix="\t")}
[/bright_cyan bold]
"""

static_options = ["1", "help", "2", "configure", "clear", "3", "exit", "4"]

_available_options_paragraph = '''
    1 - help (Displays a help message)
    2 - configure (Let you configure and set up your ninjas' API keys)
    3 - clear (Clear the console's screen)
    4 - exit (Exits the script)
    5 - fact (Get you a fun fact)
    6 - animals (Let you fetch infos about a certain animal)
    7 - quote (Give you a quote about a certain topic)
    8 - celebrity (Let you search and fetch info about a celebrity)
    9 - superhero (Allow you to fetch info about superheroes from both the comic universe)
'''

welcome_message = f"""
[bold green]Hello and welcome to Fun APIs interactive mode.[/bold green] 
Here are the available options:
[white]{_available_options_paragraph}[/white]
[bold yellow]P.S:[/bold yellow] You can use the numbers (e.g: [cyan]1[/cyan] for help) or the string itself (e.g: [cyan]help[/cyan])
"""

help_message = f'''
[bold blue]Here are the available options:[/bold blue]
[white]{_available_options_paragraph}[/white]
[bold yellow]P.S:[/bold yellow] You can use the numbers (e.g: [cyan]1[/cyan] for help) or the string itself (e.g: [cyan]help[/cyan])
'''

