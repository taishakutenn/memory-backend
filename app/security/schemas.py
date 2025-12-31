from app.schemas import TuneModel


class Token(TuneModel):
    """Модель, используемая для ответа токеном при авторизации"""
    access_token: str
    token_type: str


class TokenData(TuneModel):
    """Модель данных для сериализации пользователя"""
    username: str | None = None
