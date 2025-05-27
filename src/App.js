import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from './Navbar';
import UsingGrid from './UsingGrid';
import TokenizedResume from './TokenizedResume';
import CalculateSimilarityScore from './CalculateSimilarityScore';
import Header from './Header';
import MultiResumeAnalysis from './MultipleResume';
import AuthenticityCheck from './AuthencityCheck';

function App() {
  return (
     <Router>
        <div className="h-full overflow-hidden">
          <Navbar />
          <Routes>
            <Route path="/" element={<Header />} />
            <Route path="/multiple" element={<MultiResumeAnalysis/>} />
            <Route path="/plagiarism" element={<AuthenticityCheck />} />
            <Route path="/parse" element={<UsingGrid />} />
            <Route path="/tokenized-resume" element={<TokenizedResume />} />
            <Route path='/similarityScore' element={<CalculateSimilarityScore/>}/>
          </Routes>
        </div>
    </Router>
  );
}

export default App;
