import os;os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json,re,collections,sys
from male import male
res=json.load(open('dicta.json'))
uni=collections.defaultdict(collections.Counter);ctx=collections.defaultdict(collections.Counter)
fail=collections.Counter();sents=[]
for toks in res:
    sent=[]
    for t in toks:
        if t['sep']:
            if '\n' in t['word'] or re.search(r'[.?!:,;()"]',t['word']): sent.append(None)
            continue
        w=t['word']
        if not re.fullmatch(r'[א-ת]+',w): sent.append(None);continue
        v=male(w,t['options'][0]) if t['options'] else None
        if v is None: fail[w]+=1;v=w
        sent.append((w,v))
    sents.append(sent)
for s in sents:
    for i,x in enumerate(s):
        if not x:continue
        w,v=x;p=s[i-1][0] if i>0 and s[i-1] else '^';n=s[i+1][0] if i+1<len(s) and s[i+1] else '$'
        uni[w][v]+=1;ctx[('P',p,w)][v]+=1;ctx[('N',w,n)][v]+=1
U={w:c.most_common(1)[0][0] for w,c in uni.items()}
json.dump({'U':U,'ctx':{'|'.join(k):dict(c) for k,c in ctx.items() if c.most_common(1)[0][0]!=U[k[2] if k[0]=='P' else k[1]]}},open('raw.json','w'),ensure_ascii=False)
print('fail',fail.most_common())
amb=[(w,dict(c)) for w,c in uni.items() if len(c)>1];print('amb',len(amb))
for a in amb:print(a)
