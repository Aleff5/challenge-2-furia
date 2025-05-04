import { Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function SidebarMenu() {
  return (
    <div className="bg-light p-3" style={{ height: "100vh", minWidth: "200px" }}>
      <h5>Menu</h5>
      <Nav className="flex-column">
        <Nav.Item>
          <Nav.Link as={Link} to="/events">🎫 Eventos</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link as={Link} to="/sorteios">🎁 Sorteios</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link as={Link} to="/games">🎮 Jogos</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link as={Link} to="/ranking">🏆 Ranking</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link as={Link} to="/perfil">👤 Perfil</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link as={Link} to="https://www.furia.gg">🛒 Loja</Nav.Link>
        </Nav.Item>
      </Nav>
    </div>
  );
}
