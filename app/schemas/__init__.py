from pydantic import BaseModel


# Общий конфиг для всех pydantic моделей, чтобы не прописывать параметры везде заново
class TuneModel(BaseModel):
    model_config = {
        'from_attributes': True
    }