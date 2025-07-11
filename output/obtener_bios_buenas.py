import json

def filtrar_por_bio_larga(objetos, longitud_minima=20):
    """
    Filtra y devuelve solo 'id', 'username' y 'bio' de objetos cuya bio es larga.
    
    :param objetos: Lista de diccionarios
    :param longitud_minima: Entero mínimo de caracteres en la bio
    :return: Lista de dicts con solo 'id', 'username' y 'bio'
    """
    resultado = []
    contador = 1
    for obj in objetos:
        bio = obj.get("bio", "")
        if isinstance(bio, str) and len(bio) > longitud_minima:
            resultado.append({
                "id": contador,
                "username": obj.get("username", ""),
                "bio": bio
            })
            contador += 1
    return resultado

# Cargar archivo original
with open("output/usuarios_filtrados.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# Filtrar y simplificar
filtrados = filtrar_por_bio_larga(datos)

# Guardar resultados en nuevo archivo
with open("output/bios_filtradas.json", "w", encoding="utf-8") as f:
    json.dump(filtrados, f, ensure_ascii=False, indent=4)

print(f"✅ Se guardaron {len(filtrados)} bios largas con id en output/bios_filtradas.json")
