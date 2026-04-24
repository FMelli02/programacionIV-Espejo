export interface Producto {
  id: number;
  nombre: string;
  descripcion?: string | null;
  precio_base: number;
  imagenes_url?: string[] | null;
  stock_cantidad: number;
  disponible: boolean;
}

export interface ProductoPayload {
  nombre: string;
  descripcion?: string | null;
  precio_base: number;
  imagenes_url?: string[] | null;
  stock_cantidad: number;
  disponible: boolean;
}
