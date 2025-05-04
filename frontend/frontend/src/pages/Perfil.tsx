import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button, Form, Spinner, Alert } from "react-bootstrap";
import SidebarMenu from "../components/Sidebar";
import api from "../services/api";

interface User {
  nome: string;
  email: string;
}

const Perfil: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [docFile, setDocFile] = useState<File | null>(null);
  const [selfieFile, setSelfieFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get<User>("/auth/me");
        setUser(response.data);
      } catch (err) {
        setError("Erro ao carregar perfil.");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const handleVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!docFile || !selfieFile) return setError("Por favor, envie os dois arquivos.");

    const formData = new FormData();
    formData.append("document", docFile);
    formData.append("selfie", selfieFile);

    try {
      setUploading(true);
      await api.post("/documents/check", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccess("Documentos enviados com sucesso!");
      setError("");
    } catch {
      setError("Erro ao enviar os arquivos.");
      setSuccess("");
    } finally {
      setUploading(false);
    }
  };

  const connect = (provider: "twitter" | "steam" | "discord") => {
    let url = "";
    switch (provider) {
      case "twitter":
        url = "http://localhost:8000/twitter/auth/social/";
        break;
      case "steam":
        url = "http://localhost:8000/steam/auth/social";
        break;
      case "discord":
        url = "http://localhost:8000/discord/auth/social";
        break;
    }
    window.location.href = url;
  };

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
        <p>Carregando perfil...</p>
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
          <h2>👤 Meu Perfil</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          {success && <Alert variant="success">{success}</Alert>}

          {user && (
            <Card className="mb-4">
              <Card.Body>
                <Card.Title>{user.nome}</Card.Title>
                <Card.Text>{user.email}</Card.Text>
              </Card.Body>
            </Card>
          )}

          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Verificação de Identidade</Card.Title>
              <Form onSubmit={handleVerification}>
                <Form.Group className="mb-3">
                  <Form.Label>Documento (frente)</Form.Label>
                  <Form.Control type="file" accept="image/*" onChange={e => setDocFile((e.target as HTMLInputElement).files?.[0] || null)} />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Selfie segurando o documento</Form.Label>
                  <Form.Control type="file" accept="image/*" onChange={e => setSelfieFile((e.target as HTMLInputElement).files?.[0] || null)} />
                </Form.Group>
                <Button type="submit" variant="primary" disabled={uploading}>
                  {uploading ? "Enviando..." : "Enviar para verificação"}
                </Button>
              </Form>
            </Card.Body>
          </Card>

          <Card>
            <Card.Body>
              <Card.Title>Conectar Redes Sociais</Card.Title>
              <div className="d-flex flex-wrap gap-3">
                <Button variant="info" onClick={() => connect("twitter")}>Conectar com Twitter</Button>
                <Button variant="dark" onClick={() => connect("steam")}>Conectar com Steam</Button>
                <Button variant="secondary" onClick={() => connect("discord")}>Conectar com Discord</Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Perfil;
