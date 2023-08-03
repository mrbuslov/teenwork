import React from 'react';
import ReactDOM from 'react-dom/client';
import Home from './pages/home/Home'
import Navbar from './components/NavBar/Navbar'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode >
    {/* <Navbar /> */}
    <Home />
  </React.StrictMode>
);
