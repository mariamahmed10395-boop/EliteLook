import React from 'react'
import { Link } from 'react-router-dom'
import { useAppContext } from '../context/AppContext.jsx'

export default function Navbar() {
  const { favorites, user, cartItem } = useAppContext()

  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <Link to="/" className="brand">
          <span className="brand-mark" aria-hidden="true" />
          Aura
        </Link>

        <nav className="nav-links">
          <span
            className="nav-link-icon"
            title={`${favorites.size} favorite${favorites.size === 1 ? '' : 's'}`}
          >
            ♥
            {favorites.size > 0 && <span className="nav-badge">{favorites.size}</span>}
          </span>

          {/* رابط الكارت الجديد */}
          <Link
            to="/cart"
            className="nav-link-icon"
            title={cartItem ? '1 item in cart' : 'Cart is empty'}
          >
            🛍
            {cartItem && <span className="nav-badge">1</span>}
          </Link>

          {user ? (
            <span className="nav-link-icon" style={{ fontSize: '0.9rem', fontWeight: 600 }}>
              Hi, {user.name.split(' ')[0]}
            </span>
          ) : (
            <>
              <Link to="/login" className="btn btn-outline">
                Log in
              </Link>
              <Link to="/register" className="btn btn-accent">
                Register
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}