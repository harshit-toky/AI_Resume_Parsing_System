import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from './Header';
import UsingGrid from './UsingGrid';
import TokenizedResume from './TokenizedResume';

function App() {
  return (
    <Router>
      <div className="App">
        <Header/>
        <Routes>
          <Route path="/" element={<UsingGrid />} />
          <Route path="/tokenized-resume" element={<TokenizedResume />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
