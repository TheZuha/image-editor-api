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

const imageId = localStorage.getItem('currentImageId');
document.getElementById('imgIdHeading').innerText = imageId;

const form = document.getElementById('transformForm');
form.addEventListener('submit', async e => {
  e.preventDefault();
  const body = { transformations: {} };
  // Resize
  const w = +document.getElementById('resizeWidth').value;
  const h = +document.getElementById('resizeHeight').value;
  if (w && h) body.transformations.resize = { width: w, height: h };
  // Crop
  const cropX = +document.getElementById('cropX').value;
  const cropY = +document.getElementById('cropY').value;
  const cropW = +document.getElementById('cropW').value;
  const cropH = +document.getElementById('cropH').value;
  if (cropW && cropH) body.transformations.crop = { x: cropX||0, y: cropY||0, width: cropW, height: cropH };
  // Rotate
  const rot = +document.getElementById('rotate').value;
  if (rot) body.transformations.rotate = rot;
  // Flip & Mirror
  if (document.getElementById('flip').checked) body.transformations.flip = true;
  if (document.getElementById('mirror').checked) body.transformations.mirror = true;
  // Watermark
  const wmText = document.getElementById('wmText').value;
  const wmX = +document.getElementById('wmX').value;
  const wmY = +document.getElementById('wmY').value;
  if (wmText) body.transformations.watermark = { text: wmText, position: [wmX||10, wmY||10] };
  // Filters
  if (document.getElementById('grayscale').checked)
    body.transformations.filters = { ...(body.transformations.filters||{}), grayscale: true };
  if (document.getElementById('sepia').checked)
    body.transformations.filters = { ...(body.transformations.filters||{}), sepia: true };
  // Format
  const fmt = document.getElementById('format').value;
  if (fmt) body.transformations.format = fmt;
  // Quality
  const quality = +document.getElementById('quality').value;
  if (quality) body.transformations.compress = { quality };

  const res = await fetch(`${API}/images/${imageId}/transform/`, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });
  const alertDiv = document.getElementById('transformAlert');
  if (!res.ok) {
    alertDiv.innerHTML = '<div class="alert alert-danger">Xatolik! Rasmni tahrirlashda muammo yuz berdi.</div>';
    return;
  }
  const data = await res.json();
  const imgEl = document.getElementById('transformedImage');
  imgEl.src = data.original;
  imgEl.classList.remove('d-none');
  alertDiv.innerHTML = '<div class="alert alert-success">Rasm muvaffaqiyatli tahrirlandi!</div>';
});
