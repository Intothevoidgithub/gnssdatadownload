#!/usr/bin/python3
## coding: utf-8

## purpose : Basic python functions for automatic processing
## created : Shichao Xie 2021.8.16
## ref     : PANDA_perl script from GFZ

## def_list: [findstring, read_sitelist, mkdir,replace_string,job_file_extension,get_filename,copy_basic_files,copy_system_files,quantile_exc,read_snx_pos]

import os,re,shutil,math,ctypes,inspect
import threading
from M_timeCov import *

# Quartile
# $n = 2 ->median; n=1 ->lower quartile; n=3 ->upper quartile;
def quantile_exc(data, n):
    if n<1 or n>3:
        return -1
    data.sort()
    position = (len(data) + 1)*n/4
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer - 1])*pos_decimal
    return quartile

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
    # """if it returns a number greater than one, you're in trouble, 
    # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class MyThread(threading.Thread):
    def __init__(self, func, args):
        '''
        :param func: function
        :param args: function args
        '''
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = None
        #self._stop = threading.Event()

    def run(self):
        self.result = self.func(*self.args)
        #while True: 
        #    if self.stopped(): 
        #        return
        #    print("Hello, world!")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def getResult(self):
        return self.result
    #def _get_my_tid(self):
    #    """determines this (self's) thread id"""
    #    if not self.isAlive():
    #        raise threading.ThreadError("the thread is not active")
    #    # do we have it cached?
    #    if hasattr(self, "_thread_id"):
    #        return self._thread_id
    #    # no, look for it in the _active dict
    #    for tid, tobj in threading._active.items():
    #        if tobj is self:
    #            self._thread_id = tid
    #            return tid
    #    raise AssertionError("could not determine the thread's id")
    #def raise_exc(self, exctype):
    #    """raises the given exception type in the context of this thread"""
    #    _async_raise(self._get_my_tid(), exctype)
    #def terminate(self):
    #    """raises SystemExit in the context of the given thread, which should 
    #    cause the thread to exit silently (unless caught)"""
    #    self.raise_exc(SystemExit)

## find if a string(sstr) inside a list(slist)
## return the full string 
# xsc 2021.2.13
def findstring (sstr, sslist):
    flag = 0
    pos = 0 #where string appear in list
    for i in range(0, len(sslist)):
        if sstr in sslist[i]:
            flag = 1
            pos = i
            break
    if flag == 0:
        pos = -1
        return pos
    else:
        return pos

def read_sitelist(slist):
    sites=[]
    with open(slist) as fp:
        for site in fp.readlines() :
            site = site.rstrip('\n')
            if re.match("^\s(\w{4})$",site,flags=0) or re.match("^\s(\w{4})\s",site,flags=0) or re.match("^(\w{4})$",site,flags=0) or re.match("^(\w{4})\s+",site,flags=0) :
                sites.append(re.sub("^\s+|\s+$","",site))
    return sites

def mkdir(dirpath):         
    isExists = os.path.exists(dirpath)
    if not isExists:
        os.makedirs(dirpath)

def replace_string(mjd,hh,min,sec,string,keywords):
    tmp_yyyyddd = conv_date("mjd","yyyyddd",[mjd])
    year = tmp_yyyyddd[0]
    doy = tmp_yyyyddd[1]
    tmp_gwkgwkd = conv_date("mjd","wwwwd",[mjd])
    gwk = tmp_gwkgwkd[0]
    gwkd = tmp_gwkgwkd[1]
    tmp_yymmdd = conv_date("yyyyddd","yyyymmdd",[year,doy])
    mm = tmp_yymmdd[1]
    dd = tmp_yymmdd[2]

    year = str(year).rjust(4,"0")
    doy = str(doy).rjust(3,"0")
    gwk = str(gwk).rjust(4,"0")
    gwkd = str(gwkd).rjust(1,"0")
    mm = str(mm).rjust(2,"0")
    dd = str(dd).rjust(2,"0")
    yy = str(year)[-2:]
    hh = str(hh).rjust(2,"0")
    min = str(min).rjust(2,"0")
    sec = str(sec).rjust(2,"0")

    char = chr (ord("a")+int(hh)*1)

    string = re.sub("-YYYY-", year,string, count=0,flags=0)
    string = re.sub("-DDD-", doy,string, count=0,flags=0)
    string = re.sub("-HH-", hh,string, count=0,flags=0)
    string = re.sub("-YY-", yy,string, count=0,flags=0)
    string = re.sub("-DD-", dd,string, count=0,flags=0)
    string = re.sub("-WWWWD-", gwk+gwkd,string, count=0,flags=0)
    string = re.sub("-WWWW-", gwk,string, count=0,flags=0)
    string = re.sub("-D-", gwkd,string, count=0,flags=0)
    string = re.sub("-MM-", mm,string, count=0,flags=0)
    string = re.sub("-H-", char,string, count=0,flags=0)
    string = re.sub("-HHMMSS-", hh+min+sec,string, count=0,flags=0)    

    for keyword in keywords :
        keyword = keyword.split("=")
        key = keyword[0]
        value = keyword[1]
        string = re.sub(key,value,string,count=0,flags=0)
    return string
    
