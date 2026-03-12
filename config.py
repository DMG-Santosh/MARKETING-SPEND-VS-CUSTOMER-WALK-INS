import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Santosh@2005')   # <-- Change this to your MySQL password
    MYSQL_DATABASE = 'analytics_project'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
