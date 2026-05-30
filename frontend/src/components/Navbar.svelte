<script>
  import { authStore, cartItemsCount } from '../stores/store.svelte.js';

  let {
    currentPage = 'productos',
    navigateTo = () => {},
    onLogout = () => {}
  } = $props();

  function logout() {
    onLogout?.();
  }
</script>

<nav class="navbar">
  <div class="container navbar-shell">
    <div class="brand-block">
      <span class="eyebrow"> Tu tienda preferida</span>
      <button class="brand-button" onclick={() => navigateTo('productos')}>
         ItemGo!
      </button>
    </div>

    <div class="navbar-menu">
      <button
        class="nav-link"
        class:active={currentPage === 'productos'}
        onclick={() => navigateTo('productos')}
      >
        Catalogo
      </button>

      {#if authStore.user?.role === 'admin'}
        <button
          class="nav-link"
          class:active={currentPage === 'admin'}
          onclick={() => navigateTo('admin')}
        >
          Gestion
        </button>
      {/if}

      <button
        class="nav-link"
        class:active={currentPage === 'carrito'}
        onclick={() => navigateTo('carrito')}
      >
        Carrito
        <span class="count-pill">{cartItemsCount()}</span>
      </button>

      <button
        class="nav-link"
        class:active={currentPage === 'perfil'}
        onclick={() => navigateTo('perfil')}
      >
        Perfil
      </button>
    </div>

    <div class="navbar-user">
      <div class="user-summary">
        <span class="user-label">Cuenta activa</span>
        <span class="user-name">{authStore.user?.username}</span>
      </div>
      {#if authStore.user?.role === 'admin'}
        <span class="badge badge-admin">Admin</span>
      {/if}
      <button class="btn btn-secondary nav-logout" onclick={logout}>
        Cerrar sesion
      </button>
    </div>
  </div>
</nav>

<style>
  .navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 1rem 0 0;
  }

  .navbar-shell {
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 1rem;
    align-items: center;
    padding: 1rem 1.25rem;
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(22px);
    border: 1px solid rgba(20, 33, 29, 0.08);
    border-radius: 999px;
    box-shadow: 0 18px 50px rgba(17, 24, 39, 0.08);
    margin-top: 1rem;
  }

  .brand-block {
    display: flex;
    flex-direction: column;
    min-width: 180px;
  }

  .eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.2rem;
    font-weight: 800;
  }

  .brand-button {
    width: fit-content;
    background: none;
    border: none;
    padding: 0;
    color: var(--secondary);
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.85rem;
    box-shadow: none;
  }

  .navbar-menu {
    display: flex;
    justify-content: center;
    gap: 0.65rem;
    flex-wrap: wrap;
  }

  .nav-link {
    background: rgba(255, 255, 255, 0.72);
    color: var(--text-main);
    border: 1px solid rgba(20, 33, 29, 0.08);
    min-width: 118px;
  }

  .nav-link:hover {
    background: var(--white);
    border-color: rgba(20, 33, 29, 0.15);
  }

  .nav-link.active {
    background: var(--primary);
    color: var(--white);
  }

  .count-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.5rem;
    height: 1.5rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.22);
    font-size: 0.78rem;
    padding: 0 0.38rem;
  }

  .navbar-user {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    justify-content: flex-end;
  }

  .user-summary {
    display: flex;
    flex-direction: column;
    text-align: right;
  }

  .user-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 800;
  }

  .user-name {
    font-weight: 700;
    color: var(--secondary);
  }

  .badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.4rem 0.75rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .badge-admin {
    background: rgba(201, 165, 106, 0.22);
    color: #8a6329;
  }

  .nav-logout {
    min-width: 138px;
  }

  @media (max-width: 1024px) {
    .navbar-shell {
      grid-template-columns: 1fr;
      border-radius: 28px;
    }

    .brand-block,
    .user-summary {
      text-align: center;
      align-items: center;
    }

    .navbar-user {
      justify-content: center;
      flex-wrap: wrap;
    }
  }
</style>
