import React, { useState, useCallback, useMemo } from 'react';
import { getAuth, signInAnonymously } from 'firebase/auth';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, onSnapshot, orderBy, query, limit } from 'firebase/firestore';


const App = () => {
  // State to manage the current view (page)
  const [currentView, setCurrentView] = useState('home');

  // State for the Analyze Form
  const [analysisText, setAnalysisText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  // Function to handle navigation
  const navigateTo = useCallback((view) => {
    setCurrentView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Smooth scroll to top
  }, []);

  // Handle text analysis submission
  const handleAnalyze = async (e) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setAnalysisResult(null);

    // Simulating an API call for analysis
    setTimeout(() => {
      const mockScore = Math.random();
      let mockAnalysis = {
        score: mockScore,
        status: mockScore > 0.7 ? 'High Likelihood of Anti-India Campaign' :
                  mockScore > 0.4 ? 'Medium Likelihood' : 'Low Likelihood',
        keywords: ['propaganda', 'misinformation', 'false narrative'].sort(() => 0.5 - Math.random()).slice(0, 3)
      };

      setAnalysisResult(mockAnalysis);
      setIsAnalyzing(false);
    }, 2000); // 2-second delay to simulate network latency
  };

  // Memoized Navbar component for performance
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

  // Memoized Footer component
  const Footer = useMemo(() => (
    <footer className="bg-gray-900 text-gray-400 p-6 text-center mt-auto">
      <div className="container mx-auto">
        <p>&copy; 2024 Anti-India Campaign Detector. All rights reserved.</p>
      </div>
    </footer>
  ), []);

  // JSX for the different views
  const renderView = () => {
    switch (currentView) {
      case 'home':
        return (
          <>
            {/* Landing Page Section */}
            <section id="home" className="pt-24 min-h-screen flex flex-col justify-center items-center bg-gray-50 text-center px-4">
              <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-4">
                Anti-India Campaign Detector
              </h1>
              <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-12">
                An intelligent system that analyzes text to identify and flag potential misinformation.
              </p>

              {/* Features Section - Cards */}
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

              {/* Call-to-action */}
              <button
                onClick={() => navigateTo('analyze')}
                className="px-8 py-4 bg-indigo-600 text-white font-semibold text-lg rounded-xl shadow-lg hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-500 focus:ring-opacity-50"
              >
                Do you want to analyze?
              </button>
            </section>
          </>
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
            <div className="w-full max-w-2xl bg-white p-8 rounded-2xl shadow-xl mt-8">
              <h2 className="text-4xl font-bold text-gray-900 mb-6 text-center">Analyze Text</h2>
              <form onSubmit={handleAnalyze}>
                <textarea
                  className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none text-gray-800"
                  placeholder="Paste text to analyze here..."
                  value={analysisText}
                  onChange={(e) => setAnalysisText(e.target.value)}
                  required
                ></textarea>
                <div className="flex justify-center mt-6">
                  <button
                    type="submit"
                    disabled={isAnalyzing}
                    className="px-8 py-4 bg-indigo-600 text-white font-semibold text-lg rounded-xl shadow-lg hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-500 focus:ring-opacity-50 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {isAnalyzing ? 'Analyzing...' : 'Analyze'}
                  </button>
                </div>
              </form>

              {analysisResult && (
                <div className="mt-8 p-6 bg-gray-100 rounded-xl shadow-md border-t-4 border-indigo-500">
                  <h3 className="text-2xl font-bold text-gray-800 mb-4">Analysis Result</h3>
                  <p className="text-lg mb-2">
                    <span className="font-semibold">Status:</span> {analysisResult.status}
                  </p>
                  <p className="text-lg mb-4">
                    <span className="font-semibold">Confidence Score:</span> {(analysisResult.score * 100).toFixed(2)}%
                  </p>
                  <div className="bg-white p-4 rounded-lg shadow-inner">
                    <h4 className="font-semibold text-gray-700 mb-2">Identified Keywords:</h4>
                    <ul className="list-disc list-inside space-y-1 text-gray-600">
                      {analysisResult.keywords.map((keyword, index) => (
                        <li key={index}>{keyword}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
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