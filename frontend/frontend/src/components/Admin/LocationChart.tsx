// components/Admin/LocationChart.tsx
import React from 'react';
import { Pie } from 'react-chartjs-2';

const LocationChart = ({ locationData }: { locationData: { city: string; count: number }[] }) => {
  const data = {
    labels: locationData.map(loc => loc.city),
    datasets: [{
      data: locationData.map(loc => loc.count),
      backgroundColor: ['#36a2eb', '#ff6384', '#ffcd56', '#4bc0c0', '#9966ff'],
    }],
  };

  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Localização dos Usuários</h5>
        <Pie data={data} />
      </div>
    </div>
  );
};

export default LocationChart;
