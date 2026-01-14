# Añadir método get_all_family_members a database.py

import os

# Leer el archivo actual
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar dónde insertar el nuevo método
insert_point = "    def get_all_family_members(self) -> List[Dict]:"
if insert_point in content:
    # Encontrar el final del método anterior
    lines = content.split('\n')
    insert_index = -1
    for i, line in enumerate(lines):
        if insert_point in line:
            insert_index = i
            break
    
    if insert_index != -1:
        # Insertar el nuevo método después del método anterior
        new_method = '''    def get_all_family_members(self) -> List[Dict]:
        """Get all family members (adults + children)"""
        adults = self.get_all_adults()
        children = self.get_all_children()
        
        # Combine adults and children
        family_members = adults + children
        
        # Add type to each member
        for member in family_members:
            member['type'] = 'adult' if 'edad' in member and member['edad'] >= 18 else 'child'
        
        return family_members'''
        
        # Insertar el nuevo método
        lines.insert(insert_index + 1, new_method)
        
        # Escribir el archivo actualizado
        with open('database.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print("✅ Método get_all_family_members añadido correctamente a database.py")
    else:
        print("❌ No se encontró el punto de inserción")

print("🔄 Por favor, reinicia el servidor para aplicar los cambios...")
