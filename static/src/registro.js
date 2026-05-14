async function registrarse(event) {
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const rol = document.getElementById("rol").value;
    let rol_num = 0;

    if (rol == "Administrador") {
        rol_num = 1;
    } else {
        rol_num = 2;
    }

    const response = await fetch("/api/registro", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: nombre,
            correo: correo,
            password: password,
            rol: rol_num
        })
    });

    const data = await response.json();

    if (response.ok) {
        window.location.href = "/index";
    } else {
        alert(data.mensaje);
    }
}