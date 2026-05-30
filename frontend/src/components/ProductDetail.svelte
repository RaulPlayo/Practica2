<script>
  import { cartStore, getProductImageUrl, notificationStore } from '../stores/store.svelte.js';

  let { product = null, onClose = () => {} } = $props();

  async function addToCart() {
    const success = await cartStore.addToCart(product._id);
    if (success) {
      notificationStore.add('Producto añadido al carrito', 'success');
    } else {
      notificationStore.add(cartStore.error || 'No se pudo añadir al carrito', 'error');
    }
  }
</script>
<div class="detail-overlay" onclick={onClose}>
  <div class="detail-modal" onclick={(e) => e.stopPropagation()}>
    <button class="close-btn" onclick={onClose}>Cerrar</button>

    <div class="detail-content">
      <div class="detail-image">
        <img src={getProductImageUrl(product)} alt={product.nombre} />
      </div>

      <div class="detail-info">
        <span class="detail-kicker">Producto destacado</span>
        <div class="detail-header">
          <h2>{product.nombre}</h2>
          <span class="estado-badge" class:inactive={product.estado === 'inactivo'}>
            {product.estado === 'activo' ? '✓ Activo' : '✗ Inactivo'}
          </span>
        </div>
        <p class="detail-copy">
          
        </p>

        <div class="detail-price">
          <p class="price">${product.precio?.toFixed(2) || '0.00'}</p>
          <span>Entrega estimada en 24/48 horas</span>
        </div>

        <div class="detail-benefits">
          <div>
            <strong>Pago seguro</strong>
            <span></span>
          </div>
          <div>
            <strong>Atencion premium</strong>
            <span></span>
          </div>
        </div>

        <div class="detail-actions">
          <button class="btn btn-success" onclick={addToCart}>
            Anadir al carrito
          </button>
          <button class="btn btn-secondary" onclick={onClose}>
            Seguir viendo
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .detail-overlay {
    position: fixed;
    inset: 0;
    background: rgba(16, 24, 20, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
    overflow-y: auto;
  }

  .detail-modal {
    width: min(1080px, 100%);
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(20, 33, 29, 0.08);
    border-radius: 34px;
    box-shadow: 0 36px 90px rgba(17, 24, 39, 0.18);
    padding: 1rem;
    position: relative;
  }

  .close-btn {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    min-width: 110px;
  }

  .detail-content {
    display: grid;
    grid-template-columns: 1.15fr 0.95fr;
    gap: 1.25rem;
    align-items: stretch;
  }

  .detail-image {
    min-height: 520px;
    border-radius: 26px;
    overflow: hidden;
    background: linear-gradient(180deg, #f8f4ec 0%, #ece7dc 100%);
  }

  .detail-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .detail-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem 1.5rem;
  }

  .detail-kicker {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .detail-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5rem;
  }

  .detail-header h2 {
    margin: 0;
    flex: 1;
  }

  .estado-badge {
    display: inline-flex;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: #d4edda;
    color: #155724;
    font-size: 0.73rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .estado-badge.inactive {
    background: #f8d7da;
    color: #721c24;
  }

  .detail-copy {
    margin-top: 1rem;
    color: var(--text-muted);
  }

  .detail-price {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin: 1.5rem 0;
    padding: 1.25rem 0;
    border-top: 1px solid rgba(20, 33, 29, 0.08);
    border-bottom: 1px solid rgba(20, 33, 29, 0.08);
  }

  .detail-price span {
    color: var(--text-muted);
    font-weight: 600;
  }

  .price {
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.05em;
  }

  .detail-benefits {
    display: grid;
    gap: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .detail-benefits div {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: var(--surface-muted);
    border: 1px solid rgba(20, 33, 29, 0.07);
  }

  .detail-benefits strong,
  .detail-benefits span {
    display: block;
  }

  .detail-benefits span {
    margin-top: 0.25rem;
    color: var(--text-muted);
  }

  .detail-actions {
    display: flex;
    gap: 0.8rem;
  }

  @media (max-width: 900px) {
    .detail-content {
      grid-template-columns: 1fr;
    }

    .detail-image {
      min-height: 320px;
    }

    .close-btn {
      position: static;
      margin: 0 0 1rem auto;
    }
  }

  @media (max-width: 480px) {
    .detail-actions {
      flex-direction: column;
    }
  }
</style>
