import { useState } from "react";
import { Form, Button, Container, Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import api from "../services/api"; // importe o cliente

interface LoginRequest {
  email: string;
  password: string;
}

export default function LoginPage() {
  const [credentials, setCredentials] = useState<LoginRequest>({ email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      await api.post("/auth/login", credentials); // ✅ usa Axios
      setSuccess("Login realizado com sucesso!");
      setTimeout(() => navigate("/dashboard"), 1000);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro inesperado.");
    }
  };

  return (
    <Container className="mt-5">
      <h2>Login</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">{success}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" name="email" onChange={handleChange} required />
        </Form.Group>

        <Form.Group controlId="password">
          <Form.Label>Senha</Form.Label>
          <Form.Control type="password" name="password" onChange={handleChange} required />
        </Form.Group>

        <Button className="mt-3" type="submit">Entrar</Button>
      </Form>
    </Container>
  );
}