def job_file_extension(iyear,idoy,ihh,imm,isec):
    return "%04d%03d_%02d%02d%02d"%(iyear,idoy,ihh,imm,isec)

#
## read file-table and get the file name for the given symbolic name
## if date time are not given(mjd == 0) it returns the name with "variables" #this is for perl , python version will not need it
#
def get_filename(symbol,fltab,mjd,hh,mm,xx,keywords):
    return_file_name=" "
    iread =0
    #ireplace = 0
    PRO_RAW = {}
    SRC_RAW = {}
    PRO_REP = {}
    SRC_REP = {}
    if os.path.exists(fltab):
        itype = 0
        with open(fltab) as fp:
            for ln in fp.readlines():
                ln = ln.replace("\n","")
                if re.search(r"^\+Processing",ln):
                    itype = 1
                elif re.search(r"^\+Source",ln):
                    itype = 2
                elif re.search(r"^\+System",ln):
                    itype = 3
                if not re.search(r"^\s",ln):
                    continue
                ln=re.sub(r"\!(.*)?","",ln) #remove newline
                ln=re.sub(r"^\s+","",ln) #remove start whitespace
                ln=re.sub(r"^\s+$","",ln) #remove whitespace line
                if re.search(r"(\S+)\s+([\S|\s]+)$",ln):
                    var1=re.search(r"(\S+)\s+([\S|\s]+)$",ln).group(1)
                    var2=re.search(r"(\S+)\s+([\S|\s]+)$",ln).group(2)
                    if var2 == "":
                        continue
                    if itype == 1:
                        PRO_RAW[var1] = var2
                    elif itype == 2:
                        SRC_RAW[var1] = var2
            iread = 1
            if mjd != 0:
                for keys in PRO_RAW.keys():
                    filename = replace_string(mjd,hh,mm,xx,PRO_RAW[keys],keywords)
                    PRO_REP[keys] = filename
                for keys in SRC_RAW.keys():
                    filename = replace_string(mjd,hh,mm,xx,SRC_RAW[keys],keywords)
                    SRC_REP[keys] = filename
                #ireplace = 1
    if iread == 0:
        print("no file-table has been loaded for %s"%symbol)
        return -1
    if mjd != 0:
        symbol_sp = symbol.split(":")
        tt = symbol_sp[0]
        ss = symbol_sp[1]
        if re.search(r"^SRC",tt):
            for keys in SRC_RAW.keys():
                if keys == ss:
                    line = replace_string(mjd,hh,mm,xx,SRC_RAW[keys],keywords)
                    return_file_name = line
                    break
        else:
            for keys in PRO_RAW.keys():
                if keys == ss:
                    line = replace_string(mjd,hh,mm,xx,PRO_RAW[keys],keywords)
                    return_file_name = line
                    break
    else:
        symbol_sp = symbol.split(":")
        tt = symbol_sp[0]
        ss = symbol_sp[1]
        if re.search(r"^SRC",tt):
            for keys in SRC_REP.keys():
                if keys == ss:
                    return_file_name = SRC_REP[keys]
                    break
        else:
            for keys in PRO_REP.keys():
                if keys == ss:
                    return_file_name = PRO_REP[keys]
                    break
    if re.search(r"^\s*$",return_file_name):
        print("***ERROR(get_filename): %s symbolic name is not define in file-table."%symbol)
        return ""
    return return_file_name

