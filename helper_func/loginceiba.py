import os

def info(user, password, semester):
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    ret = os.system('cd \'{}\' && '.format(root_dir) + './helper_func/loginc ' + user + ' ' + password + ' ' + semester)
    if not ret == 0:
        return 1;
    else:
        cookie = os.path.join(os.path.dirname(__file__), 'cookie.txt')
        f = open(cookie, 'r')
        content = f.read()
        content = content.strip()
        f.close()
        return content
