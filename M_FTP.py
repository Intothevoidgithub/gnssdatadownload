#!/usr/bin/python3
## coding: utf-8

## purpose : FTP sites address and data type and some functions
## created : Shichao Xie 2021.8.15
## ref     : PANDA_perl script from GFZ

## const_list : [cmd_wget, decompress]
## def_list: [ftp_filename, ftp_setsite, ftp_session,ftp_getarg,ftp_getfiles]
## file_download will use the command 'wget'

## download ftp sites: 
#                      wum     : ftp://igs.gnsswhu.cn # wuhan university's igs datacenter
#                                MGEX_obs, MGEX_nav, MGEX_products, igs_products (no atx avalible)
#                                MGEX ACs center: CODE-COD WHUHAN-WUM GFZ-GFZ CNES-GRG IAC-IAC SHAO-SHA JAXA-JAX 
#                      igs     : ftp://igs.org  # only atx file # not use 
#                      kasi    : ftp://nfs.kasi.re.kr #korea  #hourly data is a little slow
#                                MGEX_obs, MGEX_nav, igs_products (no atx avalible)
#                      code    : ftp://ftp.aiub.unibe.ch
#                                code products: erp, clk, eph(orb), ion, DCB, snx
#                      usno    : ftp://maia.usno.navy.mil
#                                finals2000 file (poleut file)
#                      iers    : https://datacenter.iers.org
#                                finals2000 file (poleut file)
#                      cddis   : ftps://gdc.cddis.eosdis.nasa.gov # current cannot connect :2021/8/31
#                                MGEX_obs, MGEX_nav, MGEX_products, igs_products,
#                      peter   : ftp://ftp.lrz.de  # different to connect : 2021/8/31
#                                merged brdm file
#                      gfz     : ftp://ftp.gfz-potsdam.de
#                                gfz products: orb, clk, snx, erp etc.
#                      ign     : ftp://igs.ign.fr
#                                MGEX_obs, MGEX_nav, atx file
#                      ign_igs : ftp://igs.ensg.ign.fr #backup site for ign, different to connect
#                                MGEX_obs, MGEX_nav, atx file
#                      bkg     : ftp://igs.bkg.bund.de # currently only hourly file
#                                MGEX_obs, MGEX_nav,
#

from M_libcom import *
from M_ftp_ftplib import ftp_down
#import re,os
#from M_timeCov import *

cmd_wget = r"wget -T 30 -t 10 -c -nH -nc -nv " # -nc : --no-clobber skip downloads that would download to existing files (overwriting them)
#cmd_wget = r"wget -T 100 -t 10 -c -nH -N " # -N  : --timestamping  don't re-retrieve files unless newer than local

decompress="gzip -d "

