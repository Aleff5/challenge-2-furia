// components/Admin/EngagementChart.tsx
import React from 'react';
import { Line } from 'react-chartjs-2';

const EngagementChart = ({ engagementData }: { engagementData: { date: string; likes: number }[] }) => {
  const data = {
    labels: engagementData.map(e => e.date),
    datasets: [{
      label: 'Curtidas em posts da FURIA',
      data: engagementData.map(e => e.likes),
      borderColor: '#1cc88a',
      backgroundColor: 'rgba(28,200,138,0.1)',
      tension: 0.4,
    }],
  };

  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Engajamento com a FURIA</h5>
        <Line data={data} />
      </div>
    </div>
  );
};

export default EngagementChart;
