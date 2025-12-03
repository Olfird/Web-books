from pydantic import BaseModel, field_validator, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    year: int

    @field_validator('year')
    @classmethod
    def validate_year(cls, v):
        if v < 1000 or v > 2100:
            raise ValueError('Year must be between 1000 and 2100')
        return v


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AddBookOut(BaseModel):
    success: bool
    book_id: int