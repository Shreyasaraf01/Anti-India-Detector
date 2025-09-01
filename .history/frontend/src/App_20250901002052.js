import React, { useState, useCallback, useMemo } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";

// A custom component to generate a word cloud without external libraries
const InlineWordCloud = ({ words }) => {
  if (!words || words.length === 0) {
    return <p className="text-gray-500 text-center">No significant terms found.</p>;
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
    <div className="flex flex-wrap justify-center items-center p-4">
      {words.map((word, index) => (
        <span
          key={index}
          className="m-1 font-bold rounded-lg px-2 py-1 transition-all duration-300 transform hover:scale-110"
          style={{
            fontSize: `${fontSizeScale(word.value)}px`,
            color: '#1f2937', 
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
    
    // Simulating a mock API call to get the data
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
    <div className="p-8 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Analyze Text</h2>
      <form onSubmit={handleSubmit} className="mb-8">
        <textarea
          rows={4}
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste tweet or news article here..."
        />
        <button 
          type="submit" 
          disabled={loading}
          className="mt-4 px-6 py-2 w-full bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:bg-gray-400"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <div className="text-red-500 mt-4">{error}</div>}

      {result && (
        <div className="mt-8 p-6 bg-gray-100 rounded-lg shadow-inner">
          <div className="flex flex-col md:flex-row justify-around items-center">
            <div className="mb-4 md:mb-0">
              <strong>Label:</strong>{" "}
              {result.label === "fake" ? "Likely Misinformation" : "Normal"}
              <br />
              <strong>Confidence:</strong> {result.probability}%
            </div>
            
            {/* Pie chart */}
            {chartData && (
              <div className="w-full md:w-1/2 flex flex-col items-center">
                <h3 className="font-semibold text-lg mb-2">Prediction Confidence</h3>
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

          {/* Wordcloud */}
          <div className="mt-8 flex flex-col items-center">
            <h3 className="font-semibold text-lg mb-2">Frequent Negative Terms in Analyzed Text</h3>
            <div className="w-full max-w-lg" style={{ height: '300px' }}>
              <InlineWordCloud words={wordCloudData} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const App = () => {
  const [currentView, setCurrentView] = useState('home');

  const navigateTo = useCallback((view) => {
    setCurrentView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const Navbar = useMemo(() => (
    <nav className="fixed top-0 left-0 w-full bg-gray-900 text-white p-4 z-50 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-2xl font-bold text-indigo-400">
          Anti-India Campaign Detector
        </div>
        <ul className="flex space-x-6">
          <li>
            <button onClick={() => navigateTo('home')} className="hover:text-indigo-400 transition-colors focus:outline-none">Home</button>
          </li>
          <li>
            <button onClick={() => navigateTo('features')} className="hover:text-indigo-400 transition-colors focus:outline-none">Features</button>
          </li>
          <li>
            <button onClick={() => navigateTo('analyze')} className="hover:text-indigo-400 transition-colors focus:outline-none">Analyze</button>
          </li>
          <li>
            <button onClick={() => navigateTo('contact')} className="hover:text-indigo-400 transition-colors focus:outline-none">Contact</button>
          </li>
        </ul>
      </div>
    </nav>
  ), [navigateTo]);

  const Footer = useMemo(() => (
    <footer className="bg-gray-900 text-gray-400 p-6 text-center mt-auto">
      <div className="container mx-auto">
        <p>&copy; 2024 Anti-India Campaign Detector. All rights reserved.</p>
      </div>
    </footer>
  ), []);

  const renderView = () => {
    switch (currentView) {
      case 'home':
        return (
          <section id="home" className="pt-24 min-h-screen flex flex-col justify-center items-center bg-gray-50 text-center px-4">
            <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-4">
              Anti-India Campaign Detector
            </h1>
            <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-12">
              An intelligent system that analyzes text to identify and flag potential misinformation.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-6xl mb-12">
              <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 transform hover:-translate-y-2">
                <div className="flex justify-center items-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-500" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Real-Time Analysis</h3>
                <p className="text-gray-500">
                  Get instant analysis of news articles or social media posts for suspicious content.
                </p>
              </div>
              <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 transform hover:-translate-y-2">
                <div className="flex justify-center items-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-500" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">High Accuracy</h3>
                <p className="text-gray-500">
                  Our model is trained on a vast dataset to provide reliable and accurate results.
                </p>
              </div>
              <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 transform hover:-translate-y-2">
                <div className="flex justify-center items-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-500" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Key Features</h3>
                <p className="text-gray-500">
                  Get detailed insights with identified key phrases and sentiment analysis.
                </p>
              </div>
            </div>
            <button
              onClick={() => navigateTo('analyze')}
              className="px-8 py-4 bg-indigo-600 text-white font-semibold text-lg rounded-xl shadow-lg hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-500 focus:ring-opacity-50"
            >
              Do you want to analyze?
            </button>
          </section>
        );

      case 'features':
        return (
          <div className="pt-24 min-h-screen flex flex-col items-center justify-center bg-gray-50">
            <h2 className="text-4xl font-bold text-gray-900 mb-8">Detailed Features</h2>
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-4xl text-center">
              <p className="text-gray-600">
                This page would provide a more in-depth description of the features. For example, it could
                detail the machine learning model used, the types of misinformation it detects, and case studies.
              </p>
            </div>
          </div>
        );

      case 'analyze':
        return (
          <section id="analyze" className="pt-24 min-h-screen flex flex-col items-center bg-gray-50 px-4">
            <div className="w-full max-w-2xl mt-8">
              <AnalyzeForm />
            </div>
          </section>
        );

      case 'contact':
        return (
          <div className="pt-24 min-h-screen flex flex-col items-center justify-center bg-gray-50">
            <h2 className="text-4xl font-bold text-gray-900 mb-8">Contact Us</h2>
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md text-center">
              <p className="text-gray-600 mb-4">
                Have questions or feedback? Feel free to reach out to us!
              </p>
              <form className="space-y-4">
                <input type="text" placeholder="Your Name" className="w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
                <input type="email" placeholder="Your Email" className="w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
                <textarea placeholder="Your Message" rows="5" className="w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
                <button type="submit" className="w-full py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors">Send Message</button>
              </form>
            </div>
          </div>
        );

      default:
        return <div>Page not found.</div>;
    }
  };

  return (
    <div className="font-sans antialiased text-gray-800 bg-gray-50 flex flex-col min-h-screen">
      <style>{`
        .bg-gradient-to-br {
          background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
        }
      `}</style>
      {Navbar}
      <main className="flex-grow">
        {renderView()}
      </main>
      {Footer}
    </div>
  );
};

export default App;