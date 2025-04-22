"""
Script để chạy migration với FastAPI
"""
from src import engine, Base
from alembic.config import Config
from alembic import command

def create_tables():
    """
    Tạo tất cả các bảng trong database
    """
    Base.metadata.create_all(bind=engine)

def run_migrations():
    """
    Chạy migrations với Alembic
    """
    alembic_cfg = Config("migrations/alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        create_tables()
    else:
        run_migrations()