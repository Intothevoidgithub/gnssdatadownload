#!/usr/bin/python3
## coding: utf-8

## purpose : function for time convertion
## created : Shichao Xie 2021.8.15
## ref     : PANDA_perl script from GFZ
## verification by http://www.gnsscalendar.com
## verification by https://webapp.geod.nrcan.gc.ca/geod/tools-outils/calendr.php?locale=en

## def_list: [doy2monthday, monthday2doy, yeardoy2mjd, monthday2mjd, monthday2gwkd, mjd2yeardoy, mjd2monthday, gwkd2mjd, mjd2gwkd, set_YEAR, conv_date, get_systime]

import time
days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

def doy2monthday(iyear,idoy):
    days_in_month[1] = 29 if (iyear%4==0 and iyear%100!=0 or iyear%400 == 0) else 28
    iday = idoy
    imonth = 0
    for imonth in range(12):
        if (iday <= days_in_month[imonth]):
            break
        iday -= days_in_month[imonth]

    imonth += 1
    return iyear,imonth, iday

def monthday2doy(iyear, imonth, iday):
    days_in_month[1] = 29 if (iyear%4==0 and iyear%100!=0 or iyear%400 == 0) else 28
    idoy = iday
    im = 0
    for im in range(imonth -1):
        idoy += days_in_month[im]
    
    return iyear, idoy

def yeardoy2mjd(iyear, idoy):
    iyear2= iyear -1
    mjd = 365*iyear- 678941 + int(iyear2/4) - int(iyear2/100) + int(iyear2/400)
    mjd += idoy
    return mjd

# there is a more elegant algorithm below
#def mjd2yeardoy(mjd):
#    iyear = int((mjd+678940)/365.25+0.1)+1
#    idoy = 0
#    while True:
#        iyear -= 1
#        idoy = mjd - yeardoy2mjd(iyear,1) + 1
#        if idoy > 0:
#            break
#    return iyear,idoy


##############################################
##-------------------------------------------
## 年月日转为约化儒略日，没有考虑小时和分钟
##
## input:
##      year    4-digit        
##      mon     2-digit
##      day     2-digit
##
## return:
##      mjd     (int)
## ref:
#       李征航.GPS测量数据处理 P29 公式2    
##--------------------------------------------
def monthday2mjd(year,mon,day):
    if mon<=2:
        mon=mon+12
        year=year-1
    mjd=int(365.25*year)+int(30.6001*(mon+1))+day+1720981.5-2400000.5
    return int(mjd)

##-------------------------------------------
## 年月日转为GPS周和周内天，没有考虑小时和分钟
##
## input:
##      year    4-digit        
##      mon     2-digit
##      day     2-digit
##
## return:
##      week     (int)
##      dow      (int)
## ref:
#       none     
##--------------------------------------------
def monthday2gwkd(year,mon,day):
    GPS_year=1980
    GPS_mon=1
    GPS_day=6
    GPS_mjd=monthday2mjd(GPS_year,GPS_mon,GPS_day)
    cur_mjd=monthday2mjd(year,mon,day)
    dmjd=cur_mjd-GPS_mjd
    week=int(dmjd/7)
    dow=dmjd%7
    return week,dow

##-------------------------------------------
## 约化儒略日转换为年、年积日，没有考虑小时和分钟
##
## input:
##      mjd      (int)        

##
## return:
##      year     (int)
##      doy      (int)
## ref:
#       李征航.GPS测量数据处理 P29     
##--------------------------------------------
def mjd2yeardoy(mjd):
    jd=mjd+2400000.5
    a=int(jd+0.5)
    b=a+1537
    c=int((b-122.1)/365.25)
    d=int(365.25*c)
    e=int((b-d)/30.600)
    month=e-1-12*int(e/14)
    year=c-4715-int((7+month)/10)
    mjd0=monthday2mjd(year,1,1)
    doy=mjd-mjd0+1
    return year,doy

##-------------------------------------------
## 约化儒略日转换为年、月、日，没有考虑小时和分钟
##
## input:
##      mjd      (int)        

##
## return:
##      year     (int)
##      mon      (int)
##      day      (int)
## ref:
#       李征航.GPS测量数据处理 P29     
##--------------------------------------------
def mjd2monthday(mjd):
    jd=mjd+2400000.5
    a=int(jd+0.5)
    b=a+1537
    c=int((b-122.1)/365.25)
    d=int(365.25*c)
    e=int((b-d)/30.600)
    day=b-d-int(30.6001*e)+0
    month=e-1-12*int(e/14)
    year=c-4715-int((7+month)/10)  
    return year,month,day

def gwkd2mjd(gwk,gwkd):
    mjd = gwk*7 + gwkd + 44244
    return mjd

def mjd2gwkd(mjd):
    gwk = int((mjd-44244)/7)
    gwkd = mjd -44244 - gwk * 7
    return gwk , gwkd

def set_YEAR(yr):
    if yr > 100 :
        iyear = yr
    else: 
        iyear = yr + 1900 if yr >= 70 else yr + 2000
    return iyear 

## convert date type 
## input:
##      ctype      (string)
##      ctype_out  (string)
##      idate      (list(int)) 

def conv_date(ctype, ctype_out, idate):
    mjd = 0
    if (ctype == "yyyyddd"):
        mjd = yeardoy2mjd(idate[0],idate[1])
    elif (ctype == "yyddd"):
        idate[0] = set_YEAR(idate[0])
        mjd = yeardoy2mjd(idate[0],idate[1])
    elif (ctype == "yyyymmdd"):
        mjd = monthday2mjd(idate[0],idate[1],idate[2])
    elif (ctype == "yymmdd"):
        idate[0] = set_YEAR(idate[0])
        mjd = monthday2mjd(idate[0],idate[1],idate[2])    
    elif (ctype == "mjd"):
        mjd = idate[0]
    elif (ctype == "wwwwd"):
        mjd = gwkd2mjd(idate[0],idate[1])    
    else :
        print ("Unkown input date type : %s\n"%(ctype))
        return 0

    out = []
    if(ctype_out == "yyyyddd"):
        out = list(mjd2yeardoy(mjd))
    elif (ctype_out == "yyyymmdd" ):
        iyear, doy =mjd2yeardoy(mjd)
        out = list(doy2monthday(iyear,doy))
    elif (ctype_out == "mjd"):
        out.append(mjd)
    elif (ctype_out == "wwwwd"):
        out = list(mjd2gwkd(mjd))
    else:
        print ("Unkown out date type : %s\n"%(ctype_out))
        return 0
    return out

def get_systime(ctype):
    if (ctype == "gmt"):
        t=time.gmtime()
    else:
        t=time.localtime()
    iyear=t.tm_year
    imonth=t.tm_mon
    imday=t.tm_mday
    ihour=t.tm_hour
    imin=t.tm_min
    isec=t.tm_sec
    #iwday=t.tm_wday
    iyday=t.tm_yday
    #isdst=t.tm_isdst

    fday = ihour/24.0+imin/1440.0+isec/86400.0
    mjd = yeardoy2mjd(iyear,iyday)
    string = "%04d%03d_%02d%02d%02d"%(iyear,iyday,ihour,imin,isec)
    return iyear, iyday, fday, string, imonth, imday, ihour, imin, isec, mjd

