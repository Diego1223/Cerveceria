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

//Permite filtrar filas de una tabla dependiendo de la opcion seleccionada en el select
const select = document.getElementById("select_tipo");
//obtenemos todas las filas tr de tbody de la tabla con clase .tabla-historial
const filas = document.querySelectorAll(".tabla-historial tbody tr");

//Escuchar el evento con change
select.addEventListener("change", (e) => {
    //obtener el valor seleccionado
    //e.target hace referencia al elemento que disparo el evento
    const tipoSeleccionado = e.target.value.toLowerCase();
    
    //las filas se obtienen aqui porque la tabla se llena dinamicamente desde la API
    const filas = document.querySelectorAll(
        ".tabla-historial tbody tr"
    );

    //recorremos todas las filas
    filas.forEach(fila => {
        //obtener columna tipo
        //querySelector busca dentro de la fila un elemento que tenga la clase col-tipo
        const tipoFila = fila
            .querySelector(".col-tipo")
            .textContent
            .toLowerCase();
        
        //verificar la coincidencia
        const coincide = tipoFila.includes(tipoSeleccionado);

        //ocultar si no coincide 
        fila.hidden = !coincide;
    });
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
                <td class="col-tipo">${p.tipo_movimiento}</td>
                <td>${p.cantidad}</td>
                <td>${p.motivo}</td>
                <td>${p.firma}</td>
                <td>${fecha_formateda}</td>
            </tr>
        `; 
        
    });
}
