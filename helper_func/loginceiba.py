import os

def info(user, password, semester):
    ret = os.system('./helper_func/loginc ' + user + ' ' + password + ' ' + semester)
    if not ret == 0:
        return 1;
    else:
        f = open('./helper_func/cookie.txt', 'r')
        content = f.read()
        content = content.strip()
        f.close()
        return content
