"""
LifeLine Blood Bank Management - single-file Python app.
Run:   python lifeline_blood_bank.py
Then it opens http://localhost:8000 in your browser. No installs needed (Python 3 only).
Press Ctrl+C in the terminal to stop.
"""
import http.server
import socketserver
import threading
import webbrowser

PORT = 8000

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LifeLine Blood Bank Management</title>
<style>
:root{--navy:#0f1b3d;--navy2:#1a2a55;--red:#e5384f;--green:#10a37f;--bg:#f5f6fa;--card:#fff;--tx:#14213d;--mut:#6b7691;--bd:#e4e7ef}
*{box-sizing:border-box;margin:0}
body{font-family:"Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--tx);display:flex;min-height:100vh}
aside{width:260px;background:var(--navy);color:#cfd6ea;padding:20px 16px;display:flex;flex-direction:column;position:sticky;top:0;height:100vh}
.logo{display:flex;gap:12px;align-items:center;padding:0 8px 22px;border-bottom:1px solid #ffffff18;margin-bottom:18px}
.logo i{width:44px;height:44px;border-radius:50%;background:var(--red);color:#fff;display:grid;place-items:center;font-size:26px;font-style:normal}
.logo b{color:#fff;font-size:20px;display:block}.logo small{font-size:11px;letter-spacing:1px}
nav small{display:block;font-size:11px;letter-spacing:1px;padding:0 10px 8px;color:#8c97b8}
nav button{all:unset;display:flex;width:100%;gap:12px;align-items:center;padding:12px 14px;border-radius:10px;cursor:pointer;font-size:15px;color:#e3e8f6;margin-bottom:4px}
nav button:hover,nav button.on{background:var(--navy2);color:#fff}
nav button.on span{color:var(--red)}
.life{margin-top:auto;background:var(--navy2);border-radius:12px;padding:14px;font-size:12px}.life b{color:#fff;font-size:14px;display:block}
main{flex:1;min-width:0}
header{display:flex;justify-content:space-between;align-items:center;padding:16px 32px;background:#fff;border-bottom:1px solid var(--bd);position:sticky;top:0;z-index:5;flex-wrap:wrap;gap:10px}
header .crumb{font-size:13px;letter-spacing:.5px;color:var(--mut)}header .crumb b{color:var(--tx)}
.hr{display:flex;gap:22px;align-items:center;font-size:14px}.hr .ok{color:var(--green);font-weight:600}
.btn{border:0;border-radius:8px;padding:10px 16px;font-weight:600;cursor:pointer;font-size:14px;color:#fff;background:var(--red)}
.btn.b{background:#1e3a8a}.btn.g{background:var(--green)}.btn.n{background:var(--navy2)}
section{padding:28px 32px;display:none}section.on{display:block}
h1{font-size:34px}h1+p{color:var(--mut);margin:4px 0 22px}
.hero{background:var(--navy);border-radius:18px;color:#fff;padding:38px 44px;display:flex;justify-content:space-between;align-items:center;gap:24px;margin:8px 0 24px;overflow:hidden}
.hero small{color:#9fb0dc;letter-spacing:1.5px;font-size:12px;font-weight:700}
.hero h2{font-size:46px;line-height:1.1;margin:12px 0 14px}.hero p{max-width:520px;color:#d7def2;line-height:1.5;margin-bottom:22px}
.hero img{width:330px;max-width:38vw;aspect-ratio:1;object-fit:cover;border-radius:46% 54% 50% 50%/48% 40% 60% 52%;border:3px solid #b86cc0;background:#fff}
.hero .bt{display:flex;gap:12px;flex-wrap:wrap}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:22px}
.stat{border-top:4px solid var(--c)}.stat small{color:var(--mut)}.stat b{display:block;font-size:34px;margin:12px 0 6px;font-family:Consolas,monospace}
.warn{background:#ffeef0;color:#9b1c2e;border:1px solid #ffd3d9;border-radius:10px;padding:14px 18px;margin:22px 0;display:flex;justify-content:space-between;cursor:pointer}
.two{display:grid;grid-template-columns:1.5fr 1fr;gap:20px}
.bars{display:flex;gap:14px;align-items:flex-end;height:210px;margin-top:14px;border-bottom:1px solid var(--bd)}
.bars div{flex:1;text-align:center;font-size:12px}.bars i{display:block;border-radius:6px 6px 0 0;background:var(--green);margin:0 auto;width:70%;min-height:4px}.bars i.low{background:var(--red)}
.lab{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--mut);margin-top:10px}.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px}
.qa{display:flex;justify-content:space-between;align-items:center;border:1px solid var(--bd);border-left:4px solid var(--c);border-radius:8px;padding:12px 14px;margin-top:12px;cursor:pointer}.qa small{color:var(--mut)}
.tools{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
input,select{border:1px solid var(--bd);border-radius:8px;padding:10px 12px;font:inherit;background:#fff;min-width:0}
.tools input{width:300px;max-width:100%}
.chips button{border:0;background:none;padding:7px 12px;border-radius:7px;cursor:pointer;font:inherit;color:var(--mut)}.chips button.on{background:var(--navy);color:#fff}
table{width:100%;border-collapse:collapse;font-size:14px}
th{background:#f1f3f9;text-align:left;padding:14px;font-size:13px}td{padding:14px;border-top:1px solid var(--bd)}
.tbl{padding:0;overflow-x:auto}
.tag{padding:5px 10px;border-radius:6px;font-size:12px;font-weight:600;display:inline-block}
.tag.ok{background:#dcf6ec;color:#0b7a5c}.tag.lo{background:#ffe4e8;color:#b4233a}.tag.wa{background:#fff2d1;color:#9a6a00}
.mono{font-family:Consolas,monospace}
.sm{border:1px solid var(--bd);background:#fff;border-radius:6px;padding:6px 10px;cursor:pointer;font:inherit;font-size:13px;color:#1e3a8a}
.form{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;align-items:end;margin-top:14px}
.form label{font-size:12px;color:var(--mut);display:flex;flex-direction:column;gap:6px}
.tot{color:var(--red);font-family:Consolas,monospace;font-size:20px;font-weight:700}
#toast{position:fixed;bottom:24px;right:24px;background:var(--navy);color:#fff;padding:14px 20px;border-radius:10px;display:none;z-index:20}
@media(max-width:900px){aside{display:none}.hero{flex-direction:column}.two{grid-template-columns:1fr}section,header{padding-left:16px;padding-right:16px}.hero h2{font-size:34px}}
</style></head><body>
<aside>
<div class="logo"><i>+</i><div><b>LifeLine</b><small>BLOOD BANK</small></div></div>
<nav id="nav"><small>WORKSPACE</small></nav>
<div class="life"><b>Be a lifesaver</b>A little care can save a life.<hr style="border:0;border-top:1px solid #ffffff18;margin:10px 0">Emergency Hotline: +91 800-LIFELINE<br><br><a href="#" onclick="resetData();return false" style="color:#cfd6ea">↻ Reset Data</a></div>
</aside>
<main>
<header><div class="crumb">HOSPITAL MANAGEMENT / <b>BLOOD BANK</b></div>
<div class="hr"><span>🩸 Stock: <b style="color:var(--red)" id="tstock"></b></span><span class="mono" id="clock"></span><span class="ok">● SYSTEM READY</span><button class="btn" onclick="go('col')">⊕ New Donor</button></div></header>

<section id="dash" class="on">
<h1>Good day, Admin!</h1><p>Your blood bank overview at a glance. Every donation can help save a life.</p>
<div class="hero"><div><small>EVERY DROP COUNTS</small><h2>Donate blood.<br>Share life.</h2>
<p>Manage inventory, doctors, collections and billing. Real-time hospital blood reserves and cross-matching ledger.</p>
<div class="bt"><button class="btn" onclick="go('col')">Register Collection</button><button class="btn n" onclick="go('pay')">Issue Patient Bill</button></div></div>
<img src="__IMG__" alt="Lab technician checking a blood sample"></div>
<div class="stats" id="stats"></div>
<div class="warn" id="warn" onclick="go('inv')"></div>
<div class="two"><div class="card"><div class="tools" style="margin:0"><div><b style="font-size:20px">Blood inventory snapshot</b><br><small style="color:var(--mut)">Units available by blood group</small></div><a href="#" onclick="go('inv');return false" style="color:#1e3a8a">Full table</a></div>
<div class="bars" id="bars"></div><div class="lab"><span><i class="dot" style="background:var(--red)"></i>Low stock (&lt;10)</span><span><i class="dot" style="background:var(--green)"></i>Available stock</span></div></div>
<div class="card"><b style="font-size:20px">Quick actions</b><br><small style="color:var(--mut)">Frequent tasks and directory access</small>
<div class="qa" style="--c:var(--red)" onclick="go('inv')"><div><b>View blood inventory</b><br><small>Check stock and service costs</small></div>›</div>
<div class="qa" style="--c:#3b6ef5" onclick="go('doc')"><div><b>Doctors directory</b><br><small>Experience and fees</small></div>›</div>
<div class="qa" style="--c:var(--green)" onclick="go('col')"><div><b>Register collection</b><br><small>Record a donor</small></div>›</div>
<div class="qa" style="--c:#f0b429" onclick="go('pay')"><div><b>Payments &amp; bills</b><br><small>Create a sample bill</small></div>›</div></div></div>
</section>

<section id="inv"><h1>Blood Inventory</h1><p>Live stock and service cost per unit.</p>
<div class="tools"><input id="iq" placeholder="Search blood group…" oninput="rInv()"><div class="chips" id="ifl"></div></div>
<div class="card tbl"><table><thead><tr><th>Blood Group</th><th>Available Units</th><th>Service Cost (Per Unit)</th><th>Stock Status</th><th>Quick Stock Adjust</th></tr></thead><tbody id="ib"></tbody></table></div></section>

<section id="doc"><h1>Doctors Directory</h1><p>Doctor profiles, experience and consultation fees.</p><div id="dl"></div></section>
<section id="nur"><h1>Available Nurses</h1><p>Nurse details, experience and current availability.</p><div id="nl"></div></section>

<section id="col"><h1>Collections</h1><p>Register donors and blood collected.</p>
<div class="card"><b>Register collection</b>
<div class="form"><label>Donor name<input id="cn" placeholder="e.g. Amit Patel"></label>
<label>Blood group<select id="cg"></select></label><label>Units collected<input id="cu" type="number" min="1" value="1"></label>
<button class="btn g" onclick="addCol()">+ Add &amp; update stock</button></div></div><br>
<div class="card tbl"><table><thead><tr><th>#</th><th>Donor</th><th>Blood Group</th><th>Units</th><th>Date</th></tr></thead><tbody id="cb"></tbody></table></div></section>

<section id="pay"><h1>Payments &amp; Bills</h1><p>Create a demo bill and issue cross-matched blood units.</p>
<div class="card"><b>Create bill</b> <small style="color:var(--mut)">Deducts from active inventory.</small>
<div class="form"><label>Patient name<input id="pn" placeholder="e.g. Sunita Menon"></label><label>Blood group<select id="pg" onchange="est()"></select></label>
<label>Units<input id="pu" type="number" min="1" value="1" oninput="est()"></label><label>Payment method<select id="pm"><option>Cash at Hospital</option><option>Online Payment (Demo)</option></select></label></div>
<div class="tools" style="margin:18px 0 0"><span class="tot" id="est"></span><button class="btn g" onclick="addBill()">Generate bill &amp; update stock</button></div></div><br>
<div class="card tbl"><table><thead><tr><th>Bill #</th><th>Patient</th><th>Group</th><th>Units</th><th>Unit Cost</th><th>Total</th><th>Method</th><th>Status</th><th>Created</th></tr></thead><tbody id="pb"></tbody></table></div>
<p style="color:var(--mut);font-style:italic;margin-top:14px">Online payment is demo-only. Charges are illustrative service fees.</p></section>
</main><div id="toast"></div>
<script>
const KEY='lifeline_v1',$=id=>document.getElementById(id);
const seed=()=>({inv:[["A+",25,500],["A-",10,600],["B+",25,500],["B-",8,600],["AB+",15,700],["AB-",7,800],["O+",30,500],["O-",10,700]].map(a=>({g:a[0],u:a[1],c:a[2]})),
doc:[["Dr. Ravi Kumar","Hematologist",12,500],["Dr. Priya Sharma","General Physician",8,400],["Dr. Arjun Rao","Pathologist",10,600],["Dr. Sneha Reddy","Transfusion Medicine",6,350]].map(a=>({n:a[0],s:a[1],y:a[2],f:a[3],ok:1})),
nur:[["Nurse Anjali Patel","Blood collection and donor care",7],["Nurse Meera Shah","Patient care and monitoring",5],["Nurse Kavita Joshi","Transfusion support",6],["Nurse Riya Desai","Ward and recipient support",3]].map(a=>({n:a[0],s:a[1],y:a[2],ok:1})),
col:[["Rohan Mehta","O+",2,"2026-10-25"],["Neha Gupta","A+",1,"2026-10-26"],["Vikram Singh","B+",1,"2026-10-26"],["Pooja Nair","AB+",1,"2026-10-27"]].map(a=>({n:a[0],g:a[1],u:a[2],d:a[3]})),
bills:[[204,"Suresh Raina","O+",2,500,"Online Payment (Demo)","2026-10-27 11:20:10"],[203,"Sunita Menon","A+",1,500,"Cash at Hospital","2026-10-27 10:55:04"],[202,"Rajesh Khanna","B+",1,500,"Online Payment (Demo)","2026-10-26 17:30:22"],[201,"Meenakshi Iyer","AB+",1,700,"Cash at Hospital","2026-10-26 11:15:40"]].map(a=>({id:a[0],p:a[1],g:a[2],u:a[3],c:a[4],m:a[5],t:a[6]}))});
let S;try{S=JSON.parse(localStorage.getItem(KEY))}catch(e){}S=S||seed();
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const total=()=>S.inv.reduce((a,b)=>a+b.u,0),toast=m=>{const t=$('toast');t.textContent=m;t.style.display='block';setTimeout(()=>t.style.display='none',2200)};
const pages=[["dash","Dashboard","▦"],["inv","Blood Inventory","♥"],["doc","Doctors","+"],["nur","Available Nurses","✚"],["col","Collections","↗"],["pay","Payments & Bills","☰"]];
$('nav').innerHTML+=pages.map(p=>`<button data-p="${p[0]}" onclick="go('${p[0]}')"><span>${p[2]}</span>${p[1]}</button>`).join('');
function go(p){document.querySelectorAll('section').forEach(s=>s.classList.toggle('on',s.id==p));document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('on',b.dataset.p==p));scrollTo(0,0);render()}
let fl='all',df='all',nf='all';
function render(){$('tstock').textContent=total()+' units';
const low=S.inv.filter(x=>x.u<10);
$('stats').innerHTML=[["Available Units",total(),"Across all blood groups","var(--red)"],["Blood Groups",S.inv.filter(x=>x.u>0).length+"/8","Groups currently in stock","#3b6ef5"],["Available Doctors",S.doc.filter(x=>x.ok).length,"Ready for consultation","var(--green)"],["Collections",S.col.length,"Collection records","#f0b429"]].map(s=>`<div class="card stat" style="--c:${s[3]}"><small>${s[0]}</small><b>${s[1]}</b><small>${s[2]}</small></div>`).join('');
$('warn').innerHTML=low.length?`<span><b>Low Stock Warning:</b> ${low.map(x=>x.g+' ('+x.u+' units)').join(', ')} require replenishment!</span><b>Manage Stock →</b>`:'<span>All blood groups are well stocked.</span>';
const mx=Math.max(...S.inv.map(x=>x.u),1);
$('bars').innerHTML=S.inv.map(x=>`<div>${x.u}<i class="${x.u<10?'low':''}" style="height:${x.u/mx*160}px"></i></div>`).join('');
$('bars').insertAdjacentHTML('afterend','');
rInv();rPeople('doc');rPeople('nur');
$('cb').innerHTML=S.col.map((c,i)=>`<tr><td>#${i+1}</td><td><b>${c.n}</b></td><td>🩸 ${c.g}</td><td>${c.u}</td><td class="mono">${c.d}</td></tr>`).join('');
$('pb').innerHTML=S.bills.map(b=>`<tr><td class="mono">#00${b.id}</td><td><b>${b.p}</b></td><td style="color:var(--red)">🩸 ${b.g}</td><td>${b.u}</td><td class="mono">₹${b.c}.00</td><td class="mono"><b>₹${(b.u*b.c).toLocaleString('en-IN')}.00</b></td><td>${b.m}</td><td><span class="tag ${b.m.startsWith('Online')?'ok':'wa'}">${b.m.startsWith('Online')?'Paid (Demo)':'Cash Due'}</span></td><td class="mono">${b.t}</td></tr>`).join('');
est()}
function rInv(){const q=$('iq').value.toLowerCase(),l=S.inv.filter(x=>x.g.toLowerCase().includes(q)&&(fl=='all'||(fl=='low'?x.u<10:x.u>=10)));
$('ifl').innerHTML=[["all","All ("+S.inv.length+")"],["low","Low Stock (<10)"],["in","In Stock"]].map(f=>`<button class="${fl==f[0]?'on':''}" onclick="fl='${f[0]}';rInv()">${f[1]}</button>`).join('');
$('ib').innerHTML=l.map(x=>{const i=S.inv.indexOf(x);return `<tr><td><b>${x.g}</b> &nbsp;Group ${x.g}</td><td class="mono"><b>${x.u} units</b></td><td class="mono">₹${x.c}.00</td><td><span class="tag ${x.u<10?'lo':'ok'}">${x.u<10?'⚠ Low stock':'✔ Available'}</span></td><td><button class="sm" onclick="adj(${i},-1)">−</button> <button class="sm" onclick="adj(${i},1)">+</button> <button class="sm" onclick="adj(${i},5)">+5</button> <button class="sm" style="color:var(--red)" onclick="ed(${i})">✎</button></td></tr>`}).join('')}
function adj(i,d){S.inv[i].u=Math.max(0,S.inv[i].u+d);save();render()}
function ed(i){const v=prompt('Set units for '+S.inv[i].g,S.inv[i].u);if(v===null)return;const c=prompt('Service cost per unit (₹)',S.inv[i].c);S.inv[i].u=Math.max(0,+v||0);S.inv[i].c=Math.max(0,+c||S.inv[i].c);save();render()}
function rPeople(k){const isD=k=='doc',f=isD?df:nf,arr=S[k],id=isD?'dl':'nl';
$(id).innerHTML=`<div class="tools"><input placeholder="Search ${isD?'doctor or specialty':'nurse or care domain'}…" oninput="this.dataset.q=this.value.toLowerCase();rows('${k}')" id="q${k}"><div class="chips">${[["all","All ("+arr.length+")"],["1","Available"],["0","On Leave"]].map(c=>`<button class="${f==c[0]?'on':''}" onclick="${isD?'df':'nf'}='${c[0]}';rPeople('${k}')">${c[1]}</button>`).join('')}</div></div>
<div class="card tbl"><table><thead><tr><th>ID</th><th>${isD?'Doctor Name':'Nurse Name'}</th><th>${isD?'Specialization':'Care Domain & Details'}</th><th>Experience</th>${isD?'<th>Consultation Fee</th>':''}<th>Availability</th><th>Action</th></tr></thead><tbody id="r${k}"></tbody></table></div>
<div class="card" style="margin-top:20px"><b>Add a ${isD?'doctor':'nurse'}</b><div class="form"><label>Name<input id="${k}n"></label><label>${isD?'Specialization':'Details / Department'}<input id="${k}s"></label><label>Experience years<input id="${k}y" type="number"></label>${isD?`<label>Consultation fee ₹<input id="${k}f" type="number"></label>`:''}<button class="btn g" onclick="addP('${k}')">+ Add</button></div></div>`;rows(k)}
function rows(k){const isD=k=='doc',f=isD?df:nf,q=($('q'+k)||{}).dataset?.q||'';
$('r'+k).innerHTML=S[k].map((p,i)=>({p,i})).filter(o=>(f=='all'||String(o.p.ok)==f)&&(o.p.n+o.p.s).toLowerCase().includes(q)).map(o=>`<tr><td>#${o.i+1}</td><td><b>${o.p.n}</b></td><td>${o.p.s}</td><td class="mono">${o.p.y} years</td>${isD?`<td class="mono"><b>₹${o.p.f}.00</b></td>`:''}<td><span class="tag ${o.p.ok?'ok':'wa'}">${o.p.ok?'Available':'On Leave'}</span></td><td><button class="sm" onclick="S['${k}'][${o.i}].ok=${o.p.ok?0:1};save();render()">${o.p.ok?'Mark Leave':'Mark Back'}</button></td></tr>`).join('')}
function addP(k){const n=$(k+'n').value.trim(),s=$(k+'s').value.trim();if(!n||!s)return toast('Enter name and details');S[k].push({n,s,y:+$(k+'y').value||0,f:k=='doc'?+$(k+'f').value||0:0,ok:1});save();render();toast('Added '+n)}
function addCol(){const n=$('cn').value.trim(),g=$('cg').value,u=Math.max(1,+$('cu').value||1);if(!n)return toast('Enter donor name');S.col.push({n,g,u,d:new Date().toISOString().slice(0,10)});S.inv.find(x=>x.g==g).u+=u;$('cn').value='';save();render();toast('Collection recorded, stock updated')}
function est(){const g=S.inv.find(x=>x.g==$('pg').value);$('est').textContent=g?`Estimated total: ₹${((+$('pu').value||0)*g.c).toLocaleString('en-IN')}.00`:''}
function addBill(){const p=$('pn').value.trim(),g=S.inv.find(x=>x.g==$('pg').value),u=+$('pu').value||0;if(!p)return toast('Enter patient name');if(u<1||u>g.u)return toast('Only '+g.u+' units available');g.u-=u;
S.bills.unshift({id:(S.bills[0]?S.bills[0].id:200)+1,p,g:g.g,u,c:g.c,m:$('pm').value,t:new Date().toISOString().slice(0,19).replace('T',' ')});$('pn').value='';save();render();toast('Bill generated, stock updated')}
function resetData(){if(confirm('Reset all data?')){S=seed();save();render()}}
const opts=()=>S.inv.map(x=>`<option>${x.g}</option>`).join('');$('cg').innerHTML=opts();$('pg').innerHTML=opts();
setInterval(()=>$('clock').textContent='🕒 '+new Date().toLocaleTimeString('en-IN'),1000);
go('dash');
</script></body></html>
"""

HERO_B64 = (
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0d"
    "Hx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4e"
    "Hh4eHh4eHh7/wAARCAHfAn0DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUF"
    "BAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVW"
    "V1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi"
    "4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAEC"
    "AxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVm"
    "Z2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq"
    "8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD7C+2xf3X/ACFRyobsh48ALwd1U+tX9N/1Tf71AEQs5V5LJgc9TU322IcbX/IVYf7jfSsj"
    "PJz0oAuySrdL5UYIbr83SovsUv8AeT8zSWAxcD6Vo0AVEmW3TynBJXrt6UpvImBUK+Tx0FVr3/j5aol+8CPWgCx9ilPO5PzNPiBt"
    "CTJzu6baujpVPU/up9TQA/7bF/df8hUTwPcMZkKhW6Z61U61p2X/AB7LQBXS3eFhK5UqvPB5qX7bF/df8hUl3/x7v9Ky/Y0AXZT9"
    "swIuNvXdTBZS/wB5PzP+FO0z70n0FXaAKouo41CFWyOOKR7hJ1MSBgzcDPSqchxI31p9qP8ASE9M0ASfYpf7yfmaljcWqmOQEk8/"
    "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"
)


PAGE = HTML.replace("__IMG__", "data:image/jpeg;base64," + HERO_B64).encode("utf-8")


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.end_headers()
        self.wfile.write(PAGE)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as server:
        url = f"http://localhost:{PORT}"
        print(f"LifeLine Blood Bank running at {url}  (Ctrl+C to stop)")
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Stopped.")
