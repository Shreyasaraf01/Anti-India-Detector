import React, { useState, useCallback, useMemo } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";
import "./index.css";  // <-- include CSS

// Word Cloud
const InlineWordCloud = ({ words }) => {
  if (!words || words.length === 0) {
    return <p className="no-words">No significant terms found.</p>;
  }

  const maxWordValue = words.reduce((max, word) => Math.max(max, word.value), 0);
  const minWordValue = words.reduce((min, word) => Math.min(min, word.value), Infinity);

  const fontSizeScale = (value) => {
    const minSize = 16;
    const maxSize = 48;
    if (maxWordValue === minWordValue) {
      return (minSize + maxSize) / 2;
    }
    return minSize + ((value - minWordValue) / (maxWordValue - minWordValue)) * (maxSize - minSize);
  };

  return (
    <div className="wordcloud">
      {words.map((word, index) => (
        <span
          key={index}
          className="word"
          style={{
            fontSize: `${fontSizeScale(word.value)}px`,
            opacity: 0.8 + (0.2 * ((word.value - minWordValue) / (maxWordValue - minWordValue)))
          }}
        >
          {word.text}
        </span>
      ))}
    </div>
  );
};

const COLORS = ["#ff4d4f", "#36cfc9"]; 

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
    const mockData = {
      probability: Math.floor(Math.random() * 100),
      label: Math.random() > 0.5 ? "fake" : "normal",
      wordcloud: {
        words: {
          misinformation: 50,
          propaganda: 40,
          fake: 35,
          news: 30,
          viral: 25,
          false: 20,
          narrative: 15,
          social: 10,
          media: 5,
        }
      }
    };
    setTimeout(() => {
      setResult(mockData);
      setLoading(false);
    }, 1500);
  };

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

  const wordCloudData =
    result && result.wordcloud
      ? Object.entries(result.wordcloud.words).map(([text, value]) => ({
          text,
          value,
        }))
      : [];

  return (
    <div className="analyze-card">
      <h2 className="section-title">Analyze Text</h2>
      <form onSubmit={handleSubmit} className="analyze-form">
        <textarea
          rows={4}
          className="input-textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste tweet or news article here..."
        />
        <button type="submit" disabled={loading} className="btn">
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="results-card">
          <div className="results-info">
            <div>
              <strong>Label:</strong> {result.label === "fake" ? "Likely Misinformation" : "Normal"} <br />
              <strong>Confidence:</strong> {result.probability}%
            </div>
            {chartData && (
              <div className="chart-container">
                <h3>Prediction Confidence</h3>
                <PieChart width={300} height={220}>
                  <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Legend />
                  <Tooltip />
                </PieChart>
              </div>
            )}
          </div>

          <div className="wordcloud-section">
            <h3>Frequent Negative Terms in Analyzed Text</h3>
            <div className="wordcloud-container">
              <InlineWordCloud words={wordCloudData} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const App = () => {
  return (
    <div className="app">
      <header className="navbar">Anti-India Campaign Detector</header>
      <main className="main-content">
        <AnalyzeForm />
      </main>
      <footer className="footer">© 2024 Anti-India Campaign Detector. All rights reserved.</footer>
    </div>
  );
};

export default App;
