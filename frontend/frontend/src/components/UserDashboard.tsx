import { useNavigate, Outlet, NavLink } from "react-router-dom";
import { Container, Row, Col, Nav } from "react-bootstrap";

export default function UserDashboard() {
  const navigate = useNavigate();

  return (
    <Container fluid className="mt-4">
      <Row>
        {/* Sidebar */}
        <Col md={2} className="bg-light border-end min-vh-100">
          <h5 className="mt-4">Menu</h5>
          <Nav className="flex-column">
            <Nav.Link as={NavLink} to="/eventos">Eventos</Nav.Link>
            <Nav.Link as={NavLink} to="/sorteios">Sorteios</Nav.Link>
            <Nav.Link as={NavLink} to="/jogos">Jogos</Nav.Link>
            <Nav.Link as={NavLink} to="/ranking">Ranking</Nav.Link>
            <Nav.Link as={NavLink} to="/perfil">Perfil</Nav.Link>
            <Nav.Link as={NavLink} to="/loja">Loja</Nav.Link>
            </Nav>
        </Col>

        {/* Conteúdo principal (injetado pelas rotas filhas) */}
        <Col md={10} className="p-4">
          <Outlet />
        </Col>
      </Row>
    </Container>
  );
}
