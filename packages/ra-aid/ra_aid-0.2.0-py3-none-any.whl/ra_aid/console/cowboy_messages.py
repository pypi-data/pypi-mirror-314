import random

COWBOY_MESSAGES = [
    "Yeeehaw! 🤠",
    "Yippee ki yay motherfucker! 🤠",
    "Saddle up partner! 🤠",
    "This ain't my first rodeo! 🤠",
    "Lock and load, partner! 🤠",
    "i'll do my best not to fuck it up 🤠",
    "I'm just a baby 👶",
    "i'll try not to destroy everything 😏"
]

def get_cowboy_message() -> str:
    """Randomly select and return a cowboy message.
    
    Returns:
        str: A randomly selected cowboy message
    """
    return random.choice(COWBOY_MESSAGES)
