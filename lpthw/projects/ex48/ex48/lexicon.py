def convert_number(s):
    try:
        return int(s)

    except ValueError:
        return None


def scan(input_words):
    words = input_words.lower().split()
    output_words = []

    direction_words = ['north', 'south', 'east', 'west', 'down', 'up', 'left',
                        'right', 'back']
    verb_words = ['go', 'stop', 'eat', 'kill']
    stop_words = ['the', 'in', 'of', 'from', 'at', 'it']
    noun_words = ['door', 'bear', 'princess', 'cabinet']

    for word in words:
        if word in direction_words:
            output_words.append(('direction', word))

        elif word in verb_words:
            output_words.append(('verb', word))

        elif word in stop_words:
            output_words.append(('stop', word))

        
        else:
            output_words.append('WHOOPS!')

    return output_words
