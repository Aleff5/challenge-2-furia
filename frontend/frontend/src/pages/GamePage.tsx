import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button, Spinner, Alert } from "react-bootstrap";
import SidebarMenu from "../components/Sidebar"; // ou SidebarMenu, conforme seu projeto
import api from "../services/api";

interface Game {
  game_id: number;
  name: string;
  followers: number;
}

const AllGames: React.FC = () => {
  const [games, setGames] = useState<Game[]>([]);
  const [following, setFollowing] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const [all, mine] = await Promise.all([
          api.get<Game[]>("/game/all"),
          api.get<Game[]>("/game/following"),
        ]);
        setGames(all.data);
        setFollowing(mine.data.map((g) => g.game_id));
      } catch (err) {
        console.error("Erro ao carregar jogos", err);
        setError("Erro ao carregar jogos.");
      } finally {
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  const handleFollow = (id: number) => {
    api.post("/game/follow", { game_id: id })
      .then(() => setFollowing((prev) => [...prev, id]))
      .catch(() => alert("Erro ao seguir o jogo."));
  };

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
        <p>Carregando jogos...</p>
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
          <h2>🎮 Lista de Jogos</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          {games.length === 0 && !error ? (
            <Alert variant="info">Nenhum jogo encontrado.</Alert>
          ) : (
            <Row>
              {games.map((game) => (
                <Col key={game.game_id} md={4} className="mb-4">
                  <Card>
                    <Card.Body>
                      <Card.Title>{game.name}</Card.Title>
                      <Card.Text>Seguidores: {game.followers}</Card.Text>
                      <Button
                        variant={following.includes(game.game_id) ? "secondary" : "primary"}
                        onClick={() => handleFollow(game.game_id)}
                        disabled={following.includes(game.game_id)}
                      >
                        {following.includes(game.game_id) ? "Seguindo" : "Seguir"}
                      </Button>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </Row>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default AllGames;
