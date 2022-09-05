import asyncio
import warnings
from config.settings import settings
from config.database_conn import __engine
import modules.__all_models


warnings.filterwarnings("ignore", category=DeprecationWarning)


async def create_tables() -> None:

    print("Creating tables on database...")

    async with __engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tables created successfully.')

if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(create_tables())
