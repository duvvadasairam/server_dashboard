from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.api.schemas.metric import ServerMetrics, CPUMetric, RAMMetric, DiskMetric, AppMetric, NetworkMetric
from src.models.database import Metric  # Ensure Metric is the ORM model for the metric table
from src.database import get_db, AsyncSessionLocal
import asyncio

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/{server_id}", response_model=ServerMetrics)
async def get_server_metrics(
    server_id: int = Path(..., title="The ID of the server to get metrics for"),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(Metric).where(Metric.server_id == server_id).order_by(Metric.timestamp))
        metrics = result.scalars().all()
        if not metrics:
            raise HTTPException(status_code=404, detail="Metrics not found for the server")

        # Extract all RAM usage values
        ram_usage = [metric.ram_usage for metric in metrics]

        # Use the latest metric for other fields
        latest_metric = metrics[-1]
        cpu_metric = CPUMetric(cpu_usage=latest_metric.cpu_usage)
        disk_metric = DiskMetric(disk_usage=latest_metric.disk_usage)
        app_metric = AppMetric(app_usage=latest_metric.app_usage)
        network_metric = NetworkMetric(network_traffic=[latest_metric.network_traffic])

        return ServerMetrics(
            cpu=cpu_metric,
            ram=RAMMetric(ram_usage=ram_usage),
            disk=disk_metric,
            app=app_metric,
            network=network_metric
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def main():
    """
    Test the get_server_metrics function by simulating a database session.
    """
    print("🚀 Starting main function to test get_server_metrics...", flush=True)
    async with AsyncSessionLocal() as session:
        try:
            # Replace `3` with the desired server_id for testing
            server_id = 3
            result = await get_server_metrics(server_id=server_id, db=session)
            print("✅ Test successful. Result:", result, flush=True)
        except Exception as e:
            print(f"❌ Test failed. Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())