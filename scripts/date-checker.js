const due = document.querySelectorAll("[due]");
due.forEach(e => {
    const date = Date.parse(e.getAttribute("due"));
    if (date <= Date.now()) {
        const fade = "0.2";
        const closed = document.createElement("div");
        closed.classList.add("closed");
        closed.innerText = "CLOSED";
        closed.style.backgroundColor = "grey";
        e.style.opacity = fade;
        e.style.position = "relative";
        e.appendChild(closed);
        e.addEventListener("mouseover", () => {
            e.style.opacity = "0.7";
            closed.style.opacity = fade;
            closed.style.zIndex = "-1";
        });
        e.addEventListener("mouseleave", () => {
            e.style.opacity = fade;
            closed.style.opacity = "1";
            closed.style.zIndex = "10";
        });
    }
});