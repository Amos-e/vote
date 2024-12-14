window.onload = () => {let modalContainer = document.querySelector("#modal");

let openNewPollBtn = document.querySelector("button#new-poll");
let createPollBtn = document.querySelector("button#create-poll");
let createPollContainer = document.querySelector("#create-poll-container");

openNewPollBtn.addEventListener("click", (event)=>{
    

    if (openNewPollBtn.classList.contains("inactive")) {
        modalContainer.classList.replace("hidden", "flex");
        createPollContainer.classList.replace("hidden", "flex");
        openNewPollBtn.classList.replace("inactive", "active");
    } 
    else {
        modalContainer.classList.replace("flex", "hidden");
        createPollContainer.classList.replace("flex", "hidden");
        openNewPollBtn.classList.replace("active", "inactive");
    }

})

createPollBtn.addEventListener("click", (event)=>{
    let title = createPollContainer.querySelector('[name=title]').value;
    let description = createPollContainer.querySelector('textarea').value;

    fetch("/vote/api", {
        method: "POST",
        
        body: JSON.stringify({
            operation: "create_poll",
            title: title,
            description: description,

        }),

        headers: {
            "Content-type": "application/json charset=UTF-8"
        }
    })
    .then((response)=>{
        return response.json();
    })
    .then((json)=>{
        data = JSON.parse(json);
        if (data['status'] == 200) {
            location.reload();
        }
    })
})
}