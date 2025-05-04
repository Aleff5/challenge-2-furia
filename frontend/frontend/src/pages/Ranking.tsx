import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Spinner, Alert, Table } from "react-bootstrap";
import SidebarMenu from "../components/Sidebar";
import api from "../services/api";

interface UserRanking {
  id: number;
  username: string;
  score: number;
}

const Ranking: React.FC = () => {
  const [ranking, setRanking] = useState<UserRanking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchRanking = async () => {
      try {
        const response = await api.get<UserRanking[]>("/admin/user-ranking");
        setRanking(response.data);
      } catch (err) {
        console.error("Erro ao carregar ranking", err);
        setError("Erro ao carregar ranking dos usuários.");
      } finally {
        setLoading(false);
      }
    };

    fetchRanking();
  }, []);

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
        <p>Carregando ranking...</p>
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
          <h2 className="mb-4">🏆 Ranking dos Usuários</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          {ranking.length === 0 && !error ? (
            <Alert variant="info">Nenhum dado de ranking disponível.</Alert>
          ) : (
            <Card>
              <Card.Body>
                <Table striped bordered hover responsive>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Usuário</th>
                      <th>Pontuação</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ranking.map((user, index) => (
                      <tr key={user.id}>
                        <td>{index + 1}</td>
                        <td>{user.username}</td>
                        <td>{user.score}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default Ranking;
