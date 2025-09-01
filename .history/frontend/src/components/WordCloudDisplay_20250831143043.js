import React, { useEffect, useState } from "react";
import ReactWordcloud from "react-wordcloud";

function WordCloudDisplay() {
  const [words, setWords] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/wordcloud/")
      .then((res) => res.json())
      .then((d) => {
        const wc = Object.entries(d.words).map(([text, value]) => ({
          text,
          value,
        }));
        setWords(wc);
      });
  }, []);

  return (
    <div>
      <h2>Frequent Negative Terms</h2>
      <div style={{ height: 250 }}>
        <ReactWordcloud words={words} />
      </div>
    </div>
  );
}

export default WordCloudDisplay;