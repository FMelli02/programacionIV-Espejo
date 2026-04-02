import CategoriaCard from './CategoriaCard';
import type { Categoria } from '../types/categoria';

interface CategoriaListProps {
  categorias: Categoria[];
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
}

const CategoriaList = ({ categorias, onEdit, onDelete }: CategoriaListProps) => {
  return (
    <div className="overflow-hidden rounded-lg bg-white shadow">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-slate-800 text-white">
          <tr>
            <th className="px-4 py-3">NÚMERO</th>
            <th className="px-4 py-3">NOMBRE</th>
            <th className="px-4 py-3">DESCRIPCIÓN</th>
            <th className="px-4 py-3">ACCIONES</th>
          </tr>
        </thead>
        <tbody>
          {categorias.map((categoria) => (
            <CategoriaCard
              key={categoria.id}
              categoria={categoria}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </tbody>
      </table>
      {categorias.length === 0 && (
        <p className="px-4 py-5 text-center text-slate-500">
          No hay categorías para mostrar.
        </p>
      )}
    </div>
  );
};

export default CategoriaList;
