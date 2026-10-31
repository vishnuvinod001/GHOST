(function(){
window.GhostPages=window.GhostPages||{};
window.GhostPages.tasks=async function(){
const api=window.GhostAPI,ui=window.GhostUI;
try{
const r=await Promise.all([api.get("/tasks"),api.get("/stats")]),tasks=r[0],s=r[1];
const list=tasks.length?'<ul class="task-list">'+tasks.map(t=>'<li class="task-row'+(t.completed?' is-complete':'')+'"><label class="task-label"><input type="checkbox" data-action="complete-task" data-id="'+t.id+'"'+(t.completed?' checked':'')+'><span>'+ui.escapeHTML(t.task)+'</span></label><button class="icon-button" type="button" data-action="delete-task" data-id="'+t.id+'" aria-label="Delete task">Delete</button></li>').join("")+'</ul>':ui.emptyState("No tasks yet","Add a task above and it will be saved to GHOST's task store.");
const form='<form id="task-form" class="task-create-form motion-block"><label class="visually-hidden" for="new-task">New task</label><input id="new-task" name="task" type="text" maxlength="500" placeholder="Add a task..." required><button class="button button-primary" type="submit">Add task</button></form>';
return '<div class="dashboard-page tasks-page">'+ui.intro("TASKS / PLANNING","Task board","A task list backed by GHOST's SQLite task store.")+'<section class="metrics-grid">'+ui.metric("All tasks",s.task_count,"Stored tasks")+ui.metric("Active",s.active_task_count,"Not completed")+ui.metric("Completed",s.completed_task_count,"Marked complete")+'</section>'+form+ui.panel("Your tasks",list,"tasks-panel")+'</div>';
}catch(e){return ui.errorPanel(e);}
};})();