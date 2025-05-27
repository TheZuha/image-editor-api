const API = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('token');
      window.location = 'login.html';
    });
  }

  // Register
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async e => {
      e.preventDefault();
      const u = document.getElementById('username').value;
      const p = document.getElementById('password').value;
      const res = await fetch(`${API}/auth/register/`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({username:u,password:p})
      });
      if (res.ok) window.location='login.html';
      else alert('Ошибка регистрации');
    });
  }

  // Login
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const u = document.getElementById('username').value;
      const p = document.getElementById('password').value;
      const res = await fetch(`${API}/auth/login/`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({username:u,password:p})
      });
      if (!res.ok) return alert('Неверные данные');
      const data = await res.json();
      localStorage.setItem('token', data.access);
      window.location = 'gallery.html';
    });
  }
});
