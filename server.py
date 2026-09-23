from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import os
import html
import hashlib
import uuid


from database import get_connection


HOST = "localhost"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Stores logged-in users
sessions = {}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def read_template(filename):
    requested_path = os.path.join(TEMPLATE_DIR, filename)

    if os.path.exists(requested_path):
        template_path = requested_path
    else:
        target_name = filename.lower()
        template_path = requested_path

        for entry in os.listdir(TEMPLATE_DIR):
            if entry.lower() == target_name:
                template_path = os.path.join(TEMPLATE_DIR, entry)
                break

    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def send_html(handler, content, status=200, cookies=None):
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")

    if cookies:
        for cookie in cookies:
            handler.send_header("Set-Cookie", cookie)

    handler.end_headers()

    handler.wfile.write(content.encode("utf-8"))


def redirect(handler, location, cookies=None):
    handler.send_response(302)
    handler.send_header("Location", location)

    if cookies:
        for cookie in cookies:
            handler.send_header("Set-Cookie", cookie)

    handler.end_headers()


def get_session_user(handler):
    cookie = handler.headers.get("Cookie")

    if not cookie:
        return None

    for item in cookie.split(";"):
        item = item.strip()

        if item.startswith("session_id="):
            session_id = item.split("=", 1)[1]
            return sessions.get(session_id)

    return None


