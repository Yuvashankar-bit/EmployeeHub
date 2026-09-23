console.log("Employee Management System Loaded");


document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.querySelector(".sidebar-toggle");
    const sidebar = document.querySelector(".sidebar");
    const closeButton = document.querySelector(".sidebar-close");

    if (!toggle || !sidebar) {
        return;
    }

    function setSidebarState(isOpen) {
        sidebar.classList.toggle("is-visible", isOpen);
        document.body.classList.toggle("sidebar-open", isOpen);
        toggle.setAttribute("aria-expanded", String(isOpen));
    }

    toggle.addEventListener("click", function () {
        const isOpen = !sidebar.classList.contains("is-visible");

        setSidebarState(isOpen);
    });

    if (closeButton) {
        closeButton.addEventListener("click", function () {
            setSidebarState(false);
        });
    }

});


function confirmDelete() {

    return confirm(
        "Are you sure you want to delete this employee?"
    );

}