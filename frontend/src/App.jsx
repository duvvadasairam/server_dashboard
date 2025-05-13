import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { FiCpu, FiAlertTriangle, FiHardDrive, FiMoreVertical, FiUser } from 'react-icons/fi';
import { formatDistanceToNow } from 'date-fns';

function App() {
  const [servers, setServers] = useState([]);
  const [cpuUsage, setCpuUsage] = useState(null);
  const [ramUsageData, setRamUsageData] = useState([]);
  const [heatMapData, setHeatMapData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchServers = async () => {
      try {
        const response = await axios.get('https://backfinaldashboard-production.up.railway.app/servers');
        setServers(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    const fetchMetrics = async () => {
      try {
        const metricIds = [1, 2, 3, 4, 5]; // List of metric IDs
        const allRamUsageData = [];
        let cpuUsageData = null;

        // Define a sequential list of months
        const allMonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        for (const id of metricIds) {
          const response = await axios.get(`https://backfinaldashboard-production.up.railway.app/metrics/${id}`);
          const metrics = response.data;

          // Set CPU usage only for the first metric ID
          if (id === metricIds[0]) {
            cpuUsageData = metrics.cpu.cpu_usage;
          }

          // Get the month names sequentially for the current metric ID
          const monthNames = allMonths.slice((id - 1) * 1, (id - 1) * 2 + 5);

          // Aggregate RAM usage data with month names
          const ramUsage = metrics.ram.ram_usage.map((usage, index) => ({
            name: monthNames[index % monthNames.length], // Use month names sequentially
            usage,
          }));
          allRamUsageData.push(...ramUsage);
        }

        setCpuUsage(cpuUsageData);
        setRamUsageData(allRamUsageData);
      } catch (err) {
        console.error('Error fetching metrics:', err.message);
      }
    };

    const fetchAlerts = async () => {
      try {
        const response = await axios.get('https://backfinaldashboard-production.up.railway.app/alerts/count');
        const alertCounts = response.data;
        setHeatMapData([
          { name: 'Clear', value: alertCounts.clear, color: '#28a745' },
          { name: 'Critical', value: alertCounts.critical, color: '#dc3545' },
          { name: 'Trouble', value: alertCounts.trouble, color: '#ffc107' },
        ]);
      } catch (err) {
        console.error('Error fetching alerts:', err.message);
      }
    };

    fetchServers();
    fetchMetrics();
    fetchAlerts();
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Server Dashboard</h1>
      </header>
      <div className="widgets-grid">
        <div className="widget cpu-widget">
          <h2>CPU Daily Usage</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              {/* Background Arc */}
              <Pie
                data={[{ value: 100 }]}
                cx="50%"
                cy="50%"
                startAngle={180}
                endAngle={0}
                innerRadius={70}
                outerRadius={90}
                fill="#e0e0e0"
                dataKey="value"
              />
              {/* Foreground Arc */}
              <Pie
                data={[{ value: cpuUsage || 0 }]}
                cx="50%"
                cy="50%"
                startAngle={180}
                endAngle={180 - (cpuUsage || 0) * 1.8} // Scale 100% to 180 degrees
                innerRadius={70}
                outerRadius={90}
                fill={cpuUsage < 80 ? "#28a745" : "#dc3545"} // Green if <80%, Red otherwise
                dataKey="value"
              />
            </PieChart>
          </ResponsiveContainer>
          <p className="cpu-percentage">{cpuUsage ? `${cpuUsage.toFixed(2)}%` : 'Loading...'}</p>
          <p className="cpu-status">{cpuUsage && cpuUsage < 80 ? 'CPU usage is good' : 'High CPU usage detected'}</p>
        </div>

        <div className="widget alarms-widget">
          <FiAlertTriangle size={24} className="widget-icon" />
          <h2>12</h2>
          <p>Most Recent Alarams</p>
        </div>

        <div className="widget heatmap-widget">
          <h2>Heat Map</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={heatMapData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} >
                {heatMapData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="widget ram-widget">
          <h2>Ram Usage</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={ramUsageData}>
              <defs>
                <linearGradient id="colorUsage" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="usage"
                stroke="#8884d8"
                strokeWidth={2}
                fill="url(#colorUsage)"
                dot={false}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="active-instances-section">
        <h2>Active Instances</h2>
        {loading && <div className="loading-message">Loading server data...</div>}
        {error && <div className="error-message">Error fetching data: {error}</div>}
        {!loading && !error && servers.length === 0 && <p>No servers found.</p>}
        {!loading && !error && servers.length > 0 && (
          <table className="servers-table">
            <thead>
              <tr>
                <th>Servers</th>
                <th>IP Address</th>
                <th>Created</th>
                <th>Tag</th>
                <th>Provider</th>
                <th></th> 
              </tr>
            </thead>
            <tbody>
              {servers.map((server) => (
                <tr key={server.id}>
                  <td className="server-info">
                    <FiUser size={24} className="server-icon" />
                    <div>
                      <strong>{server.name}</strong>
                      <br />
                      <span className="server-specs">8GB/80GB/SF02-Ubuntu Iconic- jfkakf-daksl...</span> 
                    </div>
                  </td>
                  <td>{server.ip_address}</td>
                  <td>{formatDistanceToNow(new Date(server.created_at), { addSuffix: true })}</td>
                  <td><span className={`tag tag-${server.tag?.toLowerCase().replace(' ', '-')}`}>{server.tag}</span></td>
                  <td>{server.provider}</td>
                  <td><FiMoreVertical /></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;
