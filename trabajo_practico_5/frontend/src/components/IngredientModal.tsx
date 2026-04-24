import { useForm } from '@tanstack/react-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Ingrediente, IngredientePayload } from '../types/ingrediente';
import { useEffect } from 'react';

const API_URL = 'http://localhost:8000/ingredientes';

interface Props {
  isOpen: boolean;
  ingrediente: Ingrediente | null;
  onClose: () => void;
}

const IngredientModal = ({ isOpen, ingrediente, onClose }: Props) => {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (payload: IngredientePayload) => {
      const url = ingrediente ? `${API_URL}/${ingrediente.id}` : API_URL;
      const method = ingrediente ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Error al guardar ingrediente');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredientes'] });
      onClose();
    },
  });

  const form = useForm<IngredientePayload>({
    defaultValues: {
      nombre: ingrediente?.nombre || '',
      descripcion: ingrediente?.descripcion || '',
    },
    onSubmit: async ({ value }) => {
      mutation.mutate(value);
    },
  });

  useEffect(() => {
    if (isOpen) {
      form.reset({
        nombre: ingrediente?.nombre || '',
        descripcion: ingrediente?.descripcion || '',
      });
    }
  }, [isOpen, ingrediente, form]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-md rounded bg-white p-6 shadow-xl">
        <h3 className="mb-4 text-xl font-bold">
          {ingrediente ? 'Editar Ingrediente' : 'Añadir Ingrediente'}
        </h3>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            e.stopPropagation();
            void form.handleSubmit();
          }}
          className="space-y-4"
        >
          <form.Field
            name="nombre"
            validators={{
              onChange: ({ value }) =>
                !value ? 'El nombre es requerido' : undefined,
            }}
          >
            {(field) => (
              <div>
                <label className="mb-1 block font-medium">Nombre</label>
                <input
                  name={field.name}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  className="w-full rounded border px-3 py-2 outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                />
                {field.state.meta.errors ? (
                  <em className="text-sm text-red-500">{field.state.meta.errors.join(', ')}</em>
                ) : null}
              </div>
            )}
          </form.Field>

          <form.Field
            name="descripcion"
            validators={{
              onChange: ({ value }) =>
                !value ? 'La descripción es requerida' : undefined,
            }}
          >
            {(field) => (
              <div>
                <label className="mb-1 block font-medium">Descripción</label>
                <textarea
                  name={field.name}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  className="w-full rounded border px-3 py-2 outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                />
                {field.state.meta.errors ? (
                  <em className="text-sm text-red-500">{field.state.meta.errors.join(', ')}</em>
                ) : null}
              </div>
            )}
          </form.Field>

          <div className="mt-6 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="rounded bg-gray-200 px-4 py-2 font-medium hover:bg-gray-300"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={mutation.isPending}
              className="rounded bg-sky-600 px-4 py-2 font-medium text-white hover:bg-sky-700 disabled:opacity-50"
            >
              {mutation.isPending ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default IngredientModal;
