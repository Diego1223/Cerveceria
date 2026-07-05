const tbody = document.getElementById("tbodyPedido");

document
.getElementById("btnAgregarProducto")
.addEventListener("click", agregarFila);

const boton_enviar = document.getElementById("btn-enviar");
boton_enviar.addEventListener("click", mandarPedido);


async function agregarFila(){
    const response = await fetch(`/api/mostrar_productos_cedis`);
    const data = await response.json();
    //toma el arreglo data y lo convierte en cadena de texto con elementos <option> para llenar el select de const fila 
    //map recorre cada elemento del arreglo data y el join al final une todos los elementos en una sola cadena de texto
    const opciones = data.map(producto => `<option value="${producto.codigo}">${producto.descripcion}</option>`).join("");
    /* 
        Resultado de map 
        <option value="1">Six modelo</option><option value="2">Tecate</option><option value="3">Michelob</option>
    */
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


//Cada fila que agrega el usuario al agregar producto tiene un select con el producto y un input con la cantidad, por lo tanto en mandarPedido
//recorremos todas las filas del tbody y construimos un arreglo para enviar al backend
async function mandarPedido() {
    //buscar dentro del t_body elementos que tengan tr
    const filas = tbody.querySelectorAll("tr");
    const productos = [];

    filas.forEach(fila => {
        const producto = fila.querySelector("select").value;
        const cantidad = fila.querySelector("input").value;

        if (producto !== "") {
            productos.push({
                codigo: producto,
                cantidad: Number(cantidad)
            });
        }
    });

    console.log(productos);

    const response = await fetch("/api/crear_pedido", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                observaciones: document.getElementById("observaciones").value,
                productos: productos
            })
    });

    const resultado = await response.json();
    //ok -> 200
    if (resultado.ok) {
        //aprobar el pedido 
    }
} 