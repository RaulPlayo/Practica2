<script>
  import { notificationStore } from '../stores/store.svelte.js';

  let { message = '', type = 'info', id } = $props();

  function close() {
    notificationStore.remove(id);
  }
</script>

<div class={`notification notification-${type}`}>
  <div class="notification-content">
    <span class="notification-message">{message}</span>
    <button class="notification-close" onclick={close}>✕</button>
  </div>
</div>

<style>
  .notification {
    padding: 1rem;
    border-radius: var(--border-radius);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    min-width: 250px;
    max-width: 400px;
    animation: slideInRight 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .notification-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .notification-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .notification-info {
    background-color: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
  }

  .notification-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
  }

  .notification-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 1rem;
  }

  .notification-close {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    opacity: 0.7;
    transition: opacity 0.2s;
  }

  .notification-close:hover {
    opacity: 1;
  }

  @media (max-width: 768px) {
    .notification {
      min-width: auto;
      max-width: none;
    }
  }
</style>
