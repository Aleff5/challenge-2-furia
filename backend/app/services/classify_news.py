from typing import List, Dict
import json
import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def classify_news_by_user(news_list: List[Dict], user_profile: Dict) -> List[Dict]:
    # Exemplo do formato esperado para few-shot learning
    examples = """
    Exemplo de resposta esperada:
    [
        {
            "title": "Novo jogo da série X anunciado",
            "link": "https://exemplo.com/noticia1",
            "relevante": true
        },
        {
            "title": "Política econômica atualizada",
            "link": "https://exemplo.com/noticia2",
            "relevante": false
        }
    ]
    """
    
    user_prompt = f"""
    Com base no perfil abaixo, classifique cada notícia como relevante (true) ou irrelevante (false).
    Retorne APENAS um JSON válido com a estrutura especificada, sem comentários ou markdown.

    Perfil do usuário:
    - Bio: {user_profile['bio']}
    - Interesses: {', '.join(user_profile['interests'])}
    - Jogos Seguidos: {', '.join(user_profile['games_followed'])}

    {examples}

    Notícias para classificar:
    """
    
    for i, news in enumerate(news_list[:50]):  # Limita a 50 notícias por segurança
        user_prompt += f"{i+1}. {news['title']} - {news.get('summary', '')}\n"

    try:
        response = model.generate_content(
            user_prompt,
            generation_config={
                "temperature": 0.3,  # Menos criatividade, mais factual
                "response_mime_type": "application/json"
            }
        )
        
        # Parse seguro do JSON
        result = json.loads(response.text)
        return result
        
    except Exception as e:
        print(f"Erro ao classificar notícias: {str(e)}")
        # Retorna todas como irrelevantes em caso de erro
        return [{
            "title": news["title"],
            "link": news.get("link", ""),
            "relevante": False
        } for news in news_list]