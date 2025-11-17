const reviewBtn = document.getElementById("reviewBtn");
const codePreview = document.getElementById("codePreview");
const themeToggle = document.getElementById("themeToggle");

// Theme handling: persist choice in localStorage and set `data-theme` on <html>
function setTheme(theme){
    if(theme === 'light'){
        document.documentElement.setAttribute('data-theme','light');
        if(themeToggle) themeToggle.textContent = '🌙';
    } else {
        document.documentElement.removeAttribute('data-theme');
        if(themeToggle) themeToggle.textContent = '☀️';
    }
    try{ localStorage.setItem('ui-theme', theme); }catch(e){}
}

function initTheme(){
    try{
        const saved = localStorage.getItem('ui-theme');
        if(saved) { setTheme(saved); return; }
    }catch(e){}
    const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
    setTheme(prefersLight? 'light':'dark');
}

if(themeToggle){
    themeToggle.addEventListener('click', ()=>{
        const cur = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
        setTheme(cur === 'light' ? 'dark' : 'light');
    });
}

initTheme();

reviewBtn.addEventListener("click", async () => {
    const code = document.getElementById("codeInput").value;
    codePreview.textContent = code;
    Prism.highlightElement(codePreview);

    if (!code.trim()) { alert("Please enter some code!"); return; }

    try {
        const response = await fetch("http://127.0.0.1:8000/review", {
            method:"POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({code})
        });

        if(!response.ok) throw new Error(`Error: ${response.status}`);
        const data = await response.json();

        document.getElementById("score").innerText = data.quality_score;

        const bugsList = document.getElementById("bugs");
        bugsList.innerHTML = "";
        data.bugs.forEach(b => { let li=document.createElement("li"); li.innerText=b; bugsList.appendChild(li); });

        const securityList = document.getElementById("security");
        securityList.innerHTML = "";
        data.security_issues.forEach(s => { let li=document.createElement("li"); li.innerText=s; securityList.appendChild(li); });

        const suggestionsDiv = document.getElementById("suggestions");
        suggestionsDiv.innerHTML = "";
        data.suggestions.forEach((s,i)=>{
            const sug=document.createElement("div"); sug.className="suggestion"; sug.innerText=`Suggestion ${i+1} (click to expand)`;
            const content=document.createElement("div"); content.className="suggestion-content"; content.innerText=s;
            sug.addEventListener("click",()=>{ content.style.display = content.style.display==="block"?"none":"block"; });
            suggestionsDiv.appendChild(sug); suggestionsDiv.appendChild(content);
        });

        document.getElementById("docstring").innerText=data.docstring;
        document.getElementById("results").classList.remove("hidden");

    } catch(err) { alert("Failed to get review: "+err.message); }
});
