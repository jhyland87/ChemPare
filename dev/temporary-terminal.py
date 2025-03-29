"""Just testing out a basic temporary terminal thingy"""

import time


print('Loading...')
time.sleep(2)
print("\033[?1049h\033[H\033[J")
time.sleep(1)
print('Hello world')
time.sleep(2)
print('Going back...')
time.sleep(2)
print("\033[?1049l")
print("Back!..")
