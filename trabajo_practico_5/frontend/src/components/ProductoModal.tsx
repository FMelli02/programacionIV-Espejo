import { useEffect, useState, type FormEvent } from 'react';
import type { Producto, ProductoPayload } from '../types/producto';

interface ProductoModalProps {
  isOpen: boolean;
  productoSeleccionado: Producto | null;
  onClose: () => void;
  onSubmit: (payload: ProductoPayload) => Promise<void>;
}

const ProductoModal = ({
  isOpen,
  productoSeleccionado,
  onClose,
  onSubmit,
}: ProductoModalProps) => {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [precioBase, setPrecioBase] = useState(0);
  const [stockCantidad, setStockCantidad] = useState(0);
  const [disponible, setDisponible] = useState(true);

  useEffect(() => {
    if (!productoSeleccionado) {
      setNombre('');
      setDescripcion('');
      setPrecioBase(0);
      setStockCantidad(0);
      setDisponible(true);
      return;
    }

    setNombre(productoSeleccionado.nombre);
    setDescripcion(productoSeleccionado.descripcion || '');
    setPrecioBase(productoSeleccionado.precio_base);
    setStockCantidad(productoSeleccionado.stock_cantidad);
    setDisponible(productoSeleccionado.disponible);
  }, [productoSeleccionado]);

  if (!isOpen) return null;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSubmit({
      nombre,
      descripcion,
      precio_base: precioBase,
      stock_cantidad: stockCantidad,
      disponible,
      imagenes_url: []
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl">
        <h2 className="mb-4 text-xl font-bold text-slate-900">
          {productoSeleccionado ? 'Editar producto' : 'Nuevo producto'}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-semibold">Nombre</label>
            <input
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
              className="w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-semibold">Descripción</label>
            <textarea
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              className="w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-emerald-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="mb-1 block text-sm font-semibold">Precio Base</label>
              <input
                type="number"
                step="0.01"
                value={precioBase}
                onChange={(e) => setPrecioBase(parseFloat(e.target.value))}
                required
                className="w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-emerald-500"
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-semibold">Stock</label>
              <input
                type="number"
                value={stockCantidad}
                onChange={(e) => setStockCantidad(parseInt(e.target.value))}
                required
                className="w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-emerald-500"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="disponible"
              checked={disponible}
              onChange={(e) => setDisponible(e.target.checked)}
              className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
            />
            <label htmlFor="disponible" className="text-sm font-semibold">
              Disponible
            </label>
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

export default ProductoModal;