def ftp_filename(ftp, ctype):
    dict1 = {}
    if ftp == "code" :
        dict1 = { 
            'eph_f' : 'COD-WWWW--D-.EPH.Z',         'clk_f' : 'COD-WWWW--D-.CLK.Z', 
            'erp_f' : 'COD-WWWW--D-.ERP.Z',         'clk_f_30s'  :'COD-WWWW--D-.CLK_30S.Z', 
            'clk_f_05s'  :'COD-WWWW--D-.CLK_05S.Z', 'snx_f'      : 'COD-WWWW-7.SNX.Z', 
            'ion_f'      : 'COD-WWWW--D-.ION.Z',    'dcb_p1c1' :'P1C1-YY--MM-.DCB.Z', 
            'dcb_p1p2' :'P1P2-YY--MM-.DCB.Z',       'dcb_p2c2' :'P2C2-YY--MM-_RINEX.DCB.Z', 
            'dcb_c1c2' :'C1C2-YY--MM-.DCB.Z',
            'eph_u'    : 'COD.EPH_U.Z',             'erp_u'    : 'COD.ERP_U.Z'
        }
    elif ftp == "usno" :
        dict1 = {
            'finals2000A' : 'finals2000A.data',     'finals2000B' : 'finals2000B.data'
        }
    elif ftp == "iers" :
        dict1 = {
            'finals2000A' : 'finals2000A.data'
        }
    elif ftp == "cddis_eop" :
        dict1 = {
            'finals2000A' : 'finals2000A.data'
        }
    elif ftp == "peter" :
        dict1 = {
            'rnxp_h' : 'brdm-DDD-z.-YY-p.Z',         'rnxx_h' : 'brdm-DDD-z.-YY-x.Z'
        }
    #elif ftp == "igs" :
    #    dict1 = {
    #        'atx' : 'igs-YY-.atx'
    #    }
    elif ftp == "gfz" :
        dict1 = {
            'sp3_f'     : 'gfz-WWWW--D-.sp3.Z',       'clk_f'    : 'gfz-WWWW--D-.clk.Z', 
            'clk_f_30s' : 'gfz-WWWW--D-.clk.Z',       'clk_f_05s': 'gfz-WWWW--D-.clk.Z', 
            'snx_f'     : 'gfz-WWWW--D-.rnx.Z',       'erp_f'    : 'gfr-WWWW--D-.erp.Z', 
            'sp3_r'     : 'gfr-WWWW--D-.sp3.Z',       'clk_r'    : 'gfr-WWWW--D-.clk.Z',
            'sp3_u'     : 'gfu-WWWW--D-_-HH-.sp3.Z',  'erp_u'    : 'gfu-WWWW--D-_-HH-.erp.Z',
            'sp3x_u'    : 'gbu-WWWW--D-_-HH-.sp3.Z',  'erpx_u'   : 'gbu-WWWW--D-_-HH-.erp.Z',
            'sp3x_r'    : 'gbm-WWWW--D-.sp3.Z',       'erpx_r'   : 'gbm-WWWW--D-.erp.Z',
            'clkx_r'    : 'gbm-WWWW--D-.clk.Z',       
            'sp3m_r'    : 'GBM0MGXRAP_-YYYY--DDD-0000_01D_??M_ORB.SP3.gz',
            'erpm_r'    : 'GBM0MGXRAP_-YYYY--DDD-0000_01D_01D_ERP.ERP.gz',
            'clkm_r'    : 'GBM0MGXRAP_-YYYY--DDD-0000_01D_??M_CLK.CLK.gz', 
            'clkm_r_30s': 'GBM0MGXRAP_-YYYY--DDD-0000_01D_30S_CLK.CLK.gz'            
        }
    elif (ftp == "cddis" or ftp == "cddis_mgex" or ftp == "ign" or ftp == "ign_igs" or ftp == "ign_mgex" or ftp == "bkg" or ftp == "ndt" or ftp == "nts" or ftp == "whu" or ftp == "wum" or ftp == "kasi" or ftp == "whu_igs") :
        dict1_1 = {}
        dict1_2 = {}
        dict1_1 = {
            'sp3_f'    : 'igs-WWWW--D-.sp3.Z',       'clk_f'    : 'igs-WWWW--D-.clk.Z',
            'clk_f_30s': 'igs-WWWW--D-.clk_30s.Z',   'clk_f_05s': 'igs-WWWW--D-.clk_05s.Z',
            'sp3_r'    : 'igr-WWWW--D-.sp3.Z',       'clk_r'    : 'igr-WWWW--D-.clk.Z',
            'erp_f'    : 'igs-WWWW--D-.erp.Z',       'sp3_u'    : 'igu-WWWW--D-_-HH-.sp3.Z', 
            'erp_u'    : 'igu-WWWW--D-_-HH-.erp.Z',  'snx_f'    : 'igs-YY-P-WWWW-.snx.Z',
            'atx'      : 'igs-YY-.atx',            
            'rnxd_d': '-SITE--DDD-0.-YY-d.gz',       'rnxo_d': '-SITE--DDD-0.-YY-o.gz',
            'rnxp_d': 'brdm-DDD-0.-YY-p.gz',         'rnxl_d': '-SITE--DDD-0.-YY-l.gz',
            'rnxq_d': '-SITE--DDD-0.-YY-q.gz',                 
            'rnxO_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_01D_30S_MO.rnx.gz',
            'rnxD_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_01D_30S_MO.crx.gz', 
            'rnxP_d': '-SITE9-_?_-YYYY--DDD--HH--MI-_01D_MN.rnx.gz', 
            'rnxF_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_01D_CN.rnx.gz', 
            'rnxL_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_01D_EN.rnx.gz', 
            'rnxG_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_01D_RN.rnx.gz', 
            'rnxN_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_01D_GN.rnx.gz', 

            'rnxd_h': '-SITE--DDD--H-.-YY-d.gz',     
            'rnxl_h': '-SITE--DDD--H-.-YY-l.gz',    'rnxf_h': '-SITE--DDD--H-.-YY-f.gz',
            'rnxq_h': '-SITE--DDD--H-.-YY-q.gz',    'rnxp_h': '-SITE--DDD--H-.-YY-p.gz',            
            'rnxd_r': '-SITE--DDD--H--QQ-.-YY-d.gz', 'rnxn_r': '-SITE--DDD--H--QQ-.-YY-n.gz', 
            'rnxg_r': '-SITE--DDD--H--QQ-.-YY-g.gz', 'rnxp_r': '-SITE--DDD--H--QQ-.-YY-p.gz',
            'rnxl_r': '-SITE--DDD--H--QQ-.-YY-l.gz', 'rnxq_r': '-SITE--DDD--H--QQ-.-YY-q.gz', 
            'rnxD_r': '-SITE9-_?_-YYYY--DDD--HH--MI-_15M_01S_MO.crx.gz',           
            'rnxO_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_30S_MO.rnx.gz', 
            'rnxD_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_30S_MO.crx.gz', 
            'rnxN_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_GN.rnx.gz',    
            'rnxG_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_RN.rnx.gz',    
            'rnxL_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_EN.rnx.gz', 
            'rnxF_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_CN.rnx.gz', 
            'rnxP_h': '-SITE9-_R_-YYYY--DDD--HH--MI-_01H_MN.rnx.gz',
            'rnxN_r': '-SITE9-_?_-YYYY--DDD--HH--MI-_15M_GN.rnx.gz',
            'rnxG_r': '-SITE9-_?_-YYYY--DDD--HH--MI-_15M_RN.rnx.gz',
            'rnxL_r': '-SITE9-_?_-YYYY--DDD--HH--MI-_15M_EN.rnx.gz',
            'rnxF_r': '-SITE9-_?_-YYYY--DDD--HH--MI-_15M_CN.rnx.gz',
            'rnxP_r': '-SITE9-_?_-YYYY--DDD--HH--MI-_15M_MN.rnx.gz',           
        }
        if (ftp == "cddis" or ftp == "ign" or ftp == "kasi" or ftp == "ign_igs"):
            dict1_2 = {
                'rnxn_d': 'brdc-DDD-0.-YY-n.gz',         'rnxg_d': 'brdc-DDD-0.-YY-g.gz', 
                'rnxp_d': '-SITE--DDD-0.-YY-p.gz',       
                'rnxn_h': '-SITE--DDD--H-.-YY-n.gz',         'rnxg_h': '-SITE--DDD--H-.-YY-g.gz',         
                'rnxl_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_EN.rnx.gz',
                'rnxf_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_CN.rnx.gz',
                #'rnxg_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_RN.rnx.gz',
                #'rnxn_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_GN.rnx.gz',
                'rnxp_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_MN.rnx.gz'
            }
        elif (ftp == "cddis_mgex" or ftp == "ign_mgex"):
            dict1_2 = {
                'rnxn_d': '-SITE--DDD-0.-YY-n.gz',      'rnxg_d': '-SITE--DDD-0.-YY-g.gz', 
                'rnxn_h': '-SITE--DDD--H-.-YY-n.gz',    'rnxg_h': '-SITE--DDD--H-.-YY-g.gz'
            }
        elif ( ftp == "wum"  or ftp == "whu_igs"):
            dict1_2 = {
                'rnxn_d': 'brdc-DDD-0.-YY-n.gz',         'rnxg_d': 'brdc-DDD-0.-YY-g.gz', 
                'rnxp_d': '-SITE--DDD-0.-YY-p.gz',       
                'rnxn_h': '-SITE--DDD--H-.-YY-n.gz',         'rnxg_h': '-SITE--DDD--H-.-YY-g.gz',         
                #'rnxl_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_EN.rnx.gz',
                #'rnxf_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_CN.rnx.gz',
                #'rnxg_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_RN.rnx.gz',
                #'rnxn_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_GN.rnx.gz',
                #'rnxp_d': '-SITE9-_R_-YYYY--DDD--HH--MI-_0DH_MN.rnx.gz',
                'sp3x_f': '-ACS-0MGXFIN_-YYYY--DDD-0000_01D_??M_ORB.SP3.gz',
                'sp3x_r': '-ACS-0MGXRAP_-YYYY--DDD-0000_01D_??M_ORB.SP3.gz',
                'sp3x_u': '-ACS-0MGXULA_-YYYY--DDD--HH-00_01D_??M_ORB.SP3.gz',
                'clkx_f_30s': '-ACS-0MGXFIN_-YYYY--DDD-0000_01D_30S_CLK.CLK.gz',
                'clkx_f': '-ACS-0MGXFIN_-YYYY--DDD-0000_01D_05M_CLK.CLK.gz',
                'clkx_r': '-ACS-0MGXRAP_-YYYY--DDD-0000_01D_05M_CLK.CLK.gz',
                'sp3m_f': '-ACS-0MGXFIN_-YYYY--DDD-0000_01D_??M_ORB.SP3.gz',
                'sp3m_r': '-ACS-0MGXRAP_-YYYY--DDD-0000_01D_??M_ORB.SP3.gz',
                'sp3m_u': '-ACS-0MGXULA_-YYYY--DDD--HH-00_01D_??M_ORB.SP3.gz',
                'clkm_f_30s': '-ACS-0MGXFIN_-YYYY--DDD-0000_01D_30S_CLK.CLK.gz',
                'clkm_f': '-ACS-0MGXFIN_-YYYY--DDD-0000_01D_05M_CLK.CLK.gz',
                'clkm_r': '-ACS-0MGXRAP_-YYYY--DDD-0000_01D_05M_CLK.CLK.gz'
            }
        dict1 = dict( dict1_1, **dict1_2 )  #merge two dict
    else :
        print ("Unknown ftp site : %s\n"%(ftp))
        exit()
    sfile =""
    xfile =""

    if (ctype in dict1) :  #whether key "ctype" inside dict1
        sfile = dict1[ctype]
        xfile = re.sub("-SITE9-", "?????????",sfile, count=0,flags=0)
        xfile = re.sub("-SITE-", "????",xfile, count=0,flags=0)
        xfile = re.sub("-QQ-", "??",xfile, count=0,flags=0)
        xfile = re.sub("-MI-", "??",xfile, count=0,flags=0)
    else :
        print (" data type not found %s, %s \n"%(ctype,ftp))
        exit()
    
    return sfile,xfile

