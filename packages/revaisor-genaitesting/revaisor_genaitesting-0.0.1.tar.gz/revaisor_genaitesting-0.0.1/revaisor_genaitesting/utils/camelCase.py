import re

def camel_to_title(text):
    # Add a space before each uppercase letter, except the first one, and capitalize only the first letter
    spaced_text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
    return spaced_text.capitalize()

def title_to_camel(text):
    # Split the string into words, capitalize each word except the first, and join them
    words = text.split()
    # Convert first word to lowercase, and capitalize the rest, then join them together
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def convert_keys_to_title(d):
    # Convert the outer dictionary keys and inner dictionary keys
    new_dict = {}
    for key, value in d.items():
        # Convert the outer key
        new_key = camel_to_title(key)
        # Check if the value is a dictionary, and convert its keys if so
        if isinstance(value, dict):
            new_dict[new_key] = {camel_to_title(inner_key): inner_value for inner_key, inner_value in value.items()}
        else:
            new_dict[new_key] = value
    return new_dict
