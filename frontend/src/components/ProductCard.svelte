<script>
  import {
    authStore,
    cartStore,
    getProductImageUrl,
    notificationStore,
    productStore
  } from '../stores/store.svelte.js';

  let {
    product = {},
    onSelect = () => {},
    onEdit = () => {},
    onDelete = () => {}
  } = $props();

  async function handleDelete() {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
      const success = await productStore.deleteProduct(product._id);
      if (success) {
        onDelete();
      }
    }
  }

  async function handleAddToCart() {
    const success = await cartStore.addToCart(product._id);
    if (success) {
      notificationStore.add('Producto añadido al carrito', 'success');
    } else {
      notificationStore.add(cartStore.error || 'No se pudo añadir al carrito', 'error');
    }
  }
</script>

<article class="product-card">
  <button class="image-wrap" onclick={onSelect}>
    <img src={getProductImageUrl(product)} alt={product.nombre} />
    <span class="quick-view">Ver ficha</span>
  </button>

  <div class="product-info">
    <div class="product-head">
      <span class="product-badge estado-badge" class:inactive={product.estado === 'inactivo'}>
        {product.estado === 'activo' ? '✓ Activo' : '✗ Inactivo'}
      </span>
      <h3 class="product-name">{product.nombre}</h3>
    </div>

    <div class="price-row">
      <p class="product-price">${product.precio?.toFixed(2) || '0.00'}</p>
      <span class="tax-note">IVA incl.</span>
    </div>

    <div class="product-actions">
      <button class="btn btn-success primary-action" onclick={handleAddToCart}>
        Anadir al carrito
      </button>
      <button class="btn btn-secondary" onclick={onSelect}>
        Detalles
      </button>

      {#if authStore.user?.role === 'admin'}
        <button class="btn btn-secondary" onclick={onEdit}>
          Editar
        </button>
        <button class="btn btn-error" onclick={handleDelete}>
          Eliminar
        </button>
      {/if}
    </div>
  </div>
</article>

<style>
  .product-card {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid rgba(20, 33, 29, 0.08);
    border-radius: 28px;
    overflow: hidden;
    box-shadow: 0 24px 50px rgba(17, 24, 39, 0.07);
    transition: var(--transition);
  }

  .product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 28px 70px rgba(17, 24, 39, 0.1);
  }

  .image-wrap {
    position: relative;
    height: 280px;
    padding: 0;
    border: none;
    border-radius: 0;
    background: linear-gradient(180deg, #f8f5ef 0%, #ece7dc 100%);
    overflow: hidden;
  }

  .image-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.45s ease;
  }

  .product-card:hover .image-wrap img {
    transform: scale(1.04);
  }

  .quick-view {
    position: absolute;
    left: 1rem;
    bottom: 1rem;
    padding: 0.5rem 0.85rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.88);
    color: var(--secondary);
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .product-info {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    flex: 1;
    padding: 1.25rem;
  }

  .product-badge {
    display: inline-flex;
    width: fit-content;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    font-size: 0.73rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .estado-badge {
    background: #d4edda;
    color: #155724;
  }

  .estado-badge.inactive {
    background: #f8d7da;
    color: #721c24;
  }

  .product-name {
    margin-top: 0.7rem;
    font-size: 1.45rem;
    line-height: 1.05;
    color: var(--secondary);
  }

  .price-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
  }

  .product-price {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--primary);
  }

  .tax-note {
    color: var(--text-muted);
    font-size: 0.86rem;
    font-weight: 700;
  }

  .product-actions {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.65rem;
    margin-top: auto;
  }

  .primary-action {
    grid-column: 1 / -1;
  }

  @media (max-width: 480px) {
    .image-wrap {
      height: 240px;
    }

    .product-actions {
      grid-template-columns: 1fr;
    }
  }
</style>
