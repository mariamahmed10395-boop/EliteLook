import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAppContext } from '../context/AppContext.jsx'
import ProductImage from '../components/ProductImage.jsx'

export default function Cart() {
  const { cartItem } = useAppContext()
  const navigate = useNavigate()

  if (!cartItem) {
    return (
      <div className="cart-wrap">
        <div className="container" style={{ textAlign: 'center' }}>
          <h2>Your cart is empty</h2>
          <p style={{ color: 'var(--ink-soft)', margin: '10px 0 20px' }}>
            Pick a color and size on a product, then hit Order now.
          </p>
          <Link to="/" className="btn btn-primary">
            Browse products
          </Link>
        </div>
      </div>
    )
  }

  const { product, color, size } = cartItem

  const handleConfirm = () => {
    // No real checkout/payment yet — this is the "I already know
    // what I want" path, so we just confirm and send the shopper home.
    alert(`Order placed: ${product.name} — size ${size}. We'll take it from here!`)
    navigate('/')
  }

  return (
    <div className="cart-wrap">
      <div className="container">
        <div className="cart-card">
          <ProductImage src={product.image} alt={product.name} />

          <div className="cart-details">
            <h2>{product.name}</h2>
            <span className="product-price">${product.price.toFixed(2)}</span>

            <div className="cart-meta">
              <div className="cart-meta-item">
                <span className="label">Color</span>
                <span className="swatch" style={{ background: color }} />
              </div>
              <div className="cart-meta-item">
                <span className="label">Size</span>
                <span style={{ fontFamily: 'var(--font-mono)' }}>{size}</span>
              </div>
            </div>
          </div>
        </div>

        <h3 style={{ textAlign: 'center', margin: '32px 0 20px', color: 'var(--ink-soft)', fontWeight: 500 }}>
          How would you like to proceed?
        </h3>

        <div className="choice-row">
          <button type="button" className="choice-card" onClick={handleConfirm}>
            <span className="choice-icon">✓</span>
            <h3>I know my size and color</h3>
            <p>Confirm the selection above and place the order directly.</p>
          </button>

          <Link to={`/try-on/${product.id}`} className="choice-card">
            <span className="choice-icon">✨</span>
            <h3>Help me choose</h3>
            <p>See the item on yourself and get a color recommendation first.</p>
          </Link>
        </div>
      </div>
    </div>
  )
}
