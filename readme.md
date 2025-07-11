### To-do

-Detectar o pedir resolucion de pantalla
-Ciudades para las nacionalidades
-Score binario foto sola o con gente. Foto selfie o no. Y que eso afecte a un score global "cantidad de fotos solas"
-Algunos scores son graduales, otros binarios. Algunos son tendientes 1, otros a 0.5 (o sea, un termino medio es mejor)
-archivo para extraer datos basicos del perfil (bio, seguidores, privado, etc). o funcion dentro de score_texto. y si pasa el umbral, llama a captura de perfil. despues score_clip funciona sobre la carpeta img
-coordinar el score de texto->captura de imagenes->score de imagenes desde el main
-Hacer un diagrama de flujo
-Si el tipo tiene 6 publicaciones o menos, no haga scroll. y si el perfil es privado, solo haga la captura de la foto de perfil
-O que detecte la cantidad de elementos y haga la cantidad de recortes segun la cantidad elementos (si es que son menoss de 12)
-Score positivo y negativo en el prefiltrado
-persistencia de la sesion
-headless. 
-Hacer un criterio de descarte aparte para las minas. 
-Que links externos sea texto, no integer
-Separar extraer_datos_perfil de filtrar_perfiles
-Tabla de score_bio, score_clip, score_deepface
-Etapa de gpt
-Repensar criterio string largo. lo mismo para nobmres ambiguos
-Que detecte perfiles ya analizados
-Hacer bien las tablas de comentarios y de usuarios, coon las relaciones entre claves
-Filtrar expresiones tipo "omg"
-Usar clip para detectar perfiles de muy baja calidad
detectar fecha de nacimiento en la biografia
