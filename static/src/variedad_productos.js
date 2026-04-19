document.addEventListener("DOMContentLoaded", () => {
    panel();
});


async function panel() {
    const response = await fetch(`/api/panel_productos`);
    const data = await response.json()

    const t_body = document.getElementById("cuerpo-tabla");
    t_body.innerHTML = ``;
    //data.productos porque desde backend estamos devolviendo en el json "productos"
    data.productos.forEach(p => {
        t_body.innerHTML += `
            <tr>
                <td>${p.descripcion}</td>
                <td>${p.unidades}</td>
                <td>${p.cantidad}ml</td>
                <td>${p.existencias}</td>
                <td>
                    <button class="btn editar" onclick="editar(${p.id})">Editar</button>
                    <button class="btn eliminar">Eliminar</button>
                </td>
            </tr>
        `;
    });    
}

//Mandamos el id desde el boton, esta funcion lo que hace es que nos manda al endpoint /editar con el id del producto
//para despues en el archivo editar_producto.js usar este id para la API
function editar(id) {
    window.location.href = `/editar?id=${id}`;
}

