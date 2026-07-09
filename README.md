# Aura — Clothing E-commerce (starter project)

A React + Vite storefront with product browsing, favorites, a simple
cart/order flow, and a virtual try-on page (photo upload or live
camera, garment overlay, and a basic skin-tone color recommendation).

## Getting started

```bash
npm install
npm run dev
```

Then open the printed local URL (usually `http://localhost:5173`).

To build for production:

```bash
npm run build
npm run preview
```

## Project structure

```
src/
  main.jsx                 # React entry point, router + context providers
  App.jsx                  # Route definitions
  index.css                # Design tokens + all styling (see palette below)
  data/
    products.json           # Sample product data — edit/replace freely
  context/
    AppContext.jsx          # Favorites, cart, and in-memory "auth" state
  components/
    Navbar.jsx              # Top nav: logo, favorites count, login/register
    ProductCard.jsx          # One product tile: image, colors, sizes, actions
    ProductImage.jsx         # Image loader with automatic placeholder fallback
  pages/
    Home.jsx                # Product grid
    Login.jsx / Register.jsx # Auth forms (in-memory only, no backend yet)
    Cart.jsx                 # Order review + "confirm" vs "help me choose"
    VirtualTryOn.jsx         # Upload/camera capture, overlay, tone analysis
  utils/
    skinTone.js              # Brightness sampling + color ranking logic
public/
  images/                    # Put real product photos here (see README.txt inside)
```

## Adding real product images

1. Drop image files into `public/images/` (e.g. `product1.jpg`).
2. Make sure the file name matches the `image` field for that product
   in `src/data/products.json`.
3. That's it — no code changes needed. Until a file exists, the site
   shows a placeholder automatically.

## Color palette (defined in `src/index.css` under `:root`)

| Token                  | Hex       | Used for                        |
|-------------------------|-----------|----------------------------------|
| `--color-primary`       | `#78A4CB` | Navbar, primary buttons          |
| `--color-secondary`     | `#95BDD7` | Hover/secondary actions          |
| `--color-accent`        | `#F9E8A2` | Highlights, badges, CTA accents  |
| `--color-bg-soft`       | `#B4E1EB` | Soft background sections        |

## Notes on the virtual try-on page

- **Camera access** requires `https://` or `localhost` in most
  browsers — running `npm run dev` and opening `localhost` satisfies
  this automatically.
- **Garment overlay** is a simple absolutely-positioned image over
  the photo (no pose detection or body segmentation) — enough to
  preview fit/color at a glance. Swapping in a real try-on model
  later only means changing the `<img className="overlay-garment">`
  block in `VirtualTryOn.jsx`.
- **Skin-tone detection** samples the center of the uploaded photo,
  averages brightness, and buckets it into Light / Medium / Deep.
  Each bucket has a simple contrast rule used to rank the product's
  *actual* available colors — see `src/utils/skinTone.js` for the
  full logic and where to improve accuracy later (e.g. swapping in
  real face detection instead of a center-crop sample).

## What's stubbed for later

- **Auth** is in-memory only (no backend, no password hashing) — good
  enough to wire up the UI flow.
- **Favorites** and **cart** reset on page refresh, since they live in
  React state (`AppContext.jsx`), as requested for this stage.
- **Checkout** just shows a confirmation alert — swap `handleConfirm`
  in `Cart.jsx` for a real order API when ready.
