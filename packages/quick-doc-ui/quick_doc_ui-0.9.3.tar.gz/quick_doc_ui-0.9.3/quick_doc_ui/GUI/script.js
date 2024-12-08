window.onload = function () {
    window.resizeTo(500, 800); 
    info = getInfo()
    console.log(info.languages)
}

async function getInfo() {
    try {
        const info = await eel.get_info()();  // Вызов функции и ожидание результата
        console.log(info);  // Выводим полученные данные в консоль
        console.log("Languages:", info.languages);
        console.log("Versions:", info.versions);

        add_languages(info.languages)
        add_gpt(info.versions)
    } catch (error) {
        console.error("Error:", error);  // Обработка ошибок
    }
}

function add_languages(langs){
    parent = document.querySelector(".input .current .left")
    for (i in langs){
        language = document.createElement("div")
        language.classList.add("language");

        name_class = document.createElement("div");
        name_class.classList.add("name");
        
        p_text = document.createElement("p");
        p_text.innerHTML = langs[i]

        name_class.appendChild(p_text)
        language.appendChild(name_class)

        tick_class = document.createElement("div");
        tick_class.classList.add("tick");

        tick = document.createElement("input");
        tick.setAttribute("type", "checkbox")
        tick.setAttribute("lang", langs[i])


        tick_class.appendChild(tick)
        language.appendChild(tick_class)

        parent.appendChild(language)
    }
}

function add_gpt(gpt_vesions){
    parent = document.querySelector(".input .current .right select")
    for (i in gpt_vesions){
        op = document.createElement("option")
        op.setAttribute("value", gpt_vesions[i])
        op.innerHTML = gpt_vesions[i]

        parent.appendChild(op)
    }
}

function gen_doc(){
    name_project = document.getElementById("name").value
    path = document.getElementById("path").value
    ignore = document.getElementById("ignore").value
    g_prompt = document.getElementById("g_prompt").value
    d_prompt = document.getElementById("d_prompt").value

    gpt = document.getElementById("gpt").value
    languages = get_lang()

    eel.gen_doc(name_project, path, ignore, languages, g_prompt, d_prompt, gpt)


}

function get_lang(){
    inputs = document.querySelectorAll(".input .current .left .language .tick input")
    ex = []
    for (i in inputs){
        if (inputs[i].checked){
            ex.push(inputs[i].lang)
        }
    }

    return ex
}