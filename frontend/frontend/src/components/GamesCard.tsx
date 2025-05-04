import { useEffect, useState } from "react";
import { Card, Spinner, Alert } from "react-bootstrap";
import api from "../services/api";

interface Game {
  game_id: number;
  name: string;
  followers: number;
}

export default function GamesCard() {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get<Game[]>("/game/following")
      .then(res => {
        setGames(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao carregar jogos");
        setLoading(false);
      });
  }, []);

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <Card.Title>🎮 Jogos Seguidos</Card.Title>
        {loading ? <Spinner animation="border" size="sm" /> :
         error ? <Alert variant="danger">{error}</Alert> :
         <ul>{games.map(g => (
           <li key={g.game_id}>{g.name} ({g.followers} seguidores)</li>
         ))}</ul>}
      </Card.Body>
    </Card>
  );
}
