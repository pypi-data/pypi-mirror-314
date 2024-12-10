def toman(price):
    price = round(float(str(price)))
    return f"{price:,}"


def mask(string,n=-3):
    string = str(string)
    return string[:n].ljust(len(string), '*')