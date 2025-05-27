import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();

  const linkClasses = (path) =>
    `px-4 py-2 hover:text-gray-300 transition ${
      location.pathname === path ? "text-white font-bold" : "text-gray-400"
    }`;

  return (
    <nav className="bg-black bg-opacity-70 flex justify-between items-center px-6 py-4 shadow-md">
      <div className="text-white text-xl font-bold">AI Resume Parser</div>
      <div className="flex space-x-4">
        <Link to="/" className={linkClasses("/")}>Home</Link>
        <Link to="/parse" className={linkClasses("/parse")}>Normal Parsing</Link>
        <Link to="/multiple" className={linkClasses("/multiple")}>Multiple Resume Analysis</Link>
        <Link to="/plagiarism" className={linkClasses("/plagiarism")}>Plagiarism Check</Link>
      </div>
    </nav>
  );
};

export default Navbar;
