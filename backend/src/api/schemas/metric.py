from pydantic import BaseModel
from typing import List

class CPUMetric(BaseModel):
    cpu_usage: float

class RAMMetric(BaseModel):
    ram_usage: List[float] # Representing usage over time, e.g., last 7 months

class DiskMetric(BaseModel):
    disk_usage: float

class AppMetric(BaseModel):
    app_usage: float

class NetworkMetric(BaseModel):
    network_traffic: List[float] # Representing incoming traffic over time

class ServerMetrics(BaseModel):
    cpu: CPUMetric
    ram: RAMMetric
    disk: DiskMetric # Not in UI, but in instructions
    app: AppMetric     # Not in UI, but in instructions
    network: NetworkMetric # To be implemented in UI
