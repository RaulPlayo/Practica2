<script>
  import { authStore, cartItemsCount, productStore, notificationStore } from '../stores/store.svelte.js';

  import ProductCard from '../components/ProductCard.svelte';
  import ProductForm from '../components/ProductForm.svelte';
  import ProductDetail from '../components/ProductDetail.svelte';

  let showForm = $state(false);
  let selectedProduct = $state(null);
  let searchQuery = $state('');
  let filteredList = $derived(
    !productStore.filter?.toLowerCase()
      ? productStore.products
      : productStore.products.filter((product) =>
          product?.nombre?.toLowerCase().includes(productStore.filter.toLowerCase())
        )
  );

  $effect(() => {
    productStore.fetchProducts(searchQuery);
  });

  function handleCreateProduct() {
    selectedProduct = null;
    showForm = false;
    notificationStore.add('Producto creado exitosamente', 'success');
  }

  function handleUpdateProduct() {
    selectedProduct = null;
    showForm = false;
    notificationStore.add('Producto actualizado exitosamente', 'success');
  }

  function handleDeleteProduct() {
    selectedProduct = null;
    notificationStore.add('Producto eliminado exitosamente', 'success');
  }

  function openProductForm(product = null) {
    selectedProduct = product;
    showForm = true;
  }

  function closeProductForm() {
    showForm = false;
    selectedProduct = null;
  }

  function selectProduct(product) {
    selectedProduct = product;
  }

  function deselectProduct() {
    selectedProduct = null;
  }
</script>

<div class="catalog-shell container mt-3">
  {#if selectedProduct && !showForm}
    <ProductDetail product={selectedProduct} onClose={deselectProduct} />
  {/if}

  {#if showForm}
    <ProductForm product={selectedProduct} onSave={selectedProduct ? handleUpdateProduct : handleCreateProduct} onCancel={closeProductForm} />
  {/if}

  {#if !selectedProduct && !showForm}
    <section class="hero-panel">
      <div class="hero-copy">
        <span class="hero-kicker"></span>
        <h1>Una tienda hecha para tí.</h1>
        <p>
          Explora todos los objetos que poseemos. ¡Desde ropa hasta colonias!
        </p>
      </div>

      <div class="hero-aside">
        <div class="metric-card">
          <span class="metric-label">Productos visibles</span>
          <strong>{filteredList.length}</strong>
        </div>
        <div class="metric-card">
          <span class="metric-label">En carrito</span>
          <strong>{cartItemsCount()}</strong>
        </div>
        {#if authStore.user?.role === 'admin'}
          <button
            class="btn btn-primary hero-button"
            onclick={() => openProductForm()}
            disabled={productStore.loading}
          >
            Crear nuevo producto
          </button>
        {/if}
      </div>
    </section>

    <section class="toolbar card">
      <div class="toolbar-copy">
        <span class="toolbar-label">Catalogo</span>
        <h2>Secciones destacadas</h2>
        <p>Busca, compara y abre cada ficha de producto para saber más del producto.</p>
      </div>

      <div class="toolbar-actions">
        <div class="search-bar">
          <label for="product-search">Buscar producto</label>
          <input
            id="product-search"
            type="text"
            placeholder="Ej. sudaderas, colonias, camisetas..."
            bind:value={searchQuery}
            class="search-input"
          />
        </div>

        <div class="cart-status">
          <span>Compra actual</span>
          <strong>{cartItemsCount()} articulo(s)</strong>
        </div>
      </div>
    </section>

    {#if productStore.error}
      <div class="alert alert-error">
        {productStore.error}
      </div>
    {/if}

    {#if productStore.loading}
      <div class="grid grid-3">
        {#each Array(6) as _}
          <div class="product-skeleton"></div>
        {/each}
      </div>
    {:else if filteredList.length === 0}
      <div class="empty-state card">
        <h2>No hemos encontrado resultados</h2>
        <p>
          {#if searchQuery}
            Prueba con otro termino de busqueda o revisa el nombre del producto.
          {:else}
            Aun no hay productos disponibles en el catalogo.
          {/if}
        </p>
      </div>
    {:else}
      <section class="products-grid">
        {#each filteredList as product (product._id)}
          <ProductCard
            {product}
            onSelect={() => selectProduct(product)}
            onEdit={() => openProductForm(product)}
            onDelete={() => handleDeleteProduct()}
          />
        {/each}
      </section>
    {/if}
  {/if}
</div>

<style>
  .catalog-shell {
    padding-bottom: 3rem;
  }

  .hero-panel {
    display: grid;
    grid-template-columns: 2.2fr 1fr;
    gap: 1.5rem;
    align-items: stretch;
    margin-bottom: 1.5rem;
  }

  .hero-copy,
  .hero-aside,
  .metric-card {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(20, 33, 29, 0.08);
    box-shadow: var(--glass-shadow);
  }

  .hero-copy {
    border-radius: 34px;
    padding: 2rem;
  }

  .hero-copy p {
    max-width: 54ch;
    margin-top: 1rem;
    color: var(--text-muted);
    font-size: 1.02rem;
  }

  .hero-kicker,
  .toolbar-label,
  .metric-label {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .hero-aside {
    border-radius: 34px;
    padding: 1rem;
    display: grid;
    gap: 1rem;
    align-content: start;
  }

  .metric-card {
    border-radius: 24px;
    padding: 1.2rem 1.25rem;
  }

  .metric-card strong {
    display: block;
    margin-top: 0.55rem;
    font-size: 2.1rem;
    color: var(--primary);
  }

  .hero-button {
    margin-top: auto;
  }

  .toolbar {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 1.25rem;
    margin-bottom: 1.75rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.78);
  }

  .toolbar-copy p {
    margin-top: 0.75rem;
    color: var(--text-muted);
  }

  .toolbar-actions {
    display: grid;
    gap: 1rem;
    align-content: center;
  }

  .search-bar label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--secondary);
  }

  .cart-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.15rem;
    border-radius: 20px;
    background: var(--surface-muted);
    border: 1px solid rgba(20, 33, 29, 0.08);
  }

  .cart-status span {
    color: var(--text-muted);
    font-weight: 600;
  }

  .cart-status strong {
    color: var(--secondary);
    font-size: 1.05rem;
  }

  .product-skeleton {
    height: 390px;
    border-radius: 28px;
    background:
      linear-gradient(110deg, rgba(255, 255, 255, 0.8) 8%, rgba(243, 243, 243, 0.95) 18%, rgba(255, 255, 255, 0.8) 33%),
      #f6f6f6;
    background-size: 200% 100%;
    animation: shimmer 1.2s linear infinite;
    border: 1px solid rgba(20, 33, 29, 0.08);
  }

  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.4rem;
  }

  .empty-state {
    padding: 3rem 1.5rem;
    text-align: center;
    background: rgba(255, 255, 255, 0.8);
  }

  .empty-state p {
    margin-top: 0.75rem;
    color: var(--text-muted);
  }

  @keyframes shimmer {
    to {
      background-position: -200% 0;
    }
  }

  @media (max-width: 900px) {
    .hero-panel,
    .toolbar {
      grid-template-columns: 1fr;
    }
  }
</style>
