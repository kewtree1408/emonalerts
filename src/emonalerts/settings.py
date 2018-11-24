from environs import Env

env = Env()
DB_NAME = env("DB_NAME", default='checker.db')
