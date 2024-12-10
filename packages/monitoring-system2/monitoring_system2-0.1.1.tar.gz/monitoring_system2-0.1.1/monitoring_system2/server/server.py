import socket
import threading
from datetime import datetime
import psycopg2
from config_loader import load_config

config = load_config()
print("config,config",config)

if config:
    DB_NAME = config.get("DB_NAME", "monitoring_system")
    USER = config.get("USER", "monitoring_user")
    PASSWORD = config.get("PASSWORD", "your_secure_password")
    HOST = config.get("HOST", "localhost")
    PORT = int(config.get("PORT", 5432))

# Initialize the database and create the table if it doesn't exist
def init_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()

        # Create the 'metrics' table if it doesn't exist
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS metrics (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                hostname TEXT NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL
            )
        '''
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()

        print("Database initialized and table created successfully.")

    except Exception as e:
        print(f"Database initialization error: {e}")

# Function to handle client communication and store data in PostgreSQL
def handle_client(client_socket):
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data from client: {data}")

        try:
            # Parse received data
            hostname, metric, value = data.split("|")
            timestamp = datetime.now()

            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            cursor = conn.cursor()

            # Insert data into the database
            insert_query = """
                INSERT INTO metrics (timestamp, hostname, metric, value)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (timestamp, hostname, metric, float(value)))
            conn.commit()

            # Check if the row is inserted (Fetch last row)
            cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1;")
            last_row = cursor.fetchone()
            print(f"Last row in database: {last_row}")

            client_socket.send(b"Data received successfully")

            # Close the database connection
            cursor.close()
            conn.close()

        except ValueError:
            print(f"Data format incorrect. Expected: hostname|metric|value")
            client_socket.send(b"Invalid data format")

    except Exception as e:
        print(f"Client error: {e}")
        client_socket.send(b"Server error occurred")

    finally:
        client_socket.close()


# Main server function
def start_server(port):
    init_db()

    # Create and bind the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("0.0.0.0", port))
    server.listen(5)

    print(f"Server listening on port {port}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except KeyboardInterrupt:
        print("\nServer shutting down.")

    finally:
        server.close()


# Start the server on port 10052
if __name__ == "__main__":
    start_server(10052)
