# Django API consumer frontend

Description:

This is a Django web app the consumes an API created in C# using ASP.NET Core. The API is a simple CRUD API for managing food items, places and universities as well as users. The frontend is a simple web app that allows users to view, add, update, and delete food items.

Setting up development environment for Django API consumer frontend.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/l-velazquez/UniFood_Django.git
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

5. Copy example environment file:

```bash
cp .env_example .env
```

Edit any of the information that .env requires. If deploying to production, make sure to change the values inside of the .env file.

6. Run the Django server:

```bash
cd UniFood
python manage.py runserver
```

The server will run on 'http://localhost:8000/'.
