import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { useForm } from '@tanstack/react-form';
import type { Categoria, CategoriaPayload } from '../types/categoria';

const API_URL = 'http://localhost:8000/categorias';

const fetchCategorias = async (): Promise<Categoria[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Error al cargar categorías');
  return res.json();
};

const columnHelper = createColumnHelper<Categoria>();

const CategoriasPage = () => {
  const queryClient = useQueryClient();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState<Categoria | null>(null);

  // TanStack Query
  const { data: categorias = [], isLoading, isError } = useQuery({
    queryKey: ['categorias'],
    queryFn: fetchCategorias,
  });

  const mutation = useMutation({
    mutationFn: async (payload: CategoriaPayload) => {
      const url = categoriaSeleccionada ? `${API_URL}/${categoriaSeleccionada.id}` : API_URL;
      const method = categoriaSeleccionada ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Error al guardar categoría');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categorias'] });
      cerrarModal();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Error al eliminar categoría');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categorias'] });
    },
  });

  // TanStack Form
  const form = useForm<CategoriaPayload>({
    defaultValues: {
      nombre: '',
      descripcion: '',
    },
    onSubmit: async ({ value }) => {
      mutation.mutate(value);
    },
  });

  useEffect(() => {
    if (modalAbierto) {
      form.reset({
        nombre: categoriaSeleccionada?.nombre || '',
        descripcion: categoriaSeleccionada?.descripcion || '',
      });
    }
  }, [modalAbierto, categoriaSeleccionada, form]);

  const abrirModalAlta = () => {
    setCategoriaSeleccionada(null);
    setModalAbierto(true);
  };

  const abrirModalEdicion = (cat: Categoria) => {
    setCategoriaSeleccionada(cat);
    setModalAbierto(true);
  };

  const cerrarModal = () => {
    setModalAbierto(false);
    setCategoriaSeleccionada(null);
  };

  const handleDelete = (id: number) => {
    if (confirm('¿Seguro que querés eliminar esta categoría?')) {
      deleteMutation.mutate(id);
    }
  };

  // TanStack Table
  const columns = [
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('nombre', { header: 'Nombre' }),
    columnHelper.accessor('descripcion', { header: 'Descripción' }),
    columnHelper.display({
      id: 'acciones',
      header: 'Acciones',
      cell: (info) => (
        <div className="flex gap-2">
          <button
            onClick={() => abrirModalEdicion(info.row.original)}
            className="rounded bg-sky-500 px-3 py-1 text-sm text-white hover:bg-sky-600"
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
    data: categorias,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isLoading) return <div className="p-8 text-center">Cargando categorías...</div>;
  if (isError) return <div className="p-8 text-center text-red-500">Error al cargar datos.</div>;

  return (
    <main className="mx-auto max-w-6xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold">Categorías</h2>
        <button
          onClick={abrirModalAlta}
          className="rounded bg-sky-600 px-4 py-2 font-semibold text-white hover:bg-sky-700"
        >
          + Añadir Categoría
        </button>
      </div>

      <div className="overflow-x-auto rounded-lg shadow ring-1 ring-black ring-opacity-5">
        <table className="min-w-full divide-y divide-gray-300">
          <thead className="bg-slate-800 text-white">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="px-6 py-3 text-left text-sm font-semibold">
                    {flexRender(header.column.columnDef.header, header.getContext())}
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
          </tbody>
        </table>
      </div>

      {modalAbierto && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="w-full max-w-md rounded bg-white p-6 shadow-xl">
            <h3 className="mb-4 text-xl font-bold">
              {categoriaSeleccionada ? 'Editar Categoría' : 'Nueva Categoría'}
            </h3>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                void form.handleSubmit();
              }}
              className="space-y-4"
            >
              <form.Field name="nombre">
                {(field) => (
                  <div>
                    <label className="mb-1 block font-medium">Nombre</label>
                    <input
                      value={field.state.value}
                      onChange={(e) => field.handleChange(e.target.value)}
                      className="w-full rounded border px-3 py-2 outline-none focus:border-sky-500"
                    />
                  </div>
                )}
              </form.Field>
              <form.Field name="descripcion">
                {(field) => (
                  <div>
                    <label className="mb-1 block font-medium">Descripción</label>
                    <textarea
                      value={field.state.value}
                      onChange={(e) => field.handleChange(e.target.value)}
                      className="w-full rounded border px-3 py-2 outline-none focus:border-sky-500"
                    />
                  </div>
                )}
              </form.Field>
              <div className="mt-6 flex justify-end gap-3">
                <button type="button" onClick={cerrarModal} className="rounded bg-gray-200 px-4 py-2">
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={mutation.isPending}
                  className="rounded bg-sky-600 px-4 py-2 text-white"
                >
                  {mutation.isPending ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
};

export default CategoriasPage;
