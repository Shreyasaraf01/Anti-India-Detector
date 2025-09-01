import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';
import AnalyzeForm from './components/AnalyzeForm'; // Your existing component

// You will also need to create these placeholder components
const Features = () => <div className="p-8 mt-16 text-center"><h2>Features Page</h2></div>;
const Contact = () => <div className="p-8 mt-16 text-center"><h2>Contact Page</h2></div>;

const App = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow mt-16">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/features" element={<Features />} />
            <Route path="/analyze" element={<AnalyzeForm />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;