def ftp_setsite(ftp, ctype):
## represent password
    email = r"wonderwall@chd.edu.cn"

    user = ""
    keyword = ""
    cmd_url = ""
    ftpsite = ""
    sdir = ""
    sfile = ""
    xfile = ""
## ftp username
    user = r"anonymous"
    keyword = email    

    if ftp == "code":
        ftpsite = r"ftp://ftp.aiub.unibe.ch"
        sdir = r"/CODE/-YYYY-/"
        sfile, xfile = ftp_filename(ftp, ctype)
    elif ftp == "usno":
        ftpsite = r"ftp://maia.usno.navy.mil"
        if ctype.find("finals2000A",0,11) != -1:
            sdir = r"/ser7/"
        sfile, xfile = ftp_filename(ftp, ctype)
    elif ftp == "iers":
        ftpsite = r"https://datacenter.iers.org"
        if ctype.find("finals2000A",0,11) != -1:
            sdir = r"/products/eop/rapid/standard/"
        sfile, xfile = ftp_filename(ftp, ctype)
    elif ftp == "cddis_eop":
        ftpsite = r"ftps://gdc.cddis.eosdis.nasa.gov"
        if ctype.find("finals2000A",0,11) != -1:
            sdir = r"/pub/products/iers/"
        sfile, xfile = ftp_filename(ftp, ctype)    
    elif ftp == "peter":
        ftpsite = r"ftp://ftp.lrz.de"
        sdir = r"/transfer/steigenb/brdm/"
        sfile, xfile = ftp_filename(ftp, ctype)  
    elif ftp == "gfz":
        ftpsite = r"ftp://ftp.gfz-potsdam.de"
        if ctype.find("sp3_u",0,5) != -1:
            sdir = r"/pub/GNSS/products/ultra/w-WWWW-/"
        elif re.match(r"(sp3_r|erp_r|clk_r)" , ctype) :
            sdir = r"/pub/GNSS/products/rapid/w-WWWW-/"
        elif re.match(r"(sp3_f|clk_f|erp_f)" , ctype) :
            sdir = r"/pub/GNSS/products/final/w-WWWW-/"
        elif re.match(r"(sp3x_u|sp3x_r|erpx_u|erpx_r|clkx_r|sp3m_r|clkm_r|erpm_r|clkm_r_30s)" , ctype) :
            sdir = r"/pub/GNSS/products/mgex/-WWWW-/"
        sfile, xfile = ftp_filename(ftp, ctype)  
    elif ftp == "bkg":
        ftpsite = r"ftp://igs.bkg.bund.de"
        if ctype.find("_h",4,6) != -1:
            sdir = r"/IGS/nrt/-DDD-/-HH-/"
        sfile, xfile = ftp_filename(ftp, ctype) 

    elif ftp == "wum":
        ftpsite = r"ftp://igs.gnsswhu.cn"
        if (ctype.find("rnx",0,3) != -1) and (ctype.find("_h",4,6) != -1) :
            sdir = r"/pub/gps/data/hourly/-YYYY-/-DDD-/-HH-/"
        elif (ctype.find("rnx",0,3) != -1) and (ctype.find("_d",4,6) != -1) :
            sdir = r"/pub/gps/data/daily/-YYYY-/-DDD-/"+ r"-YY-" + ctype[3:4].lower() + r"/"
        elif ctype.find("sp3x",0,4)!= -1 or ctype.find("clkx",0,4) != -1:   #mgex products, only sp3 and clk, others can be added if need, dir: /pub/gps/
            sdir = r"/pub/gps/products/mgex/-WWWW-/"
        elif ctype.find("sp3m",0,4)!= -1 or ctype.find("clkm",0,4) != -1:   #mgex products, only sp3 and clk, others can be added if need, dir: /pub/gnss/
            sdir = r"/pub/gnss/products/mgex/-WWWW-/"
        else :
            sdir = r"/pub/gps/products/-WWWW-/"  #igs products, others can be added if need ,no atx avalible
        sfile, xfile = ftp_filename(ftp, ctype) 

    elif ftp == "kasi":   #korean igs data center
        ftpsite = r"ftp://nfs.kasi.re.kr"
        if (ctype.find("rnx",0,3) != -1) and (ctype.find("_h",4,6) != -1) :
            sdir = r"/gps/data/hourly/-YYYY-/-DDD-/-HH-/"
        elif (ctype.find("rnx",0,3) != -1) and (ctype.find("_d",4,6) != -1) :
            sdir = r"/gps/data/daily/-YYYY-/-DDD-/"+ r"-YY-" + ctype[3:4].lower() + r"/"
        else :
            sdir = r"/gps/products/-WWWW-/"  #igs products, other acs products can be added if need ,no atx avalible
        sfile, xfile = ftp_filename(ftp, ctype) 

    elif ftp == "ign" or ftp == "ign_mgex" or ftp == "ign_igs":   #igs data center
        if ftp == "ign" or ftp == "ign_mgex" :
            ftpsite = r"ftp://igs.ign.fr"
        else :
            ftpsite = r"ftp://igs.ensg.ign.fr"
        if ftp == "ign" or ftp == "ign_igs" :
            if ctype.find("atx",0,3) != -1:
                sdir = r"/pub/igs/igscb/station/general/"
            elif ctype.find("_d",4,6)!= -1:
                sdir = r"/pub/igs/data/-YYYY-/-DDD-/"
            elif ctype.find("_h",4,6)!= -1:
                sdir = r"/pub/igs/data/hourly/-YYYY-/-DDD-/"
            elif ctype.find("_r",4,6)!= -1:
                sdir = r"/pub/igs/data/highrate/-YYYY-/-DDD-/"
        elif ftp == "ign_mgex" :
            if ctype.find("_d",4,6)!= -1:
                sdir = r"/pub/igs/data/campaign/mgex/daily/rinex3/-YYYY-/-DDD-/"
            elif ctype.find("_h",4,6)!= -1:
                sdir = r"/pub/igs/data/campaign/mgex/hourly/rinex3/-YYYY-/-DDD-/"
            elif ctype.find("_r",4,6)!= -1:
                sdir = r"/pub/igs/data/campaign/mgex/highrate/rinex3/-YYYY-/-DDD-/"
        sfile, xfile = ftp_filename(ftp, ctype) 

    elif (ftp == "cddis" or ftp == "cddis_mgex"):   #cannot connect using chinese mainland network #2021/9/1
        ftpsite = r"ftps://gdc.cddis.eosdis.nasa.gov"
        if ctype.find("atx",0,3) != -1:
            sdir = r"/igscb/station/general/"
        elif ctype.find("rnx",0,3) == -1:
            sdir = r"/pub/gnss/products/-WWWW-/"
        else :
            if ftp == "cddis" :
                if ctype.find("_d",4,6)!= -1:
                    sdir = r"/pub/gnss/data/daily/-YYYY-/-DDD-/"+ r"-YY-" + ctype[3:4].lower() + r"/"
                elif ctype.find("n_h",3,6) != -1 or ctype.find("g_h",3,6) != -1 :
                    sdir = r"/pub/gnss/data/hourly/-YYYY-/-DDD-/"
                elif ctype.find("_h",4,6)!= -1:
                    sdir = r"/pub/gnss/data/hourly/-YYYY-/-DDD-/-HH-/"
                elif ctype.find("_r",4,6)!= -1:
                    sdir = r"/pub/gnss/data/highrate/-YYYY-/-DDD-/-YY-d/-HH-/"
            else :
                if ctype.find("_d",4,6)!= -1:
                    sdir = r"/pub/gnss/data/campaign/mgex/daily/rinex3/-YYYY-/-DDD-/"+ r"-YY-" + ctype[3:4].lower() + r"/"
                elif ctype.find("_h",4,6)!= -1:
                    sdir = r"/pub/gnss/data/campaign/mgex/hourly/rinex3/-YYYY-/-DDD-/-HH-/"
                elif ctype.find("_r",4,6)!= -1:
                    sdir = r"/pub/gnss/data/campaign/mgex/highrate/-YYYY-/-DDD-/-YY-d/-HH-/"                

        sfile, xfile = ftp_filename(ftp, ctype) 

    else :
        print ("Unknown ftp site : %s\n"%(ftp))
        exit()
    

    cmd_url = ftpsite + sdir
    return cmd_url,xfile

