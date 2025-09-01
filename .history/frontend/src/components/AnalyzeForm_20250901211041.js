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
    // Step 1: Clean & split the text
    const words = text
      .toLowerCase()
      .replace(/[^a-z\s]/g, "")
      .split(/\s+/)
      .filter((w) => w.length > 2); // remove very short words

    // Step 2: Count frequencies
    const freq = {};
    words.forEach((w) => {
      freq[w] = (freq[w] || 0) + 1;
    });

    // Step 3: Sort top 10 frequent words
    const sorted = Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);

    // Step 4: Prepare wordcloud object
    const wordcloud = {
      words: Object.fromEntries(sorted),
    };

    // Step 5: Fake probability + label for now
    const probability = Math.floor(Math.random() * 100);
    const label = Math.random() > 0.5 ? "fake" : "normal";

    const generatedData = { probability, label, wordcloud };

    setTimeout(() => {
      setResult(generatedData);
      setLoading(false);
    }, 1000);

  } catch (err) {
    setError("Error analyzing text");
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