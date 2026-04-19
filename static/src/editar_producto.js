document.addEventListener("DOMContentLoaded", () => {
    //Usamos esta funcion para buscar el parametro desde la URL
    const params = new URLSearchParams(window.location.search);
    //y recibimos el id con la funcion params.get
    const id = params.get("id");
    editarProducto(id);
});

async function editarProducto(id) {
    const response = await fetch(`/api/editar_stockV/${id}`);
    const data = await response.json();

    const producto = document.getElementById("producto");
    const stock = document.getElementById("stock_actual");
    const button = document.getElementById("boton-cambios");

    producto.innerHTML = `
        <label>Producto</label>
        <input type="text" value="${data.descripcion}" disabled>
    `;

    stock.innerHTML = `
        <label>Stock actual</label>
        <input type="number" value="${data.existencias}" disabled>        
    `; 

    
    button.addEventListener("click", () => {
             
        const select = document.getElementById("tipo_movimiento");
        const tipo_movimiento = select.value; //"entrada" o "salida"
        const cantidad = Number(document.getElementById("cantidad").value);
        const motivo = document.getElementById("Motivo").value;
        const firma = document.getElementById("firma").value;
        console.log(tipo_movimiento, cantidad, motivo, firma);
        editarStock(id, data.descripcion, data.existencias, tipo_movimiento, cantidad, motivo, firma);
    });

}

async function editarStock(id_producto, descripcion, existencias, tipo_movimiento,cantidad, motivo, firma) { 
    
    const response = await fetch("/api/editar_stock", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_producto: id_producto,
            descripcion: descripcion,
            existencias: existencias,
            tipo_movimiento: tipo_movimiento,
            cantidad: cantidad,
            motivo: motivo,
            firma: firma
        })
    });

    const data = await response.json()

    //200 - ok
    if (!response.ok) {
        alert(data.mensaje);
        return;
    }

    //Iremos a la pagina de la tabla de productos en existencia
    window.location.href = "/numProductos";
}