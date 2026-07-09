import React, { useRef } from 'react'
import { useAppContext } from '../context/AppContext.jsx'

const categoryTiles = [
  { title: 'Women', image: 'images/Women\'s_casual_t-shirt_displayed_2K_202607081141.jpeg' },
  { title: 'Men', image: 'images/Men\'s_formal_long_sleeve_shirt_202607081136.jpeg' },
  { title: 'Bags', image: 'images/pexels-mathilde-10897815.jpg' },
  { title: 'Shoes', image: 'images/pexels-jonathanborba-28900498.jpg' },
]

const popularTiles = [
  { title: 'Minimal', image: 'images/Women\'s_knitted_cardigan_isolate…_2K_202607081150.jpeg' },
  { title: 'Elegant', image: 'images/Women\'s_elegant_blouse_front_view_202607081147.jpeg' },
  { title: 'Casual', image: 'images/Women\'s_casual_dress_folds_2K_202607081146.jpeg' },
  { title: 'Accessories', image: 'images/pexels-ron-lach-8571860.jpg' },
]

const features = [
  { icon: '✦', label: 'Free shipping' },
  { icon: '↺', label: 'Easy returns' },
  { icon: '◍', label: 'Secure payment' },
  { icon: '✉', label: '24/7 support' },
]

export default function Home() {
  const { products } = useAppContext()
  const arrivalsRef = useRef(null)

  const handleCarouselScroll = (direction) => {
    if (!arrivalsRef.current) return

    const amount = arrivalsRef.current.clientWidth * 0.86
    arrivalsRef.current.scrollBy({ left: direction === 'next' ? amount : -amount, behavior: 'smooth' })
  }

  return (
    <main className="home-page">
      <section className="hero-section">
        <div className="container hero-layout">
          <div className="hero-copy">
            <p className="eyebrow">New season</p>
            <h1>Spring / Summer Collection</h1>
            <p className="hero-description">
              Quiet luxury essentials in soft neutrals, designed to move effortlessly from day to evening.
            </p>
            <a className="button button-dark" href="#new-arrivals">
              Shop now
            </a>
          </div>

          <div className="hero-media">
            <img
              src="/images/Women's_knitted_cardigan_isolate…_2K_202607081150.jpeg"
              alt="Model in refined neutral-toned fashion"
            />
          </div>
        </div>
      </section>

      <section className="container category-section" aria-labelledby="category-title">
        <div className="section-heading">
          <p className="eyebrow">Curated edit</p>
          <h2 id="category-title">Explore the wardrobe</h2>
        </div>

        <div className="category-grid">
          {categoryTiles.map((tile) => (
            <article key={tile.title} className="category-card" style={{ backgroundImage: `url(${tile.image})` }}>
              <div className="category-overlay" />
              <div className="category-content">
                <h3>{tile.title}</h3>
                <a href="#new-arrivals">Shop now</a>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="container arrivals-section" id="new-arrivals" aria-labelledby="arrivals-title">
        <div className="section-heading centered">
          <p className="eyebrow">Latest arrivals</p>
          <h2 id="arrivals-title">New Arrivals</h2>
          <span className="section-accent" />
        </div>

        <div className="carousel-shell">
          <button type="button" className="carousel-arrow" aria-label="Scroll left" onClick={() => handleCarouselScroll('prev')}>
            ←
          </button>

          <div className="arrival-row" ref={arrivalsRef}>
            {products.slice(0, 4).map((product) => (
              <article key={product.id} className="arrival-card">
                <span className="arrival-badge">New</span>
                <div className="arrival-photo">
                  <img src={product.image ? `/${product.image}` : '/images/back.jpg'} alt={product.name} />
                </div>
                <div className="arrival-info">
                  <h3>{product.name}</h3>
                  <p>${product.price.toFixed(2)}</p>
                  <div className="color-swatches" aria-label="Available colors">
                    {product.colors.slice(0, 3).map((color) => (
                      <span key={color} className="swatch-dot" style={{ backgroundColor: color }} />
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>

          <button type="button" className="carousel-arrow" aria-label="Scroll right" onClick={() => handleCarouselScroll('next')}>
            →
          </button>
        </div>
      </section>

      <section className="trust-bar">
        <div className="container trust-grid">
          {features.map((feature) => (
            <div key={feature.label} className="trust-item">
              <span className="trust-icon" aria-hidden="true">
                {feature.icon}
              </span>
              <span>{feature.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="container collection-section" aria-labelledby="collection-title">
        <div className="section-heading centered">
          <p className="eyebrow">Signature staples</p>
          <h2 id="collection-title">Popular Collection</h2>
          <span className="section-accent" />
        </div>

        <div className="popular-grid">
          {popularTiles.map((tile) => (
            <article key={tile.title} className="popular-card" style={{ backgroundImage: `url(${tile.image})` }}>
              <div className="category-overlay" />
              <div className="category-content">
                <h3>{tile.title}</h3>
                <a href="#new-arrivals">View edit</a>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
