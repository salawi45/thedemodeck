import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import CandidateList from "./pages/CandidateList"
import CandidateDetail from "./pages/CandidateDetail"
import About from "./pages/About"
import Navbar from "./components/Navbar"
import "./App.css"

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<CandidateList />} />
            <Route path="/candidate/:id" element={<CandidateDetail />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
