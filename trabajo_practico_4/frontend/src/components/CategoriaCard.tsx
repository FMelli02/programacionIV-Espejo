import type { Categoria } from '../types/categoria';

interface CategoriaCardProps {
  categoria: Categoria;
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
}

const CategoriaCard = ({ categoria, onEdit, onDelete }: CategoriaCardProps) => {
  return (
    <tr className="border-b border-slate-200">
      <td className="px-4 py-3">{categoria.id}</td>
      <td className="px-4 py-3 font-medium">{categoria.nombre}</td>
      <td className="px-4 py-3">{categoria.descripcion}</td>
      <td className="px-4 py-3">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => onEdit(categoria)}
            className="rounded bg-amber-500 px-3 py-1 text-sm font-semibold text-white hover:bg-amber-600"
          >
            Editar
          </button>
          <button
            type="button"
            onClick={() => onDelete(categoria.id)}
            className="rounded bg-rose-600 px-3 py-1 text-sm font-semibold text-white hover:bg-rose-700"
          >
            Eliminar
          </button>
        </div>
      </td>
    </tr>
  );
};

export default CategoriaCard;
