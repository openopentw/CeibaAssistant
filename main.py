import os
import sys
from helper_func import loginceiba

login_result = loginceiba.info('b07902000', '*****', '1062')
if login_result == 0:
    print('login_success, check cookie.txt!!')
else:
    print("can't login!!")


