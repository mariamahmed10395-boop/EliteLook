import React, { createContext, useContext, useMemo, useState } from 'react'
import productsData from '../data/products.json'

const AppContext = createContext(null)

/**
 * Central in-memory store for the whole app.
 * Nothing here is persisted to a backend or localStorage — it's all
 * plain React state, which is exactly what the brief asked for
 * ("in-memory state is fine for now"). Swap this out for real
 * auth/cart/favorites APIs later without touching the components,
 * since they only ever talk to this context.
 */
export function AppProvider({ children }) {
  const [products] = useState(productsData.products)

  // Favorites: a Set of product ids
  const [favorites, setFavorites] = useState(new Set())

  const toggleFavorite = (productId) => {
    setFavorites((prev) => {
      const next = new Set(prev)
      if (next.has(productId)) next.delete(productId)
      else next.add(productId)
      return next
    })
  }

  // Cart: the single "current order in progress".
  // Shape: { product, color, size } | null
  const [cartItem, setCartItem] = useState(null)

  const addToCart = (product, color, size) => {
    setCartItem({ product, color, size })
  }

  // Very small in-memory "auth" — just tracks a display name once
  // someone submits the register/login form. Good enough to wire up
  // the flow; swap for real auth later.
  const [user, setUser] = useState(null)

  const value = useMemo(
    () => ({
      products,
      favorites,
      toggleFavorite,
      cartItem,
      addToCart,
      user,
      setUser,
    }),
    [products, favorites, cartItem, user]
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useAppContext() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useAppContext must be used within AppProvider')
  return ctx
}
