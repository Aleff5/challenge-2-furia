import React, { useEffect, useState } from "react";
import { Card, Container, Row, Col, Spinner, Alert, Navbar, Nav } from "react-bootstrap";
import axios from "axios";
import "./css/AdminDashboard.css";

export default function AdminDashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState<any>({});

  const endpoints = [
    { key: "totalUsers", url: "http://localhost:8000/admin/total_users" },
    { key: "usersByState", url: "http://localhost:8000/admin/users_by_state" },
    { key: "mostFollowedGames", url: "http://localhost:8000/admin/most_followed_games" },
    { key: "eventEngagement", url: "http://localhost:8000/admin/event_engagement" },
    { key: "verifiedUsers", url: "http://localhost:8000/admin/verified-users" },
    { key: "ageDistribution", url: "http://localhost:8000/admin/age-distribution" },
    { key: "userRanking", url: "http://localhost:8000/admin/user-ranking" },
    { key: "sorteiosAtivos", url: "http://localhost:8000/admin/sorteios-ativos" },
    { key: "eventosAtivos", url: "http://localhost:8000/admin/eventos-ativos" },
    { key: "userGrowth", url: "http://localhost:8000/admin/crescimento-usuarios" },
  ];

  useEffect(() => {
    async function fetchData() {
      try {
        const results = await Promise.all(
          endpoints.map((endpoint) => axios.get(endpoint.url))
        );

        const newData: any = {};
        endpoints.forEach((endpoint, idx) => {
          newData[endpoint.key] = results[idx].data;
        });
        setData(newData);
      } catch (err: any) {
        setError("Erro ao carregar dados do dashboard.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) return <Spinner animation="border" className="loading-spinner" />;
  if (error) return <Alert variant="danger">{error}</Alert>;

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg" sticky="top" className="navbar-custom">
        <Container>
          <Navbar.Brand href="#">Painel Administrativo</Navbar.Brand>
          <Navbar.Toggle aria-controls="admin-navbar" />
          <Navbar.Collapse id="admin-navbar">
            <Nav className="ms-auto">
              <Nav.Link href="#">Dashboard</Nav.Link>
              <Nav.Link href="#">Configurações</Nav.Link>
              <Nav.Link href="#">Sair</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="mt-4">
        <Row>
          <Col>
            <Card body>
              <h5>Total de Usuários</h5>
              <p className="big-number">{data.totalUsers.total_users}</p>
            </Card>
          </Col>
          <Col>
            <Card body>
              <h5>Usuários Verificados</h5>
              <p className="big-number">{data.verifiedUsers.usuarios_verificados}</p>
            </Card>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col>
            <Card body>
              <h5>Usuários por Estado</h5>
              <ul>
                {data.usersByState.map((item: any, idx: number) => (
                  <li key={idx}>{item.estado}: {item.total}</li>
                ))}
              </ul>
            </Card>
          </Col>

          <Col>
            <Card body>
              <h5>Distribuição por Idade</h5>
              <ul>
                {Object.entries(data.ageDistribution).map(([age, count]: any, idx: number) => (
                  <li key={idx}>{age}: {count}</li>
                ))}
              </ul>
            </Card>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col>
            <Card body>
              <h5>Jogos Mais Seguidos</h5>
              <ul>
                {data.mostFollowedGames.map((game: any, idx: number) => (
                  <li key={idx}>{game.nome}: {game.seguidores} seguidores</li>
                ))}
              </ul>
            </Card>
          </Col>

          <Col>
            <Card body>
              <h5>Engajamento em Eventos</h5>
              <ul>
                {data.eventEngagement.map((event: any, idx: number) => (
                  <li key={idx}>{event.title}: {event.participantes} participantes</li>
                ))}
              </ul>
            </Card>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col>
            <Card body>
              <h5>Ranking de Usuários</h5>
              <ol>
                {data.userRanking.map((user: any, idx: number) => (
                  <li key={idx}>{user.username} - {user.score} pontos</li>
                ))}
              </ol>
            </Card>
          </Col>

          <Col>
            <Card body>
              <h5>Crescimento de Usuários</h5>
              <ul>
                {data.userGrowth.map((item: any, idx: number) => (
                  <li key={idx}>{item.mes}: {item.total}</li>
                ))}
              </ul>
            </Card>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col>
            <Card body>
              <h5>Sorteios Ativos</h5>
              <ul>
                {data.sorteiosAtivos.ativos.map((sorteio: any, idx: number) => (
                  <li key={idx}>{sorteio.title}</li>
                ))}
              </ul>
            </Card>
          </Col>

          <Col>
            <Card body>
              <h5>Eventos Ativos</h5>
              <ul>
                {data.eventosAtivos.ativos.map((evento: any, idx: number) => (
                  <li key={idx}>{evento.title}</li>
                ))}
              </ul>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}
