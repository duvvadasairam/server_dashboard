import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { FiCpu, FiAlertTriangle, FiHardDrive, FiMoreVertical, FiUser } from 'react-icons/fi';
import { formatDistanceToNow } from 'date-fns';

function App() {
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchServers = async () => {
      try {
        const response = await axios.get('https://skillful-mindfulness-production.up.railway.app/servers');
        setServers(response.data);
        //console.log(response.data); for checking
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchServers();
  }, []);

  //dummy data for few components
  const cpuData = [{ name: 'CPU Usage', value: 50.03 }];
  const COLORS = ['#0088FE', '#FFBB28', '#FF8042']; // Colors for pie chart segments

  const heatMapData = [
    { name: 'Clear', value: 60, color: '#28a745' }, // Green
    { name: 'Critical', value: 30, color: '#dc3545' }, // Red
    { name: 'Trouble', value: 10, color: '#ffc107' }, // Yellow
  ];

  const ramUsageData = [
    { name: 'Jan', usage: 30 },
    { name: 'Feb', usage: 70 },
    { name: 'Mar', usage: 60 },
    { name: 'Apr', usage: 100 },
    { name: 'May', usage: 80 },
    { name: 'Jun', usage: 50 },
    { name: 'Jul', usage: 70 },
  ];

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
              <Pie
                data={cpuData}
                cx="50%"
                cy="50%"
                startAngle={180}
                endAngle={0}
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                <Cell fill="#0088FE" /> 
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <p className="cpu-percentage">{cpuData[0].value}%</p>
          <p className="cpu-status">CPU usage is good</p>
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
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="usage" stroke="#8884d8" activeDot={{ r: 8 }} />
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
