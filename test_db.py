#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database import Database
import sqlite3

print("Probando Database.get_all_adults()...")
db = Database()
adults = db.get_all_adults()
print(f"Adultos encontrados: {len(adults)}")
if adults:
    print(f"Primer adulto: {adults[0]}")
else:
    print("Lista vacía")

print("\nProbando directamente con sqlite3...")
conn = sqlite3.connect('family_kitchen.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM adults ORDER BY nombre')
rows = cursor.fetchall()
print(f"Filas encontradas: {len(rows)}")
if rows:
    row = rows[0]
    print(f"Tipo de fila: {type(row)}")
    print(f"Keys: {list(row.keys())}")
    result = [{key: row[key] for key in row.keys()} for row in rows]
    print(f"Resultado convertido: {len(result)}")
    print(f"Primer resultado: {result[0] if result else 'None'}")
conn.close()
