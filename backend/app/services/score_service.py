from app.models.user import User

async def add_score(user: User, points: int):
    user.score += points
    await user.save()
    # Futuramente: salvar histórico de pontos com motivo
''