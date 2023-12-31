import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Dot,
} from 'recharts';

const ChartComponent = ({ data }) => {
  // Extract the data from modelsPerformance[selectedKeyWithoutNumber]
  const chartData = Object.values(data).map((item) => ({
    Epoch: item.Epoch,
    Loss: item.Loss,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="Epoch" />
        <YAxis label={{ value: 'Loss', angle: -90, position: 'insideLeft', offset: -2 }} />
        <Tooltip formatter={(value) => `${value.toFixed(2)}`} />
        <Legend />
        <Line
          name="Loss Vs Epoch"
          type="monotone"
          dataKey="Loss"
          stroke="#8884d8"
          strokeWidth={2}
          dot={{ strokeWidth: 4, fill: '#8884d8' }}
        />
        <Dot dataKey="Loss" fill="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default ChartComponent;