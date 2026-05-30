<script>
  import { getProductImageUrl, productStore, notificationStore } from '../stores/store.svelte.js';

  let {
    product = null,
    onSave = () => {},
    onCancel = () => {}
  } = $props();

  let nombre = $state(product?.nombre || '');
  let precio = $state(product?.precio || '');
  let estado = $state(product?.estado || 'activo');
  let imagen = $state(null);
  let imagePreview = $state(product?.imagen ? getProductImageUrl(product) : null);
  let loading = $state(false);
  let errors = $state({
    nombre: '',
    precio: ''
  });

  $effect(() => {
    nombre = product?.nombre || '';
    precio = product?.precio || '';
    estado = product?.estado || 'activo';
    imagen = null;
    imagePreview = product?.imagen ? getProductImageUrl(product) : null;
  });

  function validateForm() {
    errors.nombre = '';
    errors.precio = '';
    let isValid = true;

    if (!nombre.trim()) {
      errors.nombre = 'El nombre es requerido';
      isValid = false;
    }

    if (!precio || precio <= 0) {
      errors.precio = 'El precio debe ser mayor a 0';
      isValid = false;
    }

    return isValid;
  }

  function handleImageChange(e) {
    const file = e.target.files?.[0];
    if (file) {
      imagen = file;
      const reader = new FileReader();
      reader.onload = (event) => {
        imagePreview = event.target?.result;
      };
      reader.readAsDataURL(file);
    }
  }

  async function handleSubmit(e) { if (e) e.preventDefault();
    if (!validateForm()) return;

    loading = true;
    try {
      const formData = new FormData();
      formData.append('nombre', nombre);
      formData.append('precio', parseFloat(precio));
      formData.append('estado', estado);
      if (imagen) {
        formData.append('imagen', imagen);
      }

      const success = product
        ? await productStore.updateProduct(product._id, formData)
        : await productStore.createProduct(formData);

      if (success) {
        notificationStore.add(
          product ? 'Producto actualizado' : 'Producto creado',
          'success'
        );
        onSave();
      } else {
        notificationStore.add(
          productStore.error || (product ? 'Error al actualizar' : 'Error al crear'),
          'error'
        );
      }
    } finally {
      loading = false;
    }
  }
</script>

<div class="form-overlay" onclick={onCancel}>
  <div class="form-modal" onclick={(e) => e.stopPropagation()}>
    <h2>{product ? 'Editar Producto' : 'Nuevo Producto'}</h2>

    <form onsubmit={handleSubmit}>
      <div class="form-group">
        <label for="nombre">Nombre</label>
        <input
          id="nombre"
          type="text"
          placeholder="Nombre del producto"
          bind:value={nombre}
          disabled={loading}
          class:error={errors.nombre}
        />
        {#if errors.nombre}
          <span class="error-message">{errors.nombre}</span>
        {/if}
      </div>

      <div class="form-group">
        <label for="precio">Precio</label>
        <input
          id="precio"
          type="number"
          placeholder="0.00"
          bind:value={precio}
          step="0.01"
          min="0"
          disabled={loading}
          class:error={errors.precio}
        />
        {#if errors.precio}
          <span class="error-message">{errors.precio}</span>
        {/if}
      </div>

      <div class="form-group">
        <label for="estado">Estado</label>
        <select
          id="estado"
          bind:value={estado}
          disabled={loading}
        >
          <option value="activo">Activo</option>
          <option value="inactivo">Inactivo</option>
        </select>
      </div>

      <div class="form-group">
        <label for="imagen">Imagen {product ? '(opcional para reemplazar)' : ''}</label>
        <input
          id="imagen"
          type="file"
          accept="image/*"
          onchange={handleImageChange}
          disabled={loading}
        />
      </div>

      {#if imagePreview}
        <div class="image-preview">
          <img src={imagePreview} alt="Preview" />
        </div>
      {/if}

      {#if productStore.error}
        <div class="alert alert-error">
          {productStore.error}
        </div>
      {/if}

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" disabled={loading}>
          {loading ? 'Guardando...' : (product ? 'Actualizar' : 'Crear')}
        </button>
        <button type="button" class="btn btn-secondary" onclick={onCancel} disabled={loading}>
          Cancelar
        </button>
      </div>
    </form>
  </div>
</div>

<style>
  .form-overlay {
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
    padding: 1rem;
  }

  .form-modal {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-filter);
    -webkit-backdrop-filter: var(--glass-filter);
    border: 1px solid var(--glass-border);
    box-shadow: var(--glass-shadow);
    border-radius: var(--border-radius);
    padding: 2.5rem;
    max-width: 500px;
    width: 100%;
    animation: slideUp 0.3s ease;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(50px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .form-modal h2 {
    margin-top: 0;
  }

  .image-preview {
    margin-bottom: 1rem;
    border-radius: var(--border-radius);
    overflow: hidden;
    max-height: 200px;
  }

  .image-preview img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .form-actions button {
    flex: 1;
  }

  input.error {
    border-color: var(--error);
  }

  @media (max-width: 480px) {
    .form-modal {
      padding: 1.5rem;
    }

    .form-actions {
      flex-direction: column;
    }
  }
</style>
