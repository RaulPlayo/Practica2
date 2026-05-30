<script>
  import { authStore, cartStore, notificationStore, initializeApp } from './stores/store.svelte.js';
  import './styles/global.css';

  import Navbar from './components/Navbar.svelte';
  import Notification from './components/Notification.svelte';
  import LoginPage from './pages/LoginPage.svelte';
  import ProductsPage from './pages/ProductsPage.svelte';
  import AdminPage from './pages/AdminPage.svelte';
  import ProfilePage from './pages/ProfilePage.svelte';
  import CartPage from './pages/CartPage.svelte';

  let currentPage = $state('login');

  $effect(() => {
    initializeApp();
  });

  $effect(() => {
    if (!authStore.isAuthenticated && currentPage !== 'login') {
      currentPage = 'login';
    }
  });

  $effect(() => {
    if (authStore.isAuthenticated && currentPage === 'login') {
      currentPage = 'productos';
    }
  });

  $effect(() => {
    if (authStore.isAuthenticated) {
      cartStore.fetchCart();
    }
  });

  function navigateTo(page) {
    if (!authStore.isAuthenticated && page !== 'login') {
      notificationStore.add('Debe iniciar sesión primero', 'error');
      return;
    }
    currentPage = page;
  }

  function handleLogout() {
    authStore.logout();
    cartStore.clear();
    currentPage = 'login';
    notificationStore.add('Sesión cerrada', 'success');
  }
</script>

<div class="app">
  {#if authStore.isAuthenticated}
    <Navbar {currentPage} {navigateTo} onLogout={handleLogout} />
  {/if}

  <main>
    {#if currentPage === 'login' && !authStore.isAuthenticated}
      <LoginPage {navigateTo} />
    {:else if currentPage === 'productos'}
      <ProductsPage />
    {:else if currentPage === 'admin' && authStore.user?.role === 'admin'}
      <AdminPage />
    {:else if currentPage === 'perfil'}
      <ProfilePage />
    {:else if currentPage === 'carrito'}
      <CartPage />
    {:else if !authStore.isAuthenticated}
      <LoginPage {navigateTo} />
    {/if}
  </main>

  <div class="notifications">
    {#each notificationStore.messages as notification (notification.id)}
      <Notification message={notification.message} type={notification.type} id={notification.id} />
    {/each}
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    position: relative;
    z-index: 1;
  }

  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .notifications {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  @media (max-width: 768px) {
    .notifications {
      bottom: 0.5rem;
      right: 0.5rem;
      left: 0.5rem;
      width: auto;
    }
  }
</style>
