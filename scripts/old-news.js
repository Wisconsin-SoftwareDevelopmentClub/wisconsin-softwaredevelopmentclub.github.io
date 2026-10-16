// get the first four articles, show them. The rest, put behind an arrow
const showOld = document.createElement("button");
showOld.innerText = ">";
showOld.classList.add("more-news");
const hideOld = document.createElement("button");
hideOld.innerText = "<";
hideOld.classList.add("more-news");
hideOld.classList.add("hide");
const articles = Array.from(document.querySelectorAll(".article"));
showOld.addEventListener("click", () => toggleOld());
hideOld.addEventListener("click", () => toggleOld());
let old;
let shown;

function calcShow() {
    console.log("resized");
    // hide all articles
    articles.forEach(e => e.classList.add("hide"));
    // add one by one until overflow
    let overflow = false;
    for (let i = 0; i < articles.length; i++) {
        // add next
        articles[i].classList.toggle("hide");
        overflow = detectOverflowX(articles[i].parentNode);
        if (overflow) {
            articles[i].classList.toggle("hide");
            shown = i;
            break;
        }
    }
    old = articles.slice(shown);
    if (old.length > 0) {
        old[0].parentElement.appendChild(showOld);
        old[0].parentElement.appendChild(hideOld);
    }
}
calcShow();
window.addEventListener("resize", () => calcShow());

function toggleOld() {
    showOld.classList.toggle("hide");
    hideOld.classList.toggle("hide");
    old.forEach(e => e.classList.toggle("hide"));
}

function detectOverflowX(e) {
    const overflow = e.style.overflowX;
    e.style.overflowX = "hidden";
    const isOverflowing = e.clientWidth < e.scrollWidth;
    e.style.overflowX = overflow;
    return isOverflowing;
}
