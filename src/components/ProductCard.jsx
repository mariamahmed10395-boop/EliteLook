import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppContext } from '../context/AppContext.jsx'
import ProductImage from './ProductImage.jsx'

/**
 * A single product tile in the homepage grid.
 * Holds its own "which color/size is selected" state locally —
 * that choice only matters once the shopper hits Order Now, at
 * which point it's handed off to the cart via context.
 */
export default function ProductCard({ product }) {
  const { favorites, toggleFavorite, addToCart } = useAppContext()
  const navigate = useNavigate()

  const [selectedColor, setSelectedColor] = useState(product.colors[0])
  const [selectedSize, setSelectedSize] = useState(null)

  const isFavorite = favorites.has(product.id)

  const handleOrderNow = () => {
    addToCart(product, selectedColor, selectedSize)
    navigate('/cart')
  }

  return (
    <article className="product-card">
      <span className="tag-hole" aria-hidden="true" />

      <button
        type="button"
        className={`favorite-btn${isFavorite ? ' active' : ''}`}
        onClick={() => toggleFavorite(product.id)}
        aria-pressed={isFavorite}
        aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
      >
        {isFavorite ? '♥' : '♡'}
      </button>

      <ProductImage src={product.image} alt={product.name} />

      <div className="product-info">
        <span className="product-name">{product.name}</span>
        <span className="product-price">${product.price.toFixed(2)}</span>

        {/* Color swatches */}
        <div className="swatch-row" role="group" aria-label="Available colors">
          {product.colors.map((color) => (
            <button
              key={color}
              type="button"
              className={`swatch${selectedColor === color ? ' selected' : ''}`}
              style={{ background: color }}
              onClick={() => setSelectedColor(color)}
              aria-label={`Color ${color}`}
              aria-pressed={selectedColor === color}
            />
          ))}
        </div>

        {/* Size buttons */}
        <div className="size-row" role="group" aria-label="Available sizes">
          {product.sizes.map((size) => (
            <button
              key={size}
              type="button"
              className={`size-btn${selectedSize === size ? ' selected' : ''}`}
              onClick={() => setSelectedSize(size)}
              aria-pressed={selectedSize === size}
            >
              {size}
            </button>
          ))}
        </div>

        <div className="card-actions">
          <button
            type="button"
            className="btn btn-primary btn-block"
            onClick={handleOrderNow}
            disabled={!selectedSize}
            title={!selectedSize ? 'Pick a size first' : undefined}
          >
            Order now
          </button>
        </div>
      </div>
    </article>
  )
}