class EmployeeServer(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # ---------------- HOME ----------------
        if path == "/":
            redirect(self, "/login")
            return

        # ---------------- LOGIN ----------------
        if path == "/login":
            content = read_template("login.html")
            content = content.replace(
                "{{message}}",
                "Please login if you have an account"
            )
            send_html(self, content)
            return

        # ---------------- SIGNUP ----------------
        if path == "/signup":
            content = read_template("signup.html")
            content = content.replace(
                "{{message}}",
                "Please create an account"
            )
            send_html(self, content)
            return

        # ---------------- DASHBOARD ----------------
        if path == "/dashboard":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM employees")
            total_employees = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            content = read_template("dashboard.html")

            content = content.replace(
                "{{username}}",
                html.escape(username)
            )

            content = content.replace(
                "{{total_employees}}",
                str(total_employees)
            )

            send_html(self, content)
            return

        # ---------------- ADD EMPLOYEE ----------------
        if path == "/add-employee":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            content = read_template("add_Employee.html")
            send_html(self, content)
            return

        # ---------------- VIEW EMPLOYEES ----------------
        if path == "/employees":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id, name, email, phone, position,
                       department, salary
                FROM employees
                  ORDER BY id ASC
                """
            )

            employees = cursor.fetchall()

            cursor.close()
            connection.close()

            rows = ""

            for employee in employees:

                rows += f"""
                <tr>
                    <td>{employee[0]}</td>
                    <td>{html.escape(str(employee[1]))}</td>
                    <td>{html.escape(str(employee[2]))}</td>
                    <td>{html.escape(str(employee[3]))}</td>
                    <td>{html.escape(str(employee[4]))}</td>
                    <td>{html.escape(str(employee[5]))}</td>
                    <td>₹{employee[6]}</td>

                    <td>
                        <a class="edit-btn"
                           href="/update?id={employee[0]}">
                           Edit
                        </a>

                        <a class="delete-btn"
                           href="/delete?id={employee[0]}"
                           onclick="return confirm('Delete this employee?');">
                           Delete
                        </a>
                    </td>
                </tr>
                """

            content = read_template("Employees.html")
            content = content.replace("{{employee_rows}}", rows)

            send_html(self, content)
            return

        # ---------------- UPDATE PAGE ----------------
        if path == "/update":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            employee_id = query.get("id", [None])[0]

            if not employee_id:
                redirect(self, "/employees")
                return

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM employees WHERE id = %s",
                (employee_id,)
            )

            employee = cursor.fetchone()

            cursor.close()
            connection.close()

            if not employee:
                redirect(self, "/employees")
                return

            content = read_template("update_employee.html")

            content = content.replace("{{id}}", str(employee[0]))
            content = content.replace("{{name}}", html.escape(str(employee[1])))
            content = content.replace("{{email}}", html.escape(str(employee[2])))
            content = content.replace("{{phone}}", html.escape(str(employee[3])))
            content = content.replace("{{position}}", html.escape(str(employee[4])))
            content = content.replace("{{department}}", html.escape(str(employee[5])))
            content = content.replace("{{salary}}", str(employee[6]))

            send_html(self, content)
            return

        # ---------------- DELETE ----------------
        if path == "/delete":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            employee_id = query.get("id", [None])[0]

            if employee_id:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "DELETE FROM employees WHERE id = %s",
                    (employee_id,)
                )

                connection.commit()

                cursor.close()
                connection.close()

            redirect(self, "/employees")
            return

        # ---------------- STATIC FILES ----------------
        if path.startswith("/static/"):

            filename = path.replace("/static/", "", 1)
            file_path = os.path.join(STATIC_DIR, filename)

            if os.path.exists(file_path):

                if filename.endswith(".css"):
                    content_type = "text/css"

                elif filename.endswith(".js"):
                    content_type = "application/javascript"

                else:
                    content_type = "text/plain"

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    content_type
                )
                self.end_headers()

                with open(file_path, "rb") as file:
                    self.wfile.write(file.read())

                return

        self.send_error(404, "Page Not Found")

    # ====================================================
    # POST REQUESTS
    # ====================================================

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))

        body = self.rfile.read(length).decode("utf-8")

        data = parse_qs(body)

        # ---------------- SIGNUP ----------------
        if self.path == "/signup":

            username = data.get("username", [""])[0]
            password = data.get("password", [""])[0]

            if not username or not password:

                content = read_template("signup.html")

                content = content.replace(
                    "{{message}}",
                    "Please fill all fields."
                )

                send_html(self, content)
                return

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE username = %s",
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                cursor.close()
                connection.close()

                content = read_template("signup.html")

                content = content.replace(
                    "{{message}}",
                    "Username already exists."
                )

                send_html(self, content)
                return

            password_hash = hash_password(password)

            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                """,
                (username, password_hash)
            )

            connection.commit()

            cursor.close()
            connection.close()

            redirect(self, "/login")
            return

        # ---------------- LOGIN ----------------
        if self.path == "/login":

            username = data.get("username", [""])[0]
            password = data.get("password", [""])[0]

            password_hash = hash_password(password)

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = %s AND password = %s
                """,
                (username, password_hash)
            )

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:

                session_id = str(uuid.uuid4())

                sessions[session_id] = username

                cookie = (
                    f"session_id={session_id}; "
                    f"HttpOnly; Path=/"
                )

                redirect(
                    self,
                    "/dashboard",
                    cookies=[cookie]
                )

            else:

                content = read_template("login.html")

                content = content.replace(
                    "{{message}}",
                    "Invalid username or password."
                )

                send_html(self, content)

            return

        # ---------------- ADD EMPLOYEE ----------------
        if self.path == "/add-employee":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            name = data.get("name", [""])[0]
            email = data.get("email", [""])[0]
            phone = data.get("phone", [""])[0]
            position = data.get("position", [""])[0]
            department = data.get("department", [""])[0]
            salary = data.get("salary", [""])[0]

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO employees
                (name, email, phone, position, department, salary)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    phone,
                    position,
                    department,
                    salary
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            redirect(self, "/employees")
            return

        # ---------------- UPDATE EMPLOYEE ----------------
        if self.path == "/update":

            username = get_session_user(self)

            if not username:
                redirect(self, "/login")
                return

            employee_id = data.get("id", [""])[0]
            name = data.get("name", [""])[0]
            email = data.get("email", [""])[0]
            phone = data.get("phone", [""])[0]
            position = data.get("position", [""])[0]
            department = data.get("department", [""])[0]
            salary = data.get("salary", [""])[0]

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE employees
                SET name = %s,
                    email = %s,
                    phone = %s,
                    position = %s,
                    department = %s,
                    salary = %s
                WHERE id = %s
                """,
                (
                    name,
                    email,
                    phone,
                    position,
                    department,
                    salary,
                    employee_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            redirect(self, "/employees")
            return

        # ---------------- LOGOUT ----------------
        if self.path == "/logout":

            cookie = self.headers.get("Cookie")

            if cookie:

                for item in cookie.split(";"):

                    item = item.strip()

                    if item.startswith("session_id="):

                        session_id = item.split("=", 1)[1]

                        sessions.pop(
                            session_id,
                            None
                        )

            logout_cookie = (
                "session_id=; "
                "Expires=Thu, 01 Jan 1970 00:00:00 GMT; "
                "Path=/"
            )

            redirect(
                self,
                "/login",
                cookies=[logout_cookie]
            )

            return

        self.send_error(404, "Page Not Found")


server = HTTPServer(
    (HOST, PORT),
    EmployeeServer
)

print(f"Server running at http://{HOST}:{PORT}")

server.serve_forever()