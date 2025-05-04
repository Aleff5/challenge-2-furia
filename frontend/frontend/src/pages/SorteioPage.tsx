import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button, Spinner, Alert } from "react-bootstrap";
import SidebarMenu from "../components/Sidebar";
import api from "../services/api";

interface Sorteio {
  sorteio_id: number;
  title: string;
  description?: string;
  start_date: string;
  end_date: string;
}

const AllSorteios: React.FC = () => {
  const [sorteios, setSorteios] = useState<Sorteio[]>([]);
  const [joined, setJoined] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSorteios = async () => {
      try {
        const [all, mine] = await Promise.all([
          api.get<Sorteio[]>("/sorteio/all"),
          api.get<Sorteio[]>("/sorteio/myraffles"),
        ]);

        setSorteios(all.data);
        setJoined(mine.data.map((s) => s.sorteio_id));
      } catch (err) {
        console.error("Erro ao carregar sorteios", err);
        setError("Erro ao carregar sorteios.");
      } finally {
        setLoading(false);
      }
    };

    fetchSorteios();
  }, []);

  const handleParticipar = (id: number) => {
    api.post("/sorteio/join", { sorteio_id: id })
      .then(() => setJoined((prev) => [...prev, id]))
      .catch(() => alert("Erro ao participar do sorteio."));
  };

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
        <p>Carregando sorteios...</p>
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
          <h2 className="mb-4">🎁 Todos os Sorteios</h2>
          {error && <Alert variant="danger">{error}</Alert>}

          <Row xs={1} md={2} lg={3} className="g-4">
            {sorteios.map((s) => (
              <Col key={s.sorteio_id}>
                <Card className={joined.includes(s.sorteio_id) ? "border-success" : ""}>
                  <Card.Body>
                    <Card.Title>{s.title}</Card.Title>
                    <Card.Text>
                      {s.description}<br />
                      <small className="text-muted">
                        De: {new Date(s.start_date).toLocaleDateString()} <br />
                        Até: {new Date(s.end_date).toLocaleDateString()}
                      </small>
                    </Card.Text>
                    {joined.includes(s.sorteio_id) ? (
                      <Button variant="outline-success" disabled>Inscrito</Button>
                    ) : (
                      <Button variant="warning" onClick={() => handleParticipar(s.sorteio_id)}>Participar</Button>
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

export default AllSorteios;
