import React, { useState } from "react";

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
      const res = await fetch("http://127.0.0.1:8000/analyze/", {
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
          <strong>Label:</strong> {result.label === "fake" ? "Likely Anti-India Campaign" : "Normal"}
          <br />
          <strong>Confidence:</strong> {result.probability}%
        </div>
      )}
    </div>
  );
}

export default AnalyzeForm;