import React from 'react';

const Sidebar = () => {
  return (
    <div className="bg-dark text-white vh-100 p-3" style={{ width: '250px' }}>
      <h4 className="mb-4">Admin Panel</h4>
      <ul className="nav flex-column">
        <li className="nav-item mb-2">
          <a className="nav-link text-white" href="#">Dashboard</a>
        </li>
        <li className="nav-item mb-2">
          <a className="nav-link text-white" href="#">Usuários</a>
        </li>
        <li className="nav-item mb-2">
          <a className="nav-link text-white" href="#">Eventos</a>
        </li>
        <li className="nav-item mb-2">
          <a className="nav-link text-white" href="#">Sorteios</a>
        </li>
        <li className="nav-item">
          <a className="nav-link text-white" href="#">Análises</a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
