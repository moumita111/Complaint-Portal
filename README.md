# University Complaint-Portal

## Overview
The **University Complaint-Portal** is a web-based platform designed to streamline the process of lodging, managing, and resolving complaints within a university environment. This system enables students, faculty, and staff to submit complaints and track their status efficiently.

## Features
- **User Authentication**: Secure login and registration for students, faculty, and administrators.
- **Complaint Submission**: Users can file complaints with relevant details and attachments.
- **Complaint Tracking**: Users can track the status of their complaints.
- **Admin Dashboard**: University authorities can view, categorize, and resolve complaints.
- **Notifications**: Email or in-system notifications for status updates.
- **Reports & Analytics**: Insights into complaint trends and resolutions.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: Tailwind CSS, HTML, JavaScript
- **Database**: SQLite/PostgreSQL/MySQL
- **Version Control**: Git & GitHub

## Installation & Setup
### 1. Clone the Repository
```bash
git clone https://github.com/moumita111/Complaint-Portal.git
cd Complaint-Portal
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Tailwind CSS
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

### 4. Configure Tailwind CSS
Edit `tailwind.config.js` to include:
```javascript
module.exports = {
  content: ['./templates/**/*.html', './static/**/*.js'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 5. Configure the Database
```bash
python manage.py migrate
python manage.py makemigrations
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## Usage
- **Students & Faculty**: Register, log in, and submit complaints.
- **Admins**: Log in to manage and resolve complaints.
