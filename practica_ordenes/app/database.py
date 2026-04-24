from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./ordenes.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    # app.models defines all table models — importing it registers them with SQLModel metadata
    import app.models  # noqa: F401  # Product, Order, OrderItem
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
