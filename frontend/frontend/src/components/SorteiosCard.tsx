import { useEffect, useState } from "react";
import { Card, Spinner, Alert } from "react-bootstrap";
import api from "../services/api";

interface Sorteio {
  sorteio_id: number;
  title: string;
}

export default function SorteiosCard() {
  const [sorteios, setSorteios] = useState<Sorteio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get<Sorteio[]>("/sorteio/myraffles")
      .then(res => {
        setSorteios(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao carregar sorteios");
        setLoading(false);
      });
  }, []);

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <Card.Title>🎁 Sorteios Participando</Card.Title>
        {loading ? <Spinner animation="border" size="sm" /> :
         error ? <Alert variant="danger">{error}</Alert> :
         <ul>{sorteios.map(s => (
           <li key={s.sorteio_id}>{s.title}</li>
         ))}</ul>}
      </Card.Body>
    </Card>
  );
}
