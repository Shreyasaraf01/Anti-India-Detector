import React from "react";
import AnalyzeForm from "./components/AnalyzeForm";

function App() {
  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 20 }}>
      <h1>Anti-India Campaign Detector</h1>
      <AnalyzeForm />
      <hr />
      <WordCloudDisplay />
    </div>
  );
}

export default App;