const tbody = document.getElementById("tbodyPedido");

document
.getElementById("btnAgregarProducto")
.addEventListener("click", agregarFila);


async function agregarFila(){
    const response = await fetch(`/api/mostrar_productos_cedis`);
    const data = await response.json();
    const opciones = data.map(producto => `<option value="${producto.id_producto}">${producto.descripcion}</option>`).join("");


    const fila = document.createElement("tr");
    fila.innerHTML = `
        <td>
            <select>

                <option value="">
                    Seleccionar producto
                </option>

                ${opciones}
            </select>
        </td>

        <td>
            <input
                type="number"
                min="1"
                value="1"
            >
        </td>

        <td>
            <button class="btn-eliminar">
                🗑
            </button>
        </td>
    `;

    fila
    .querySelector(".btn-eliminar")
    .addEventListener("click", () => {
        fila.remove();
    });

    tbody.appendChild(fila);
}