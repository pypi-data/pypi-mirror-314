from flask import Flask, render_template, jsonify
import psycopg2
from datetime import datetime
from config_loader import main
# Flask setup
app = Flask(__name__)

# PostgreSQL connection parameters
# DATABASE = "monitoring_system"
# USER = "monitoring_user"
# PASSWORD = "cool"
# HOST = "localhost"
# PORT = "5432"

config = main()

if config:
    DB_NAME = config.get("DB_NAME")
    USER = config.get("USER")
    PASSWORD = config.get("PASSWORD")
    HOST = config.get("HOST", "localhost")
    PORT = int(config.get("PORT", 5432))

# Function to fetch metrics from the database
def get_data_from_db():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()

        # Fetch the latest stored data (limit 5 rows)
        cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 5;")
        rows = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Return rows as a list of dictionaries
        metrics = [
            {
                "hostname": row[2],  # hostname column
                "metric": row[3],    # metric column
                "value": row[4],     # value column
                "timestamp": row[1]  # timestamp column
            }
            for row in rows
        ]

        return metrics

    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return []

# Define Flask home route
# @app.route('/')
# def index():
#     metrics = get_data_from_db()
#
#     # Render HTML content dynamically
#     html_content = """
#     <html>
#         <head>
#             <title>Monitoring Dashboard</title>
#         </head>
#         <body>
#             <h1>Server Monitoring Dashboard</h1>
#             <h2>Recent Metrics</h2>
#             <table border="1" cellspacing="0" cellpadding="5">
#                 <tr>
#                     <th>Hostname</th>
#                     <th>Metric</th>
#                     <th>Value</th>
#                     <th>Timestamp</th>
#                 </tr>
#     """
#
#     for metric in metrics:
#         html_content += f"""
#             <tr>
#                 <td>{metric['hostname']}</td>
#                 <td>{metric['metric']}</td>
#                 <td>{metric['value']}</td>
#                 <td>{metric['timestamp']}</td>
#             </tr>
#         """
#
#     html_content += """
#             </table>
#         </body>
#     </html>
#     """
#
#     return html_content
@app.route('/')
def index():
    metrics = get_data_from_db()
    return render_template("dashboard.html", metrics=metrics)

# Run Flask server on port 8080
if __name__ == "__main__":
    app.run(port=8090, host="0.0.0.0", debug=True)

# def main():
#     app.run(port=8090, host="0.0.0.0", debug=True)