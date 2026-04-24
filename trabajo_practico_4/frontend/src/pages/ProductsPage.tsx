import { useEffect, useState } from 'react';
import ProductoList from '../components/ProductoList';
import ProductoModal from '../components/ProductoModal';
import type { Producto, ProductoPayload } from '../types/producto';

const API_URL = 'http://localhost:8000/productos';

const ProductsPage = () => {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [productoSeleccionado, setProductoSeleccionado] =
    useState<Producto | null>(null);

  useEffect(() => {
    const cargarProductos = async () => {
      const response = await fetch(API_URL);
      const data: Producto[] = await response.json();
      setProductos(data);
    };

    void cargarProductos();
  }, []);

  const handleCreate = async (payload: ProductoPayload) => {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) return;

    const nuevoProducto: Producto = await response.json();
    setProductos((prev) => [...prev, nuevoProducto]);
  };

  const handleUpdate = async (payload: ProductoPayload) => {
    if (!productoSeleccionado) return;

    const response = await fetch(`${API_URL}/${productoSeleccionado.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) return;

    const productoActualizado: Producto = await response.json();
    setProductos((prev) =>
      prev.map((prod) =>
        prod.id === productoActualizado.id ? productoActualizado : prod,
      ),
    );
  };

  const handleDelete = async (id: number) => {
    const confirmar = confirm('¿Seguro que querés eliminar este producto?');
    if (!confirmar) return;

    const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    if (!response.ok) return;

    setProductos((prev) => prev.filter((prod) => prod.id !== id));
  };

  const abrirModalAlta = () => {
    setProductoSeleccionado(null);
    setModalAbierto(true);
  };

  const abrirModalEdicion = (producto: Producto) => {
    setProductoSeleccionado(producto);
    setModalAbierto(true);
  };

  const cerrarModal = () => {
    setModalAbierto(false);
    setProductoSeleccionado(null);
  };

  const guardarProducto = async (payload: ProductoPayload) => {
    if (productoSeleccionado) {
      await handleUpdate(payload);
    } else {
      await handleCreate(payload);
    }
    cerrarModal();
  };

  return (
    <main className="mx-auto max-w-6xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold">Productos</h2>
        <button
          type="button"
          onClick={abrirModalAlta}
          className="rounded bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-700"
        >
          + Añadir Producto
        </button>
      </div>

      <ProductoList
        productos={productos}
        onEdit={abrirModalEdicion}
        onDelete={handleDelete}
      />

      <ProductoModal
        isOpen={modalAbierto}
        productoSeleccionado={productoSeleccionado}
        onClose={cerrarModal}
        onSubmit={guardarProducto}
      />
    </main>
  );
};

export default ProductsPage;
