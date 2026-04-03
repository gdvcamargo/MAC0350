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

  const confirmPassword = data.get('confirm_password');

  const errorDiv = document.getElementById('error-message');
  console.log("Payload:", payload, "Confirm Password:", confirmPassword);
  if (payload.password !== confirmPassword) {
    if (errorDiv) {
      errorDiv.textContent = 'As senhas devem ser iguais.';
    }
    return;
  }

  const response = await fetch('/users/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (response.ok) {
    if (errorDiv) {
      errorDiv.textContent = '';
    }
    window.location.href = '/';
    return;
  }

  const errorData = await response.json();
  const errorMessage = Array.isArray(errorData.detail)
    ? (errorData.detail[0]?.msg || 'Erro ao registrar usuário.')
    : (errorData.detail || errorData.message || 'Erro ao registrar usuário.');
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

async function deleteMyAccount(event) {
  if (event) {
    event.preventDefault();
  }

  const shouldDelete = window.confirm('Tem certeza que deseja excluir sua conta? Esta acao nao pode ser desfeita.');
  if (!shouldDelete) {
    return;
  }

  const response = await fetch('/users/me', {
    method: 'DELETE'
  });

  const messageDiv = document.getElementById('profile-message');
  if (response.ok) {
    if (messageDiv) {
      messageDiv.textContent = '';
    }
    window.location.href = '/home';
    return;
  }

  const errorData = await response.json();
  const errorMessage = errorData.detail || errorData.message || 'Nao foi possivel excluir a conta.';
  if (messageDiv) {
    messageDiv.textContent = errorMessage;
  }
}