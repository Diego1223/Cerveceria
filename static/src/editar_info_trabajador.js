document.addEventListener("DOMContentLoaded", () => {
    //Usamos esta funcion para buscar el parametro desde la URL
    const params = new URLSearchParams(window.location.search);
    //recibir el id
    const id = params.get("id");
    editar_info_trabajador(id);

    const form = document.getElementById("mi_form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const nombre = document.getElementById("nombre").value;
        const correo = document.getElementById("correo").value;
        const rfc = document.getElementById("rfc").value;
        const seguro_social = document.getElementById("seguro_social").value;
        mandar_informacion(id, nombre, correo, rfc, seguro_social);
    });

});

async function editar_info_trabajador(id) {
    const response = await fetch(`/api/editar_trabajadorView/${id}`);
    const data = await response.json();


    let faltantes = [];
    //En el caso de que falten datos, remarcaremos esa casilla para que se de cuenta el cliente donde falta agregar cosas
    //lo haremos agregando al ClassList y en el css le pondremos .error
    if (data.rfc === "" || data.rfc === null) {
        faltantes.push("RFC");
        document.getElementById("rfc").classList.add("error");
    }
    if (data.numero_seguro_social === "" || data.numero_seguro_social === null) {
        faltantes.push("Numero de seguro social");
        document.getElementById("seguro_social").classList.add("error");

    }
    if (faltantes.length > 0) {
        alert("Faltan los siguientes campos: \n\n" +
        faltantes.join("\n")
        );
    }
    document.getElementById("nombre").value = data.nombre || "";

    document.getElementById("correo").value = data.correo || "";

    document.getElementById("rfc").value = data.rfc || "";

    document.getElementById("seguro_social").value = data.numero_seguro_social || "";

    if (data.antiguedad) {
        //Convertir texto a objeto Date
        const fecha = new Date(data.antiguedad);
        //Convertirlo a formato ISo 2026-05-05T22:04:38.000Z; si es formato estandar
        document.getElementById("fecha_ingreso").value =
            //Lo que hace split divide el texto en el T 2026-05-05 T 22:04:38.000Z
            //y con 0 totamos solo la parte de la fecha
            fecha.toISOString().split("T")[0];
    }

}

async function mandar_informacion(id, nombre, correo, rfc, seguro_social) {
    const response = await fetch("/api/editar_trabajador", {
        method: "PUT",
        headers: {
            "Content-Type": "Application/json"
        },
        body: JSON.stringify({
            id_trabajador: id,
            nombre: nombre,
            correo: correo,
            rfc: rfc,
            seguro_social: seguro_social 
        })
    });

    const data = await response.json();
    
    if (!response.ok) {
        alert(data.mensaje);
    }
    window.location.href = "/lista_trabajadores";
}