from fastapi import APIRouter, HTTPException, Path
from src.api.schemas.metric import ServerMetrics, CPUMetric, RAMMetric, DiskMetric, AppMetric, NetworkMetric

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/{server_id}", response_model=ServerMetrics)
async def get_server_metrics(server_id: int = Path(..., title="The ID of the server to get metrics for")):
    """Retrieve CPU, RAM, disk, app usage, and network traffic data for a specific server."""
    # Mock data as per UI/instructions
    # Actual implementation would fetch this from a database based on server_id
    if server_id not in [1, 2, 3]: # Assuming server IDs from mock server data
        raise HTTPException(status_code=404, detail="Server not found")

    cpu_metric = CPUMetric(cpu_usage=50.03)
    # RAM usage for 7 months (Jan-Jul) with values like 40, 60, 80, 50, 70, 30, 20.
    ram_metric = RAMMetric(ram_usage=[40.0, 60.0, 80.0, 50.0, 70.0, 30.0, 20.0])
    disk_metric = DiskMetric(disk_usage=75.0) # Mock value
    app_metric = AppMetric(app_usage=60.0)    # Mock value
    # Mock network traffic data (e.g., for the last 7 time points)
    network_metric = NetworkMetric(network_traffic=[10.0, 15.0, 12.0, 18.0, 20.0, 17.0, 22.0])

    return ServerMetrics(
        cpu=cpu_metric,
        ram=ram_metric,
        disk=disk_metric,
        app=app_metric,
        network=network_metric
    )
