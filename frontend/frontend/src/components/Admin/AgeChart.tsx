import React from 'react';
import { Bar } from 'react-chartjs-2';

const AgeChart = ({ ageData }: { ageData: { ageRange: string; count: number }[] }) => {
  const data = {
    labels: ageData.map(a => a.ageRange),
    datasets: [{
      label: 'Usuários por faixa etária',
      data: ageData.map(a => a.count),
      backgroundColor: '#4e73df',
    }],
  };

  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Distribuição de Idade</h5>
        <Bar data={data} />
      </div>
    </div>
  );
};

export default AgeChart;
