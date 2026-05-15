import random
def genotp():
    otp=''
    x=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    y=[chr(i) for i in range(ord('a'),ord('z')+1)]
    z=[i for i in range(0,10)]
    for i in range(2):
        otp+=random.choice(x)+str(random.choice(z))+random.choice(y)
    return otp
# print(genotp())