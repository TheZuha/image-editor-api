const API = 'http://127.0.0.1:8000';
const token = localStorage.getItem('token');
if (!token) window.location = 'login.html';

const imageId = localStorage.getItem('currentImageId');
document.getElementById('imgIdHeading').innerText = imageId;

document.getElementById('transformForm').addEventListener('submit', async e => {
  e.preventDefault();
  // Собираем JSON
  const body = { transformations: {} };
  const w = +document.getElementById('resizeWidth').value;
  const h = +document.getElementById('resizeHeight').value;
  if (w && h) body.transformations.resize = { width: w, height: h };
  const rot = +document.getElementById('rotate').value;
  if (rot) body.transformations.rotate = rot;
  if (document.getElementById('grayscale').checked)
    body.transformations.filters = { ...(body.transformations.filters||{}), grayscale: true };
  if (document.getElementById('sepia').checked)
    body.transformations.filters = { ...(body.transformations.filters||{}), sepia: true };

  const res = await fetch(`${API}/images/${imageId}/transform/`, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) return alert('Error transforming');
  const data = await res.json();
  const imgEl = document.getElementById('transformedImage');
  imgEl.src = data.original;
  imgEl.style.display = 'block';
});