def ftp_session (cmode, ctype, mjd, hh, dh, ftpname):
    ifactor = 0 
    if cmode == r"+" : #time forward
        ifactor = 1
    elif cmode == r"-" : #time backward
        ifactor = -1
    if dh != 0:
        hh = hh + ifactor * dh
    else :
        if (ctype == "rnxn_h" or ctype == "rnxg_h") and ftpname == "cddis":
            mjd = mjd + ifactor * 1
        elif (ctype == "rnxp_h" and ftpname == "peter"):
            mjd = mjd + ifactor * 1 
        elif ctype.find("rnx",0,3) != -1 :
            if ctype.find("d",5,6) != -1:
                mjd = mjd + ifactor * 1
            elif ctype.find("h",5,6) != -1:
                hh = hh + ifactor * 1
            elif ctype.find("r",5,6) != -1:
                hh = hh + ifactor * 1
            else :
                print (" undefined data type %s \n"%(ctype))
#                return -1
        elif ctype.find("dcb",0,3) != -1 :
            year, month, day = conv_date("mjd","yyyymmdd",[mjd])
            month = month + ifactor * 1
            if month * 1 > 12 :
                month -= 1
                year += 1
            elif month * 1 <= 0 :
                month += 1
                year -= 1
            mjd = conv_date ("yyyymmdd","mjd", [year,month,15])
        elif re.match(r"(sp3x_u|erpx_u)" , ctype) :
            hh = hh + ifactor * 3
        else :
            if ctype.find("u",4,5) != -1 :
                hh = hh + ifactor * 6
            else:
                mjd += ifactor * 1
    while hh >= 24 :
        mjd += 1
        hh -= 24
    while hh < 0 :
        mjd -= 1
        hh += 24
    return mjd, hh


