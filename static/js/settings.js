(function(){
window.GhostPages=window.GhostPages||{};
window.GhostPages.settings=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/version"),api.get("/diagnostics")]),v=r[0],d=r[1];
const rows=[ui.statusLine("Application version",v.version,"Backend version"),ui.statusLine("Primary model",v.model,"Chat generation"),ui.statusLine("Router model",v.router_model||"not exposed","MCP tool selection"),ui.statusLine("Knowledge index",d.faiss,"FAISS retrieval index"),ui.statusLine("Browser MCP",d.browser_mcp,"Configured integration"),ui.statusLine("Filesystem MCP",d.filesystem_mcp,"Configured integration")].join("");
return '<div class="dashboard-page settings-page">'+ui.intro("SETTINGS / CONFIGURATION","System configuration","A read-only view of the configuration exposed by the running backend.")+ui.panel("Runtime settings",rows,"settings-panel")+'<div class="notice-block motion-block"><strong>Configuration is read-only here.</strong><p>Model switching, MCP management, and memory controls do not currently have backend settings endpoints, so inactive controls are not displayed.</p></div></div>';
}catch(e){return ui.errorPanel(e);}
};})();