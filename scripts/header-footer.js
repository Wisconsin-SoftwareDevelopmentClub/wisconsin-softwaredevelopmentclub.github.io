// This was my solution to not repeatedly adding the header and footer to each page.
// All pages simply need to include the style.css sheet and this script, then put
// the corresponding element with id matching one of these. See bottom of script.
// I call the header the banner here

fetch("config.json").then(r => r.json())
    .then(j => injectHeaders(j))
    .catch(e => {
        console.error("Failed to load config file: " + e);
        injectHeaders({
            isShowCriticalInfo: true,
            criticalInfo: "AHHHH: Configuration file 'config.json' failed to load",
            board: [],
        });
    });

// toggle the critical section
function injectHeaders(config) {
    const bannerHTML = `
    <div id="banner">
<a href="index.html"><img id="logo" src="images/sdc-icon.png"/></a>
<div id="header" class="flex text-white" style="justify-content: space-between; width: 100%;">
    <h1 style="margin: auto 0;"><div>UW-Madison</div>Software Development Club</h1>
    <div id="links">
        <div id="ext-links">
            <a class="ext-link" id="project-link" href="${config.projectLink}">Project GitHub
                <img src="images/github-icon.png"/>
            </a>
            <a href="${config.discordLink}" class="ext-link" id="discord-link">Discord
                <img src="images/discord-icon.png"/>
            </a>
        </div>
        <div id="int-links">
            <a href="index.html" class="int-link">Home</a>
            <a href="project.html" class="int-link">Projects</a>
            <a href="info.html" class="int-link">About</a>
        </div>
    </div>
</div>
</div>
`;

    let boardHTML = "";
    let contactHTML = "";
    for (let b of config.board) {
        boardHTML += "<li>" + b.name + " - " + b.title + "</li>";
        if (b.isContact)
            contactHTML += "<li>Email " + b.email + ", our " + b.title + "</li>";
    }

    const footerHTML = `
    <div id="footer">
    <div id="info">
        <div>
            <h1>
                Club Info
            </h1>
            <ul>
                <li>
                    If you are interested in projects, check out our project
                    <a href="${config.projectLink}">GitHub</a>
                </li>
                <li>Meetings for Spring 2022 are every other Wednesday, starting 2/6.</li>
                <li>Project meetings are the Sunday before the Wednesday meeting.</li>
                <li>Website maintained by VP of Engineering</li>
            </ul>
        </div>
        <div>
            <h1>
                Current Board (${config.semester})
            </h1>
            <ul>
            ${boardHTML}
            </ul>
        </div>
    </div>

        <div id="contact">
<div>
            <h1>
                Contact Us
            </h1>
            <ul>
                <li>Message us on <a href="${config.discordLink}">discord</a></li>
                <li>Message us on <a href="${config.linkedInLink}">LinkedIn</a></li>
                ${contactHTML}
            </ul>
        </div>
        </div>
</div>
        `;

    const body = document.querySelector("body");
    const banner = document.createElement("div");
    banner.innerHTML = bannerHTML;
    const footer = document.createElement("div");
    footer.innerHTML = footerHTML;
    const critical = document.createElement("div");
    critical.innerHTML = `<div id="critical"><p>${config.criticalInfo}</p></div>`;

    body.insertBefore(banner, body.firstChild);
    body.insertBefore(critical, body.children[1]);
    body.append(footer);
    if (!config.isShowCriticalInfo)
        critical.style.display = "none";

}