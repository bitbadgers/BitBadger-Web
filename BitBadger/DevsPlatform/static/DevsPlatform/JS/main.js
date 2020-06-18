document.getElementById("view-older-projects").addEventListener('click', ev => {
    hideShowOldProjects()
});

function hideShowOldProjects(){
    var oldProject = document.getElementById("old-projects");
    var button = document.getElementById("view-older-projects")
    if(oldProject.style.display != 'none'){
        oldProject.style.display = 'none';
        button.innerHTML = "View older projects"
    }else{
        oldProject.style.display = 'block';
        button.innerHTML = "Hide older projects"
    }

}