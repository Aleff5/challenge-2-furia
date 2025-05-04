import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button, Spinner, Alert } from "react-bootstrap";
import SidebarMenu from "../components/Sidebar";
import api from "../services/api"; // seu axios customizado com baseURL + withCredentials

interface Event {
  event_id: number;
  title: string;
  description?: string;
  event_date: string;
}

const AllEvents: React.FC = () => {
  const [allEvents, setAllEvents] = useState<Event[]>([]);
  const [myEvents, setMyEvents] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const [allRes, myRes] = await Promise.all([
          api.get<Event[]>("/events/allevents"),
          api.get<Event[]>("/events/myevents"),
        ]);

        setAllEvents(allRes.data);
        setMyEvents(myRes.data.map(e => e.event_id));
      } catch (err) {
        console.error("Erro ao carregar eventos", err);
        setError("Não foi possível carregar os eventos.");
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const handleJoin = async (id: number) => {
    try {
      await api.post("/events/join", { event_id: id });
      setMyEvents(prev => [...prev, id]);
    } catch {
      alert("Erro ao participar do evento.");
    }
  };

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
        <p>Carregando eventos...</p>
      </Container>
    );
  }

  return (
    <Container fluid>
      <Row>
        <Col md={2}>
          <SidebarMenu />
        </Col>
        <Col md={10} className="p-4">
          <h2 className="mb-4">📅 Todos os Eventos</h2>
          {error && <Alert variant="danger">{error}</Alert>}

          <Row xs={1} md={2} lg={3} className="g-4">
            {allEvents.map(event => (
              <Col key={event.event_id}>
                <Card className={myEvents.includes(event.event_id) ? "border-success" : ""}>
                  <Card.Body>
                    <Card.Title>{event.title}</Card.Title>
                    <Card.Text>
                      {event.description}<br />
                      <small className="text-muted">Data: {new Date(event.event_date).toLocaleDateString()}</small>
                    </Card.Text>
                    {myEvents.includes(event.event_id) ? (
                      <Button variant="outline-success" disabled>Inscrito</Button>
                    ) : (
                      <Button variant="primary" onClick={() => handleJoin(event.event_id)}>Participar</Button>
                    )}
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default AllEvents;
