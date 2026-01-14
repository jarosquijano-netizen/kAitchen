import sqlite3

# Verificar qué tablas existen en la base de datos
conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📋 Tablas en la base de datos:")
for table in tables:
    print(f"  ✅ {table[0]}")

# Verificar si las tablas adults y children existen
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
adults_exists = cursor.fetchone()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
children_exists = cursor.fetchone()

print(f"\n🔍 Verificación de tablas específicas:")
print(f"  Tabla 'adults' existe: {'✅ SÍ' if adults_exists else '❌ NO'}")
print(f"  Tabla 'children' existe: {'✅ SÍ' if children_exists else '❌ NO'}")

conn.close()

print("\n📋 CONCLUSIÓN:")
if adults_exists and children_exists:
    print("✅ Ambas tablas existen. El problema debe estar en el código.")
else:
    print("❌ Las tablas no existen. Se necesita inicializar la base de datos.")
