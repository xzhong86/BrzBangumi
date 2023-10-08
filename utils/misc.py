
import re
import difflib
import json

def splitStr(istr, sep):
    re_spc = re.compile(r'\s+')
    re_sep = re.compile(r'\s*,\s*')
    str_1  = re_spc.sub(' ', istr)
    return re_sep.split(str_1)
 

def keywordMatch(kw, string):
    if len(kw) == 0:
        return False
    if kw in string:
        return True

    seqm = difflib.SequenceMatcher(None, kw, string)
    ms1  = seqm.get_matching_blocks()
    blks = list(filter(lambda m: m.size > 0, ms1))
    if len(blks) == 0:
        return False

    start = min([ m.b for m in blks ])
    end   = max([ m.b + m.size for m in blks ])
    str2  = string[start:end]

    rat = difflib.SequenceMatcher(None, kw, str2).ratio()
    return rat > 0.9

def ostruct2dict(st):
    return { k:v for k,v in st.items() }


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as fh:
        return json.load(fh)

def dump_json(filepath, obj):
    with open(filepath, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=4, sort_keys=True, ensure_ascii=False)

