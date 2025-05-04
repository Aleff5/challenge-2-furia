import React from 'react';

const PopularEventsList = () => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Eventos mais populares</h5>
        <ul className="list-group">
          <li className="list-group-item">🔥 Final CBLOL - 320 participantes</li>
          <li className="list-group-item">🎯 Torneio FURIA FPS - 210 participantes</li>
          <li className="list-group-item">🎮 Game Night - 185 participantes</li>
        </ul>
      </div>
    </div>
  );
};

export default PopularEventsList;
