<script>
  import {
    cartItemsCount,
    cartStore,
    cartTotal,
    getProductImageUrl,
    notificationStore
  } from '../stores/store.svelte.js';

  async function removeItem(productId) {
    const success = await cartStore.removeFromCart(productId);
    if (success) {
      notificationStore.add('Producto eliminado del carrito', 'success');
    } else {
      notificationStore.add(cartStore.error || 'No se pudo eliminar el producto', 'error');
    }
  }

  async function checkout() {
    const summary = await cartStore.checkout();
    if (summary) {
      notificationStore.add('Compra realizada correctamente', 'success');
    } else {
      notificationStore.add(cartStore.error || 'No se pudo simular la compra', 'error');
    }
  }
</script>

<div class="cart-shell container mt-3">
  <section class="cart-hero">
    <div>
      <span class="cart-kicker"></span>
      <h1>Carrito.</h1>
      <p>
        Revisa tus articulos, elimina lo que no quieras y pídelo.
      </p>
    </div>

    <div class="cart-hero-metrics">
      <div>
        <span>Articulos</span>
        <strong>{cartItemsCount()}</strong>
      </div>
      <div>
        <span>Total</span>
        <strong>${cartTotal().toFixed(2)}</strong>
      </div>
    </div>
  </section>

  {#if cartStore.error}
    <div class="alert alert-error">{cartStore.error}</div>
  {/if}

  {#if cartStore.checkoutSummary}
    <div class="summary-card">
      <div>
        <span class="cart-kicker">Compra realizada</span>
        <h2>Operacion completada</h2>
        <p>{cartStore.checkoutSummary.message}</p>
      </div>
      <div class="summary-actions">
        <p class="summary-total">Total: ${cartStore.checkoutSummary.total.toFixed(2)}</p>
        <button class="btn btn-secondary" onclick={() => cartStore.clearSummary()}>
          Cerrar resumen
        </button>
      </div>
    </div>
  {/if}

  {#if cartStore.loading && cartStore.items.length === 0}
    <div class="card empty-card">
      <p>Cargando carrito...</p>
    </div>
  {:else if cartStore.items.length === 0}
    <div class="card empty-card">
      <h2>Tu carrito esta vacio</h2>
      <p>Añade productos desde el catalogo para construir tu compra.</p>
    </div>
  {:else}
    <div class="cart-layout">
      <div class="cart-items">
        {#each cartStore.items as item (item.productId?._id || `${item.quantity}-${item.productId?.nombre || 'producto'}`)}
          <article class="cart-item">
            <img
              class="cart-image"
              src={getProductImageUrl(item.productId)}
              alt={item.productId?.nombre || 'Producto'}
            />

            <div class="cart-info">
              <span class="item-label">Articulo</span>
              <h3>{item.productId?.nombre || 'Producto no disponible'}</h3>
              <div class="item-meta">
                <span>Cantidad: {item.quantity}</span>
                <span>Precio unitario: ${item.productId?.precio?.toFixed(2) || '0.00'}</span>
              </div>
            </div>

            <div class="cart-line">
              <p class="line-total">
                ${((item.productId?.precio || 0) * item.quantity).toFixed(2)}
              </p>
              <button
                class="btn btn-error"
                onclick={() => removeItem(item.productId?._id)}
                disabled={cartStore.loading}
              >
                Eliminar
              </button>
            </div>
          </article>
        {/each}
      </div>

      <aside class="cart-summary">
        <span class="cart-kicker">Order summary</span>
        <h2>Tu pedido</h2>
        <div class="summary-row">
          <span>Subtotal</span>
          <strong>${cartTotal().toFixed(2)}</strong>
        </div>
        <div class="summary-row">
          <span>Envio</span>
          <strong>Gratis</strong>
        </div>
        <div class="summary-row total-row">
          <span>Total</span>
          <strong>${cartTotal().toFixed(2)}</strong>
        </div>
        <button class="btn btn-success" onclick={checkout} disabled={cartStore.loading}>
          {cartStore.loading ? 'Procesando...' : 'Simular compra'}
        </button>
      </aside>
    </div>
  {/if}
</div>

<style>
  .cart-shell {
    padding-bottom: 3rem;
  }

  .cart-hero,
  .summary-card,
  .cart-summary,
  .cart-item,
  .empty-card {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(20, 33, 29, 0.08);
    box-shadow: var(--glass-shadow);
    border-radius: 30px;
  }

  .cart-hero {
    display: grid;
    grid-template-columns: 1.8fr 1fr;
    gap: 1rem;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
  }

  .cart-hero p {
    max-width: 60ch;
    margin-top: 1rem;
    color: var(--text-muted);
  }

  .cart-kicker,
  .item-label {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .cart-hero-metrics {
    display: grid;
    gap: 1rem;
  }

  .cart-hero-metrics div {
    padding: 1.25rem;
    border-radius: 22px;
    background: var(--surface-muted);
  }

  .cart-hero-metrics span {
    display: block;
    color: var(--text-muted);
    font-weight: 700;
  }

  .cart-hero-metrics strong {
    display: block;
    margin-top: 0.35rem;
    font-size: 2rem;
    color: var(--primary);
  }

  .summary-card {
    display: flex;
    justify-content: space-between;
    gap: 1.25rem;
    align-items: center;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .summary-card p {
    color: var(--text-muted);
  }

  .summary-actions {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.8rem;
  }

  .cart-layout {
    display: grid;
    grid-template-columns: 1.8fr 0.9fr;
    gap: 1.5rem;
    align-items: start;
  }

  .cart-items {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .cart-item {
    display: grid;
    grid-template-columns: 130px 1fr auto;
    gap: 1rem;
    padding: 1rem;
    align-items: center;
  }

  .cart-image {
    width: 130px;
    height: 130px;
    object-fit: cover;
    border-radius: 22px;
    background: #f1efe8;
  }

  .item-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.9rem;
    margin-top: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
  }

  .cart-line {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.75rem;
  }

  .line-total,
  .summary-total {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.04em;
  }

  .cart-summary {
    padding: 1.5rem;
    position: sticky;
    top: 7rem;
  }

  .summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(20, 33, 29, 0.08);
    color: var(--text-muted);
  }

  .summary-row strong {
    color: var(--secondary);
  }

  .total-row {
    margin-bottom: 1rem;
  }

  .total-row span,
  .total-row strong {
    color: var(--secondary);
    font-size: 1.02rem;
  }

  .empty-card {
    padding: 3rem 1.5rem;
    text-align: center;
  }

  .empty-card p {
    margin-top: 0.75rem;
    color: var(--text-muted);
  }

  @media (max-width: 980px) {
    .cart-hero,
    .cart-layout,
    .summary-card {
      grid-template-columns: 1fr;
      flex-direction: column;
      align-items: stretch;
    }

    .summary-actions {
      align-items: stretch;
    }

    .cart-summary {
      position: static;
    }
  }

  @media (max-width: 640px) {
    .cart-item {
      grid-template-columns: 1fr;
      text-align: left;
    }

    .cart-image {
      width: 100%;
      height: 240px;
    }

    .cart-line {
      align-items: stretch;
    }
  }
</style>
