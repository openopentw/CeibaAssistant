import os

def info(user, password, semester):
    os.system('./helper_func/loginc ' + user + ' ' + password + ' ' + semester)
