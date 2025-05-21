


This is the **backend** of a full-stack authentication system, built using **Django REST Framework** and **MongoDB** (via `pymongo`).
---

## ⚙️ Tech Stack

- Python 3.x
- Django + Django REST Framework
- JWT Authentication (`djangorestframework-simplejwt`)
- MongoDB (native, via `pymongo`)
- Custom user model

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
        git clone : https://github.com/umarulshahin/Antlegs_Backend.git
        cd Antlegs

2. Set Up Virtual Environment

        python -m venv venv
        source venv/bin/activate
        # On
        Windows: venv\Scripts\activate

3. Install Dependencies

     pip install -r requirements.txt

4. Set Environment Variables

Create a .env file and add your MongoDB URI and secret:
    
    DB_URLmongodb+srv://your-db-uri
    SECRET_KEY=your-secret-key
    Ensure your settings.py loads these securely using os.environ.

5. Run the Server

    python manage.py runserver

🔑 Endpoints

    Method	Endpoint	Description
    POST	/signup/	User registration
    POST	/signin/	User login (JWT)
    POST        /token/refresh/  jwt refresh token
    GET	        /usermanagement/	List users (auth)
    PATCH	/usermanagement/	Update user
    DELETE	/usermanagement/	Delete user

