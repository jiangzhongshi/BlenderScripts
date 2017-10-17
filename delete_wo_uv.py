import re

def check_uv(f):
    with open(obj) as f:
        for l in f:
            if l[0] == 'f':
                slash = l.find('/')
                if slash != -1 and l[slash+1] != '/':
                    return True # UV exists leave untouched
                else:
                    return False

if __name__ == '__main__':
    import sys, glob, os
    d = sys.argv[1]
    all_files = glob.glob(d+'/*.[Oo][Bb][Jj]')
    for obj in all_files:
        if not check_uv(obj):
            os.remove(obj)
