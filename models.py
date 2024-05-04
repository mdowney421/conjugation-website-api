from pydantic import BaseModel, Field


class RandomVerbCriteria(BaseModel):
    mood: str
    use_irregular: bool
    use_vosotros: bool
    tenses: list[str]
