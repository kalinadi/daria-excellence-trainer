import os;os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json,urllib.request,time,sys
u=json.load(open('uniq.json'))
chunks=[];cur=[];n=0
for x in u:
    if n+len(x)>8000 and cur: chunks.append(cur);cur=[];n=0
    cur.append(x);n+=len(x)+1
chunks.append(cur)
res=[]
for i,ch in enumerate(chunks):
    data=json.dumps({"task":"nakdan","data":"\n".join(ch),"genre":"modern"}).encode()
    for t in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request("https://nakdan-u1-0.loadbalancer.dicta.org.il/api",data,{"Content-Type":"application/json"}),timeout=120)
            toks=json.load(r);break
        except Exception as e: print('retry',i,e,file=sys.stderr);time.sleep(3)
    res.append(toks);print(i,len(chunks),len(toks),file=sys.stderr)
json.dump(res,open('dicta.json','w'),ensure_ascii=False)