def ftp_getarg(slist, itstart, nses, target0, ctype, ftp, flist) : #reform command line args
    if len(ctype) == 0 or itstart[0] == 0 :
        print(" Unknown start-time or unknown data type \n")
        exit()
    if not re.match(r"(wum|igs|kasi|code|usno|iers|cddis|peter|gfz|ign|ign_mgex|ign_igs|bkg)",ftp) :
        print(" Unknown ftp site (wum|igs|kasi|code|usno|iers|cddis|peter|gfz|ign|ign_mgex|ign_igs|bkg) \n")
        exit()
    if ctype.find("rnx",0,3) == -1 :
        slist = ""
    if len(itstart) == 1 : # if itstart[] has one elem, that will be hrate, if there is 3 elements, that will be start year, doy and hh, if there is 2 elements, that will be start year, doy
        hrate = itstart[0]
        sys_time=get_systime("gmt")
        year0 = sys_time[0]
        doy0 = sys_time[1]
        hh0 = sys_time[2]
        hh0 = int (int (hh0*24/hrate)*hrate+0.01)
    else:
        year0 = itstart[0]
        doy0 = itstart[1]    
        hh0 = 0 if len(itstart) == 2 else itstart[2]
    return flist, year0, doy0, hh0, nses, target0, slist, ctype, ftp   
