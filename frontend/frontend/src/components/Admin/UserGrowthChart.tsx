import React from 'react';

const UserGrowthChart = () => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Novos usuários (semana)</h5>
        <div style={{ height: '200px', background: '#eee' }}>
          <p className="text-center pt-5 text-muted">[Gráfico de barras aqui]</p>
        </div>
      </div>
    </div>
  );
};

export default UserGrowthChart;
