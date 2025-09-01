import React, { useState } from "react";
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";
import WordCloud from "react-d3-cloud";

const COLORS = ["#ff4d4f", "#36cfc9"]; // Colors for the pie chart slices

function AnalyzeForm() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }

    setLoading(true);
    try {
      // Using a mock API call for now since the backend is local
      // const res = await fetch("http://127.0.0.1:8000/api/analyze/", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({ text }),
      // });
      // const data = await res.json();
     
      // Simulating a mock response
      const mockData = {
        probability: Math.floor(Math.random() * 100),
        label: Math.random() > 0.5 ? "fake" : "normal",
        wordcloud: {
          words: {
            "misinformation": 50,
            "propaganda": 40,
            "fake": 35,
            "news": 30,
            "viral": 25,
            "false": 20,
            "narrative": 15,
            "social": 10,
            "media": 5,
          }
        }
      };
      setTimeout(() => {
        setResult(mockData);
        setLoading(false);
      }, 1500);

    } catch (err) {
      setError("API error");
      setLoading(false);
    }
  };

  // Prepare data for pie chart
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

  // Wordcloud data
  const wordCloudData =
    result && result.wordcloud
      ? Object.entries(result.wordcloud.words).map(([text, value]) => ({
          text,
          value,
        }))
      : [];

  // Wordcloud settings for react-d3-cloud
  const fontSizeMapper = (word) => Math.log2(word.value) * 10;
  const rotate = (word) => (Math.random() > 0.5 ? 0 : 90);

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
          
          {/* Pie chart */}
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

          {/* Wordcloud */}
          <div style={{ marginTop: 20 }}>
            <h3>Frequent Negative Terms in Analyzed Text</h3>
            {wordCloudData.length > 0 ? (
              <WordCloud
                data={wordCloudData}
                fontSizeMapper={fontSizeMapper}
                rotate={rotate}
                width={500}
                height={300}
              />
            ) : (
              <p>No significant terms found.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalyzeForm;