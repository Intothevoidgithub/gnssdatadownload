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
#                      whu     : ftp://10.10.5.10 # wuhan university's igmas datacenter
#                                MGEX_obs, MGEX_nav, iGMAS_obs, iGMAS_nav
#                      whu_igs : ftp://10.10.5.10 # wuhan university's igs datacenter backup at wuhan university's igmas datacenter 
#                                MGEX_obs, MGEX_nav, MGEX_products, igs_products
#                                MGEX ACs center: CODE-COD WHUHAN-WUM GFZ-GFZ CNES-GRG IAC-IAC SHAO-SHA JAXA-JAX 
#                      ndt     : ftp://10.11.5.10 # changsha
#                                MGEX_obs, MGEX_nav, iGMAS_obs, iGMAS_nav
#                      nts     : ftp://10.12.5.10 # xian
#                                MGEX_obs, MGEX_nav, iGMAS_obs, iGMAS_nav
#                      igs     : ftp://igs.org  # only atx file # not use 
#                      kasi    : ftp://nfs.kasi.re.kr #korea  #hourly data is a little slow
#                                MGEX_obs, MGEX_nav, igs_products (no atx avalible)
#                      code    : ftp://ftp.aiub.unibe.ch
#                                code products: erp, clk, eph(orb), ion, DCB, snx
#                      usno    : ftp://maia.usno.navy.mil
#                                finals2000 file (poleut file)
#                      iers    : ftp://ftp.iers.org
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
    email_nts = r"kfiw82mj"
    email_ndt = r"qazxsw"
    email_whu = r"igmasftp@whugnss"

    user = ""
    keyword = ""
    cmd_url = ""
    ftpsite = ""
    sdir = ""
    sfile = ""
    xfile = ""
## ftp username
    if ftp == "nts":  #national time service center
        user = r"test2"
        keyword = email_nts
    elif  ftp == "ndt": #national university of defense technology
        user = r"pub"
        keyword = email_ndt
    elif  ftp == "whu" or ftp == "whu_igs": #whuhan university igmas data center
        user = r"igmasftp_whu"
        keyword = email_whu
    else :
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
        ftpsite = r"ftp://ftp.iers.org"
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

    elif ftp == "nts":
        ftpsite = r"ftp://10.12.5.10"
        if ctype.find("_h",4,6) != -1:
            sdir = r"/data/IGS/-YYYY-/-DDD-/hourly/-HH-/"
        elif ctype.find("_d",4,6) != -1:
            sdir = r"/data/IGS/-YYYY-/-DDD-/daily/"
        sfile, xfile = ftp_filename(ftp, ctype)        
    elif ftp == "ndt":
        ftpsite = r"ftp://10.11.5.10"
        if ctype.find("_h",4,6) != -1:
            sdir = r"/data/IGS/-YYYY-/-DDD-/hourly/-HH-/"
        elif ctype.find("_d",4,6) != -1:
            sdir = r"/data/IGS/-YYYY-/-DDD-/daily/"
        sfile, xfile = ftp_filename(ftp, ctype)    
    elif ftp == "whu":
        ftpsite = r"ftp://10.10.5.10"
        if ctype.find("_h",4,6) != -1:
            sdir = r"/data/IGS/-YYYY-/-DDD-/hourly/-HH-/"
        elif ctype.find("_d",4,6) != -1:
            sdir = r"/data/IGS/-YYYY-/-DDD-/daily/"
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

    elif ftp == "whu_igs":   #same as wum ,except ftpsites and address
        ftpsite = r"ftp://10.10.5.10"
        if (ctype.find("rnx",0,3) != -1) and (ctype.find("_h",4,6) != -1) :
            sdir = r"/data/aliftp/pub/data/hourly/-YYYY-/-DDD-/-HH-/"
        elif (ctype.find("rnx",0,3) != -1) and (ctype.find("_d",4,6) != -1) :
            sdir = r"/data/aliftp/pub/data/daily/-YYYY-/-DDD-/"+ r"-YY-" + ctype[3:4].lower() + r"/"
        elif ctype.find("sp3x",0,4)!= -1 or ctype.find("clkx",0,4) != -1:   #mgex acs products, only sp3 and clk, others can be added if need, dir: /pub/gps/
            sdir = r"/data/aliftp/pub/products/mgex/-WWWW-/"
        elif ctype.find("sp3m",0,4)!= -1 or ctype.find("clkm",0,4) != -1:   #mgex products, only sp3 and clk, others can be added if need, dir: /pub/gnss/
            sdir = r"/data/aliftp/pub/products/mgex/-WWWW-/"
        else :
            sdir = r"/data/aliftp/pub/products/-WWWW-/"  #igs products, other acs products can be added if need ,no atx avalible
        sfile, xfile = ftp_filename(ftp, ctype) 

    elif ftp == "kasi":   #korean igs data center
        ftpsite = r"ftp://nfs.kasi.re.kr"
        if (ctype.find("rnx",0,3) != -1) and (ctype.find("_h",4,6) != -1) :
            sdir = r"/gps/data/hourly/-YYYY-/-DDD-/-HH-/"
        elif (ctype.find("rnx",0,3) != -1) and (ctype.find("_d",4,6) != -1) :
            sdir = r"/gps/data/daily/-YYYY-/-DDD-/"+ r"-YY-" + ctype[3:4].lower() + r"/"
        else :
            sdir = r"/data/aliftp/pub/products/-WWWW-/"  #igs products, other acs products can be added if need ,no atx avalible
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
    
    if re.match(r"(whu|nts|ndt|whu_igs)" , ftp) :
        cmd_url = " --ftp-user=" + user + " --ftp-password=" + keyword + " " + ftpsite + sdir
    else:
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
    if not re.match(r"(wum|whu|whu_igs|ndt|nts|igs|kasi|code|usno|iers|cddis|peter|gfz|ign|ign_mgex|ign_igs|bkg)",ftp) :
        print(" Unknown ftp site (wum|whu|whu_igs|ndt|nts|igs|kasi|code|usno|iers|cddis|peter|gfz|ign|ign_mgex|ign_igs|bkg) \n")
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
    if ( ftpname == "wum"  or ftpname == "whu_igs") and (ctype.find("sp3x",0,4) != -1 or ctype.find("clkx",0,4) != -1 ) and (not re.match(r"COD|WUM|GFZ|GRG|IAC|SHA|JAX",ACname)):
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

iGMASnetwork= [
 'ABJA',
 'ALGR',
 'BJF1',
 'BRCH',
 'BYNS',
 'CANB',
 'CHU1',
 'CLGY',
 'CNYR',
 'CEGS',
 'DWIN',
 'GUA1',
 'HMNS',
 'ICUK',
 'KNDY',
 'KRCH',
 'KUN1',
 'LHA1',
 'LPGS',
 'OUNZ',
 'PETH',
 'RDJN',
 'SHA1',
 'TAHT',
 'WUH1',
 'XIA1',
 'ZHON']

StationsList= [
 'abmf',
 'abpo',
 'adis',
 'aira',
 'alic',
 'antc',
 'areq',
 'artu',
 'auck',
 'badg',
 'bake',
 'bako',
 'bjfs',
 'bogi',
 'bogt',
 'braz',
 'brst',
 'bucu',
 'cags',
 'cas1',
 'ccj2',
 'cedu',
 'chan',
 'chti',
 'chum',
 'chur',
 'cusv',
 'darw',
 'dav1',
 'dgar',
 'drao',
 'faa1',
 'fair',
 'falk',
 'ffmj',
 'flin',
 'godz',
 'gold',
 'gras',
 'graz',
 'guam',
 'hnus',
 'hob2',
 'hofn',
 'hrao',
 'iisc',
 'ineg',
 'iqal',
 'iqqe',
 'kerg',
 'kir0',
 'kit3',
 'kokv',
 'kour',
 'lama',
 'lhaz',
 'lpgs',
 'mac1',
 'mana',
 'mar6',
 'mas1',
 'maw1',
 'mbar',
 'mcm4',
 'mkea',
 'mobj',
 'mobs',
 'morp',
 'mqzg',
 'nano',
 'nico',
 'nium',
 'nklg',
 'not1',
 'novm',
 'nril',
 'ntus',
 'nyal',
 'ohi2',
 'palm',
 'parc',
 'park',
 'pert',
 'pets',
 'pie1',
 'pimo',
 'polv',
 'prds',
 'ptag',
 'qaq1',
 'reun',
 'reyk',
 'rio2',
 'riop',
 'salu',
 'sant',
 'savo',
 'sbok',
 'sch2',
 'scor',
 'scub',
 'sfer',
 'shao',
 'ssia',
 'sthl',
 'stjo',
 'stk2',
 'suth',
 'sutm',
 'svtl',
 'sydn',
 'syog',
 'tash',
 'thti',
 'tixi',
 'tow2',
 'tro1',
 'tsk2',
 'twtf',
 'ufpr',
 'ulab',
 'uldi',
 'unbj',
 'unsa',
 'vndp',
 'warn',
 'whit',
 'will',
 'yakt',
 'yar3',
 'yell',
 'ykro',
 'zamb',
 'zeck'] 

IGSnetwork= [
 'ABMF00GLP',
 'ABPO00MDG',
 'ACRG00GHA',
 'ADIS00ETH',
 'AGGO00ARG',
 'AIRA00JPN',
 'AJAC00FRA',
 'ALBH00CAN',
 'ALGO00CAN',
 'ALIC00AUS',
 'ALRT00CAN',
 'AMC400USA',
 'ANKR00TUR',
 'ANMG00MYS',
 'ANTC00CHL',
 'AREG00PER',
 'AREQ00PER',
 'ARHT00ATA',
 'ARTU00RUS',
 'ARUC00ARM',
 'ASCG00SHN',
 'ASPA00USA',
 'ATRU00KAZ',
 'AUCK00NZL',
 'BADG00RUS',
 'BAIE00CAN',
 'BAKE00CAN',
 'BAKO00IDN',
 'BAMF00CAN',
 'BARH00USA',
 'BELE00BRA',
 'BHR300BHR',
 'BHR400BHR',
 'BIK000KGZ',
 'BILL00USA',
 'BJCO00BEN',
 'BJFS00CHN',
 'BJNM00CHN',
 'BLYT00USA',
 'BNOA00IDN',
 'BOAV00BRA',
 'BOGI00POL',
 'BOGT00COL',
 'BOR100POL',
 'BRAZ00BRA',
 'BREW00USA',
 'BRFT00BRA',
 'BRMU00GBR',
 'BRST00FRA',
 'BRUN00BRN',
 'BRUX00BEL',
 'BSHM00ISR',
 'BTNG00IDN',
 'BUCU00ROU',
 'CAGS00CAN',
 'CAS100ATA',
 'CCJ200JPN',
 'CEBR00ESP',
 'CEDU00AUS',
 'CGGN00NGA',
 'CHAN00CHN',
 'CHIL00USA',
 'CHOF00JPN',
 'CHPG00BRA',
 'CHPI00BRA',
 'CHTI00NZL',
 'CHUM00KAZ',
 'CHUR00CAN',
 'CHWK00CAN',
 'CIBG00IDN',
 'CIT100USA',
 'CKIS00COK',
 'CKSV00TWN',
 'CMP900USA',
 'CMUM00THA',
 'CNMR00USA',
 'COCO00AUS',
 'CORD00ARG',
 'COSO00USA',
 'COTE00ATA',
 'COYQ00CHL',
 'CPNM00THA',
 'CPVG00CPV',
 'CRAO00UKR',
 'CRFP00USA',
 'CRO100VIR',
 'CUSV00THA',
 'CUT000AUS',
 'CUUT00THA',
 'CZTG00ATF',
 'DAE200KOR',
 'DAEJ00KOR',
 'DAKR00SEN',
 'DARW00AUS',
 'DAV100ATA',
 'DEAR00ZAF',
 'DGAR00GBR',
 'DHLG00USA',
 'DJIG00DJI',
 'DLF100NLD',
 'DLTV00VNM',
 'DRAG00ISR',
 'DRAO00CAN',
 'DUBO00CAN',
 'DUMG00ATA',
 'DUND00NZL',
 'DYNG00GRC',
 'EBRE00ESP',
 'EIL300USA',
 'EIL400USA',
 'ENAO00PRT',
 'EPRT00USA',
 'ESCU00CAN',
 'EUSM00MYS',
 'FAA100PYF',
 'FAIR00USA',
 'FALE00WSM',
 'FALK00FLK',
 'FFMJ00DEU',
 'FLIN00CAN',
 'FLRS00PRT',
 'FRDN00CAN',
 'FTNA00WLF',
 'FUNC00PRT',
 'GAMB00PYF',
 'GAMG00KOR',
 'GANP00SVK',
 'GCGO00USA',
 'GENO00ITA',
 'GLPS00ECU',
 'GLSV00UKR',
 'GMSD00JPN',
 'GODE00USA',
 'GODN00USA',
 'GODS00USA',
 'GODZ00USA',
 'GOL200USA',
 'GOLD00USA',
 'GOP600CZE',
 'GOP700CZE',
 'GOPE00CZE',
 'GRAC00FRA',
 'GRAS00FRA',
 'GRAZ00AUT',
 'GUAM00GUM',
 'GUAO00CHN',
 'GUAT00GTM',
 'GUUG00GUM',
 'HAL100USA',
 'HAMD00IRN',
 'HARB00ZAF',
 'HERS00GBR',
 'HERT00GBR',
 'HKSL00HKG',
 'HKWS00HKG',
 'HLFX00CAN',
 'HNLC00USA',
 'HNPT00USA',
 'HNUS00ZAF',
 'HOB200AUS',
 'HOFN00ISL',
 'HOLB00CAN',
 'HOLM00CAN',
 'HOLP00USA',
 'HRAG00ZAF',
 'HRAO00ZAF',
 'HUEG00DEU',
 'HYDE00IND',
 'IENG00ITA',
 'IISC00IND',
 'INEG00MEX',
 'INVK00CAN',
 'IQAL00CAN',
 'IQQE00CHL',
 'IRKJ00RUS',
 'IRKM00RUS',
 'IRKT00RUS',
 'ISBA00IRQ',
 'ISHI00JPN',
 'ISPA00CHL',
 'ISTA00TUR',
 'IZMI00TUR',
 'JCTW00ZAF',
 'JFNG00CHN',
 'JNAV00VNM',
 'JOG200IDN',
 'JOZ200POL',
 'JOZE00POL',
 'JPLM00USA',
 'JPRE00ZAF',
 'KARR00AUS',
 'KAT100AUS',
 'KERG00ATF',
 'KGNI00JPN',
 'KHAR00UKR',
 'KIR000SWE',
 'KIR800SWE',
 'KIRI00KIR',
 'KIRU00SWE',
 'KIT300UZB',
 'KITG00UZB',
 'KMNM00TWN',
 'KOKB00USA',
 'KOKV00USA',
 'KOS100NLD',
 'KOST00KAZ',
 'KOUC00NCL',
 'KOUG00GUF',
 'KOUR00GUF',
 'KRGG00ATF',
 'KRS100TUR',
 'KSMV00JPN',
 'KUJ200CAN',
 'KZN200RUS',
 'LAE100PNG',
 'LAMA00POL',
 'LAUT00FJI',
 'LBCH00USA',
 'LCK300IND',
 'LCK400IND',
 'LEIJ00DEU',
 'LHAZ00CHN',
 'LICC00GBR',
 'LLAG00ESP',
 'LMMF00MTQ',
 'LPAL00ESP',
 'LPGS00ARG',
 'LROC00FRA',
 'M0SE00ITA',
 'MAC100AUS',
 'MAD200ESP',
 'MADR00ESP',
 'MAG000RUS',
 'MAJU00MHL',
 'MAL200KEN',
 'MANA00NIC',
 'MAR600SWE',
 'MAR700SWE',
 'MARS00FRA',
 'MAS100ESP',
 'MAT100ITA',
 'MATE00ITA',
 'MATG00ITA',
 'MAUI00USA',
 'MAW100ATA',
 'MAYG00MYT',
 'MBAR00UGA',
 'MCHL00AUS',
 'MCIL00JPN',
 'MCM400ATA',
 'MDO100USA',
 'MDVJ00RUS',
 'MEDI00ITA',
 'MELI00ESP',
 'MERS00TUR',
 'MET300FIN',
 'METG00FIN',
 'METS00FIN',
 'MFKG00ZAF',
 'MGUE00ARG',
 'MIKL00UKR',
 'MIZU00JPN',
 'MKEA00USA',
 'MOBJ00RUS',
 'MOBK00RUS',
 'MOBN00RUS',
 'MOBS00AUS',
 'MOIU00KEN',
 'MONP00USA',
 'MORP00GBR',
 'MQZG00NZL',
 'MRC100USA',
 'MRL100NZL',
 'MRL200NZL',
 'MRO100AUS',
 'MTKA00JPN',
 'MTV100URY',
 'MTV200URY',
 'NAIN00CAN',
 'NANO00CAN',
 'NAUR00NRU',
 'NCKU00TWN',
 'NICO00CYP',
 'NIST00USA',
 'NIUM00NIU',
 'NKLG00GAB',
 'NLIB00USA',
 'NNOR00AUS',
 'NOT100ITA',
 'NOVM00RUS',
 'NRC100CAN',
 'NRIL00RUS',
 'NRMD00NCL',
 'NTUS00SGP',
 'NVSK00RUS',
 'NYA100NOR',
 'NYA200NOR',
 'NYAL00NOR',
 'OAK100GBR',
 'OAK200GBR',
 'OBE400DEU',
 'OHI200ATA',
 'OHI300ATA',
 'ONS100SWE',
 'ONSA00SWE',
 'OP7100FRA',
 'OPMT00FRA',
 'ORID00MKD',
 'OSN300KOR',
 'OSN400KOR',
 'OUS200NZL',
 'OWMG00NZL',
 'PADO00ITA',
 'PALM00ATA',
 'PARC00CHL',
 'PARK00AUS',
 'PDEL00PRT',
 'PEN200HUN',
 'PENC00HUN',
 'PERT00AUS',
 'PETS00RUS',
 'PGEN00PHL',
 'PICL00CAN',
 'PIE100USA',
 'PIMO00PHL',
 'PIN100USA',
 'PNGM00PNG',
 'POAL00BRA',
 'POHN00FSM',
 'POL200KGZ',
 'POLV00UKR',
 'POTS00DEU',
 'POVE00BRA',
 'PPPC00PHL',
 'PRDS00CAN',
 'PRE300ZAF',
 'PRE400ZAF',
 'PTAG00PHL',
 'PTBB00DEU',
 'PTGG00PHL',
 'PTVL00VUT',
 'QAQ100GRL',
 'QIKI00CAN',
 'QUI300ECU',
 'QUI400ECU',
 'QUIN00USA',
 'RABT00MAR',
 'RAEG00PRT',
 'RAMO00ISR',
 'RBAY00ZAF',
 'RCMN00KEN',
 'RDSD00DOM',
 'REDU00BEL',
 'RESO00CAN',
 'REUN00REU',
 'REYK00ISL',
 'RGDG00ARG',
 'RIGA00LVA',
 'RIO200ARG',
 'RIOP00ECU',
 'ROAG00ESP',
 'ROCK00USA',
 'ROTH00ATA',
 'SALU00BRA',
 'SAMO00WSM',
 'SANT00CHL',
 'SASK00CAN',
 'SAVO00BRA',
 'SBOK00ZAF',
 'SCH200CAN',
 'SCIP00USA',
 'SCOR00GRL',
 'SCRZ00BOL',
 'SCTB00ATA',
 'SCUB00CUB',
 'SEJN00KOR',
 'SEME00KAZ',
 'SEY200SYC',
 'SEYG00SYC',
 'SFDM00USA',
 'SFER00ESP',
 'SGOC00LKA',
 'SGPO00USA',
 'SHAO00CHN',
 'SHE200CAN',
 'SIN100SGP',
 'SMST00JPN',
 'SNI100USA',
 'SOD300FIN',
 'SOFI00BGR',
 'SOLO00SLB',
 'SPK100USA',
 'SPT000SWE',
 'SPTU00BRA',
 'SSIA00SLV',
 'STFU00USA',
 'STHL00GBR',
 'STJ300CAN',
 'STJO00CAN',
 'STK200JPN',
 'STPM00SPM',
 'STR100AUS',
 'STR200AUS',
 'SULP00UKR',
 'SUTH00ZAF',
 'SUTM00ZAF',
 'SUWN00KOR',
 'SVTL00RUS',
 'SYDN00AUS',
 'SYOG00ATA',
 'TABL00USA',
 'TANA00ETH',
 'TASH00UZB',
 'TCMS00TWN',
 'TDOU00ZAF',
 'TEHN00IRN',
 'THTG00PYF',
 'THTI00PYF',
 'THU200GRL',
 'TID100AUS',
 'TIDB00AUS',
 'TIT200DEU',
 'TIXI00RUS',
 'TLSE00FRA',
 'TLSG00FRA',
 'TNML00TWN',
 'TONG00TON',
 'TOPL00BRA',
 'TORP00USA',
 'TOW200AUS',
 'TRAK00USA',
 'TRO100NOR',
 'TSK200JPN',
 'TSKB00JPN',
 'TUBI00TUR',
 'TUVA00TUV',
 'TWTF00TWN',
 'UCAL00CAN',
 'UCLP00USA',
 'UCLU00CAN',
 'UFPR00BRA',
 'ULAB00MNG',
 'ULDI00ZAF',
 'UNB300CAN',
 'UNBD00CAN',
 'UNBJ00CAN',
 'UNBN00CAN',
 'UNSA00ARG',
 'UNX200AUS',
 'UNX300AUS',
 'URAL00RUS',
 'URUM00CHN',
 'USN700USA',
 'USN800USA',
 'USN900USA',
 'USNO00USA',
 'USP100FJI',
 'USUD00JPN',
 'UTQI00USA',
 'UZHL00UKR',
 'VACS00MUS',
 'VALD00CAN',
 'VILL00ESP',
 'VIS000SWE',
 'VNDP00USA',
 'VOIM00MDG',
 'WAB200CHE',
 'WARK00NZL',
 'WARN00DEU',
 'WDC500USA',
 'WDC600USA',
 'WES200USA',
 'WGTN00NZL',
 'WHC100USA',
 'WHIT00CAN',
 'WIDC00USA',
 'WILL00CAN',
 'WIND00NAM',
 'WLSN00USA',
 'WROC00POL',
 'WSRT00NLD',
 'WTZ300DEU',
 'WTZA00DEU',
 'WTZR00DEU',
 'WTZS00DEU',
 'WTZZ00DEU',
 'WUH200CHN',
 'WUHN00CHN',
 'XMIS00AUS',
 'YAKT00RUS',
 'YAR200AUS',
 'YAR300AUS',
 'YARR00AUS',
 'YEBE00ESP',
 'YEL200CAN',
 'YELL00CAN',
 'YIBL00OMN',
 'YKRO00CIV',
 'YONS00KOR',
 'YSSK00RUS',
 'ZAMB00ZMB',
 'ZECK00RUS',
 'ZIM200CHE',
 'ZIM300CHE',
 'ZIMM00CHE']