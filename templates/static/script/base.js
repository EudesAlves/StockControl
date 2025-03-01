function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("btnOpenMenu").style.display = "none";

    let menu_items = document.querySelectorAll("span");
    menu_items.forEach((item) => {
        item.classList.remove("display-none");
    });
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "78px";
    document.getElementById("main").style.marginLeft= "78px";
    document.getElementById("btnOpenMenu").style.display = "block";

    let menu_items = document.querySelectorAll("span");
    menu_items.forEach((item) => {
        item.classList.add("display-none");
    });
}

//openNav();