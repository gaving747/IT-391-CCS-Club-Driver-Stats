
document.addEventListener("DOMContentLoaded", () => {
    const links = [
        {text: "Home", href : "driver_status_logged_in_home.html"},
        {text: "Race Schedule", href : "schedule_race_logged_in.html"},
        {text: "Garage", href : "garage.html"},
        {text: "Stats", href : "stats_logged_in.html"},
        {text: "Personal Stats", href : "personal_stats.html"},
        {text: "Weather", href : "weather.html"},
    ];

    const taskbar = document.createElement("div");
    taskbar.className = "taskbar";

    links.forEach(link=>{
    const a = document.createElement("a");
    a.textContent =link.text;
    a.href = link.href;

    if(link.text === "Profile"){
        a.className = "right";
    }

        taskbar.appendChild(a);
    });

    const profileDropDown = document.createElement("div");
    profileDropDown.className = "dropdown right";

    const profileButton = document.createElement("button");
    profileButton.className = "dropbtn";
    profileButton.textContent = "Profile";

    const dropdownContent = document.createElement("div");
    dropdownContent.className = "dropdown-content";
    
    const profileLink = document.createElement("a");
    profileLink.textContent = "View Profile";
    profileLink.href = "driver_status_home.html";//change this

    const garageLink = document.createElement("a");
    garageLink.textContent = "Garage";
    garageLink.href = "garage.html";//change this

    const signOutLink = document.createElement("a");
    signOutLink.textContent = "Sign Out";
    signOutLink.href = "index.html";//change this

    dropdownContent.appendChild(profileLink);
    dropdownContent.appendChild(garageLink);
    dropdownContent.appendChild(signOutLink);

    profileDropDown.appendChild(profileButton);
    profileDropDown.appendChild(dropdownContent);
    taskbar.appendChild(profileDropDown);



        document.getElementById("taskbar-container").appendChild(taskbar);
});


        