from core.security import verify_password

hash = "$2b$12$MNsEgJjGdSC0ZViZsWWdsODlKhGPcOzc37jibgZtySxIKHAkAh1ke"
print(len(hash))
print(verify_password("admin123", hash))