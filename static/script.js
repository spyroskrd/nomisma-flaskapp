const chatIcon = document.getElementById("chat-icon");
    const chatBox = document.getElementById("chat-box");
    const chatInput = document.getElementById("chat-input");
    const chatLog = document.getElementById("chat-log");

    chatIcon.onclick = () => {
      chatBox.style.display = chatBox.style.display === "flex" ? "none" : "flex";
    };

    chatInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter" && chatInput.value.trim() !== "") {
        const userMsg = chatInput.value;
        chatLog.innerHTML += `<div><strong>You:</strong> ${userMsg}</div>`;
        chatInput.value = "";

        fetch("/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: userMsg })
        })
        .then(res => res.json())
        .then(data => {
          chatLog.innerHTML += `<div><strong>Obolus:</strong> ${data.response}</div>`;
          chatLog.scrollTop = chatLog.scrollHeight;
        })
        .catch(() => {
          chatLog.innerHTML += `<div style="color:red;">Error getting response.</div>`;
        });
      }
    });

//kodikas gia to koympi darkmode, TO EGRAPSA MONOS!!
let darkmode = localStorage.getItem('darkmode')
const themeSwitch = document.getElementById('theme-switch')

const enableDarkmode = () => {
    document.documentElement.classList.add('darkmode')
    localStorage.setItem('darkmode', 'active')
}

const disableDarkmode = () => {
    document.documentElement.classList.remove('darkmode')
    localStorage.setItem('darkmode', null)
}
//an apoo th mnhmh einai enabled to darkmode, na einai etsi otan aniogei 
if(darkmode === "active") enableDarkmode()

//an darkmode=active kane ayto, allios kane ekeino (if statement)
themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem('darkmode')
    darkmode !== "active" ? enableDarkmode () : disableDarkmode()
})