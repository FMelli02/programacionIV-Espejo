import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { Ingrediente, IngredientePayload } from '../types/ingrediente';
import IngredientModal from '../components/IngredientModal';

const API_URL = 'http://localhost:8000/ingredientes';

const fetchIngredientes = async (): Promise<Ingrediente[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Error al cargar ingredientes');
  return res.json();
};

const columnHelper = createColumnHelper<Ingrediente>();

const IngredientsPage = () => {
  const queryClient = useQueryClient();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [ingredienteSeleccionado, setIngredienteSeleccionado] = useState<Ingrediente | null>(null);

  // TanStack Query: Fetch data
  const { data: ingredientes = [], isLoading, isError } = useQuery({
    queryKey: ['ingredientes'],
    queryFn: fetchIngredientes,
  });

  // TanStack Query: Mutations
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Error al eliminar ingrediente');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });

  const handleDelete = (id: number) => {
    if (confirm('¿Seguro que querés eliminar este ingrediente?')) {
      deleteMutation.mutate(id);
    }
  };

  const abrirModalAlta = () => {
    setIngredienteSeleccionado(null);
    setModalAbierto(true);
  };

  const abrirModalEdicion = (ing: Ingrediente) => {
    setIngredienteSeleccionado(ing);
    setModalAbierto(true);
  };

  // TanStack Table: Setup columns
  const columns = [
    columnHelper.accessor('id', {
      header: 'ID',
      cell: (info) => info.getValue(),
    }),
    columnHelper.accessor('nombre', {
      header: 'Nombre',
      cell: (info) => info.getValue(),
    }),
    columnHelper.accessor('descripcion', {
      header: 'Descripción',
      cell: (info) => info.getValue(),
    }),
    columnHelper.display({
      id: 'acciones',
      header: 'Acciones',
      cell: (info) => (
        <div className="flex gap-2">
          <button
            onClick={() => abrirModalEdicion(info.row.original)}
            className="rounded bg-yellow-500 px-3 py-1 text-sm text-white hover:bg-yellow-600"
          >
            Editar
          </button>
          <button
            onClick={() => handleDelete(info.row.original.id)}
            className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700"
          >
            Eliminar
          </button>
        </div>
      ),
    }),
  ];

  const table = useReactTable({
    data: ingredientes,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isLoading) return <div className="p-8 text-center">Cargando ingredientes...</div>;
  if (isError) return <div className="p-8 text-center text-red-500">Error al cargar datos.</div>;

  return (
    <main className="mx-auto max-w-6xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold">Ingredientes</h2>
        <button
          onClick={abrirModalAlta}
          className="rounded bg-sky-600 px-4 py-2 font-semibold text-white hover:bg-sky-700"
        >
          + Añadir Ingrediente
        </button>
      </div>

      <div className="overflow-x-auto rounded-lg shadow ring-1 ring-black ring-opacity-5">
        <table className="min-w-full divide-y divide-gray-300">
          <thead className="bg-gray-50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className="px-6 py-3 text-left text-sm font-semibold text-gray-900"
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="whitespace-nowrap px-6 py-4 text-sm text-gray-700">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
            {table.getRowModel().rows.length === 0 && (
              <tr>
                <td colSpan={columns.length} className="px-6 py-4 text-center text-sm text-gray-500">
                  No hay ingredientes registrados.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <IngredientModal
        isOpen={modalAbierto}
        ingrediente={ingredienteSeleccionado}
        onClose={() => setModalAbierto(false)}
      />
    </main>
  );
};

export default IngredientsPage;
