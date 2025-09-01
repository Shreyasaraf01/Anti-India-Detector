import React, { useState } from "react";
import WordCloud from "react-d3-cloud";

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

      console.log("Extracted words:", sorted); // ✅ debug log

      // Step 4: Prepare wordcloud object
      const wordcloud = {
        words: Object.fromEntries(sorted),
      };

      setTimeout(() => {
        setResult({ wordcloud });
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError("Error analyzing text");
      setLoading(false);
    }
  };

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
  const rotate = () => (Math.random() > 0.5 ? 0 : 90);

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
        <div style={{ marginTop: 20 }}>
          {/* Wordcloud */}
          <h3>Frequent Words in Text</h3>
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
      )}
    </div>
  );
}

export default AnalyzeForm;
