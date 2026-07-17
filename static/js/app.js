// =========================
// Dark Mode
// =========================

const toggle = document.getElementById("theme-toggle");

if(toggle){

    if(localStorage.getItem("theme") === "dark"){

        document.body.classList.add("dark");

        toggle.innerHTML = "☀️";

    }

    toggle.onclick = () =>{

        document.body.classList.toggle("dark");

        if(document.body.classList.contains("dark")){

            localStorage.setItem("theme","dark");

            toggle.innerHTML="☀️";

        }else{

            localStorage.setItem("theme","light");

            toggle.innerHTML="🌙";

        }

    }

}

// =========================
// Auto-hide alerts
// =========================

setTimeout(function(){

    document.querySelectorAll(".alert").forEach(alert=>{

        alert.style.transition="0.5s";

        alert.style.opacity="0";

        setTimeout(()=>alert.remove(),500);

    });

},3000);