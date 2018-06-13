import os
import sys
from helper_func import loginceiba

cookie = loginceiba.info('b07902000', '*****', '1062')
if cookie == 1:
    print("can't login!!")
else:
    print('login_success, cookie:')
    print(cookie)


