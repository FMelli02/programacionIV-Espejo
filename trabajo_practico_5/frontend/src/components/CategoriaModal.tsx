import { useEffect, useState, type FormEvent } from 'react';
import type { Categoria, CategoriaPayload } from '../types/categoria';

interface CategoriaModalProps {
  isOpen: boolean;
  categoriaSeleccionada: Categoria | null;
  onClose: () => void;
  onSubmit: (payload: CategoriaPayload) => Promise<void>;
}

const CategoriaModal = ({
  isOpen,
  categoriaSeleccionada,
  onClose,
  onSubmit,
}: CategoriaModalProps) => {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');

  useEffect(() => {
    if (!categoriaSeleccionada) {
      setNombre('');
      setDescripcion('');
      return;
    }

    setNombre(categoriaSeleccionada.nombre);
    setDescripcion(categoriaSeleccionada.descripcion);
  }, [categoriaSeleccionada]);

  if (!isOpen) return null;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSubmit({ nombre, descripcion });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl">
        <h2 className="mb-4 text-xl font-bold text-slate-900">
          {categoriaSeleccionada ? 'Editar categoría' : 'Nueva categoría'}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-semibold">Nombre</label>
            <input
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
              className="w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-semibold">Descripción</label>
            <textarea
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              required
              className="w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-sky-500"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded bg-slate-300 px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-400"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="rounded bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CategoriaModal;
