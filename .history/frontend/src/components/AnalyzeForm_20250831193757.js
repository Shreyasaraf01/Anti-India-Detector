import React, { useState } from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";

const COLORS = ["#ff4d4f", "#36cfc9"]; // Colors for the pie chart slices

function AnalyzeForm() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }
    try {
      const res = await fetch("http://127.0.0.1:8000/api/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else setResult(data);
    } catch (err) {
      setError("API error");
    }
  };

  // Function to prepare data for the confidence pie chart
  const getChartData = () => {
    if (!result) return null;
    const confidence = result.probability;
    const remaining = 100 - confidence;

    // Based on the prediction, we prepare the data for the two slices.
    // The order determines the color from the COLORS array.
    if (result.label === "fake") {
      return [
        { name: "Confidence (Fake)", value: confidence },
        { name: "Uncertainty", value: remaining },
      ];
    } else {
      return [
        { name: "Confidence (Normal)", value: confidence },
        { name: "Uncertainty", value: remaining },
      ];
    }
  };

  const chartData = getChartData();

  return (
    <div>
      <h2>Analyze Text</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={4}
          style={{ width: "100%" }}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste tweet or news article here..."
        />
        <br />
        <button type="submit">Analyze</button>
      </form>

      {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}

      {result && (
        <div style={{ marginTop: 10 }}>
          <strong>Label:</strong>{" "}
          {result.label === "fake" ? "Likely Anti-India Campaign" : "Normal"}
          <br />
          <strong>Confidence:</strong> {result.probability}%
          
          {/* Pie Chart displaying confidence */}
          {chartData && (
            <div style={{ marginTop: 20 }}>
              <h3>Prediction Confidence</h3>
              <PieChart width={300} height={220}>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Legend />
                <Tooltip />
              </PieChart>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AnalyzeForm;