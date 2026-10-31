(function(){
window.GhostPages=window.GhostPages||{};
window.GhostPages.files=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/documents"),api.get("/stats")]),docs=r[0],s=r[1];
const list=docs.length?'<ul class="resource-list file-list">'+docs.map(n=>{const safe=ui.escapeHTML(n);return '<li><span class="file-glyph">PDF</span><span class="resource-name">'+safe+'</span><button class="icon-button" type="button" data-action="delete-document" data-filename="'+safe+'" aria-label="Delete '+safe+'">Delete</button></li>';}).join("")+'</ul>':ui.emptyState("Your document library is empty","PDFs uploaded here are indexed for GHOST's knowledge retrieval.");
const upload='<form id="pdf-upload-form" class="upload-form motion-block"><div><strong>Add a PDF</strong><p>Upload a document to the knowledge base.</p></div><input type="file" name="file" accept="application/pdf,.pdf" required aria-label="Choose PDF file"><button class="button button-primary" type="submit">Upload PDF</button></form>';
return '<div class="dashboard-page files-page">'+ui.intro("FILES / DOCUMENTS","Document library","Manage the PDFs stored in GHOST's searchable knowledge base.")+'<section class="metrics-grid">'+ui.metric("Documents",s.pdf_count,"Indexed PDF sources")+ui.metric("Chunks",s.chunk_count,"Searchable text segments")+ui.metric("Embeddings",s.embedding_count,"Stored vectors")+'</section>'+upload+ui.panel("Stored documents",list,"document-panel")+'</div>';
}catch(e){return ui.errorPanel(e);}
};})();