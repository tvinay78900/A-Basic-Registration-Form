const form = document.getElementById("registerForm");

let formData = {};

form.addEventListener("submit", function(e){

    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();

    if(name === "" || email === "" || phone === ""){
        showError("Please fill all fields.");
        return;
    }

    if(phone.length !== 10 || isNaN(phone)){
        showError("Please enter a valid 10-digit phone number.");
        return;
    }

    formData = {
        name,
        email,
        phone
    };

    document.getElementById("confirmPopup").style.display = "flex";

});

function closeConfirm(){
    document.getElementById("confirmPopup").style.display = "none";
}

function confirmRegister(){

    closeConfirm();

    document.getElementById("loadingPopup").style.display = "flex";

    setTimeout(()=>{

        fetch("http://127.0.0.1:5000/register",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(formData)

        })

        .then(response=>response.json())

        .then(data=>{

            document.getElementById("loadingPopup").style.display="none";

            if(data.success){

                document.getElementById("successPopup").style.display="flex";

                form.reset();

            }
            else{

                showError(data.message);

            }

        })

        .catch(()=>{

            document.getElementById("loadingPopup").style.display="none";

            showError("Unable to connect to server.");

        });

    },2500);

}

function closeSuccess(){

    document.getElementById("successPopup").style.display="none";

}

function showError(message){

    document.getElementById("errorMessage").innerText=message;

    document.getElementById("errorPopup").style.display="flex";

}

function closeError(){

    document.getElementById("errorPopup").style.display="none";

}