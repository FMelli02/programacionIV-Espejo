import ProductoCard from './ProductoCard';
import type { Producto } from '../types/producto';

interface ProductoListProps {
  productos: Producto[];
  onEdit: (producto: Producto) => void;
  onDelete: (id: number) => void;
}

const ProductoList = ({ productos, onEdit, onDelete }: ProductoListProps) => {
  return (
    <div className="overflow-hidden rounded-lg bg-white shadow">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-slate-800 text-white">
          <tr>
            <th className="px-4 py-3">NÚMERO</th>
            <th className="px-4 py-3">NOMBRE</th>
            <th className="px-4 py-3">DESCRIPCIÓN</th>
            <th className="px-4 py-3">PRECIO BASE</th>
            <th className="px-4 py-3">STOCK</th>
            <th className="px-4 py-3">DISPONIBLE</th>
            <th className="px-4 py-3">ACCIONES</th>
          </tr>
        </thead>
        <tbody>
          {productos.map((producto) => (
            <ProductoCard
              key={producto.id}
              producto={producto}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </tbody>
      </table>
      {productos.length === 0 && (
        <p className="px-4 py-5 text-center text-slate-500">
          No hay productos para mostrar.
        </p>
      )}
    </div>
  );
};

export default ProductoList;
