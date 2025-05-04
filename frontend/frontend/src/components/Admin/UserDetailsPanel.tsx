import React from 'react';

interface User {
  username: string;
  points: number;
  events: number;
  raffles: number;
  social: string[];
  lastActive: string;
}

interface Props {
  user: User;
}

const UserDetailsPanel: React.FC<Props> = ({ user }) => {
  return (
    <div className="card mt-4">
      <div className="card-body">
        <h5 className="card-title">{user.username}</h5>
        <p className="mb-2"><strong>Pontuação:</strong> {user.points} pts</p>
        <p className="mb-2"><strong>Eventos Participados:</strong> {user.events}</p>
        <p className="mb-2"><strong>Sorteios Participados:</strong> {user.raffles}</p>
        <p className="mb-2">
          <strong>Redes Sociais:</strong> {user.social.join(', ')}
        </p>
        <p><strong>Última Atividade:</strong> {user.lastActive}</p>
      </div>
    </div>
  );
};

export default UserDetailsPanel;
