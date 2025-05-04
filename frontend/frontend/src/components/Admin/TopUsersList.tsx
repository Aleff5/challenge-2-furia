import React from 'react';

const TopUsersList = () => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <h5 className="card-title">Top usuários (pontuação)</h5>
        <ul className="list-group">
          <li className="list-group-item">1. @player1 - 1450 pts</li>
          <li className="list-group-item">2. @gamerpro - 1330 pts</li>
          <li className="list-group-item">3. @furiavip - 1220 pts</li>
        </ul>
      </div>
    </div>
  );
};

export default TopUsersList;
