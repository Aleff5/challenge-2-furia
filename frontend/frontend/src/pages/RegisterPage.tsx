import { useState } from "react";
import { Form, Button, Container, Alert } from "react-bootstrap";

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  nome: string;
  cpf: string;
  idade?: number;
  bio?: string;
  estado?: string;
  endereco?: string;
  interesses?: string;
}

export default function RegisterPage() {
  const [formData, setFormData] = useState<RegisterRequest>({
    username: "",
    email: "",
    password: "",
    nome: "",
    cpf: "",
    idade: undefined,
    bio: "",
    interesses: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === "idade" ? (value ? parseInt(value) : undefined) : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Erro ao registrar usuário.");
      }

      await response.json();
      setSuccess("Usuário registrado com sucesso!");
    } catch (err: any) {
      setError(err.message || "Erro inesperado.");
    }
  };

  return (
    <Container className="mt-5">
      <h2>Cadastro</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">{success}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="username">
          <Form.Label>Usuário</Form.Label>
          <Form.Control type="text" name="username" onChange={handleChange} required />
        </Form.Group>

        <Form.Group controlId="nome">
          <Form.Label>Nome</Form.Label>
          <Form.Control type="text" name="nome" onChange={handleChange} required />
        </Form.Group>

        <Form.Group controlId="cpf">
          <Form.Label>CPF</Form.Label>
          <Form.Control type="text" name="cpf" onChange={handleChange} required />
        </Form.Group>

        <Form.Group controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" name="email" onChange={handleChange} required />
        </Form.Group>

        <Form.Group controlId="password">
          <Form.Label>Senha</Form.Label>
          <Form.Control type="password" name="password" onChange={handleChange} required />
        </Form.Group>

        <Form.Group controlId="idade">
          <Form.Label>Idade</Form.Label>
          <Form.Control type="number" name="idade" onChange={handleChange} min={0} />
        </Form.Group>

        <Form.Group controlId="bio">
          <Form.Label>Bio</Form.Label>
          <Form.Control as="textarea" rows={2} name="bio" onChange={handleChange} />
        </Form.Group>

        <Form.Group controlId="interesses">
          <Form.Label>Interesses</Form.Label>
          <Form.Control type="text" name="interesses" onChange={handleChange} />
        </Form.Group>

        <Button className="mt-3" type="submit">Cadastrar</Button>
      </Form>
    </Container>
  );
}
