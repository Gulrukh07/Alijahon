🛍️ Alijahon – E-Commerce Platform
Alijahon — bu zamonaviy va kengaytiriladigan e-commerce veb ilovasi bo‘lib, foydalanuvchilar, adminlar, operatorlar va yetkazib beruvchilar uchun turli rollarni qo‘llab-quvvatlaydi. Ilova Django asosida qurilgan va zamonaviy backend arxitektura amaliyotlarini o‘zida mujassam etgan.

🎯 Maqsad
Foydalanuvchilarga mahsulotlarni ko‘rish, xarid qilish, o‘z mahsulotlarini sotuvga qo‘yish, sevimli mahsulotlarni belgilash va buyurtmalar tarixini ko‘rish imkonini beruvchi ko‘p tilli e-commerce platformani yaratish.

🧱 Arxitektura
📁 Loyihaning asosiy modullari:

auth/ – Login & registratsiya (telefon, Google, Telegram orqali)

products/ – Mahsulotlar bilan ishlash, filtering, favorites

orders/ – Buyurtmalar va tarix

dashboard/ – Admin, operator, yetkazib beruvchi panellari

stats/ – Foydalanuvchi va tizim statistikasi

giveaway/ – Sovrinli o‘yin moduli

multilang/ – UZ, RU, EN tillarni qo‘llab-quvvatlash

🚀 Ishlatilgan texnologiyalar
Texnologiya	Maqsadi
Django	Asosiy backend framework
PostgreSQL	Ma’lumotlar bazasi
Docker + Compose	Konteynerlash va orchestration
HTML/CSS/JS	Frontend interfeys
Telegram Bot API	Telegram orqali login imkoniyati
Google OAuth	Google orqali autentifikatsiya
Django Admin	Admin panel

⚙️ Ishga tushirish
Talablar:

Docker & Docker Compose

.env fayl sozlamalari

Ishga tushirish:

bash
Copy
Edit
cp .env.example .env
docker-compose up --build

✨ Qo‘shimcha imkoniyatlar

Buyurtmalar tarixi

Giveaway moduli

Statistik analiz

3 tilda interfeys (UZ, RU, EN)

🤝 Hissa qo‘shish
Pull requestlar va issue'lar orqali loyihani rivojlantirishda qatnashing.

Made with ❤️ by Gulrukh Khayrullaeva


---English
🛍️ Alijahon – E-Commerce Platform
Alijahon is a modern, scalable e-commerce web application built with Django. It supports various user roles such as customers, admins, operators, and delivery staff. The project demonstrates best practices in backend architecture, multilingual support, and user interaction.

🎯 Goal
To build a multilingual e-commerce platform where users can browse and purchase products, manage their favorites and orders, create product listings, and access role-specific dashboards.

🧱 Architecture
📁 Main Modules:

auth/ – Authentication via phone number, Google, and Telegram

products/ – Product management, filtering, and favorites

orders/ – Order tracking and history

dashboard/ – Admin, operator, and delivery panels

stats/ – System and user analytics

giveaway/ – Giveaway module

multilang/ – Language switch (UZ, RU, EN)

🚀 Technologies Used
Technology	Purpose
Django	Web framework
PostgreSQL	Database
Docker + Compose	Containerization & orchestration
HTML/CSS/JavaScript	Frontend UI
Telegram Bot API	Telegram authentication
Google OAuth	Google login support
Django Admin	Built-in admin interface

⚙️ Getting Started
Requirements:

Docker & Docker Compose

Properly configured .env file

Run the project:

bash
Copy
Edit
cp .env.example .env
docker-compose up --build

✨ Future Improvements

Order logging and history

Admin interface enhancements

Giveaway module

Language toggle (Uzbek 🇺🇿, Russian 🇷🇺, English 🇬🇧)

🤝 Contributions
You are welcome to contribute via pull requests or by opening issues.

Made with ❤️ by Gulrukh Khayrullaeva