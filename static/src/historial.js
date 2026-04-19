document.addEventListener("DOMContentLoaded", () => {
    historial();
});

//Buscador que lee lo que escribiste, lee cada fila de la tabla, si coincide se muestra y si no se oculta
const buscador = document.getElementById("buscador");
//keyup - cada vez que suelte una tecla, ejecuta esto:
buscador.addEventListener("keyup", function() {
    let filtro = buscador.value.toLowerCase();
    //obtener TODAS las filas de la tabla
    let filas = document.querySelectorAll(".tabla-historial tbody tr");

    //recorremos fila por fila
    filas.forEach(fila => {
        //convierte todo el texto de la fila en minusculas
        let texto = fila.innerText.toLowerCase();
        
        //si la fila contiene lo que escribio el usuario 
        if (texto.includes(filtro)) {
            //muestra la fila
            fila.style.display = "";
        } else {
            //caso contrario, la oculta
            fila.style.display = "none";
        }
    })

});

async function historial() {
    const response = await fetch(`/api/mostrar_historial`);
    const data = await response.json();

    
    const t_body = document.getElementById("cuerpo-tabla");
    t_body.innerHTML = "";
    //datos lo recibimos desde el backend
    data.forEach(p => {
        const fecha = new Date(p.fecha);

        const fecha_formateda = fecha.toLocaleString('es-MX', {
            timeZone: 'UTC',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        t_body.innerHTML += `
            <tr>
                <td>${p.descripcion}</td>
                <td>${p.tipo_movimiento}</td>
                <td>${p.cantidad}</td>
                <td>${p.motivo}</td>
                <td>${p.firma}</td>
                <td>${fecha_formateda}</td>
            </tr>
        `; 
    });
}


function verMotivo(texto) {
    document.getElementById("modal").style.display = "flex";
    document.getElementById("texto-motivo").innerHTML = texto;
}

function cerrarModal() {
    document.getElementById("modal").style.display = "none";
}