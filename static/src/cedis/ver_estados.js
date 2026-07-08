document.addEventListener("DOMContentLoaded", () => {
    verEstado();
});

async function verEstado() {
    const response = await fetch(`api/visualizar_pedido`);
    const data = await response.json();

    const p = document.getElementById("estado");
    p.innerHTML = `Pedido actual ${data.estado}`;
}