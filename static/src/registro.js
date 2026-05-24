async function registrarse(event) {
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    //Esto del rol recibimos 1 si es admin y 2 si es trabajador
    const rol = document.getElementById("rol").value;


    const response = await fetch("/api/registro", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: nombre,
            correo: correo,
            password: password,
            rol: rol 
        })
    });

    const data = await response.json();

    if (response.ok) {
        window.location.href = "/index";
    } else {
        alert(data.mensaje);
    }
}