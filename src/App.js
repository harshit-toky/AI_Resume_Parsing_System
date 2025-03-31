import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from './Header';
import UsingGrid from './UsingGrid';
import TokenizedResume from './TokenizedResume';
import CalculateSimilarityScore from './CalculateSimilarityScore';

function App() {
  return (
    <Router>
      <div className="App">
        <Header/>
        <Routes>
          <Route path="/" element={<UsingGrid />} />
          <Route path="/tokenized-resume" element={<TokenizedResume />} />
          <Route path='/similarityScore' element={<CalculateSimilarityScore/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
