async function registerUser(event) {
  if (event) {
    event.preventDefault();
  }

  const form = document.getElementById('register-form');
  const data = new FormData(form);

  const payload = {
    name: data.get('name'),
    username: data.get('username'),
    username_display: data.get('username'),
    password: data.get('password')
  };

  const response = await fetch('/users/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const errorDiv = document.getElementById('error-message');

  if (response.ok) {
    if (errorDiv) {
      errorDiv.textContent = '';
    }
    window.location.href = '/';
    return;
  }

  const errorData = await response.json();
  const errorMessage = errorData.detail || 'Erro ao registrar usuário.';
  if (errorDiv) {
    errorDiv.textContent = errorMessage;
  }
}

async function loginUser(event) {
  if (event) {
    event.preventDefault();
  }

  const form = document.getElementById('login-form');
  const messageDiv = document.getElementById('login-message');
  if (!form) {
    return;
  }

  const data = new FormData(form);
  const payload = {
    username: data.get('username'),
    password: data.get('password')
  };

  const response = await fetch('/users/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (response.ok) {
    if (messageDiv) {
      messageDiv.textContent = '';
    }
    window.location.href = '/home';
    return;
  }

  const errorData = await response.json();
  const errorMessage = errorData.detail || errorData.message || 'Credenciais inválidas.';
  if (messageDiv) {
    messageDiv.textContent = errorMessage;
  }
}