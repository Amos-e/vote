let selector = document.querySelector("select");
let voteBtn = document.querySelector("#choose-btn");
let modalContainer = document.querySelector("#modal");

fetch("/vote/members")

.then((response)=>{
    return response.json();
})

.then((data)=>{
    members = JSON.parse(data);

    for(member of members) {
        option = document.createElement("option");
        option.setAttribute("value", member['member__code']);
        option.innerText = `${member['member__code']} \t ${member['member__full_names']}`;
        selector.appendChild(option);
    }

})


let voterImageContainer = document.querySelector("#voter-image");
let voteImageContainer = document.querySelector("#vote-image");


selector.addEventListener("change", (event)=>{
    let code = selector.value;

    fetch("/vote/api", {
        method: "POST",
        body: JSON.stringify({
            operation: "search_member",
            search_term: code,
        }),
        headers: {
            "Content-type": "application/json charset=UTF-8"
        }
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log(data);
        member = JSON.parse(data);
        image = `<img src=${member['image']} class=rounded-full>`;
        voterImageContainer.innerHTML = image;
    })

})

let innerModal = document.querySelector("#modal-inner");
let voteExistsError = document.querySelector("#vote-exists-error");
let voteDetails = document.querySelector("#vote-details");

let loading = document.querySelector('#loading');
console.log(loading);

voteBtn.addEventListener("click", function(event){
    
    console.log("clicked");
    modalContainer.classList.replace("hidden", "flex");
    innerModal.classList.replace("hidden", "flex");
    loading.classList.replace("hidden", "flex");

    setTimeout(()=>{

        modalContainer.classList.replace("flex", "hidden");
        innerModal.classList.replace("flex", "hidden");
        loading.classList.replace("flex", "hidden");


        let code = selector.value;
        
        fetch("/vote/cast-vote", {
            method: "POST",

            body: JSON.stringify({
                member_code: code,
            }),

            headers: {
                "Content-type": "application/json charset=UTF-8"
            }
        })
        .then((response)=>{
            return response.json();
        })
        .then((json)=>{
            
            let data = JSON.parse(json);

            if (data.status == 200) {
                let img = `<img src=${data["vote_image"]} class='rounded-full'>`;
                voteImageContainer.innerHTML = img;
                voteDetails.querySelector('.code').innerText = data["vote_code"];
                voteDetails.querySelector('.name').innerText = data["vote_name"];
            } 

            else if (data.status == 403) {
                modalContainer.classList.replace("hidden", "flex");
                innerModal.classList.replace("hidden", "flex");
                voteExistsError.classList.replace("hidden", "flex");
            }
        })
    }, 2000);

});

//Some UI Configuration

let searchForm = document.querySelector("form#search-name-form");
let searchMemberInput = document.querySelector("input#search-member-input");
let searchMemberBtn = document.querySelector("button#search-member-btn");

searchForm.addEventListener("submit", (event=>{
    
    event.preventDefault();

    let name = searchMemberInput.value;

    fetch("/vote/api", {
        method: "POST",

        body: JSON.stringify({
            "operation": "search_members",
            "search_term": name,
        }),

        headers: {
            "Content-type": "application/json charset=UTF-8"
        }
    })
    
    .then((response)=>{
        return response.json();
    })

    .then((data)=>{
        searchMemberInput.value = "";
        members = JSON.parse(data);

        let html = `<option value='Select Member'>Select Member</option>`;

        for (member of members) {
            html += `<option value=${member["member__code"]}>${member["member__code"]} ${member["member__full_names"]}</option>`
        }
        selector.innerHTML = html;
    })

}))


let closeModalBtns = Array.from(document.querySelectorAll(".close-modal"));

closeModalBtns.forEach((btn)=>{
    btn.addEventListener("click", (event)=>{
        modalContainer.classList.replace("flex", "hidden");
        voteExistsError.classList.replace("flex", "hidden");
    })
})


