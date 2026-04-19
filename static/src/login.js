async function login(event) {
    event.preventDefault();
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            correo:correo,
            password:password
        })
    });
    
    const data = await response.json();
    //ok = 200
    if (response.ok) {
        window.location.href = "/index";
    } else {
        alert(data.mensaje);
    }
}