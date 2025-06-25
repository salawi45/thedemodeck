import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import CandidateList from "./pages/CandidateList"
import CandidateDetail from "./pages/CandidateDetail"
import BillsList from "./pages/BillsList"
import VotesList from "./pages/VotesList"
import BillDetail from "./pages/BillDetail"
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
            <Route path="/bills" element={<BillsList />} />
            <Route path="/votes" element={<VotesList />} />
            <Route path="/bill/:billId" element={<BillDetail />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
