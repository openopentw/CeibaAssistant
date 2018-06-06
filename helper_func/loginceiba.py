import os

def info(user, password, semester):
    return os.system('./helper_func/loginc ' + user + ' ' + password + ' ' + semester)
