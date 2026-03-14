function resetForm() {
    document.getElementById('name').value = '';
    document.getElementById('password').value = '';
    document.getElementById('bio').value = '';
}

async function createUser() {
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    const bio = document.getElementById('bio').value;
    
    const response = await fetch('/sign-up', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, password, bio })
    });
    if (!response.ok) {
        alert('Erro ao criar usuário.');
    }
    resetForm();

    if (response.ok) {
        window.location.href = '/home';
    }
}

async function loginUser() {
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch('/sign-in', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, password })
    });
    if (!response.ok) {
        alert('Erro ao logar usuário.');
    }
    resetForm();

    if (response.ok) {
        window.location.href = '/home';
    }
}