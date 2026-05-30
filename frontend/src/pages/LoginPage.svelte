<script>
  import { authStore, notificationStore } from '../stores/store.svelte.js';

  let { navigateTo = () => {} } = $props();
  
  let username = $state('');
  let password = $state('');
  let isLogin = $state(true);
  let errors = $state({
    username: '',
    password: ''
  });

  function validateForm() {
    errors.username = '';
    errors.password = '';
    let isValid = true;

    if (!username.trim()) {
      errors.username = 'El usuario es requerido';
      isValid = false;
    }

    if (!password.trim()) {
      errors.password = 'La contraseña es requerida';
      isValid = false;
    } else if (password.length < 3) {
      errors.password = 'La contraseña debe tener al menos 3 caracteres';
      isValid = false;
    }

    return isValid;
  }

  async function handleSubmit(e) { if (e) e.preventDefault();
    if (!validateForm()) return;

    if (isLogin) {
      const success = await authStore.login(username, password);
      if (success) {
        notificationStore.add('¡Bienvenido!', 'success');
        navigateTo('productos');
      } else {
        notificationStore.add(authStore.error, 'error');
      }
    } else {
      const success = await authStore.register(username, password);
      if (success) {
        notificationStore.add('Registro exitoso. Por favor inicia sesión', 'success');
        isLogin = true;
        username = '';
        password = '';
      } else {
        notificationStore.add(authStore.error, 'error');
      }
    }
  }

  function toggleMode() {
    isLogin = !isLogin;
    authStore.clearError();
    errors = { username: '', password: '' };
  }
</script>

<div class="login-container">
  <div class="login-card">
    <div class="login-header">
      <h1>ItemGo!, tu tienda</h1>
      <p class="subtitle">{isLogin ? 'Inicia sesión en tu cuenta' : 'Crea una nueva cuenta'}</p>
    </div>

    <form onsubmit={handleSubmit}>
      <div class="form-group">
        <label for="username">Usuario</label>
        <input
          id="username"
          type="text"
          placeholder="Ingresa tu usuario"
          bind:value={username}
          disabled={authStore.loading}
          class:error={errors.username}
        />
        {#if errors.username}
          <span class="error-message">{errors.username}</span>
        {/if}
      </div>

      <div class="form-group">
        <label for="password">Contraseña</label>
        <input
          id="password"
          type="password"
          placeholder="Ingresa tu contraseña"
          bind:value={password}
          disabled={authStore.loading}
          class:error={errors.password}
        />
        {#if errors.password}
          <span class="error-message">{errors.password}</span>
        {/if}
      </div>

      {#if authStore.error}
        <div class="alert alert-error">
          {authStore.error}
        </div>
      {/if}

      <button
        type="submit"
        class="btn btn-primary w-full"
        disabled={authStore.loading}
      >
        {#if authStore.loading}
          <span class="spinner"></span>
          {isLogin ? 'Iniciando sesión...' : 'Registrando...'}
        {:else}
          {isLogin ? 'Iniciar sesión' : 'Registrarse'}
        {/if}
      </button>
    </form>

    <div class="toggle-mode">
      <p>
        {isLogin ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?'}
        <button
          type="button"
          class="toggle-btn"
          onclick={toggleMode}
          disabled={authStore.loading}
        >
          {isLogin ? 'Regístrate' : 'Inicia sesión'}
        </button>
      </p>
    </div>

    <div class="demo-info">
      <p><strong>Demo:</strong></p>
      <p>Admin: admin / admin123</p>
      <p>User: user / user123</p>
    </div>
  </div>
</div>

<style>
  .login-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 1rem;
    /* Background is handled globally now */
    background: transparent;
  }

  .login-card {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-filter);
    -webkit-backdrop-filter: var(--glass-filter);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 2.5rem;
    box-shadow: var(--glass-shadow);
    width: 100%;
    max-width: 420px;
  }

  .login-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .login-header h1 {
    margin-bottom: 0.5rem;
    color: var(--primary);
    font-size: 2.25rem;
    font-weight: 700;
  }

  .subtitle {
    color: var(--text-muted);
    font-size: 1rem;
  }

  form {
    margin-bottom: 1.5rem;
  }

  .w-full {
    width: 100%;
  }

  input.error {
    border-color: var(--error);
  }

  .toggle-mode {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--gray);
  }

  .toggle-mode p {
    margin: 0;
  }

  .toggle-btn {
    background: none;
    border: none;
    color: var(--primary);
    cursor: pointer;
    font-weight: 600;
    text-decoration: underline;
    margin-left: 0.5rem;
    transition: var(--transition);
  }

  .toggle-btn:hover:not(:disabled) {
    color: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: none;
  }

  .toggle-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .demo-info {
    background-color: rgba(255, 255, 255, 0.5);
    border: 1px solid var(--glass-border);
    padding: 1rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .demo-info p {
    margin: 0.25rem 0;
  }

  .spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: var(--white);
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  @media (max-width: 480px) {
    .login-card {
      padding: 1.5rem;
    }

    .login-header h1 {
      font-size: 1.5rem;
    }
  }
</style>
