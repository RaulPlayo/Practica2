<script>
  import { onMount } from 'svelte';
  import { authStore, productStore, userStore, notificationStore } from '../stores/store.svelte.js';

  let showDeleteConfirm = $state(null);

  onMount(() => {
    userStore.fetchUsers();
    productStore.fetchProducts();
  });

  let stats = $derived({
    totalProducts: productStore.products.length,
    totalUsers: userStore.users.length,
    totalAdmins: userStore.users.filter(u => u.role === 'admin').length
  });

  async function toggleUserRole(userId, currentRole) {
    const newRole = currentRole === 'admin' ? 'usuario' : 'admin';
    
    try {
      const response = await fetch(`http://localhost:3000/api/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify({ role: newRole })
      });

      if (!response.ok) throw new Error('Error al actualizar rol');
      
      // Update local state
      const user = userStore.users.find(u => u._id === userId);
      if (user) user.role = newRole;
      
      notificationStore.add('Rol actualizado', 'success');
    } catch (err) {
      notificationStore.add(err.message, 'error');
    }
  }

  async function deleteUser(userId) {
    try {
      const response = await fetch(`http://localhost:3000/api/users/${userId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      });

      if (!response.ok) throw new Error('Error al eliminar usuario');
      
      userStore.users = userStore.users.filter(u => u._id !== userId);
      notificationStore.add('Usuario eliminado', 'success');
      showDeleteConfirm = null;
    } catch (err) {
      notificationStore.add(err.message, 'error');
    }
  }
</script>

<div class="container mt-3">
  <div class="admin-header">
    <h1>Panel de Administración</h1>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <h3>Productos Totales</h3>
      <p class="stat-number">{stats.totalProducts}</p>
    </div>
    <div class="stat-card">
      <h3>Usuarios Totales</h3>
      <p class="stat-number">{stats.totalUsers}</p>
    </div>
    <div class="stat-card">
      <h3>Administradores</h3>
      <p class="stat-number">{stats.totalAdmins}</p>
    </div>
  </div>

  <div class="admin-section">
    <h2>Gestión de Usuarios</h2>
    
    {#if userStore.loading}
      <div>Cargando...</div>
    {:else if userStore.error}
      <div class="alert alert-error">{userStore.error}</div>
    {:else}
      <div class="table-responsive">
        <table class="users-table">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Rol</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each userStore.users as user (user._id)}
              <tr>
                <td>{user.username}</td>
                <td>
                  <span class="badge" class:badge-admin={user.role === 'admin'}>
                    {user.role}
                  </span>
                </td>
                <td>
                  <button
                    class="btn btn-secondary btn-small"
                    onclick={() => toggleUserRole(user._id, user.role)}
                  >
                    Cambiar rol
                  </button>
                  
                  {#if user._id !== authStore.user?.id}
                    <button
                      class="btn btn-error btn-small"
                      onclick={() => (showDeleteConfirm = user._id)}
                    >
                      Eliminar
                    </button>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>

  <div class="admin-section">
    <h2>Productos del Sistema</h2>
    
    {#if productStore.loading}
      <div>Cargando...</div>
    {:else}
      <p>Total: {productStore.products.length} productos</p>
    {/if}
  </div>
</div>

{#if showDeleteConfirm}
  <div class="confirm-dialog-overlay" onclick={() => (showDeleteConfirm = null)}>
    <div class="confirm-dialog" onclick={(e) => e.stopPropagation()}>
      <h3>Confirmar eliminación</h3>
      <p>¿Estás seguro de que deseas eliminar este usuario?</p>
      <div class="dialog-actions">
        <button
          class="btn btn-error"
          onclick={() => deleteUser(showDeleteConfirm)}
        >
          Eliminar
        </button>
        <button
          class="btn btn-secondary"
          onclick={() => (showDeleteConfirm = null)}
        >
          Cancelar
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .admin-header {
    margin-bottom: 2rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .stat-card {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-filter);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    box-shadow: var(--glass-shadow);
    text-align: center;
  }

  .stat-card h3 {
    margin: 0 0 0.5rem 0;
    color: var(--dark-gray);
    font-size: 0.95rem;
  }

  .stat-number {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary);
  }

  .admin-section {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-filter);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--glass-shadow);
  }

  .admin-section h2 {
    margin-top: 0;
    margin-bottom: 1.5rem;
  }

  .table-responsive {
    overflow-x: auto;
  }

  .users-table {
    width: 100%;
    border-collapse: collapse;
  }

  .users-table thead {
    background-color: var(--light-gray);
  }

  .users-table th,
  .users-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--gray);
  }

  .users-table th {
    font-weight: 600;
    color: var(--secondary);
  }

  .users-table tbody tr:hover {
    background-color: var(--light-gray);
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    background-color: #e3e3e3;
    color: var(--secondary);
  }

  .badge-admin {
    background-color: var(--primary);
    color: var(--white);
  }

  .btn-small {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
    margin-right: 0.5rem;
  }

  .confirm-dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .confirm-dialog {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-filter);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 2.5rem;
    max-width: 400px;
    width: 100%;
    box-shadow: var(--glass-shadow);
  }

  .confirm-dialog h3 {
    margin-top: 0;
  }

  .dialog-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .dialog-actions button {
    flex: 1;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  @media (max-width: 768px) {
    .stats-grid {
      grid-template-columns: 1fr;
    }

    .users-table {
      font-size: 0.9rem;
    }

    .users-table th,
    .users-table td {
      padding: 0.5rem;
    }
  }
</style>
