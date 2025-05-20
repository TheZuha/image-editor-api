# 🖼️ Image Editor API

Bu loyiha `Django Rest Framework` yordamida yaratilgan **Rasm tahrirlovchi (Image Editor) API** hisoblanadi. Foydalanuvchilar ro‘yxatdan o‘tib, rasm yuklashi, ko‘rishi, tahrirlashi va rasmga turli effektlar qo‘llashi mumkin.

---

## 📌 Imkoniyatlar

* 📤 Rasm yuklash
* 📁 Rasm ro‘yxatini olish
* 🔍 Bitta rasm tafsilotlarini ko‘rish
* 🛠️ Rasmga transformatsiya: rotate, crop, resize, filter, watermark, format va h.k.
* 🔐 Ro‘yxatdan o‘tish va login qilish (Token authentication)

---

## 📁 API Endpointlar

| Yo‘l (`Endpoint`)  | Method | Tavsifi                                     |
| ------------------ | ------ | ------------------------------------------- |
| `/auth/register/`       | POST   | Ro‘yxatdan o‘tish                           |
| `auth//login/`          | POST   | Login qilish (token olish)                  |
| `/images/`                | POST   | Rasm yuklash                                |
| `/images/list/`           | GET    | Foydalanuvchining barcha rasmlari           |
| `/images/<pk>/`           | GET    | Bitta rasm tafsilotlari                     |
| `/images/<pk>/transform/` | POST   | Rasmga o‘zgartirishlar kiritish (transform) |

---

## 🛠 O‘rnatish va ishga tushirish

```bash
# 1. Repositoriyani yuklab oling
git clone https://github.com/TheZuha/image-editor-api.git
cd image-editor-api

# 2. Virtual muhit yaratish
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Kutubxonalarni o‘rnatish
pip install -r requirements.txt
# yoki
pip install django djangorestframework pillow

# 4. Migratsiyalarni bajarish
python manage.py makemigrations
python manage.py migrate

# 5. Superuser yaratish (ixtiyoriy)
python manage.py createsuperuser

# 6. Serverni ishga tushiring
python manage.py runserver
```

---

## 📬 Qanday foydalaniladi?

### 1. Ro‘yxatdan o‘tish

**POST** `/auth/register/`

```json
{
  "username": "ali123",
  "password": "parol123"
}
```

### 2. Login qilish

**POST** `/auth/login/`

```json
{
  "username": "ali123",
  "password": "parol123"
}
```

**Javob:**

```json
{
  "token": "your_token_here"
}
```

Tokenni boshqa so‘rovlarda `Authorization` sarlavhasida yuboring:

```
Authorization: Token your_token_here
```

---

### 3. Rasm yuklash

**POST** `/images/`

**Header:** `Authorization: Token ...`

**Form-data:**

```
original: [fayl tanlang]
```

---

### 4. Rasm ro‘yxati

**GET** `/images/list/`

**Header:** `Authorization: Token ...`

---

### 5. Rasm tafsiloti

**GET** `/images/<pk>/`

**Header:** `Authorization: Token ...`

---

### 6. Rasmni transformatsiya qilish

**POST** `/images/<pk>/transform/`

**Header:** `Authorization: Token ...`

```json
{
  "transformations": {
    "resize": {"width": 200, "height": 200},
    "crop": {"x": 10, "y": 10, "width": 100, "height": 100},
    "rotate": 90,
    "flip": true,
    "mirror": true,
    "watermark": {
      "text": "My Logo",
      "position": [20, 20]
    },
    "filters": {
      "grayscale": true,
      "sepia": false
    },
    "format": "JPEG",
    "compress": {
      "quality": 80
    }
  }
}
```

---

## 🧾 Texnologiyalar

* Python
* Django
* Django REST Framework
* Pillow (PIL) — Rasmni qayta ishlash uchun

---

## 📁 Papkalar tuzilishi

```
image-editor-api/
├── images/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── users/
│   ├── views.py
│   ├── urls.py
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

## ✅ Eslatma

* Har bir endpoint uchun `Authorization` token kerak.
* Rasm transformatsiyasi JSON formatida yuboriladi.
* Yuklangan rasmlar `originals/` papkaga saqlanadi.

---

## 👤 Muallif

Made with ❤️ by [TheZuha](https://github.com/TheZuha)

---

## 🧾 Litsenziya

Bu loyiha ochiq manba bo‘lib, istalgan maqsadda foydalanish uchun ochiq.
