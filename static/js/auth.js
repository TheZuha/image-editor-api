const API = 'http://127.0.0.1:8000';
document.getElementById('logoutBtn')?.addEventListener('click', () => {
  localStorage.removeItem('token');
  window.location = 'login.html';
});

// Register
document.getElementById('registerForm')?.addEventListener('submit', async e => {
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

// Login
document.getElementById('loginForm')?.addEventListener('submit', async e => {
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