def copy_basic_files(srcdir, ctrl_file, file_table, site_list):
####ctrl_file
    if not os.path.exists(ctrl_file):
        fsrc = srcdir + "/" +ctrl_file
        if not os.path.exists(fsrc):
            print("***ERROR: source-file %s not exist and no local file %s"%(fsrc,ctrl_file))
            return -1
        shutil.copyfile(fsrc,"./"+ctrl_file)
        print(" ctrl-file not exist, copied from %s"%fsrc)
    else :
        print(" use local ctrl-file:  %s"%ctrl_file)
####file_table
    if not os.path.exists(file_table):
        fsrc = srcdir + "/" +file_table
        if not os.path.exists(fsrc):
            print("***ERROR: source-file %s not exist and no local file %s"%(fsrc,file_table))
            return -1
        shutil.copyfile(fsrc,"./"+file_table)
        print(" file_table not exist, copied from %s"%fsrc)
    else :
        print(" use local file_table:  %s"%file_table)
####site_list
    if not os.path.exists(site_list):
        fsrc = srcdir + "/" +site_list
        if not os.path.exists(fsrc):
            print("***ERROR: source-file %s not exist and no local file %s"%(fsrc,site_list))
            return -1
        shutil.copyfile(fsrc,"./"+site_list)
        print(" site_list not exist, copied from %s"%fsrc)
    else :
        print(" use local site_list:  %s"%site_list)
    
    if (not os.path.exists(ctrl_file)) or (not os.path.exists(file_table)) or (not os.path.exists(site_list)):
        print(" one of the basic files is neither in local nor in source %s"%srcdir)
        print("    %s, %s, %s "%(ctrl_file, file_table,site_list))
        return -1
    return 0

## copy system files defined in ctrl-file within +/-System Files from the given source
def copy_system_files(cmode, file_table, src_dir):
    if os.path.exists(file_table):
        with open(file_table) as fp:
            isys = 0
            file = ""
            lines = fp.readlines()
            for ln in lines:
                ln = ln.replace("\n","")
                if re.search(r"^\-System Files",ln):
                    break
                isys = 1 if re.search(r"^\+System Files",ln) else isys
                if isys != 1 :
                    continue
                if not re.search(r"^\s+\S+",ln) : # only line with leading space
                    continue
                file = re.search(r"^\s+(\S+)",ln).group(1)
                src = src_dir +  "/" + file
                if not os.path.exists(src):
                    print(" source file %s not exiting"%src)
                    if not os.path.exists(file):
                        print("***WARNING both local and source files not exist, %s, %s"%(file,src))
                        continue
                if re.search(r"^cp",cmode):
                    if os.path.exists(file):
                        os.remove(file)
                    shutil.copyfile(src,file)
                    print(" system file %s copied from %s"%(file,src))
                elif re.search(r"^ln",cmode):
                    if os.path.exists(file):
                        os.remove(file)
                    os.symlink(src,file)
                    print(" system file %s symblic link with %s"%(file,src))
                elif re.search(r"^up",cmode):
                    timestamp_local = os.stat(file).st_mtime if os.path.exists(file) else 0
                    timestamp_src = os.stat(src).st_mtime if os.path.exists(src) else 0
                    if timestamp_src > timestamp_local :
                        shutil.copyfile(src,file)
                        print(" source file %s is newer, copied to local %s"%(src,file))
                    else:
                        print(" source file %s is not newer, use local %s"%(src,file))
    else :
        print("No file_table!!! (copy_system_files)")
        return -1
    return 0

