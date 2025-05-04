import { useEffect, useState } from "react";
import { Card, Spinner, Alert } from "react-bootstrap";
import api from "../services/api"; 


interface Event {
  event_id: number;
  title: string;
  event_date: string;
}

export default function EventsCard() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get<Event[]>("/events/myevents")
      .then(res => {
        setEvents(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao carregar eventos");
        setLoading(false);
      });
  }, []);

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <Card.Title>🎫 Eventos Participando</Card.Title>
        {loading ? <Spinner animation="border" size="sm" /> :
         error ? <Alert variant="danger">{error}</Alert> :
         <ul>
           {events.map(e => (
             <li key={e.event_id}>{e.title} - {new Date(e.event_date).toLocaleDateString()}</li>
           ))}
         </ul>}
      </Card.Body>
    </Card>
  );
}
