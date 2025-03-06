let btnChange = document.getElementById("btnSidebarChange");
function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    btnChange.classList.remove("openSidebar");

    let menu_items = document.querySelectorAll("span");
    menu_items.forEach((item) => {
        item.classList.remove("display-none");
    });
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "78px";
    document.getElementById("main").style.marginLeft= "78px";
    btnChange.classList.add("openSidebar");

    let menu_items = document.querySelectorAll("span");
    menu_items.forEach((item) => {
        item.classList.add("display-none");
    });
}

function sidebarChange() {
    if(btnChange.classList.contains("openSidebar")) {
        openNav();
    }
    else {
        closeNav();
    }
}