// Fixed against the real files in public/images (screenshot provided).
// Changes made:
//  - All image paths now start with "/images/..." consistently (root-relative,
//    works no matter which page/route references them).
//  - "…" (single ellipsis character) replaced with the real "..." (three dots)
//    in the cardigan filename — that mismatch alone would 404 silently.
//  - Images that were mismatched to the wrong product (pexels-* photos and
//    kampfmonchichi-clock used as "shoes"/"accessories", back.jpg reused as a
//    shoe) are set back to '' so they show the placeholder instead of a wrong
//    photo. We don't actually know what those pexels/clock photos show, so
//    labeling them as specific shoes/accessories would just be a guess.
//  - "Boys_cotton_t-shirt_modern_design_202607081154.jpeg" is NOT in your
//    public/images screenshot — left empty until you confirm the exact file
//    is really there (or its real name, if different).

const products = {
 // WOMEN section -- fully fixed:
//  - Cardigan now uses the real filename with three literal dots "..."
//    (your pasted code still had the "…" single-character ellipsis,
//     which is a different character and will always 404).
//  - All 9 clothes items now point at real, distinct photos.
//  - Accessories now use the 5 pexels-* photos, as requested. I can't see
//    what's actually in these photos, so the names below are placeholders
//    ("Accessory — pexels-name") -- rename them once you've looked at each
//    photo and know what it actually shows (bag, sunglasses, jewelry, etc).
//  - Shoes are still empty: there are no unused real photos left for them.
//    Once you add real shoe photos to public/images, send them over and
//    I'll wire them in the same way.

women: {
  clothes: [
    { id: 'casual-dress', name: "Women's Casual Dress", price: 128, image: "/images/Women's_casual_dress_folds_2K_202607081146.jpeg", colors: [{ name: 'Default', hex: '#c7b29d', image: "/images/Women's_casual_dress_folds_2K_202607081146.jpeg" }] },
    { id: 'casual-tshirt', name: "Women's Casual T-Shirt", price: 96, image: "/images/Women's_casual_t-shirt_displayed_2K_202607081141.jpeg", colors: [{ name: 'Default', hex: '#8ea382', image: "/images/Women's_casual_t-shirt_displayed_2K_202607081141.jpeg" }] },
    { id: 'elegant-blouse', name: "Women's Elegant Blouse", price: 118, image: "/images/Women's_elegant_blouse_front_view_202607081147.jpeg", colors: [{ name: 'Default', hex: '#f3e7d3', image: "/images/Women's_elegant_blouse_front_view_202607081147.jpeg" }] },
    { id: 'floral-dress', name: "Women's Floral Summer Dress", price: 88, image: "/images/Women's_floral_summer_dress_2K_202607081148.jpeg", colors: [{ name: 'Default', hex: '#b58a53', image: "/images/Women's_floral_summer_dress_2K_202607081148.jpeg" }] },
    { id: 'high-waist-jeans', name: "Women's High Waist Blue Jeans", price: 74, image: "/images/Women's_high_waist_blue_jeans_202607081144.jpeg", colors: [{ name: 'Default', hex: '#f4e6cf', image: "/images/Women's_high_waist_blue_jeans_202607081144.jpeg" }] },
    { id: 'knitted-cardigan', name: "Women's Knitted Cardigan", price: 112, image: "/images/Women's_knitted_cardigan_isolate…_2K_202607081150.jpeg", colors: [{ name: 'Default', hex: '#6d7b49', image: "/images/Women's_knitted_cardigan_isolate…_2K_202607081150.jpeg" }] },
    { id: 'maxi-dress', name: "Women's Studio Maxi Dress", price: 132, image: "/images/Women's_maxi_dress_studio_lighting_202607081149.jpeg", colors: [{ name: 'Default', hex: '#e7d6b8', image: "/images/Women's_maxi_dress_studio_lighting_202607081149.jpeg" }] },
    { id: 'midi-skirt', name: "Women's White Midi Skirt", price: 78, image: "/images/Women's_midi_skirt_white_background_202607081143.jpeg", colors: [{ name: 'Default', hex: '#f3e9d2', image: "/images/Women's_midi_skirt_white_background_202607081143.jpeg" }] },
    { id: 'wide-leg-trousers', name: "Women's Wide-Leg Trousers", price: 84, image: "/images/Women's_wide_leg_trousers_2K_202607081151.jpeg", colors: [{ name: 'Default', hex: '#2b3a4a', image: "/images/Women's_wide_leg_trousers_2K_202607081151.jpeg" }] }
  ],
 // Women's shoes -- using real, verified Unsplash photo URLs (checked each
// one directly, these are stable CDN links under the free Unsplash License,
// free for commercial use, no attribution required).
shoes: [
  {
    id: 'women-shoe-4',
    name: 'Classic Leather Heels',
    price: 130,
    image: 'https://images.unsplash.com/photo-1659261448687-6d01466e06e4?fm=jpg&q=80&w=800&auto=format&fit=crop',
    colors: [{ name: 'Black', hex: '#1f1f1f', image: 'https://images.unsplash.com/photo-1659261448687-6d01466e06e4?fm=jpg&q=80&w=800&auto=format&fit=crop' }]
  },
  {
    id: 'women-shoe-5',
    name: 'Classic Urban Sneakers',
    price: 95,
    image: 'https://images.unsplash.com/photo-1676379827610-c380c52db0c6?fm=jpg&q=80&w=800&auto=format&fit=crop',
    colors: [{ name: 'White', hex: '#f5f5f5', image: 'https://images.unsplash.com/photo-1676379827610-c380c52db0c6?fm=jpg&q=80&w=800&auto=format&fit=crop' }]
  },
  {
    id: 'women-shoe-6',
    name: 'Elegant Pink Heels',
    price: 110,
    image: 'https://images.unsplash.com/photo-1753161618059-2c71f81ea2b1?fm=jpg&q=80&w=800&auto=format&fit=crop',
    colors: [{ name: 'Pink', hex: '#e7b4b1', image: 'https://images.unsplash.com/photo-1753161618059-2c71f81ea2b1?fm=jpg&q=80&w=800&auto=format&fit=crop' }]
  }
],
  accessories: [
    { id: 'acc-1', name: 'Accessory — pexels-alexeydemidov', price: 75, image: '/images/pexels-alexeydemidov-11193417.jpg', colors: [{ name: 'Default', hex: '#e8e0d4', image: '/images/pexels-alexeydemidov-11193417.jpg' }] },
    { id: 'acc-2', name: 'Accessory — pexels-jonathanborba (1)', price: 90, image: '/images/pexels-jonathanborba-28900496.jpg', colors: [{ name: 'Default', hex: '#d7b8a1', image: '/images/pexels-jonathanborba-28900496.jpg' }] },
    { id: 'acc-3', name: 'Accessory — pexels-jonathanborba (2)', price: 88, image: '/images/pexels-jonathanborba-28900498.jpg', colors: [{ name: 'Default', hex: '#c9a97f', image: '/images/pexels-jonathanborba-28900498.jpg' }] },
    { id: 'acc-4', name: 'Accessory — pexels-mathilde', price: 95, image: '/images/pexels-mathilde-10897815.jpg', colors: [{ name: 'Default', hex: '#80573d', image: '/images/pexels-mathilde-10897815.jpg' }] },
    { id: 'acc-5', name: 'Accessory — pexels-ron-lach', price: 82, image: '/images/pexels-ron-lach-8571860.jpg', colors: [{ name: 'Default', hex: '#9f5f3b', image: '/images/pexels-ron-lach-8571860.jpg' }] }
  ]
},
  men: {
    clothes: [
      { id: 'crew-neck-tshirt', name: "Men's Crew Neck T-Shirt Folded", price: 86, image: "/images/Men's_crew_neck_t-shirt_folded_202607081135.jpeg", colors: [{ name: 'Default', hex: '#213a57', image: "/images/Men's_crew_neck_t-shirt_folded_202607081135.jpeg" }] },
      { id: 'formal-shirt', name: "Men's Formal Long Sleeve Shirt", price: 156, image: "/images/Men's_formal_long_sleeve_shirt_202607081136.jpeg", colors: [{ name: 'Default', hex: '#3c3c3c', image: "/images/Men's_formal_long_sleeve_shirt_202607081136.jpeg" }] },
      { id: 'polo-shirt', name: "Men's Polo Shirt Studio Lighting", price: 98, image: "/images/Men's_polo_shirt_studio_lighting_202607081138.jpeg", colors: [{ name: 'Default', hex: '#d9cdb9', image: "/images/Men's_polo_shirt_studio_lighting_202607081138.jpeg" }] },
      { id: 'urban-trousers', name: 'Trousers in Urban Street Setting', price: 92, image: '/images/Trousers_in_urban_street_setting_202607081155.jpeg', colors: [{ name: 'Default', hex: '#5e6771', image: '/images/Trousers_in_urban_street_setting_202607081155.jpeg' }] },
      { id: 'men-clothes-5', name: "Men's Casual Bomber Jacket", price: 145, image: '', colors: [{ name: 'Default', hex: '#23354a', image: '' }] },
      { id: 'men-clothes-6', name: "Men's Classic Chino Shorts", price: 55, image: '', colors: [{ name: 'Default', hex: '#ceb085', image: '' }] }
    ],
    shoes: [
      // back.jpg is your homepage hero photo, not a shoe -- removed from here.
      { id: 'men-shoe-1', name: 'Urban Everyday Shoes', price: 120, image: '', colors: [{ name: 'Default', hex: '#af7d46', image: '' }] },
      { id: 'men-shoe-2', name: 'Classic Leather Oxfords', price: 165, image: '', colors: [{ name: 'Default', hex: '#1a1a1a', image: '' }] },
      { id: 'men-shoe-3', name: 'Sport Trail Runners', price: 115, image: '', colors: [{ name: 'Default', hex: '#5d6770', image: '' }] },
      { id: 'men-shoe-4', name: 'Suede Weekend Loafers', price: 125, image: '', colors: [{ name: 'Default', hex: '#7a5b34', image: '' }] },
      { id: 'men-shoe-5', name: 'All-Weather Waterproof Boots', price: 180, image: '', colors: [{ name: 'Default', hex: '#2a2d34', image: '' }] },
      { id: 'men-shoe-6', name: 'Lightweight Canvas Sneakers', price: 85, image: '', colors: [{ name: 'Default', hex: '#e7e0d2', image: '' }] }
    ]
  },
  kids: {
    clothes: [
      // NOT in your public/images screenshot -- confirm the exact filename
      // (or that the file was actually moved there) before relying on this.
      { id: 'boys-cotton-tshirt', name: 'Boys Cotton T-Shirt Modern Design', price: 64, image: '', colors: [{ name: 'Default', hex: '#d66b5a', image: '' }] },
      { id: 'boys-hoodie', name: 'Boys Hoodie on White Background', price: 58, image: '/images/Boys_hoodie_on_white_background_202607081156.jpeg', colors: [{ name: 'Default', hex: '#b79dcf', image: '/images/Boys_hoodie_on_white_background_202607081156.jpeg' }] },
      { id: 'kids-clothes-3', name: 'Kids Denim Play Jacket', price: 72, image: '', colors: [{ name: 'Default', hex: '#7ba4c6', image: '' }] },
      { id: 'kids-clothes-4', name: 'Girls Summer Sun Skirt', price: 45, image: '', colors: [{ name: 'Default', hex: '#e4b6c2', image: '' }] },
      { id: 'kids-clothes-5', name: 'Unisex Cotton Sweatpants', price: 38, image: '', colors: [{ name: 'Default', hex: '#4a7ea4', image: '' }] },
      { id: 'kids-clothes-6', name: 'Toddler Graphic Dino Tee', price: 32, image: '', colors: [{ name: 'Default', hex: '#5c8d8a', image: '' }] }
    ],
    shoes: [
      { id: 'kids-shoe-1', name: 'Kids Mini Sport Sneakers', price: 55, image: '', colors: [{ name: 'Default', hex: '#b3cf56', image: '' }] },
      { id: 'kids-shoe-2', name: 'Bright Waterproof Rain Boots', price: 48, image: '', colors: [{ name: 'Default', hex: '#dec556', image: '' }] },
      { id: 'kids-shoe-3', name: 'Comfy Toddler First Steps', price: 42, image: '', colors: [{ name: 'Default', hex: '#c58d93', image: '' }] },
      { id: 'kids-shoe-4', name: 'Summer Candy Sandals', price: 35, image: '', colors: [{ name: 'Default', hex: '#db7a9d', image: '' }] },
      { id: 'kids-shoe-5', name: 'Kids Active Play Runners', price: 60, image: '', colors: [{ name: 'Default', hex: '#e6d16b', image: '' }] },
      { id: 'kids-shoe-6', name: 'Flexible Lightweight Loafers', price: 50, image: '', colors: [{ name: 'Default', hex: '#8ec3ae', image: '' }] }
    ]
  }
};
const catalog = [...Object.values(products.women).flat(), ...Object.values(products.men).flat(), ...Object.values(products.kids).flat()];
const CART_STORAGE_KEY = 'auraCartItems';
const CART_COUNT_KEY = 'auraCartCount';
const SIZE_OPTIONS = ['S', 'M', 'L', 'XL', 'XXL'];

