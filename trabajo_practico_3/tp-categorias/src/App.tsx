import { useEffect, useState } from 'react';
import CategoriaList from './components/CategoriaList';
import CategoriaModal from './components/CategoriaModal';
import Navbar from './components/Navbar';
import type { Categoria, CategoriaPayload } from './types/categoria';

const API_URL = 'http://localhost:8000/categorias';

function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [categoriaSeleccionada, setCategoriaSeleccionada] =
    useState<Categoria | null>(null);

  useEffect(() => {
    const cargarCategorias = async () => {
      const response = await fetch(API_URL);
      const data: Categoria[] = await response.json();
      setCategorias(data);
    };

    void cargarCategorias();
  }, []);

  const handleCreate = async (payload: CategoriaPayload) => {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) return;

    const nuevaCategoria: Categoria = await response.json();
    setCategorias((prev) => [...prev, nuevaCategoria]);
  };

  const handleUpdate = async (payload: CategoriaPayload) => {
    if (!categoriaSeleccionada) return;

    const response = await fetch(`${API_URL}/${categoriaSeleccionada.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) return;

    const categoriaActualizada: Categoria = await response.json();
    setCategorias((prev) =>
      prev.map((cat) =>
        cat.id === categoriaActualizada.id ? categoriaActualizada : cat,
      ),
    );
  };

  const handleDelete = async (id: number) => {
    const confirmar = confirm('¿Seguro que querés eliminar esta categoría?');
    if (!confirmar) return;

    const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    if (!response.ok) return;

    setCategorias((prev) => prev.filter((cat) => cat.id !== id));
  };

  const abrirModalAlta = () => {
    setCategoriaSeleccionada(null);
    setModalAbierto(true);
  };

  const abrirModalEdicion = (categoria: Categoria) => {
    setCategoriaSeleccionada(categoria);
    setModalAbierto(true);
  };

  const cerrarModal = () => {
    setModalAbierto(false);
    setCategoriaSeleccionada(null);
  };

  const guardarCategoria = async (payload: CategoriaPayload) => {
    if (categoriaSeleccionada) {
      await handleUpdate(payload);
    } else {
      await handleCreate(payload);
    }
    cerrarModal();
  };

  return (
    <div className="min-h-screen">
      <Navbar />

      <main className="mx-auto max-w-6xl px-6 py-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold">Categorías</h2>
          <button
            type="button"
            onClick={abrirModalAlta}
            className="rounded bg-sky-600 px-4 py-2 font-semibold text-white hover:bg-sky-700"
          >
            + Añadir Categoría
          </button>
        </div>

        <CategoriaList
          categorias={categorias}
          onEdit={abrirModalEdicion}
          onDelete={handleDelete}
        />

        <CategoriaModal
          isOpen={modalAbierto}
          categoriaSeleccionada={categoriaSeleccionada}
          onClose={cerrarModal}
          onSubmit={guardarCategoria}
        />
      </main>
    </div>
  );
}

export default App;
