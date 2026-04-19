//Mandar a pedir por API rest los productos de nuestra tienda
document.addEventListener("DOMContentLoaded", () => {
    num_productos();
});


async function num_productos() {
    const contador = document.getElementById("contador");
    const response = await fetch(`/api/numProductos`);
    const data = await response.json();
    contador.innerHTML += "";
    contador.innerHTML = `
    <p>📦 Variedad de productos acutales: ${data.numero_productos.total_registros}</p>
    `;
}