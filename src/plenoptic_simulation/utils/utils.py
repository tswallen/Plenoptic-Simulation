def str_to_float(string: str) -> float:
    '''Turns a number string into a float'''
    string = string.strip()
    if not len(string):
        return 0.0
    return float(string)