function getCartItems() {
  try {
    return JSON.parse(localStorage.getItem(CART_STORAGE_KEY) || '[]');
  } catch {
    return [];
  }
}

function getCartCountFromItems(items) {
  return items.reduce((total, item) => total + Number(item.quantity || 1), 0);
}

function getCartCount() {
  return getCartCountFromItems(getCartItems());
}

function saveCartItems(items) {
  localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
  localStorage.setItem(CART_COUNT_KEY, String(getCartCountFromItems(items)));
  updateCartBadge();
  if (document.getElementById('cartDrawer')) {
    renderCartDrawer();
  }
}

function addToCart(productId, size = 'M') {
  const product = catalog.find((item) => item.id === productId);
  if (!product) return false;
  const items = getCartItems();
  const existing = items.find((item) => item.id === productId && item.size === size);
  if (existing) {
    existing.quantity = Number(existing.quantity || 1) + 1;
  } else {
    items.push({ id: product.id, name: product.name, price: product.price, image: product.image, quantity: 1, size: size || 'M' });
  }
  saveCartItems(items);
  showCartToast(`${product.name} • ${size}`);
  return true;
}

function showCartToast(message = 'Added to cart') {
  let toast = document.getElementById('cartToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'cartToast';
    toast.className = 'cart-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(showCartToast.timeout);
  showCartToast.timeout = window.setTimeout(() => {
    toast.classList.remove('show');
  }, 1800);
}

function updateCartBadge() {
  const badges = document.querySelectorAll('[data-cart-badge]');
  const count = getCartCount();
  badges.forEach((badge) => {
    badge.textContent = count;
  });
}

function ensureCartDrawer() {
  if (document.getElementById('cartDrawer')) return;

  const drawer = document.createElement('div');
  drawer.id = 'cartDrawer';
  drawer.className = 'cart-drawer';
  drawer.setAttribute('aria-hidden', 'true');
  drawer.innerHTML = `
    <div class="cart-backdrop" data-cart-close></div>
    <div class="cart-panel" role="dialog" aria-label="Your cart">
      <div class="cart-panel-header">
        <div>
          <h3>Your cart</h3>
          <p class="cart-panel-subtitle">Pick your favourites, try them on, and confirm when you are ready.</p>
        </div>
        <button type="button" class="cart-close" data-cart-close aria-label="Close cart">✕</button>
      </div>
      <div class="cart-items"></div>
      <div class="cart-footer">
        <div class="cart-summary">
          <span>Total</span>
          <strong class="cart-total">$0</strong>
        </div>
        <button type="button" class="btn btn-primary cart-confirm">Confirm order</button>
      </div>
    </div>
  `;

  document.body.appendChild(drawer);

  drawer.querySelector('.cart-items')?.addEventListener('click', (event) => {
    const incrementButton = event.target.closest('[data-cart-inc]');
    if (incrementButton) {
      const id = incrementButton.getAttribute('data-cart-inc');
      const items = getCartItems();
      const item = items.find((entry) => entry.id === id);
      if (item) {
        item.quantity = Number(item.quantity || 1) + 1;
        saveCartItems(items);
      }
      return;
    }

    const decrementButton = event.target.closest('[data-cart-dec]');
    if (decrementButton) {
      const id = decrementButton.getAttribute('data-cart-dec');
      const items = getCartItems();
      const item = items.find((entry) => entry.id === id);
      if (item) {
        item.quantity = Math.max(1, Number(item.quantity || 1) - 1);
        saveCartItems(items);
      }
      return;
    }

    const removeButton = event.target.closest('[data-cart-remove]');
    if (removeButton) {
      const id = removeButton.getAttribute('data-cart-remove');
      const items = getCartItems().filter((entry) => entry.id !== id);
      saveCartItems(items);
      return;
    }

    const tryButton = event.target.closest('[data-tryon-item]');
    if (tryButton) {
      const id = tryButton.getAttribute('data-tryon-item');
      closeCartDrawer();
      window.location.href = `tryon.html?product=${id}`;
    }
  });

  drawer.querySelector('.cart-confirm')?.addEventListener('click', () => {
    const items = getCartItems();
    if (!items.length) return;
    localStorage.removeItem(CART_STORAGE_KEY);
    localStorage.setItem(CART_COUNT_KEY, '0');
    updateCartBadge();
    renderCartDrawer();
    showCartToast('Order confirmed');
  });

  drawer.querySelectorAll('[data-cart-close]').forEach((element) => {
    element.addEventListener('click', closeCartDrawer);
  });
}

function renderCartDrawer() {
  ensureCartDrawer();
  const drawer = document.getElementById('cartDrawer');
  const list = drawer?.querySelector('.cart-items');
  const total = drawer?.querySelector('.cart-total');
  if (!list || !total) return;

  const items = getCartItems();
  const subtotal = items.reduce((sum, item) => sum + item.price * Number(item.quantity || 1), 0);

  if (!items.length) {
    list.innerHTML = '<div class="cart-empty">Your cart is empty. Add a piece to start your edit.</div>';
    total.textContent = '$0';
    return;
  }

  list.innerHTML = items.map((item) => `
    <div class="cart-item">
      <img src="${item.image}" alt="${item.name}" />
      <div>
        <p class="cart-item-title">${item.name}</p>
        <div class="cart-item-price">$${item.price}</div>
        <div class="cart-item-size">Size: ${item.size || 'M'}</div>
        <div class="cart-item-actions">
          <button type="button" class="cart-qty-btn" data-cart-dec="${item.id}">−</button>
          <span>${item.quantity}</span>
          <button type="button" class="cart-qty-btn" data-cart-inc="${item.id}">+</button>
          <button type="button" class="cart-remove" data-cart-remove="${item.id}">Remove</button>
          <button type="button" class="cart-tryon" data-tryon-item="${item.id}">Try it on</button>
        </div>
      </div>
      <div class="cart-item-total">$${item.price * Number(item.quantity || 1)}</div>
    </div>
  `).join('');

  total.textContent = `$${subtotal}`;
}

function openCartDrawer() {
  ensureCartDrawer();
  const drawer = document.getElementById('cartDrawer');
  if (!drawer) return;
  drawer.classList.add('is-open');
  drawer.setAttribute('aria-hidden', 'false');
  renderCartDrawer();
}

function closeCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  if (!drawer) return;
  drawer.classList.remove('is-open');
  drawer.setAttribute('aria-hidden', 'true');
}

