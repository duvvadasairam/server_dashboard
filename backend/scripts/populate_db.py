import asyncio
# Remove Faker import as it's no longer used for primary data generation
# from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys
import os
import json # Added for JSON handling
from datetime import datetime, timezone # Ensure timezone is imported for UTC conversion

#Begin debug prints
print(f"Initial __file__: {__file__}")
print(f"Initial os.path.abspath(__file__): {os.path.abspath(__file__)}")
backend_dir_calc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Calculated backend_dir: {backend_dir_calc}")
sys.path.insert(0, backend_dir_calc)
print(f"sys.path after insert: {sys.path}")

src_path_check = os.path.join(backend_dir_calc, 'src')
print(f"Expected src_path: {src_path_check}")
print(f"Does src_path exist? {os.path.exists(src_path_check)}")
print(f"Is src_path a directory? {os.path.isdir(src_path_check)}")
# end debug prints

from src.models.database import Base, Server, Alert, Metric, ServerStatus, AlertSeverity
# Remove timedelta and random if no longer needed after full replacement
#import random 
#from datetime import timedelta 
from dotenv import load_dotenv

# Load .env from the 'backend' directory (parent of 'scripts')
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Check .env file path and content.")

async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def populate_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    await create_tables(engine) # Assuming Alembic handles table creation

    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # Define path for the user data JSON file
    user_data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data.json')

    try:
        with open(user_data_file_path, 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {user_data_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {user_data_file_path}")
        return

    async with AsyncSessionLocal() as session:
        async with session.begin():
            created_servers_map = {} # To map JSON server name/identifier to DB server object for relations

            for server_data_json in user_data.get("servers", []):
                #Convert string dates to datetime objects
                #Assuming created_at is in ISO 8601 format and needs to be UTC
                created_at_dt_aware = datetime.fromisoformat(server_data_json["created_at"].replace('Z', '+00:00'))
                # Convert to naive UTC datetime for TIMESTAMP WITHOUT TIME ZONE columns
                created_at_dt_naive = created_at_dt_aware.astimezone(timezone.utc).replace(tzinfo=None)
                
                server = Server(
                    name=server_data_json["name"],
                    ip_address=server_data_json["ip_address"],
                    created_at=created_at_dt_naive, # Use naive UTC datetime
                    tag=server_data_json["tag"],
                    provider=server_data_json["provider"],
                    status=ServerStatus[server_data_json["status"]] # Convert string to Enum
                )
                session.add(server)
                
                #Flush to get the server ID for immediate use in related alerts/metrics.
                

                await session.flush() 
                await session.refresh(server) # Ensure the server object has the ID
                created_servers_map[server_data_json["name"]] = server # Or use another unique ID from JSON if available

                # Create Alerts for this server
                for alert_data_json in server_data_json.get("alerts", []):
                    timestamp_dt_aware = datetime.fromisoformat(alert_data_json["timestamp"].replace('Z', '+00:00'))
                    # Convert to naive UTC datetime
                    timestamp_dt_naive = timestamp_dt_aware.astimezone(timezone.utc).replace(tzinfo=None)

                    alert = Alert(
                        server_id=server.id,
                        severity=AlertSeverity[alert_data_json["severity"]], # Convert string to Enum
                        message=alert_data_json["message"],
                        timestamp=timestamp_dt_naive # Use naive UTC datetime
                    )
                    session.add(alert)

                # Create Metrics for this server
                for metric_data_json in server_data_json.get("metrics", []):
                    metric_timestamp_dt_aware = datetime.fromisoformat(metric_data_json["timestamp"].replace('Z', '+00:00'))
                    # Convert to naive UTC datetime
                    metric_timestamp_dt_naive = metric_timestamp_dt_aware.astimezone(timezone.utc).replace(tzinfo=None)
                    
                    metric = Metric(
                        server_id=server.id,
                        cpu_usage=metric_data_json["cpu_usage"],
                        ram_usage=metric_data_json["ram_usage"],
                        disk_usage=metric_data_json["disk_usage"],
                        app_usage=metric_data_json["app_usage"],
                        network_traffic=metric_data_json["network_traffic"],
                        timestamp=metric_timestamp_dt_naive # Use naive UTC datetime
                    )
                    session.add(metric)
            
           

        await session.commit()
    await engine.dispose()

if __name__ == "__main__":
    print("Attempting to populate database...") # DEBUG
    asyncio.run(populate_db())
    print("Database populated with mock data.")
