import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { useForm } from '@tanstack/react-form';
import type { Producto, ProductoPayload } from '../types/producto';

const API_URL = 'http://localhost:8000/productos';

const fetchProductos = async (): Promise<Producto[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Error al cargar productos');
  return res.json();
};

const columnHelper = createColumnHelper<Producto>();

const ProductsPage = () => {
  const queryClient = useQueryClient();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [productoSeleccionado, setProductoSeleccionado] = useState<Producto | null>(null);

  const { data: productos = [], isLoading, isError } = useQuery({
    queryKey: ['productos'],
    queryFn: fetchProductos,
  });

  const mutation = useMutation({
    mutationFn: async (payload: ProductoPayload) => {
      const url = productoSeleccionado ? `${API_URL}/${productoSeleccionado.id}` : API_URL;
      const method = productoSeleccionado ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Error al guardar producto');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
      cerrarModal();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Error al eliminar producto');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
    },
  });

  const form = useForm<ProductoPayload>({
    defaultValues: {
      nombre: '',
      descripcion: '',
      precio_base: 0,
      stock_cantidad: 0,
      disponible: true,
    },
    onSubmit: async ({ value }) => {
      mutation.mutate(value);
    },
  });

  useEffect(() => {
    if (modalAbierto) {
      form.reset({
        nombre: productoSeleccionado?.nombre || '',
        descripcion: productoSeleccionado?.descripcion || '',
        precio_base: productoSeleccionado?.precio_base || 0,
        stock_cantidad: productoSeleccionado?.stock_cantidad || 0,
        disponible: productoSeleccionado?.disponible ?? true,
      });
    }
  }, [modalAbierto, productoSeleccionado, form]);

  const abrirModalAlta = () => {
    setProductoSeleccionado(null);
    setModalAbierto(true);
  };

  const abrirModalEdicion = (prod: Producto) => {
    setProductoSeleccionado(prod);
    setModalAbierto(true);
  };

  const cerrarModal = () => {
    setModalAbierto(false);
    setProductoSeleccionado(null);
  };

  const handleDelete = (id: number) => {
    if (confirm('¿Seguro que querés eliminar este producto?')) {
      deleteMutation.mutate(id);
    }
  };

  const columns = [
    columnHelper.accessor('id', { header: 'ID' }),
    columnHelper.accessor('nombre', { header: 'Nombre' }),
    columnHelper.accessor('precio_base', {
      header: 'Precio',
      cell: (info) => `$${info.getValue()}`,
    }),
    columnHelper.accessor('stock_cantidad', { header: 'Stock' }),
    columnHelper.accessor('disponible', {
      header: 'Disponible',
      cell: (info) => (info.getValue() ? '✅' : '❌'),
    }),
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
    data: productos,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isLoading) return <div className="p-8 text-center">Cargando productos...</div>;
  if (isError) return <div className="p-8 text-center text-red-500">Error al cargar datos.</div>;

  return (
    <main className="mx-auto max-w-6xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold">Productos</h2>
        <button
          onClick={abrirModalAlta}
          className="rounded bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-700"
        >
          + Añadir Producto
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
              {productoSeleccionado ? 'Editar Producto' : 'Nuevo Producto'}
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
              <form.Field name="precio_base">
                {(field) => (
                  <div>
                    <label className="mb-1 block font-medium">Precio</label>
                    <input
                      type="number"
                      value={field.state.value}
                      onChange={(e) => field.handleChange(Number(e.target.value))}
                      className="w-full rounded border px-3 py-2 outline-none focus:border-sky-500"
                    />
                  </div>
                )}
              </form.Field>
              <form.Field name="stock_cantidad">
                {(field) => (
                  <div>
                    <label className="mb-1 block font-medium">Stock</label>
                    <input
                      type="number"
                      value={field.state.value}
                      onChange={(e) => field.handleChange(Number(e.target.value))}
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
                  className="rounded bg-emerald-600 px-4 py-2 text-white"
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

export default ProductsPage;
