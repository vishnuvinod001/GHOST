(function(){
window.GhostPages=window.GhostPages||{};
window.GhostPages.developer=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/diagnostics"),api.get("/version"),api.get("/stats")]),d=r[0],v=r[1],s=r[2];
const rows=[ui.statusLine("FastAPI backend",d.backend,"Application service"),ui.statusLine("Primary model",v.model,"Configured chat model"),ui.statusLine("Router model",v.router_model||"not exposed","Configured tool-routing model"),ui.statusLine("FAISS",d.faiss,s.chunk_count+" indexed chunks"),ui.statusLine("Browser MCP",d.browser_mcp,"Configuration status, not a live health probe"),ui.statusLine("Filesystem MCP",d.filesystem_mcp,"Configuration status, not a live health probe")].join("");
return '<div class="dashboard-page developer-page">'+ui.intro("DEVELOPER / DIAGNOSTICS","System diagnostics","Runtime information exposed by the current GHOST backend.")+'<section class="metrics-grid">'+ui.metric("Documents",s.pdf_count,"Indexed sources")+ui.metric("Chunks",s.chunk_count,"Stored segments")+ui.metric("Embeddings",s.embedding_count,"Persisted vectors")+ui.metric("Tasks",s.task_count,"Stored records")+'</section>'+ui.panel("Runtime configuration",rows,"diagnostics-panel")+'<p class="subtle-note motion-block">MCP labels report configured integrations only. A live server health check is not currently exposed by the backend.</p></div>';
}catch(e){return ui.errorPanel(e);}
};})();