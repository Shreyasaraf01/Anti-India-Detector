import React, { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";

const COLORS = ["#ff4d4f", "#36cfc9"];

function StatsChart() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/stats/")
      .then((res) => res.json())
      .then((d) => {
        setData([
          { name: "Flagged", value: d.flagged },
          { name: "Normal", value: d.normal },
        ]);
      });
  }, []);

  if (!data) return <div>Loading chart...</div>;

  return (
    <div>
      <h2>Flagged vs Normal Content</h2>
      <PieChart width={300} height={220}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={80}
          label
        >
          {data.map((entry, idx) => (
            <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
          ))}
        </Pie>
        <Legend />
        <Tooltip />
      </PieChart>
    </div>
  );
}

export default StatsChart;