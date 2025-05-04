import { Container, Row, Col } from "react-bootstrap";
import SidebarMenu from "../components/Sidebar";
import EventsCard from "../components/EventsCard";
import SorteiosCard from "../components/SorteiosCard";
import RankingCard from "../components/RankingCard";
import NewsCard from "../components/NewsCard";
import GamesCard from "../components/GamesCard";

export default function UserDashboard() {
  return (
    <Container fluid>
      <Row>
        <Col md={2}>
          <SidebarMenu />
        </Col>
        <Col md={10} className="p-4">
          <h2>Meu Dashboard</h2>
          <Row>
            <Col md={6}><EventsCard /></Col>
            <Col md={6}><SorteiosCard /></Col>
          </Row>
          <Row>
            <Col md={6}><RankingCard /></Col>
            <Col md={6}><NewsCard /></Col>
          </Row>
          <Row>
            <Col><GamesCard /></Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}
