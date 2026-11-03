import re
MARK=re.compile('[֑-ׇ]')
def split(v):
    out=[]
    for ch in v:
        if 'א'<=ch<='ת': out.append([ch,''])
        elif out: out[-1][1]+=ch
    return out
HOL='ֹֺ';KUB='ֻ';CHK='ֳ'
def male(word,v):
    v=v.replace('|','');L=split(v);res=[];j=0;i=0
    while i<len(word):
        c=word[i]
        if j<len(L) and L[j][0]==c:
            # doubled vav/yod where vocal has single
            if c in 'וי' and i+1<len(word) and word[i+1]==c and not (j+1<len(L) and L[j+1][0]==c):
                res.append(L[j][:]);res.append([c,'']);i+=2;j+=1;continue
            res.append(L[j][:]);i+=1;j+=1;continue
        if c=='ו' and res:
            pm=res[-1][1]
            if KUB in pm: res[-1][1]=pm.replace(KUB,'');res.append(['ו','ּ']);i+=1;continue
            if any(h in pm for h in HOL): res[-1][1]=re.sub('[ֹֺ]','',pm);res.append(['ו','ֹ']);i+=1;continue
            if CHK in pm: res[-1][1]=pm.replace(CHK,'');res.append(['ו','ֹ']);i+=1;continue
        if c in 'ויא': res.append([c,'']);i+=1;continue
        return None
    if j!=len(L): return None
    return ''.join(a+b for a,b in res)
