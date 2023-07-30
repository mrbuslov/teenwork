import React from 'react'
import ReactDOM from 'react-dom/client'
import Home from './pages/home/Home'
import Navbar from './components/NavBar/Navbar'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Navbar />
    <Home />
  </React.StrictMode>,
)
