import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-white shadow px-4 py-3">
      <div className="container-fluid">
        <a className="navbar-brand fw-bold" href="#">Logo</a>
        <div className="collapse navbar-collapse justify-content-between">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0 gap-3">
            <li className="nav-item">
              <a className="nav-link" href="#">Início Rápido</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">Eventos FURIA</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">Comunidade</a>
            </li>
          </ul>
          <button className="btn btn-dark">Entrar</button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
