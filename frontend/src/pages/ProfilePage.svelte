<script>
  import { authStore } from '../stores/store.svelte.js';

</script>

<div class="container mt-3">
  <div class="profile-header">
    <h1>Mi Perfil</h1>
  </div>

  <div class="profile-card card">
    <h2>Información de la cuenta</h2>
    
    <div class="profile-info">
      <div class="info-row">
        <label>Usuario:</label>
        <span>{authStore.user?.username}</span>
      </div>
      
      <div class="info-row">
        <label>Rol:</label>
        <span>
          {authStore.user?.role === 'admin' ? 'Administrador' : 'Usuario'}
        </span>
      </div>

      <div class="info-row">
        <label>ID:</label>
        <span class="user-id">{authStore.user?.id}</span>
      </div>
    </div>
  </div>
</div>

<style>
  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .profile-header {
    margin-bottom: 2rem;
  }

  .profile-card {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-filter);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 2.5rem;
    box-shadow: var(--glass-shadow);
  }

  .profile-card h2 {
    margin-top: 0;
    margin-bottom: 1.5rem;
  }

  .profile-info {
    margin-bottom: 1.5rem;
  }

  .info-row {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--gray);
  }

  .info-row label {
    font-weight: 600;
    color: var(--secondary);
  }

  .info-row span {
    color: var(--dark-gray);
  }

  .user-id {
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    word-break: break-all;
  }

  @media (max-width: 480px) {
    .profile-card {
      padding: 1.5rem;
    }

    .info-row {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
</style>
