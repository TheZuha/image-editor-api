const API = 'http://127.0.0.1:8000';
const token = localStorage.getItem('token');
if (!token) window.location = 'login.html';

async function loadGallery() {
  const res = await fetch(`${API}/images/list/`, {
    headers:{'Authorization': `Bearer ${token}`}
  });
  const imgs = await res.json();
  const row = document.getElementById('galleryRow');
  row.innerHTML = '';
  imgs.forEach(img => {
    const col = document.createElement('div');
    col.className = 'col-md-4 mb-4';
    col.innerHTML = `
      <div class="card shadow-sm">
        <img src="${img.original}" class="card-img-top">
        <div class="card-body text-center">
          <button class="btn btn-sm btn-outline-primary" onclick="toTransform(${img.id})">
            Transform
          </button>
        </div>
      </div>`;
    row.appendChild(col);
  });
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
