const adminUsername = document.querySelector("#username").value;
const adminPassword = document.querySelector("#password").value;
const login = document.querySelector(".btn")
login.addEventListener("click", function(event) {
    
    const adminUsername = document.querySelector("#username").value;
    const adminPassword = document.querySelector("#password").value;

    const username = 'apdcl@543';
    const password = '56789';

    if (adminUsername === username && adminPassword === password){
        //Redirect to the required page        
        console.log("Welcome admin");
    }else{
        console.log("Wrong credential entered!");
    }
    
})