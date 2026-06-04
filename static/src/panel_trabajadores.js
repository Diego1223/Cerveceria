document.addEventListener("DOMContentLoaded", () => {
    trabajadores();
});

async function trabajadores() {
    const response = await fetch(`/api/trabajadores`);
    const data = await response.json();

    const t_body = document.getElementById("cuerpo-tabla");
    t_body.innerHTML = "";

    data.forEach(p => {
        const fecha = new Date(p.antiguedad);

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
                <td>${p.nombre}</td>
                <td>${p.correo}</td>
                <td>${p.rfc || "No registrado aun"}</td>
                <td>${p.numero_seguro_social || "No registrado aun"}</td>
                <td>${fecha_formateda}</td>
                <td>
                    <button class="btn editar" onclick="editar(${p.id})">Editar</button>
                    <button class="btn eliminar">Eliminar</button>
                </td>
            </tr>
        `;
    });
}
//Mandamos el id desde el boton, lo cual nos llevara al endpoint para actualizar la informacion del trabajador
function editar(id) {
    window.location.href = `/editar_info_trabajador?id=${id}`
}