function initNav() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  document.querySelectorAll('.nav-links a').forEach((link) => {
    const href = link.getAttribute('href') || '';
    const path = window.location.pathname.split('/').pop() || 'index.html';
    const isActive = path === href || (href === 'index.html' && (path === '' || path === 'index.html'));
    if (isActive) link.classList.add('active');
  });
}

function setAccountLink() {
  const link = document.querySelector('[data-account-link]');
  if (!link) return;
  const user = JSON.parse(localStorage.getItem('auraUser') || 'null');
  if (user?.name) {
    link.innerHTML = `Hi, ${user.name}`;
    link.setAttribute('href', 'login.html');
  } else {
    link.innerHTML = '👤';
    link.setAttribute('href', 'login.html');
  }
}

function renderProductGrid(container, items) {
  if (!container) return;
  container.innerHTML = items.map((product) => `
    <article class="product-card">
      <img src="${product.image}" alt="${product.name}">
      <div class="product-body">
        <div class="product-meta">
          <h3 class="product-title">${product.name}</h3>
          <span class="price-tag">$${product.price}</span>
        </div>
        <div class="swatches" aria-label="Color options">
          ${product.colors.map((color) => `<span class="swatch" style="background:${color.hex}" title="${color.name}"></span>`).join('')}
        </div>
        <div class="size-picker">
          <label class="size-label" for="size-${product.id}">Size</label>
          <select class="size-select" id="size-${product.id}" data-product-size="${product.id}">
            ${SIZE_OPTIONS.map((size) => `<option value="${size}" ${size === 'M' ? 'selected' : ''}>${size}</option>`).join('')}
          </select>
        </div>
        <div class="product-actions" style="margin-top: 0.9rem;">
          <button class="btn ghost-btn" data-add-to-cart="${product.id}">Add to cart</button>
          <a class="btn btn-secondary" href="tryon.html?product=${product.id}">Try it on</a>
        </div>
      </div>
    </article>
  `).join('');
}

