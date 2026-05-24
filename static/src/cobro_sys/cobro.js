//Escuchar la tecla enter y ejecutar la funcion
document.getElementById("codigo-producto").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        buscar_producto();
        //limpiar el input
        document.getElementById("codigo-producto").value = "";
    }
})

let total_venta = 0;

async function buscar_producto() {
    const codigo = document.getElementById("codigo-producto").value;

    if (!codigo) {
        alert("Ingresa un codigo");
        return;
    }

    const response = await fetch(`/api/buscar_producto/${codigo}`);
    const data = await response.json();

    if (data.mensaje) {
        alert(data.mensaje);
        return;
    }

    const producto = data[0];

    document.getElementById("nombre-producto").textContent = producto.descripcion;
    document.getElementById("precio-producto").textContent = `Precio: $${producto.precio}`;

    document.getElementById("stock-producto").textContent = `Stock disponible: ${producto.existencias}`;
    document.getElementById("unidad-producto").textContent = `Unidad: ${producto.cantidad}ml x ${producto.unidades}`;

    //Agregar automaticamente al carrito
    agregarAlCarrito(producto);
}

function agregarAlCarrito(producto) {
    const lista = document.getElementById("lista-productos");

    const nuevoProducto = document.createElement("div");
    nuevoProducto.classList.add("producto-item");

    nuevoProducto.innerHTML = `
        <div class="info-producto">
            <h3>${producto.descripcion}</h3>
            <p>Cantidad: 1</p>
            <span>$${producto.precio}</span>
            
            <div class="controles-cantidad">
                <button class="btn-cantidad menos">
                -
                </button>
                
                <span class="cantidad-producto">
                1
                </span>
                
                <button class="btn-cantidad mas">
                +
                </button>
            </div>
        </div>
    `;
    lista.appendChild(nuevoProducto);
    let cantidad = 1;
    total_venta += producto.precio;

    actualizarTotal();

    const btnMas = nuevoProducto.querySelector(".mas");
    const btnMenos = nuevoProducto.querySelector(".menos");

    const cantidadTexto = nuevoProducto.querySelector(".cantidad-producto");

    btnMas.addEventListener("click", () => {
        cantidad++;

        cantidadTexto.textContent = cantidad;
        total_venta += producto.precio;
        actualizarTotal();
    });

    btnMenos.addEventListener("click", () => {
        if (cantidad > 1) {
            cantidad--;
            
            cantidadTexto.textContent = cantidad;
            total_venta -= producto.precio;
            actualizarTotal();
        } else {
            //eliminar producto completo
            nuevoProducto.remove();

            total_venta -= producto.precio;
            actualizarTotal();
        }
    });
}

function actualizarTotal() {
    document.getElementById("subtotal").textContent = `$${total_venta}`;
    document.getElementById("total-final").textContent = `$${total_venta}`;
}