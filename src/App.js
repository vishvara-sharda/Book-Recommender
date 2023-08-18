import './App.css';
import LandingPage from './Pages/LandingPage';
import RecommendPage from './Pages/RecommendPage';
import { BrowserRouter as Router,Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="App">
     <Router>
     <Routes>
        <Route path="/" element={<LandingPage />}/>
        <Route path="/recommender" element={<RecommendPage />}/>
      </Routes>
      </Router>
    </div>
  );
}

export default App;
