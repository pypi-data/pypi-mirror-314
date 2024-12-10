def chunks(lst, n, reverse=False):
    """return successive n-sized chunks from lst."""
    res = []
    for i in range(0, len(lst), n):
        if reverse:
            res += [reversed(lst[i:i + n])]
        else:
            res += [lst[i:i + n]]
    return res


def chunk_dict(dict_in,lim):
    out =[]
    temp={}
    x=0
    for k,v in dict_in.items():
        if x!=0 and x%lim==0:
            out+=[temp]
            temp={}
        x+=1
        temp[k]=v
    if temp:out+=[temp]
    return out


import collections
def sort_dict_by_key(item:dict,reverse=False):
    return dict(collections.OrderedDict(sorted(item.items(),reverse=reverse)))

def sort_dict_by_val(item:dict,reverse=False):
    sorted_x = sorted(item.items(), key=lambda kv: kv[1],reverse=reverse)
    return dict(collections.OrderedDict(sorted_x))
