import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DashboardMain from './pages/DashboardMain'; // layout base com menu lateral
import GamesPage from './pages/GamePage';
import AdminPage from './pages/AdminPage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import EventsPage from './pages/EventsPage';
import SorteiosPage from './pages/SorteioPage';
import RankingPage from './pages/Ranking'; // página de ranking
import Perfil from './pages/Perfil'; 
import 'bootstrap/dist/css/bootstrap.min.css';// página de perfil
// demais páginas:
// import PerfilPage from './pages/PerfilPage';
// import LojaPage from './pages/LojaPage';
// import RankingPage from './pages/RankingPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<DashboardMain />} />
        <Route path="/perfil" element={<Perfil />} />
        {/* <Route path="/loja" element={<LojaPage />} /> */}
        <Route path="/ranking" element={<RankingPage />} />
        <Route path="/games" element={<GamesPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/sorteios" element={<SorteiosPage />} />
        <Route path='/admin' element={<AdminPage />} />

        {/* Dashboard com rotas aninhadas */}

      </Routes>
    </Router>
  );
}

export default App;
