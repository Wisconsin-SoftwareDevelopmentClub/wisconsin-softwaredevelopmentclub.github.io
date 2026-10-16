fetch("config.json").then(r => r.json())
.then(j => injectInfo(j))
.catch(e => {
    console.error("Failed to load config file: " + e);
    injectInfo({
        isShowCriticalInfo: true,
        criticalInfo: "AHHHH: Configuration file 'config.json' failed to load",
        board: [],
    });
});

function injectInfo(config) {
    const boardElement = document.querySelector("#board");
    let boardHTML = "";
    for (let b of config.board) {
    boardHTML += `
        <div class="bio"> 
            <h1>${b.name}</h1>
            <h2>${b.title}</h2>
            <img src="${b.imgURL}" alt="Image of ${b.name}">
        </div>
    `;
    }
    boardElement.innerHTML = boardHTML;
}