# Usage: 
#	 -tstart year doy hour of the start time
#	 -slist file with a list of stations for which data are requested
#	 -nses number of sessions/days are downloaded
#	    minus means backwards
#	 -target directory where the data to be stored
#	 -type data type:
#	    for rinex data: rnx#_%, # can be d/o/n/g for RINEX 2.xx and p/l/e for 3.xx
#	                            % can be d/h/r for daily/hourly/highrate 
#	    for igs products : sp3_f/r/u  clk_f clk_f_30s clk_f_05s snx_f erp_f erp_u
#	    for code ftpsite : eph_f/r/u clk_f clk_f_30s clk_f_05s snx_f erp_f erp_u
#	                       dcb_p1c1 dcb_p1p2 dcb_p2c2
#	 -ftp  ftpsite name: cddis code ign gfz bkg
#	 -flist all/new/old/none, default none


#def ftp_getsitelit(year0,day0,hh0,nses,slist,ctype,ftpname):  #this function get the existed file_list in the ftp_site, saved inside "slist", not complete
#    cmd_url,xfile = ftp_setsite(ftpname,ctype)
#    nses = nses if (nses >= 0 ) else -nses
#    cdir = "+" if  (nses >= 0 ) else "-"
#    mjd0 = conv_date("yyyyddd","mjd",[year0,day0])
#    mjd , hh = ftp_session(" ",ctype,mjd0,hh0,0,ftpname)
    
