document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('email').value;
    const password = document.getElementById('senha').value;
    const errorElement = document.getElementById('errorMessage');

    try {
      const response = await fetch('http://localhost:3002/auth/login', {// URL do backend temporário
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password})
      });

      if (!response.ok) {
        const data = await response.json();
        errorElement.textContent = data.message || 'Erro ao fazer login';
        return;
      }

      const data = await response.json();
      localStorage.setItem('token', data.token); // Salva o token

      window.location.href = '/home.html'; // Redireciona
    } catch (error) {
      console.error('Erro de requisição:', error);
      errorElement.textContent = 'Erro ao conectar com o servidor';
    }
  });