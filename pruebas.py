from core.security import verify_password

hash = "postgresql://waterdb_ophw_user:XMaTXaUWeuZZPRLI6ZmAYa0ZEBJ0FUm2@dpg-d7okj9f7f7vs73auqtc0-a.oregon-postgres.render.com/waterdb_ophw"
print(verify_password("2o72o623s", hash))