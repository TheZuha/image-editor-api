const API = 'http://127.0.0.1:8000';
const token = localStorage.getItem('token');
if (!token) window.location = 'login.html';

// Logout universal
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location = 'login.html';
  });
}

async function loadGallery() {
  const res = await fetch(`${API}/images/list/`, {
    headers:{'Authorization': `Bearer ${token}`}
  });
  const imgs = await res.json();
  const row = document.getElementById('galleryRow');
  row.innerHTML = '';
  if (imgs.length === 0) {
    row.innerHTML = `
      <div class="col-12 text-center mt-5">
        <div class="empty-anim mb-3">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-image animate-fade-in">
            <rect x="3" y="3" width="18" height="18" rx="2.5"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </div>
        <div class="alert alert-info shadow-sm d-inline-block animate-fade-in" style="font-size:1.2rem;">Sizning rasmlaringiz yo'q</div>
      </div>
      <style>
        .animate-fade-in { animation: fadeIn 1.2s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(30px);} to { opacity: 1; transform: none; } }
        .empty-anim svg { opacity: 0.5; }
      </style>
    `;
    return;
  }
  imgs.forEach(img => {
    const col = document.createElement('div');
    col.className = 'col-md-4 mb-4';
    col.innerHTML = `
      <div class="card shadow-sm">
        <img src="${img.original}" class="card-img-top">
        <div class="card-body text-center">
          <button class="btn btn-sm btn-outline-primary me-2" onclick="toTransform(${img.id})">
            Transform
          </button>
          <button class="btn btn-sm btn-outline-danger" onclick="deleteImage(${img.id})">
            O‘chirish
          </button>
        </div>
      </div>`;
    row.appendChild(col);
  });
}

window.deleteImage = async function(id) {
  if (!confirm('Rasmni o‘chirishni istaysizmi?')) return;
  const res = await fetch(`${API}/images/${id}/`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (res.ok) {
    loadGallery();
  } else {
    alert('O‘chirishda xatolik!');
  }
}

document.getElementById('uploadForm')?.addEventListener('submit', async e => {
  e.preventDefault();
  const file = document.getElementById('imageFile').files[0];
  const fd = new FormData();
  fd.append('original', file);
  const res = await fetch(`${API}/images/`, {
    method:'POST',
    headers:{'Authorization': `Bearer ${token}`},
    body:fd
  });
  if (res.ok) {
    document.getElementById('uploadAlert').innerHTML = '<div class="alert alert-success">Uploaded</div>';
    loadGallery();
  } else {
    document.getElementById('uploadAlert').innerHTML = '<div class="alert alert-danger">Error</div>';
  }
});

function toTransform(id) {
  localStorage.setItem('currentImageId', id);
  window.location = 'transform.html';
}

// initial load
loadGallery();
