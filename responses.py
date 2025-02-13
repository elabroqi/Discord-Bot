from random import choice, randint


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower() # python is case sensitive, so all user input needs to be lowered

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1,6)}'
    else:
        return choice(['I dont undersetand', 'what', 'who are you'])
