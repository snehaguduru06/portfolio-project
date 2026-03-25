import mysql.connector
import os
from urllib.parse import urlparse

# Get the URL from Railway variables
url_str = os.environ.get('DATABASE_URL')
url = urlparse(url_str)

db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:], # removes the slash from the start
    port=url.port
)
