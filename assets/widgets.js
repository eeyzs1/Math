"use strict";
const $=id=>document.getElementById(id);
function path(points,color,dash=''){return `<polyline points="${points.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}"/>`;}
const axes=(x=65,y=270)=>`<path d="M25 ${y}H580M${x} 15V290" stroke="#5f7470" fill="none"/><text x="565" y="300">x</text>`;
function render(){
 if(!$('h'))return;
 let h=+$('h').value, pts=[];const xy=(x,y)=>[65+x*200,270-y*55];
 for(let x=0;x<=2.21;x+=.03)pts.push(xy(x,x*x));
 $('derivative-svg').innerHTML=axes()+path(pts,'#086a67')+path([xy(0,-1),xy(2.3,3.6)],'#697c78','6 5')+path([xy(.5,1-(2+h)*.5),xy(2,1+(2+h))],'#bd6029')+[xy(1,1),xy(1+h,(1+h)**2)].map(p=>`<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="#bd6029"/>`).join('')+'<text x="280" y="220">固定点 (1,1)</text>';
 $('h-out').textContent=`h=${h.toFixed(2)}；割线斜率=${(2+h).toFixed(2)}；切线斜率=2`;
 let a=+$('a').value, x=300, y=250,s=90;
 $('linear-svg').innerHTML=axes(x,y)+`<rect x="300" y="160" width="90" height="90" fill="none" stroke="#677c77" stroke-dasharray="6 4"/><rect x="${Math.min(x,x+a*s)}" y="160" width="${Math.abs(a*s)}" height="90" fill="#147d7866" stroke="#086a67"/><text x="30" y="35">单位边长对应 90 像素</text>`;
 $('a-out').textContent=`a=${a.toFixed(1)}；det(A)=${a.toFixed(1)}；面积=${Math.abs(a).toFixed(1)}`;
 let p=+$('p').value, bars='',sum=0;function choose(n,k){let c=1;for(let j=1;j<=k;j++)c=c*(n-j+1)/j;return c;}
 for(let k=0;k<=10;k++){let v=choose(10,k)*p**k*(1-p)**(10-k);sum+=v;bars+=`<rect x="${40+k*48}" y="${270-v*230}" width="32" height="${v*230}" fill="#086a67"><title>k=${k}，概率=${v.toFixed(5)}</title></rect><text x="${45+k*48}" y="295">${k}</text>`;}
 $('prob-svg').innerHTML=bars+'<text x="30" y="25">概率（纵轴 0–1）；横轴：正面次数 k</text>';
 $('p-out').textContent=`p=${p.toFixed(2)}；期望=${(10*p).toFixed(2)}；方差=${(10*p*(1-p)).toFixed(2)}；概率和=${sum.toFixed(6)}`;
 let step=+$('step').value;if(!(step>0))step=0.1;let arr=[[0,1]],v=1;for(let j=1;j*step<=10+1e-9;j++){v*=1-2*step;arr.push([j*step,v]);}
 const scale=Math.max(1,...arr.map(x=>Math.abs(x[1]))),pos=(t,v)=>[45+t*52,155-v/scale*120];let exact=[];for(let t=0;t<=10;t+=.05)exact.push(pos(t,Math.exp(-2*t)));
 $('euler-svg').innerHTML=axes(45,155)+path(exact,'#086a67')+path(arr.map(([t,v])=>pos(t,v)),'#bd6029')+`<text x="40" y="25">纵轴范围约 ±${scale.toFixed(2)}；横轴 t=0…10</text>`;
 $('step-out').textContent=`h=${step.toFixed(1)}；单步倍率=${(1-2*step).toFixed(2)}；末步 t=${arr.at(-1)[0].toFixed(1)}，y≈${v.toFixed(5)}`;
 if($('n')){const nn=+$('n').value,groups=2000,means=[];for(let g=0;g<groups;g++){let s=0;for(let i=0;i<nn;i++)s+=Math.random()<.5?0:1;means.push(s/nn);}
  const bins=40,hist=new Array(bins).fill(0);for(const m of means)hist[Math.min(bins-1,Math.floor(m*bins))]++;
  const mx=Math.max(...hist),bw=540/bins,sd=Math.sqrt(.25/nn);let bars='';hist.forEach((h,i)=>{bars+=`<rect x="${30+i*bw}" y="${270-h/mx*230}" width="${bw-2}" height="${h/mx*230}" fill="#086a67"><title>区间 ${(i/bins).toFixed(2)}–${((i+1)/bins).toFixed(2)}：${h} 组</title></rect>`});
  const pk=groups*(1/bins)/(sd*Math.sqrt(2*Math.PI)),curve=[];for(let i=0;i<=120;i++){const x=i/120,d=groups*(1/bins)/(sd*Math.sqrt(2*Math.PI))*Math.exp(-((x-.5)**2)/(2*sd*sd));curve.push([30+x*540,270-d/pk*230]);}
  $('clt-svg').innerHTML=axes(30,270)+path(curve,'#5f7470','6 5')+bars+'<text x="30" y="25">正面比例直方图（2000 组）与理论正态密度（虚线）</text>';
  const mo=means.reduce((a,b)=>a+b,0)/groups,ms=Math.sqrt(means.reduce((a,b)=>a+(b-mo)**2,0)/groups);
  $('n-out').textContent=`n=${nn}；理论 σ=√(0.25/n)=${sd.toFixed(4)}；样本 σ=${ms.toFixed(4)}；样本均值≈${mo.toFixed(3)}`;}
 if($('x0')){const f=x=>x**3-2*x+2,fp=x=>3*x*x-2,px=v=>30+(v+2.5)/5*540,py=v=>270-(Math.max(-0.9,Math.min(8,v))/8)*230;
  let x=+$('x0').value,lines='',dots='',list=[x];for(let i=0;i<8&&Math.abs(x)<=3;i++){const y=f(x),d=fp(x);if(Math.abs(d)<1e-6)break;const xn=x-y/d;lines+=path([[px(x),py(y)],[px(xn),270]],'#bd6029','4 4');dots+=`<circle cx="${px(x)}" cy="${py(y)}" r="5" fill="#bd6029"/>`;x=xn;list.push(x);}
  const curve=[];for(let t=-2.5;t<=2.51;t+=.05)curve.push([px(t),py(f(t))]);
  $('newton-svg').innerHTML=axes(300,270)+path(curve,'#086a67')+lines+dots+'<text x="30" y="25">f(x)=x³−2x+2 的牛顿迭代：切线零点作为下一步</text>';
  const tail=list.slice(0,5).map(v=>v.toFixed(3)).join(' → '),y4=list.length>4?f(list[4]):f(list[list.length-1]);
  $('x0-out').textContent=`迭代：${tail}${list.length>5?' → …':''}；f(x₄)=${y4.toFixed(4)}`;}
}
for(const el of document.querySelectorAll('input[type=range]'))el.addEventListener('input',render);render();
// 打印时自动展开全部折叠解析，打印后还原（新版浏览器已不受 details>*{display:block} 影响）。
let printed=[];
addEventListener('beforeprint',()=>{printed=[...document.querySelectorAll('details:not([open])')];printed.forEach(d=>d.open=true)});
addEventListener('afterprint',()=>{printed.forEach(d=>d.open=false);printed=[]});
