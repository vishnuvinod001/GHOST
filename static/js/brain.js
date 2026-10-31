(function(){
window.GhostPages=window.GhostPages||{};
window.GhostPages.brain=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/memories"),api.get("/stats")]),memories=r[0],s=r[1],categories={};
memories.forEach(m=>{categories[m.type]=(categories[m.type]||0)+1;});
const cats=Object.keys(categories).length?'<ul class="category-list">'+Object.keys(categories).sort().map(k=>'<li><span>'+ui.escapeHTML(k)+'</span><strong>'+categories[k]+'</strong></li>').join("")+'</ul>':ui.emptyState("No memory categories","Categories appear as GHOST stores memories.");
const items=memories.length?'<ul class="memory-list">'+memories.map(m=>'<li><span class="memory-type">'+ui.escapeHTML(m.type)+'</span><p>'+ui.escapeHTML(m.value)+'</p></li>').join("")+'</ul>':ui.emptyState("No saved memories","GHOST has not stored any long-term memories yet.");
return '<div class="dashboard-page brain-page">'+ui.intro("BRAIN / MEMORY","Memory","Browse the long-term memory records currently stored by GHOST.")+'<section class="metrics-grid">'+ui.metric("Memories",s.memory_count,"Persisted entries")+ui.metric("Documents",s.pdf_count,"Knowledge sources")+ui.metric("Knowledge chunks",s.chunk_count,"Retrieval context")+'</section><div class="two-column-layout">'+ui.panel("Memory categories",cats,"category-panel")+ui.panel("Saved memories",items,"memory-panel")+'</div></div>';
}catch(e){return ui.errorPanel(e);}
};})();