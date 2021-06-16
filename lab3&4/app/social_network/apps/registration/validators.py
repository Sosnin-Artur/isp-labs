import re

def validate_name(name):
    return re.fullmatch(r"^[A-Za-zА-Яа-я]{2,20}$", name) != None
    
def validate_email(password):
    reg = r"[^@]+@[^@]+\.[^@]+"
    pat = re.compile(reg)
    return re.search(pat, password) != None

