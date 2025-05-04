import React, { useState } from 'react';
import UserDetailsPanel from './UserDetailsPanel';

interface User {
  username: string;
  points: number;
  events: number;
  raffles: number;
  social: string[];
  lastActive: string;
}

const mockUsers: User[] = [
  {
    username: '@furiagamer',
    points: 1250,
    events: 5,
    raffles: 2,
    social: ['Twitter', 'Discord'],
    lastActive: '2025-04-28 15:00',
  },
  {
    username: '@cspro',
    points: 980,
    events: 2,
    raffles: 1,
    social: ['Twitter'],
    lastActive: '2025-04-27 20:12',
  },
];

const UserSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const filteredUsers = mockUsers.filter((user) =>
    user.username.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="mb-4">
      <h5 className="mb-2">Buscar usuário</h5>
      <input
        className="form-control mb-2"
        type="text"
        placeholder="Digite o @username..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {query && (
        <ul className="list-group">
          {filteredUsers.map((user, index) => (
            <li
              key={index}
              className="list-group-item list-group-item-action"
              onClick={() => setSelectedUser(user)}
              style={{ cursor: 'pointer' }}
            >
              {user.username}
            </li>
          ))}
        </ul>
      )}
      {selectedUser && <UserDetailsPanel user={selectedUser} />}
    </div>
  );
};

export default UserSearch;
