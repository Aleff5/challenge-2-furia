import { useEffect, useState } from "react";
import { Card, Spinner, Alert } from "react-bootstrap";
import api from "../services/api";

interface UserRanking {
  id: number;
  username: string;
  score: number;
}

export default function RankingCard() {
  const [ranking, setRanking] = useState<UserRanking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get<UserRanking[]>("/admin/user-ranking")
      .then(res => {
        setRanking(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao carregar ranking");
        setLoading(false);
      });
  }, []);

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <Card.Title>🏆 Ranking dos Usuários</Card.Title>
        {loading ? <Spinner animation="border" size="sm" /> :
         error ? <Alert variant="danger">{error}</Alert> :
         <ol>
           {ranking.map(u => (
             <li key={u.id}>{u.username} - {u.score} pts</li>
           ))}
         </ol>}
      </Card.Body>
    </Card>
  );
}
