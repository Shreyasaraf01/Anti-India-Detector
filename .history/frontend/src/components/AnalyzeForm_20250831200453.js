import React, { useState } from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";
import { scaleOrdinal } from "d3-scale";
import { schemeCategory10 } from "d3-scale-chromatic";

// The WordCloud component
// This part of the code is new and will draw the word cloud
function WordCloud({ words }) {
  const color = scaleOrdinal(schemeCategory10);
  const maxWordSize = 40;
  const minWordSize = 12;
  
  if (!words || Object.keys(words).length === 0) {
    return <p>No significant terms found.</p>;
  }

  const wordEntries = Object.entries(words);
  const maxFreq = Math.max(...wordEntries.map(([_, freq]) => freq));
  
  return (
    <div style={{ padding: "20px", display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "center", minHeight: "200px" }}>
      {wordEntries.map(([word, freq], index) => {
        const fontSize = minWordSize + (freq / maxFreq) * (maxWordSize - minWordSize);
        return (
          <span
            key={index}
            style={{
              fontSize: `${fontSize}px`,
              margin: "5px",
              color: color(index),
              cursor: "pointer",
            }}
            title={`Frequency: ${freq}`}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
}

const COLORS = ["#ff4d4f", "#36cfc9"]; // Colors for the pie chart slices

function AnalyzeForm() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // New state for loading

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }
    setLoading(true); // Start loading
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
    } finally {
      setLoading(false); // Stop loading regardless of success or failure
    }
  };

  // Function to prepare data for the confidence pie chart
  const getChartData = () => {
    if (!result) return null;
    const confidence = result.probability;
    const remaining = 100 - confidence;

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
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}

      {result && (
        <div style={{ marginTop: 10 }}>
          <strong>Label:</strong>{" "}
          {result.label === "fake" ? "Likely Misinformation" : "Normal"}
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
          
          {/* The word cloud now displays data from the analyzed text */}
          <div style={{ marginTop: 20 }}>
            <h3>Frequent Negative Terms in Analyzed Text</h3>
            {result.wordcloud && <WordCloud words={result.wordcloud.words} />}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalyzeForm;