export interface Ingrediente {
  id: number;
  nombre: string;
  descripcion: string;
  imagen_url?: string;
}

export interface IngredientePayload {
  nombre: string;
  descripcion: string;
  imagen_url?: string;
}
