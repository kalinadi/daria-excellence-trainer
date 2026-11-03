const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
p.on('pageerror',e=>console.error('ERR',e.message));
await p.goto('file://'+require('path').resolve(__dirname,'../../index.html'));await p.waitForTimeout(800);
const out=await p.evaluate(()=>{const S=new Set();const d=document.createElement('div');
 const add=t=>{if(t&&/[א-ת]/.test(t))S.add(t.trim())};
 for(const k of Object.keys(GEN))for(let L=1;L<=5;L++)for(let r=0;r<400;r++){try{const q=GEN[k](L);
  add(q.prompt);add(q.lead);add(q.explain);if(q.stim){d.innerHTML=q.stim;d.querySelectorAll('svg').forEach(x=>x.remove());const tw=document.createTreeWalker(d,NodeFilter.SHOW_TEXT);let n;while(n=tw.nextNode())add(n.nodeValue)}
  (q.opts||[]).forEach(o=>add(o.text))}catch(e){}}
 return [...S]});
require('fs').writeFileSync(__dirname+'/corpus.json',JSON.stringify(out));console.log(out.length);await b.close()})();
