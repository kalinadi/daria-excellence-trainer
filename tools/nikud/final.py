import os;os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json,re
raw=json.load(open('raw.json'));U=raw['U'];ctx=raw['ctx']
DAG='ּ'
NAMES={'נועה':'נוֹעָה','יואב':'יוֹאָב','איתי':'אִיתַי','מאיה':'מָאיָה','עומר':'עוֹמֶר','תמר':'תָּמָר','אורי':'אוּרִי','שירה':'שִׁירָה','רון':'רוֹן','ליה':'לִיָּה','דן':'דָּן','גאיה':'גַּאיָה'}
def nodag(v): return v[0]+v[1:].replace(DAG,'',1) if v[1:2]==DAG else v
def adddag(v): return v if len(v)>1 and v[1]==DAG else v[0]+DAG+v[1:]
OV={}
for n,v in NAMES.items():
    first=n[0];gut=first in 'אהחער'
    OV[n]=v
    OV['ל'+n]='לְ'+nodag(v)
    OV['מ'+n]=('מֵ'+v) if gut else ('מִ'+adddag(v))
    OV['ו'+n]=('וּ' if first in 'בומפ' else 'וְ')+nodag(v)
    OV['ול'+n]='וּלְ'+nodag(v)
    OV['ש'+n]='שֶׁ'+(v if gut else adddag(v))
OV.update({'שוחה':'שׂוֹחֶה','אבן':'אֶבֶן','חצי':'חֲצִי','כבד':'כָּבֵד','מי':'מִי','שרים':'שָׁרִים','להחזיר':'לְהַחֲזִיר','ספר':'סֵפֶר','עין':'עַיִן','שווה':'שָׁוֶוה','ממהיר':'מִמָּהִיר','לצעיר':'לְצָעִיר','משירה':'מִשִּׁירָה','מתמר':'מִתָּמָר','מרון':'מֵרוֹן','מאורי':'מֵאוּרִי','מספר':'מִסְפָּר'})
for k,v in OV.items():
    U[k]=v
C={}
for k,c in ctx.items():
    t,a,b=k.split('|');w=b if t=='P' else a
    if w in OV or w not in U: continue
    if not re.fullmatch(r'[א-ת]+',w):continue
    top=max(c,key=c.get)
    if top!=U[w]: C[k]=top
C.pop('P|הסיפור|וענו',None);C.pop('N|דג|$',None)
U.update({'דג':'דָּג','בחרו':'בַּחֲרוּ','ופתרו':'וּפִתְרוּ','פתרו':'פִּתְרוּ'})
U={k:v for k,v in U.items() if k!=v}
json.dump({'U':U,'C':C},open('nik.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(U),len(C),len(json.dumps({'U':U,'C':C},ensure_ascii=False,separators=(',',':')).encode()))
for k,v in C.items(): print(k,v,U.get(k.split('|')[2] if k[0]=='P' else k.split('|')[1]))

# inject into index.html
p='../../index.html';h=open(p).read()
line='const NIK='+json.dumps({'U':U,'C':C},ensure_ascii=False,separators=(',',':'))+';'
h2=re.sub(r'^const NIK=.*;$',lambda m:line,h,count=1,flags=re.M)
assert h2!=h or line in h;open(p,'w').write(h2);print('index.html updated')