def read_snx_pos(site_list,snx):
    if not os.path.exists(snx):
        print("***Error***: There is no snx file")
        return -1
    sites_lon = {}
    sites_lat = {}
    sites_h = {}
    lons = []
    lats = []
    hs = []
    with open(snx) as fp:
        lines=fp.readlines()
        num=len(lines)
        rec_start= 0
        rec_end = 0
        for i in range(num):
            if re.search(r"\+SITE\/ID",lines[i]):
                rec_start = i+2
            if re.search(r"\-SITE\/ID",lines[i]):
                rec_end = i
                break
        for ii in range(rec_start,rec_end):
            ln = lines[ii].split()
            lon=  int(lines[ii][44:47])+int(lines[ii][48:50])/60.0+float(lines[ii][51:55])/3600.0
            lat=  int(lines[ii][56:59])+int(lines[ii][60:62])/60.0+float(lines[ii][63:67])/3600.0
            h = float(lines[ii][68:75])
            sites_lon.update({ln[0]: lon}) 
            sites_lat.update({ln[0]: lat}) 
            sites_h.update({ln[0]: h}) 
    for si in site_list:
        if si.upper() in sites_lon.keys():
            lons.append(sites_lon[si.upper()])
            lats.append(sites_lat[si.upper()])
            hs.append(sites_h[si.upper()])
        else :
            lons.append(0)
            lats.append(0)
            hs.append(0)
    #print(sites_lon)
    #print(sites_lat)
    #print(sites_h)
    return lons,lats,hs

def cluster_to_sitelist( fcluster, site_list ):
    allsite = []
    if os.path.exists(fcluster):
        with open(fcluster) as fp:
            for line in fp.readlines():
                line=line.replace("\n","")
                if re.match(r"^\s+",line):
                    sites=line.split()
                    del sites[0:4]
                    allsite = allsite + sites
        sits_uniq = list(set(allsite))
        sits_uniq.sort()
        with open(site_list,"w") as fp:
            for si in sits_uniq :
                fp.write(''.join([" ",si,"\n"]))
    return 0

def frnx_n2o(file_new):
    file_old = ""
    site=""
    yy  =0
    doy =0
    hh  =0
    dorh=""
    type=""
    rorc=""
    zip =""
    if re.match(r"\w{9}_R_\d{11}_\d{2}\w{1}_\d{2}\w{1}_\w{2}\.(crx|rnx)(.gz|.Z|$)",file_new):
        match = re.match(r"(\w{4})\w{5}_R_\d{2}(\d{2})(\d{3})(\d{2})\d{2}_\d{2}(\w{1})_\w{3}_\w{1}(\w{1}).(\w{3})(.gz|.Z|$)",file_new)
        site=match.group(1)
        yy  =match.group(2)
        doy =match.group(3)
        hh  =match.group(4)
        dorh=match.group(5)
        type=match.group(6)
        rorc=match.group(7)
        zip =match.group(8)
        if type != "O":
            print(" frnx_n2o: wrong rnx-file type  %s "%type)
            return file_old
        else :
            if rorc == "rnx":
                type = "o"
            else :
                type = "d"
    elif re.match(r"\w{9}_R_\d{11}_\d{2}\w{1}_\w{2}\.(crx|rnx)(.gz|.Z|$)",file_new) :
        match = re.match(r"(\w{4})\w{5}_R_\d{2}(\d{2})(\d{3})(\d{2})\d{2}_(\w{3})_(\w{2}).(\w{3})(.gz|.Z|$)",file_new)
        site=match.group(1)
        yy  =match.group(2)
        doy =match.group(3)
        hh  =match.group(4)
        dorh=match.group(5)
        type=match.group(6)
        rorc=match.group(7)
        zip =match.group(8)
        if type == "GN":
            type = "n"
        elif type == "RN" :
            type = "g"
        elif type == "EN" :
            type = "l"
        elif type == "CN" :
            type = "f"
        elif type == "MN" :
            type = "p"
        else :
            print(" frnx_n2o: unknow rinex navigaiton type (GN/RN/EN/CN/MN/) : %s"%type)
            return file_old
    else :
        print("frnx_n2o: unknown new rinex-file name : %s"%file_new)
        return file_old
    if dorh == "D":
        dorh = "0"
    elif dorh == "H":
        dorh = chr(ord("a")+int(hh)*1)
    file_old = ''.join([site.lower(),doy,dorh,".",yy,type,zip])
    return file_old
