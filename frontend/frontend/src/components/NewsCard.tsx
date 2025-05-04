import { useEffect, useState } from "react";
import { Card, Spinner, Alert } from "react-bootstrap";
import api from "../services/api";

interface NewsItem {
  title: string;
  link: string;
  relevante: boolean;
}

export default function NewsCard() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get<{ news: NewsItem[] }>("/ia/personalized_news")
      .then((res: { data: { news: NewsItem[] } }) => {
        const response: NewsItem[] = res.data.news || [];
        setNews(response.filter((n: NewsItem) => n.relevante));
      })
      .catch(() => setError("Erro ao carregar feed de notícias"))
      .then(() => setLoading(false));
  }, []);

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <Card.Title>📰 Feed de Notícias</Card.Title>
        {loading ? <Spinner animation="border" size="sm" /> :
         error ? <Alert variant="danger">{error}</Alert> :
         <ul>
           {news.map((n, i) => (
             <li key={i}>
               <a href={n.link} target="_blank" rel="noopener noreferrer">
                 <strong>{n.title}</strong>
               </a>
             </li>
           ))}
         </ul>}
      </Card.Body>
    </Card>
  );
}
