import React from 'react';

interface RankingItem {
  name: string;
  followers: number;
}

interface RankingTableProps {
  title: string;
  data: RankingItem[];
}

const RankingTable: React.FC<RankingTableProps> = ({ title, data }) => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <table className="table table-sm table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>Nome</th>
              <th>Seguidores</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, idx) => (
              <tr key={idx}>
                <td>{idx + 1}</td>
                <td>{item.name}</td>
                <td>{item.followers}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RankingTable;