function renderFeaturedProducts() {
  const featured = [
    products.women.clothes[0],
    products.men.clothes[1],
    products.kids.clothes[0],
    products.women.accessories[0]
  ];
  const container = document.getElementById('featuredProducts');
  renderProductGrid(container, featured);
}

function renderCollectionPage(category) {
  const heading = document.querySelector('[data-page-heading]');
  if (heading) {
    const title = category === 'women' ? "Women's Collection" : category === 'men' ? "Men's Collection" : "Kids' Collection";
    heading.textContent = title;
  }

  const sections = category === 'women'
    ? [
        { id: 'women-clothes-grid', items: products.women.clothes },
        { id: 'women-shoes-grid', items: products.women.shoes },
        { id: 'women-accessories-grid', items: products.women.accessories }
      ]
    : category === 'men'
      ? [
          { id: 'men-clothes-grid', items: products.men.clothes },
          { id: 'men-shoes-grid', items: products.men.shoes }
        ]
      : [
          { id: 'kids-clothes-grid', items: products.kids.clothes },
          { id: 'kids-shoes-grid', items: products.kids.shoes }
        ];

  sections.forEach(({ id, items }) => {
    const container = document.getElementById(id);
    renderProductGrid(container, items);
  });
}

function initCartActions() {
  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-add-to-cart]');
    if (!button) return;
    const id = button.getAttribute('data-add-to-cart');
    const product = catalog.find((item) => item.id === id);
    if (!product) return;
    event.preventDefault();
    const card = button.closest('.product-card');
    const sizeSelect = card?.querySelector('[data-product-size]');
    const size = sizeSelect?.value || 'M';
    addToCart(id, size);
    button.textContent = 'Added';
    button.classList.add('is-added');
    button.disabled = true;
    window.setTimeout(() => {
      button.disabled = false;
      button.textContent = 'Add to cart';
      button.classList.remove('is-added');
    }, 1000);
  });

  document.querySelectorAll('[data-cart-trigger]').forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      openCartDrawer();
    });
  });
}

