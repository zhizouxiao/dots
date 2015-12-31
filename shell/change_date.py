import sys
import os
if __name__ == '__main__':
    str_date = sys.argv[1]
    if '/' not in str_date:
        print("input format error!")
    y, m, d, h, s = str_date.split("/")
    os.system("sudo date %s%s%s%s%s" % (m, d, h, s, y))


