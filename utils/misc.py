
import re

def splitStr(istr, sep):
    re_spc = re.compile(r'\s+')
    re_sep = re.compile(r'\s*,\s*')
    str_1  = re_spc.sub(' ', istr)
    return re_sep.split(str_1)
 