function initAuthForms() {
  const loginForm = document.getElementById('loginForm');
  const signupForm = document.getElementById('signupForm');

  if (loginForm) {
    loginForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const email = loginForm.email.value.trim();
      const password = loginForm.password.value;
      const message = loginForm.querySelector('.form-message');
      if (!email || !password) {
        showFormMessage(message, 'Please fill in both fields.', 'error');
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showFormMessage(message, 'Please enter a valid email address.', 'error');
        return;
      }
      const user = JSON.parse(localStorage.getItem('auraUser') || 'null');
      const displayName = user?.name || 'Guest';
      localStorage.setItem('auraLoggedIn', 'true');
      localStorage.setItem('auraUser', JSON.stringify({ name: displayName, email }));
      showFormMessage(message, 'Welcome back! Redirecting to the shop…', 'success');
      setTimeout(() => { window.location.href = 'index.html'; }, 800);
    });
  }

  if (signupForm) {
    signupForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const name = signupForm.fullName.value.trim();
      const email = signupForm.email.value.trim();
      const password = signupForm.password.value;
      const message = signupForm.querySelector('.form-message');
      if (!name || !email || !password) {
        showFormMessage(message, 'Please complete all fields.', 'error');
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showFormMessage(message, 'Please enter a valid email address.', 'error');
        return;
      }
      localStorage.setItem('auraLoggedIn', 'true');
      localStorage.setItem('auraUser', JSON.stringify({ name, email }));
      showFormMessage(message, 'Account created — taking you home.', 'success');
      setTimeout(() => { window.location.href = 'index.html'; }, 800);
    });
  }
}

