
// API Configuration
const API_BASE_URL = import.meta.env.MODE === 'development' 
  ? 'http://localhost:3000/api'
  : '/api';
const UPLOAD_BASE_URL = import.meta.env.MODE === 'development'
  ? 'http://localhost:3000/uploads'
  : '/uploads';

// Global store - Authentication state
export const authStore = $state({
  user: null,
  token: null,
  loading: false,
  error: null,
  isAuthenticated: false,
  
  init() {
    this.token = null;
    this.user = null;
    this.isAuthenticated = false;
    this.error = null;
  },

  // Login
  async login(username, password) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!response.ok) {
        throw new Error('Credenciales inválidas');
      }

      const data = await response.json();
      this.token = data.token;
      this.isAuthenticated = true;
      
      // Decode and store user info
      const decoded = parseJWT(data.token);
      this.user = decoded;
      
      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  // Register
  async register(username, password) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Error en el registro');
      }

      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  // Logout
  logout() {
    this.token = null;
    this.user = null;
    this.isAuthenticated = false;
    this.error = null;
  },

  // Clear error
  clearError() {
    this.error = null;
  }
});

// Products store
export const productStore = $state({
  products: [],
  loading: false,
  error: null,
  currentProduct: null,
  filter: '',
  
  async fetchProducts(filter = '') {
    this.loading = true;
    this.error = null;
    try {
      const url = filter 
        ? `${API_BASE_URL}/productos?name=${encodeURIComponent(filter)}`
        : `${API_BASE_URL}/productos`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error('Error al obtener productos');
      
      this.products = await response.json();
      this.filter = filter;
    } catch (err) {
      this.error = err.message;
    } finally {
      this.loading = false;
    }
  },

  async createProduct(formData) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/productos`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        },
        body: formData
      });

      if (!response.ok) throw new Error('Error al crear producto');
      
      const product = await response.json();
      this.products.push(product);
      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  async updateProduct(id, formData) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/productos/${id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        },
        body: formData
      });

      if (!response.ok) throw new Error('Error al actualizar producto');
      
      const updated = await response.json();
      const index = this.products.findIndex(p => p._id === id);
      if (index > -1) {
        this.products[index] = updated;
      }
      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  async deleteProduct(id) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/productos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      });

      if (!response.ok) throw new Error('Error al eliminar producto');
      
      this.products = this.products.filter(p => p._id !== id);
      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  setCurrentProduct(product) {
    this.currentProduct = product;
  },

  clearError() {
    this.error = null;
  }
});

export const cartStore = $state({
  items: [],
  loading: false,
  error: null,
  checkoutSummary: null,

  async fetchCart() {
    if (!authStore.token) {
      this.items = [];
      return;
    }

    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/cart`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      });

      if (!response.ok) throw new Error('Error al obtener el carrito');
      this.items = await response.json();
    } catch (err) {
      this.error = err.message;
    } finally {
      this.loading = false;
    }
  },

  async addToCart(productId) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/cart/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify({ productId })
      });

      if (!response.ok) throw new Error('Error al añadir al carrito');
      this.items = await response.json();
      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  async removeFromCart(productId) {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${productId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      });

      if (!response.ok) throw new Error('Error al eliminar del carrito');
      this.items = await response.json();
      return true;
    } catch (err) {
      this.error = err.message;
      return false;
    } finally {
      this.loading = false;
    }
  },

  async checkout() {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/cart/checkout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      });

      if (!response.ok) throw new Error('Error al simular la compra');
      this.checkoutSummary = await response.json();
      this.items = [];
      return this.checkoutSummary;
    } catch (err) {
      this.error = err.message;
      return null;
    } finally {
      this.loading = false;
    }
  },

  clear() {
    this.items = [];
    this.loading = false;
    this.error = null;
    this.checkoutSummary = null;
  },

  clearSummary() {
    this.checkoutSummary = null;
  }
});

// Users store (for admin management)
export const userStore = $state({
  users: [],
  loading: false,
  error: null,
  
  async fetchUsers() {
    this.loading = true;
    this.error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      });

      if (!response.ok) throw new Error('Error al obtener usuarios');
      
      this.users = await response.json();
    } catch (err) {
      this.error = err.message;
    } finally {
      this.loading = false;
    }
  },

  clearError() {
    this.error = null;
  }
});

// Notifications store
export const notificationStore = $state({
  messages: [],

  add(message, type = 'info', duration = 3000) {
    const id = Date.now();
    this.messages.push({ id, message, type });
    
    if (duration > 0) {
      setTimeout(() => {
        this.messages = this.messages.filter(m => m.id !== id);
      }, duration);
    }
    
    return id;
  },

  remove(id) {
    this.messages = this.messages.filter(m => m.id !== id);
  },

  clearAll() {
    this.messages = [];
  }
});

// Derived state
export const isAdmin = () => authStore.user?.role === 'admin';
export const cartItemsCount = () =>
  cartStore.items.reduce((sum, item) => sum + (item.quantity || 0), 0);
export const cartTotal = () =>
  cartStore.items.reduce(
    (sum, item) => sum + ((item.productId?.precio || 0) * (item.quantity || 0)),
    0
  );

export const filteredProducts = () => {
  if (!productStore.filter) {
    return productStore.products;
  }
  
  const filter = productStore.filter.toLowerCase();
  return productStore.products.filter(p => 
    p.nombre.toLowerCase().includes(filter)
  );
};

export const productCount = () => productStore.products.length;

export const canEditProducts = () => authStore.isAuthenticated && isAdmin();
export const getProductImageUrl = (product) => {
  if (!product?.imagen) return '/placeholder.svg';
  if (product.imagen.startsWith('http')) return product.imagen;
  return `${UPLOAD_BASE_URL}/${product.imagen}`;
};

// Utility: Decode JWT
function parseJWT(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/[-_]/g, (c) => {
      return c === '-' ? '+' : '/';
    });
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (err) {
    console.error('Error decoding JWT:', err);
    return null;
  }
}

// Initialize auth on app start
export function initializeApp() {
  authStore.init();
  cartStore.clear();
}
