(function(){
window.GhostPages=window.GhostPages||{};
window.GhostPages.knowledge=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/stats"),api.get("/documents"),api.get("/diagnostics")]),s=r[0],docs=r[1],d=r[2];
const list=docs.length?'<ul class="resource-list">'+docs.map(n=>'<li><span class="file-glyph">PDF</span><span class="resource-name">'+ui.escapeHTML(n)+'</span><span class="resource-meta">Indexed</span></li>').join("")+'</ul>':ui.emptyState("No indexed documents yet","Upload a PDF from the Files page to start building the knowledge base.");
const state=[ui.statusLine("FAISS index",d.faiss||"unknown","Vector similarity index"),ui.statusLine("Stored chunks",s.chunk_count,"Text segments in SQLite"),ui.statusLine("Stored embeddings",s.embedding_count,"Embedding records in SQLite")].join("");
return '<div class="dashboard-page knowledge-page">'+ui.intro("KNOWLEDGE / RETRIEVAL","Knowledge base","Explore the documents and indexed data GHOST can retrieve during a conversation.")+'<section class="metrics-grid">'+ui.metric("Documents",s.pdf_count,"Distinct PDF sources")+ui.metric("Chunks",s.chunk_count,"Stored text segments")+ui.metric("Embeddings",s.embedding_count,"Persisted vectors")+'</section>'+ui.panel("Indexed documents",list,"document-panel")+ui.panel("Index status",state,"index-status")+'</div>';
}catch(e){return ui.errorPanel(e);}
};})();