import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegistrationFlow from './components/RegistrationFlow';
import { Toaster } from './components/ui/Toaster';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<RegistrationFlow />} />
        </Routes>
        <Toaster />
      </div>
    </Router>
  );
}

export default App;
