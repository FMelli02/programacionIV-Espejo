import type { Producto } from '../types/producto';

interface ProductoCardProps {
  producto: Producto;
  onEdit: (producto: Producto) => void;
  onDelete: (id: number) => void;
}

const ProductoCard = ({ producto, onEdit, onDelete }: ProductoCardProps) => {
  return (
    <tr className="border-b border-slate-200 transition-colors hover:bg-slate-50">
      <td className="px-4 py-3 font-semibold text-slate-700">#{producto.id}</td>
      <td className="px-4 py-3 font-medium text-slate-900">{producto.nombre}</td>
      <td className="px-4 py-3 text-slate-600">{producto.descripcion || '-'}</td>
      <td className="px-4 py-3 font-medium text-slate-700">${producto.precio_base}</td>
      <td className="px-4 py-3 text-slate-600">{producto.stock_cantidad}</td>
      <td className="px-4 py-3 text-slate-600">
        <span className={`px-2 py-1 rounded text-xs font-semibold ${producto.disponible ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
          {producto.disponible ? 'Sí' : 'No'}
        </span>
      </td>
      <td className="px-4 py-3">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => onEdit(producto)}
            className="rounded bg-slate-200 px-3 py-1 text-sm font-semibold text-slate-700 hover:bg-slate-300"
          >
            Editar
          </button>
          <button
            type="button"
            onClick={() => onDelete(producto.id)}
            className="rounded bg-red-100 px-3 py-1 text-sm font-semibold text-red-700 hover:bg-red-200"
          >
            Eliminar
          </button>
        </div>
      </td>
    </tr>
  );
};

export default ProductoCard;
