import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import Cart from './pages/Cart.jsx'
import VirtualTryOn from './pages/VirtualTryOn.jsx'
import backImage from './data/images/back.jpg';

export default function App() {
  return (
    <div className="page">
      <div className="announcement-bar">
        <span>Free shipping on orders over $99</span>
      </div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/try-on/:productId" element={<VirtualTryOn />} />
      </Routes>
    </div>
  )
}
