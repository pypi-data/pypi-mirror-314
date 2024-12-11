import time
import sys
cargs = sys.argv[1:]
def conlist(lis) :
    return "".join(lis)
def rev(txt) :
    return txt[::-1]
def oth(txt) :
    return txt[::2]
def stop() :
    sys.exit()
def loop(func) :
    while True :
        func()
def a(one) :
    if one < 0 :
        return(0 - one)
    else :
        return(one)
def rep(text, toreplace, replacewith):
    return(text.replace(toreplace, replacewith))
def p(string) :
    print(string)
def wait(tm) :
    time.sleep(tm / 1000)
