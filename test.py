#!/usr/bin/python3
## coding: utf-8

import os,sys
from M_timeCov import *
from M_FTP import *
from M_libcom import *

def main():
    print(sys.argv)
    dir = "/home/beidou/Prince_study/EOP/"
    year4=2021
    doy0=220
    mjd0 = yeardoy2mjd(year4, doy0)
    mjd,hh = ftp_session(" "," ",mjd0,0,0," ")
    ii = 0
    while ii < 31:
        tmp_yyyyddd = conv_date("mjd","yyyyddd",[mjd])
        year = tmp_yyyyddd[0]
        doy = tmp_yyyyddd[1]
        os.chdir(''.join([dir,"work/%04d%03d%02d"%(year,doy,0)]))
        shutil.copyfile("poleut1_%04d%03d_%02d"%(year,doy,0),''.join([dir,"eop/","poleut1_%04d%03d_%02d"%(year,doy,0)]))
        os.chdir(dir)
        mjd,hh=ftp_session("+"," ",mjd,hh,24," ")
        ii = ii+1
    #iyear = int(sys.argv[1])
    #idoy = int(sys.argv[2])
    #iday = int(sys.argv[3])

    #gwk = int(sys.argv[1])
    #gwkd = int(sys.argv[2])
    #yr = int(sys.argv[3])
    #rapid_orbit_cmd()
    #Merge_hrnxo("/home/beidou/Prince_study/","Prince_study/test_py/",2021,317,0,0,"slist","test_py/test","ext")

    #ftp = sys.argv[1]
    #ctype = sys.argv[2]
    #ttype = sys.argv[3]

    #sfile , xfile = ftp_filename(ftp , ctype)
    #cmd= ftp_setsite(ftp , ctype)

    #print (sfile)
    #print (xfile)
    #print (cmd)
    #mjd = gwkd2mjd(gwk, gwkd)
    #iyear, idoy = mjd2yeardoy(mjd)

    #idate = [2020,2,19]

    #ctype_out = "yyyymmdd"
    #ctype = "mjd"
#
    #year, month,day = conv_date(ctype, ctype_out, [58898])
    #merge_hrnxo()
    #print (year,month,day)
    #year = get_systime("gmt")[0]
    #sys_time=get_systime("gmt")
    #year = sys_time[0]
    #string = replace_string(58898,5,30,0,'-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_MN.rnx.gz',["-SITE9-=ABMF"])
    #string = "zimm"
    #match=findstring(string.upper(),IGSnetwork)
    #print(IGSnetwork[match],"     ",match)
    #slist = " "

    slist = "/home/beidou/Prince_study/test_py/site_list"
    ##itstart = [1]
    #nses= 49
    #nses = -49
    target0=r"/home/beidou/Prince_study/test_py/FTP"
    ctype1 = "sp3m_u"
    ctype2 = "dcb_p1p2"
    ctype3 = "dcb_p2c2"
    ###ctype="rnxD_d"
    ftp = "whu_igs"
    ##flist = "all"
    #hrate=1
    #print("ign")
    #print("111")
    target = "/home/beidou/Prince_study/data/WUM_finals"
    snx = "/home/beidou/Prince_study/sys_data/igs21P2173.snx"
    #read_snx_pos("",snx)
    #fn="/home/beidou/Prince_study/test/perl/cf_gfz"
    ####flist, year0, doy0, hh0, target0, slist, ctype, ftp=ftp_getarg(slist, itstart, nses, target0, ctype, ftp, flist)
    
    #ftp_getfiles(2021,256,0,10,target,"/home/beidou/Prince_study/test/igs14core_available","rnxD_d",ftp," ",24)
    ics = "/home/beidou/Prince_study/test/python/ics_202015400"
    ftp_getfiles(2021,220,0,-3,target," ","sp3x_f","wum","WUM",24)
    file_new = "NRC100CAN_R_20213150200_01H_30S_MO.crx.gz"
    #frnx_n2o(file_new)
    #print(frnx_n2o(file_new))
    #d2o_single("/home/beidou/Prince_study/","/home/beidou/Prince_study/data/obs/zeck317n.21d.gz")
    #d2o_multi_thread("/home/beidou/Prince_study/",[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
    #cluster_to_sitelist("/home/beidou/Prince_study/input/cluster_ultra","/home/beidou/Prince_study/test/test_site")
    #get_sp3_cycle(2021,281,4,target0,ctype1,ftp,"WUM",3,1)
    #upics_time(ics,59001, 84900.00000,  59002, 84300.00000,0,0,0,0)
    #orbpred_chd("/home/beidou/Prince_study","/home/beidou/Prince_study/B1CB2a_orbfit/sc_1d_work","cf","C","file_table",59307,0,"lsq_2021091_upd.sp3",24,"c_pred_test")

    

    #read_sp3_pos("/home/beidou/Prince_study/data/products/WUM0MGXULA_20210860000_01D_05M_ORB.SP3",1)
    #ftp_getfiles(2021,240,0,nses,target,slist,ctype2,ftp," ",1)
    #ftp_getfiles(2021,240,0,nses,target,slist,ctype3,ftp," ",1)
    #ftp_getfiles(2021,240,2,-1,target0,"","finals2000A","iers"," ",0)
    #check_eop_file(fn)
    #sats=["C01","C02","C03"]
    #updctrl_time("/home/beidou/Prince_study/input/cf_gfz",2021,9,12,0,0,86400,0)
    #write_ctrlsta("/home/beidou/Prince_study/input/cf_test","/home/beidou/Prince_study/input/sl","CLK")
    #print(job_file_extension(2021,251,3,4,5))
#
    #print(monthday2gwkd(idate[0],idate[1],idate[2]))
#
    #print(get_systime(ttype))


    #mjd = yeardoy2mjd(iyear, idoy)
    #imonth,iday = doy2monthday(iyear, idoy)

    #iyear4 = set_YEAR(yr)

    #iyear2, idoy2 = mjd2yeardoy(mjd)
    #iyear3, idoy3 = mjd2ydoy(mjd)

    #iyear,idoy = monthday2doy(iyear,imonth,iday)
    #print ("year: %04d , doy: %03d"%(iyear,idoy))
    #print ("year: %04d , month: %02d , day: %02d "%(iyear,imonth,iday))
    ##print (imonth,iday)
    #print ("mjd: %d"%(mjd))
    ##print ("year2: %04d , doy2: %03d"%(iyear,idoy))
    ##print ("year3: %04d , doy3: %03d"%(iyear,idoy))
    #print ("year4: %d"%(iyear4))


if __name__ == '__main__':
    main()
