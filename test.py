#!/usr/bin/python3
## coding: utf-8

import sys
from M_timeCov import *
from M_FTP import *
from M_libcom import *

def main():
    print(sys.argv)
    
    slist = "site_list"
    year = 2021
    doy = 211
    hour = 0
    nsesh = 7
    hstep = 24
    target0=r"/data"
    ctype = "sp3m_u"
    ftp = "wum"
    ac = " "    
    ftp_getfiles(year,doy,hour,nsesh,target0,slist,ctype,ftp,ac,hstep)
    

if __name__ == '__main__':
    main()
