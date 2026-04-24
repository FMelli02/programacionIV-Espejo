import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <header className="bg-slate-900 px-6 py-4 text-white shadow-md flex justify-between items-center">
      <h1 className="text-xl font-bold">Food Store Admin</h1>
      <nav className="flex gap-4">
        <Link to="/categorias" className="hover:text-sky-400 font-medium transition-colors">
          Categorías
        </Link>
        <Link to="/productos" className="hover:text-emerald-400 font-medium transition-colors">
          Productos
        </Link>
      </nav>
    </header>
  );
};

export default Navbar;
