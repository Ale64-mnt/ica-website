
(function(){
  var list=document.getElementById('newsList');
  if(!list) return;
  var src=list.getAttribute('data-news-src');
  fetch(src).then(r=>r.json()).then(itms=>{
    var items = itms.items || itms;
    list.innerHTML = items.map(it=>{
      const d = it.date? new Date(it.date).toLocaleDateString(document.documentElement.lang||'it-IT',{year:'numeric',month:'short',day:'2-digit'}) : '';
      const img = it.image? `<img src="${it.image}" alt="" style="max-width:100%;border-radius:10px;margin:8px 0">` : '';
      const vid = it.video? `<p><a href="${it.video}" target="_blank" rel="noopener">Guarda il video</a></p>` : '';
      const link = it.link? `<p><a href="${it.link}" target="_blank" rel="noopener">Leggi →</a></p>` : '';
      return `<article class="news-card"><h3>${it.title||''}</h3><div class="meta">${d}${it.author?(' · '+it.author):''}</div>${img}<p>${it.summary||''}</p>${vid}${link}</article>`;
    }).join('');
  }).catch(()=>{ list.innerHTML='<p>Impossibile caricare le news.</p>'; });
})();