def ftp_getfiles(year0,doy0,hh0,nses0,target0,slist,ctype,ftpname,ACname,hrate):  ###using wget
    cmd_url0,sfile0=ftp_setsite(ftpname,ctype)
    if ( ftpname == "wum" ) and (ctype.find("sp3x",0,4) != -1 or ctype.find("clkx",0,4) != -1 ) and (not re.match(r"COD|WUM|GFZ|GRG|IAC|SHA|JAX",ACname)):
        print ("Please specify the AC's name!")
        exit()

    if ( ftpname == "wum" ) and (ctype.find("sp3x",0,4) != -1 or ctype.find("clkx",0,4) != -1 or ctype.find("sp3m",0,4) != -1 or ctype.find("clkm",0,4) != -1 ) and re.match(r"COD|WUM|GFZ|GRG|IAC|SHA|JAX",ACname):
        sfile0 = re.sub("-ACS-",ACname,sfile0,count=0,flags=0)       

    nses = nses0 if (nses0 >= 0 ) else -nses0
    cdir = "+" if  (nses0 >= 0 ) else "-"
    #print(nses0)
    #print(cdir)
    mjd0 = conv_date("yyyyddd","mjd",[year0,doy0])
    mjd0=mjd0[0]
    sites=[]
    FailedDocument = [] 
    if re.match("^\s+",slist,flags=0) :
        slist = ""
    else: 
        sites=read_sitelist(slist)
    mjd,hh = ftp_session(" ",ctype,mjd0,hh0,0,ftpname)
    if type(mjd) == type([]):
        mjd = mjd[0]
    if type(hh) == type([]):
        hh = hh[0]    
    #mjd = tmp_mjdhh[0]
    #hh = tmp_mjdhh[1]
    #print(type(mjd))
    ii = 0
    while ii < nses :
        target1 = target0
        cmd_url = replace_string(mjd,hh,0,0,cmd_url0,[])
        target = replace_string(mjd,hh,0,0,target1,[])
        sfile = replace_string(mjd,hh,0,0,sfile0,[])

        mkdir(target)
        os.chdir(target)

        if len(sites) == 0 : #when no site is match in the sitelist or no sitelist is given and ctype == rnx, 
