let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

function guardarCarrito() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarContador();
}

function agregarAlCarrito(id, nombre, precio) {
    const productoExistente = carrito.find(item => item.product_id === id);
    if (productoExistente) {
        productoExistente.cantidad += 1;
    } else {
        carrito.push({ product_id: id, nombre: nombre, precio: precio, cantidad: 1 });
    }
    guardarCarrito();
    alert("Producto agregado exitosamente al carrito.");
}

function agregarAlCarritoDesdeCatalogo(event, id, nombre, precio, stockMaximo) {
    const inputCantidad = document.getElementById('cantidad-' + id);
    const cantidadSeleccionada = parseInt(inputCantidad.value);

    if (isNaN(cantidadSeleccionada) || cantidadSeleccionada <= 0) {
        alert("Ingrese una cantidad válida.");
        return;
    }

    const productoExistente = carrito.find(item => item.product_id === id);
    const cantidadActualEnCarrito = productoExistente ? productoExistente.cantidad : 0;

    if (cantidadActualEnCarrito + cantidadSeleccionada > stockMaximo) {
        alert(`No puedes agregar esa cantidad. Solo hay ${stockMaximo} disponibles y ya tienes ${cantidadActualEnCarrito} en tu carrito.`);
        return;
    }

    if (productoExistente) {
        productoExistente.cantidad += cantidadSeleccionada;
    } else {
        carrito.push({ product_id: id, nombre: nombre, precio: precio, cantidad: cantidadSeleccionada });
    }
    
    guardarCarrito();
    
    const boton = event.currentTarget;
    const textoOriginal = boton.innerHTML;
    
    boton.innerHTML = '<i class="fas fa-check"></i> Agregado';
    boton.style.backgroundColor = '#10b981';
    
    setTimeout(() => {
        boton.innerHTML = textoOriginal;
        boton.style.backgroundColor = '';
    }, 1500);
}

function eliminarDelCarrito(id) {
    carrito = carrito.filter(item => item.product_id !== id);
    guardarCarrito();
    renderizarCarrito();
}

function actualizarContador() {
    const contador = document.getElementById('carrito-count');
    if (contador) {
        const totalItems = carrito.reduce((acc, item) => acc + item.cantidad, 0);
        contador.innerText = totalItems;
    }
}

function renderizarCarrito() {
    const tbody = document.getElementById('carrito-body');
    const totalElement = document.getElementById('carrito-total');
    
    if (!tbody || !totalElement) return;

    tbody.innerHTML = '';
    let total = 0;

    if (carrito.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 20px;">El carrito está vacío</td></tr>';
        totalElement.innerText = "0.00";
        return;
    }

    carrito.forEach(item => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;
        
        const tr = document.createElement('tr');
        tr.style.borderBottom = "1px solid #f1f5f9";
        tr.innerHTML = `
            <td style="padding: 12px;"><strong>${item.nombre}</strong></td>
            <td style="padding: 12px; text-align: right;">${item.precio.toFixed(2)} Bs.</td>
            <td style="padding: 12px; text-align: center;">${item.cantidad}</td>
            <td style="padding: 12px; text-align: right; font-weight: bold;">${subtotal.toFixed(2)} Bs.</td>
            <td style="padding: 12px; text-align: center;">
                <button onclick="eliminarDelCarrito(${item.product_id})" style="background: none; border: none; color: #ef4444; cursor: pointer; font-weight: bold;">Quitar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    totalElement.innerText = total.toFixed(2);
}

async function procesarCompra() {
    if (carrito.length === 0) {
        alert("El carrito se encuentra vacío. Agregue productos antes de procesar.");
        return;
    }

    try {
        const response = await fetch('/ventas/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(carrito)
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message);
            carrito = [];
            guardarCarrito();
            
            // Abrir la factura en una pestaña nueva
            window.open(`/ventas/recibo/${data.venta_id}`, '_blank');
            
            // Redirigir al usuario al historial en su pestaña actual
            window.location.href = '/ventas/historial';
        } else {
            alert("Error al procesar: " + data.message);
        }
    } catch (error) {
        alert("Ocurrió un error de conexión al procesar la compra.");
    }
}

document.addEventListener("DOMContentLoaded", actualizarContador);