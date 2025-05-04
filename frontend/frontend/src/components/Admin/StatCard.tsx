import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  bgColor?: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, bgColor = 'primary' }) => {
  return (
    <div className="col-md-6 col-lg-3 mb-4">
      <div className={`card text-white bg-${bgColor}`}>
        <div className="card-body">
          <h5 className="card-title">{title}</h5>
          <p className="card-text fs-4">{value}</p>
        </div>
      </div>
    </div>
  );
};

export default StatCard;
