🚍 QuickPass
QuickPass is a Django-based web application designed to simplify the process of applying, renewing, and managing student bus passes. It offers an easy-to-use interface for students and a dedicated admin dashboard for clerks to verify and approve passes.

✨ Features
User Authentication – Student registration and login system

Dynamic Pricing – Select town and view bus pass price automatically

QR Code Payment – Integrated QR code for seamless UPI payments

PDF Pass Generation – Download monthly bus passes with details & photo

Clerk/Admin Dashboard – Search students, verify payments, and renew passes

🛠️ Tech Stack
Backend: Python, Django

Frontend: HTML5, CSS3, JavaScript, Bootstrap

Database: SQLite (default, can be switched to MySQL/PostgreSQL)

Others: Pillow (image handling), ReportLab (PDF generation)

📦 Installation & Setup
Follow these steps to run QuickPass locally:

Clone the repository


git clone https://github.com/sarthak-4488/quickpass.git
cd quickpass
Create and activate a virtual environment

Windows (PowerShell):


python -m venv env
.\env\Scripts\activate
macOS/Linux:

python3 -m venv env
source env/bin/activate
Install dependencies


pip install -r requirements.txt
Apply database migrations


python manage.py migrate
Run the development server


python manage.py runserver
Open in browser


http://127.0.0.1:8000/
📖 Usage
Students:

Register with your name, course, academic year, and photo.

Select your town to see the bus pass price.

Pay via the QR code displayed.

Download your monthly bus pass as a PDF after payment confirmation.

Clerks/Admins:

Log in to view student details.

Verify payment and manually renew passes if needed.

📷 Screenshots
(Add screenshots here to make it more visual)

📜 License
This project is licensed under the MIT License – feel free to use and modify.

📬 Contact
Author: Sarthak Revansiddha Chikhale

GitHub: sarthak-4488

Email: sarthakchikhale4488@gmail.com