#                            #all files will be download, when ctype != rnx, maybe only one file will be download, more test needed
            cmd_get = cmd_wget + cmd_url + sfile
            ret1 = os.system(cmd_get)
            if ret1 != 0 :
                FailedDocument.append(sfile0)
        else :
        #### download from a url_list file
            #file_list = "tmp_"+ftpname+"_"+ctype+"_"+slist.split("/")[-1]+"_"+str(mjd)+"_"+str(hh)
            #with open(file_list,"a") as fp:
            #    for site in sites:
            #        if sfile0[0:9] == "?????????":
            #            sfile_1 = re.sub(r"^\?{9}",str(site).upper()+"?????",sfile,count=0,flags=0)
            #        else :
            #            sfile_1 = re.sub(r"^\?{4}$",str(site).lower(),sfile,count=0,flags=0)
            #        fp.write(cmd_url+sfile_1+"\n")
            #cmd_get = cmd_wget + "-i "+  file_list
            #ret1 = os.system(cmd_get)
            #os.remove(file_list)
        #### download through one by one wget command
            for site in sites:
                if sfile0[0:9] == "?????????":
                    sfile_1 = re.sub(r"^\?{9}",str(site).upper()+"?????",sfile,count=0,flags=0)
                else :
                    sfile_1 = re.sub(r"^\?{4}",str(site).lower(),sfile,count=0,flags=0)
                cmd_get = cmd_wget + cmd_url + sfile_1
                ret1 = os.system(cmd_get)
                if ret1 != 0 :
                    FailedDocument.append(sfile)
        mjd,hh=ftp_session(cdir,ctype,mjd,hh,hrate,ftpname)
        ii+=1
    #if nses < 0:
def ftp_getfiles_ftplib(year0,doy0,hh0,nses0,target0,slist,ctype,ftpname,ACname,hrate):  ###using ftplib
    cmd_url0,sfile0=ftp_setsite(ftpname,ctype)
    if ( ftpname == "wum"  or ftpname == "whu_igs") and (ctype.find("sp3x",0,4) != -1 or ctype.find("clkx",0,4) != -1 or ctype.find("sp3m",0,4) != -1 or ctype.find("clkm",0,4) != -1 ) and (not re.match(r"COD|WUM|GFZ|GRG|IAC|SHA|JAX",ACname)):
        print ("Please specify the AC's name!")
        exit()

    if ( ftpname == "wum"  or ftpname == "whu_igs") and (ctype.find("sp3x",0,4) != -1 or ctype.find("clkx",0,4) != -1 or ctype.find("sp3m",0,4) != -1 or ctype.find("clkm",0,4) != -1 ) and re.match(r"COD|WUM|GFZ|GRG|IAC|SHA|JAX",ACname):
        sfile0 = re.sub("-ACS-",ACname,sfile0,count=0,flags=0)       

    nses = nses0 if (nses0 >= 0 ) else -nses0
    cdir = "+" if  (nses0 >= 0 ) else "-"
    #print(nses0)
    #print(cdir)
    mjd0 = conv_date("yyyyddd","mjd",[year0,doy0])
    mjd0=mjd0[0]
    sites=[]
    if re.match("^\s+",slist,flags=0) :
        slist = ""
    else: 
        sites=read_sitelist(slist)
    mjd,hh = ftp_session(" ",ctype,mjd0,hh0,0,ftpname)
    if type(mjd) == type([]):
        mjd = mjd[0]
    if type(hh) == type([]):
        hh = hh[0]    
    #mjd = tmp_mjdhh[0]
    #hh = tmp_mjdhh[1]
    #print(type(mjd))
    if re.match(r"(whu|nts|ndt|whu_igs)" , ftpname) :
        urlss = cmd_url0.split()
        urls = urlss[2].split('/')
        username = urlss[0].split("=")[1]
        password = urlss[1].split("=")[1]
        host_1 = ''.join([urls[0],'//',urls[2]])
        host = urls[2]
        remote_dir0 = re.sub(host_1,'',urlss[2])
    else:
        urls = cmd_url0.split('/')
        host_1 = ''.join([urls[0],'//',urls[2]])
        host = urls[2]
        remote_dir0 = re.sub(host_1,'',cmd_url0)
        username = "anonymous"
        password = "wonderwall@chd.edu.cn"
    ii = 0
    while ii < nses :
        target1 = target0
        remote_dir = replace_string(mjd,hh,0,0,remote_dir0,[])
        target = replace_string(mjd,hh,0,0,target1,[])
        sfile = replace_string(mjd,hh,0,0,sfile0,[])

        mkdir(target)
        os.chdir(target)
        log_file = ''.join([target,"/",ftpname,"_",ctype,"_",str(ii)])
        ftp_down(host,username,password,log_file,target,remote_dir,sites,sfile)
        os.chdir(target)
        os.remove(log_file)
        mjd,hh=ftp_session(cdir,ctype,mjd,hh,hrate,ftpname)
        ii+=1
