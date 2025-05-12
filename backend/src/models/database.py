from sqlalchemy import Column, Integer, String, Enum as DBEnum, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ServerStatus(enum.Enum):
    online = "online"
    offline = "offline"

class AlertSeverity(enum.Enum):
    critical = "critical"
    trouble = "trouble"
    clear = "clear"

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    tag = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    status = Column(DBEnum(ServerStatus), nullable=False, default=ServerStatus.online)

    alerts = relationship("Alert", back_populates="server")
    metrics = relationship("Metric", back_populates="server")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"))
    severity = Column(DBEnum(AlertSeverity), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    server = relationship("Server", back_populates="alerts")

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"))
    cpu_usage = Column(Float, nullable=False)
    ram_usage = Column(Float, nullable=False)  # Storing current RAM usage, historical data can be aggregated or stored differently
    disk_usage = Column(Float, nullable=False)
    app_usage = Column(Float, nullable=False)
    network_traffic = Column(Float, nullable=False) # Storing current network traffic
    timestamp = Column(DateTime, default=datetime.utcnow)

    server = relationship("Server", back_populates="metrics")