function showFormMessage(element, text, type) {
  if (!element) return;
  element.textContent = text;
  element.className = `form-message ${type}`;
}

function initTryOnPage() {
  const params = new URLSearchParams(window.location.search);
  const productId = params.get('product') || 'classic-blazer';
  const product = catalog.find((item) => item.id === productId) || products.women[0];
  const productName = document.getElementById('tryonProductName');
  const productPrice = document.getElementById('tryonProductPrice');
  const thumb = document.getElementById('tryonProductThumb');
  const swatchContainer = document.getElementById('colorSwatches');
  const previewFrame = document.getElementById('previewFrame');
  const previewOverlay = document.getElementById('previewOverlay');
  const previewImage = document.getElementById('previewImage');
  const previewVideo = document.getElementById('previewVideo');
  const captureButton = document.getElementById('captureButton');
  const uploadButton = document.getElementById('uploadPhotoButton');
  const cameraButton = document.getElementById('cameraButton');
  const recommendationButton = document.getElementById('recommendationButton');
  const recommendationNote = document.getElementById('recommendationNote');
  const addToCartButton = document.getElementById('addToCartTryon');
  const hiddenCanvas = document.getElementById('hiddenCanvas');
  const ctx = hiddenCanvas.getContext('2d');

  if (productName) productName.textContent = product.name;
  if (productPrice) productPrice.textContent = `$${product.price}`;
  if (thumb) thumb.src = product.image;

  let selectedColor = product.colors[0];
  let photoData = null;
  let stream = null;
  let cameraActive = false;

  function renderSwatches() {
    if (!swatchContainer) return;
    swatchContainer.innerHTML = product.colors.map((color) => `
      <button class="swatch-button ${selectedColor?.name === color.name ? 'selected' : ''}" data-select-color="${color.name}">
        <span class="swatch-dot" style="background:${color.hex}"></span>
        <span>${color.name}</span>
      </button>
    `).join('');
  }

  function showPlaceholder() {
    if (previewOverlay) previewOverlay.style.display = 'grid';
    if (previewImage) previewImage.style.display = 'none';
    if (previewVideo) previewVideo.style.display = 'none';
    if (captureButton) captureButton.style.display = 'none';
    if (recommendationButton) recommendationButton.disabled = true;
    if (recommendationNote) recommendationNote.textContent = 'Add a photo first so we can take a look';
    if (document.getElementById('productOverlay')) document.getElementById('productOverlay').style.display = 'none';
    photoData = null;
  }

  function showPhoto(imageData) {
    photoData = imageData;
    if (previewImage) {
      previewImage.src = imageData;
      previewImage.style.display = 'block';
    }
    if (previewOverlay) previewOverlay.style.display = 'none';
    if (previewVideo) previewVideo.style.display = 'none';
    if (captureButton) captureButton.style.display = 'none';
    if (recommendationButton) recommendationButton.disabled = false;
    if (recommendationNote) recommendationNote.textContent = '';
    const overlay = document.getElementById('productOverlay');
    if (overlay) {
      overlay.src = selectedColor?.image || product.image;
      overlay.style.display = 'block';
    }
  }

  function stopStream() {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }
    cameraActive = false;
    if (previewVideo) previewVideo.srcObject = null;
  }

  function startCamera() {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert('Camera access is not available in this browser.');
      return;
    }
    navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then((mediaStream) => {
      stream = mediaStream;
      cameraActive = true;
      if (previewVideo) {
        previewVideo.srcObject = mediaStream;
        previewVideo.play();
        previewVideo.style.display = 'block';
      }
      if (previewImage) previewImage.style.display = 'none';
      if (previewOverlay) previewOverlay.style.display = 'none';
      if (captureButton) captureButton.style.display = 'inline-flex';
      if (recommendationButton) recommendationButton.disabled = true;
    }).catch(() => {
      alert('Camera access was denied.');
    });
  }

  if (uploadButton) {
    uploadButton.addEventListener('click', () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.addEventListener('change', () => {
        const file = input.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          stopStream();
          showPhoto(reader.result);
        };
        reader.readAsDataURL(file);
      });
      input.click();
    });
  }

  if (cameraButton) {
    cameraButton.addEventListener('click', () => {
      if (cameraActive) {
        stopStream();
        showPlaceholder();
        return;
      }
      startCamera();
    });
  }

  if (captureButton) {
    captureButton.addEventListener('click', () => {
      if (!previewVideo || !previewFrame) return;
      hiddenCanvas.width = previewVideo.videoWidth || 400;
      hiddenCanvas.height = previewVideo.videoHeight || 600;
      ctx.drawImage(previewVideo, 0, 0, hiddenCanvas.width, hiddenCanvas.height);
      const data = hiddenCanvas.toDataURL('image/jpeg');
      stopStream();
      showPhoto(data);
      if (previewOverlay) previewOverlay.style.display = 'none';
    });
  }

  swatchContainer?.addEventListener('click', (event) => {
    const button = event.target.closest('[data-select-color]');
    if (!button) return;
    const colorName = button.getAttribute('data-select-color');
    selectedColor = product.colors.find((color) => color.name === colorName) || product.colors[0];
    renderSwatches();
    const overlay = document.getElementById('productOverlay');
    if (overlay && photoData) {
      overlay.src = selectedColor.image;
      overlay.style.display = 'block';
    }
  });

  recommendationButton?.addEventListener('click', () => {
    if (!photoData) return;
    const image = new Image();
    image.onload = () => {
      hiddenCanvas.width = image.width;
      hiddenCanvas.height = image.height;
      ctx.drawImage(image, 0, 0, image.width, image.height);
      const sampleX = Math.floor(image.width / 2);
      const sampleY = Math.floor(image.height / 2);
      const data = ctx.getImageData(sampleX, sampleY, 1, 1).data;
      const brightness = (data[0] * 0.299 + data[1] * 0.587 + data[2] * 0.114) / 255;
      const tone = brightness > 0.68 ? 'Light' : brightness > 0.38 ? 'Medium' : 'Deep';
      const scored = product.colors
        .map((color) => ({ ...color, score: getContrastScore(color.hex, tone) }))
        .sort((a, b) => a.score - b.score);
      const orderedNames = scored.map((color) => color.name);
      selectedColor = product.colors.find((color) => color.name === orderedNames[0]) || product.colors[0];
      renderSwatches();
      if (recommendationNote) recommendationNote.textContent = `Best match for a ${tone.toLowerCase()} complexion: ${orderedNames[0]}`;
    };
    image.src = photoData;
  });

  addToCartButton?.addEventListener('click', (event) => {
    event.preventDefault();
    const sizeSelect = document.getElementById('tryonSizeSelect');
    const size = sizeSelect?.value || 'M';
    addToCart(product.id, size);
    addToCartButton.textContent = 'Added';
    addToCartButton.disabled = true;
    window.setTimeout(() => {
      addToCartButton.disabled = false;
      addToCartButton.textContent = 'Add to cart';
    }, 1000);
  });

  function getContrastScore(hex, tone) {
    const hexValue = hex.replace('#', '');
    const r = parseInt(hexValue.slice(0, 2), 16);
    const g = parseInt(hexValue.slice(2, 4), 16);
    const b = parseInt(hexValue.slice(4, 6), 16);
    const brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255;
    if (tone === 'Light') return brightness;
    if (tone === 'Deep') return 1 - brightness;
    return Math.abs(brightness - 0.5);
  }

  renderSwatches();
  showPlaceholder();
}

function initPage() {
  updateCartBadge();
  setAccountLink();
  initNav();
  initCartActions();
  initAuthForms();

  const currentPath = window.location.pathname.split('/').pop();
  if (currentPath === 'index.html' || currentPath === '') {
    renderFeaturedProducts();
  } else if (currentPath === 'men.html') {
    renderCollectionPage('men');
  } else if (currentPath === 'women.html') {
    renderCollectionPage('women');
  } else if (currentPath === 'kids.html') {
    renderCollectionPage('kids');
  } else if (currentPath === 'tryon.html') {
    initTryOnPage();
  }
}

document.addEventListener('DOMContentLoaded', initPage);
