import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="text-center p-8 bg-gray-50 min-h-screen flex flex-col justify-center items-center">
      <h1 className="text-5xl font-bold text-gray-800 mb-4">Anti-India Campaign Detector</h1>
      <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-12">
        An intelligent system that analyzes text content to identify and flag potential misinformation.
      </p>

      {/* Features Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-4xl mb-12">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold text-gray-700 mb-2">Real-Time Analysis</h3>
          <p className="text-gray-500">
            Get instant analysis of news articles or social media posts.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold text-gray-700 mb-2">High Accuracy</h3>
          <p className="text-gray-500">
            Our model is trained on a vast dataset to provide reliable results.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold text-gray-700 mb-2">Frequent Terms</h3>
          <p className="text-gray-500">
            Identify common terms used in malicious campaigns for deeper insights.
          </p>
        </div>
      </section>

      <Link
        to="/analyze"
        className="px-8 py-4 bg-indigo-600 text-white font-semibold text-lg rounded-xl shadow-md hover:bg-indigo-700 transition-colors duration-200"
      >
        Analyze Text
      </Link>
    </div>
  );
};

export default LandingPage;