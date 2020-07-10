
try {
    document.getElementById("view-older-projects").addEventListener('click', ev => {
        hideShowOldProjects()
    });
    
    document.getElementById('id_project_end').addEventListener('change', ev => {
        greaterThanToday(ev.target)
    })
    document.getElementById("show-add-member-link").addEventListener('click', ev =>{
        ev.preventDefault();
        hideShowAddTeamForm();
        document.getElementById("hide-add-member-link").style.display = 'block';
        ev.target.style.display = 'none';
    })
    
    document.getElementById("hide-add-member-link").addEventListener('click', ev =>{
        ev.preventDefault();
        hideShowAddTeamForm();
        document.getElementById("show-add-member-link").style.display = 'block';
        ev.target.style.display = 'none';
    })
} catch (error) {
    
}

/** the function below  ensures that the end date is greater than today*/
function greaterThanToday(targetElement){
    console.log("Hello")
    var selectedDate = new Date(targetElement.value);
    var today = new Date();
    if(selectedDate < today){
        console.log("I tested");
        targetElement.value -= targetElement.empty
        targetElement.style.borderColor = "red";
        alert("The date must be greator or equal to today");
    }else{
        targetElement.style.borderColor = "black";
    }
}

var id_team = document.querySelectorAll('#id_team')
var ln = id_team.length
while(ln--){
    id_team[ln].className = "form-active";
}
// document.getElementById("id-team").className = "form-active";



function hideShowAddTeamForm(){
    var form = document.getElementById('add-team-member-form');
    console.log(form.style.display);
    if(form.style.display == 'none'){
        form.style.display = 'block';
    }else{
        form.style.display = 'none';
    }
}
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