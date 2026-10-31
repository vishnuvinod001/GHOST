(function () {
window.GhostPages=window.GhostPages||{};
window.GhostPages.overview=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/stats"),api.get("/version"),api.get("/diagnostics")]),s=r[0],v=r[1],d=r[2];
const brief=[ui.statusLine("Backend",d.backend||"unknown","FastAPI service"),ui.statusLine("Knowledge index",d.faiss||"unknown",s.chunk_count+" stored chunks"),ui.statusLine("Browser MCP",d.browser_mcp||"unknown","Tool configuration"),ui.statusLine("Filesystem MCP",d.filesystem_mcp||"unknown","Tool configuration")].join("");
return '<div class="dashboard-page overview-page">'+ui.intro("GHOST / WORKSPACE","Your workspace, at a glance.","A live snapshot of the data currently stored by GHOST.")+'<section class="metrics-grid">'+ui.metric("Documents",s.pdf_count,"Indexed PDF sources")+ui.metric("Memories",s.memory_count,"Saved memory entries")+ui.metric("Tasks",s.task_count,s.active_task_count+" active")+ui.metric("Knowledge chunks",s.chunk_count,s.embedding_count+" embeddings")+'</section>'+ui.panel("System snapshot",brief,"system-snapshot")+'<section class="overview-footer motion-block"><span>Running '+ui.escapeHTML(v.version)+'</span><span>Primary model · '+ui.escapeHTML(v.model)+'</span></section></div>';
}catch(e){return ui.errorPanel(e);}
};})();