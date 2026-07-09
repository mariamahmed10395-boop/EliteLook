import React, { useState } from 'react'

/**
 * Renders a product's image from the path given in products.json.
 * Since real images get dropped into /public/images later, this
 * quietly falls back to a placeholder if the file isn't there yet —
 * so the layout looks right end-to-end before a single photo exists.
 */
export default function ProductImage({ src, alt }) {
  const [failed, setFailed] = useState(false)

  if (!src || failed) {
    return (
      <div className="product-image">
        <div className="product-image-placeholder">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
              d="M4 16l4.5-6 3 3.5L15 8l5 8H4z"
              stroke="currentColor"
              strokeWidth="1.4"
              strokeLinejoin="round"
            />
            <circle cx="8" cy="7" r="1.6" stroke="currentColor" strokeWidth="1.4" />
          </svg>
          <span>Image coming soon</span>
        </div>
      </div>
    )
  }

  return (
    <div className="product-image">
      {/* Vite serves /public at the site root, so "images/x.jpg" in
          products.json resolves to /images/x.jpg */}
      <img src={`/${src}`} alt={alt} onError={() => setFailed(true)} />
    </div>
  )
}
