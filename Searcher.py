import mysql.connector
import re

class Buscador:

    def __init__(self):
        connection = mysql.connector.connect(user='root',
                                             password='root',
                                             host='localhost',
                                             database='cataleg_plataformes',
                                             port='3306')
        self.connection = connection
        self.cursor = connection.cursor()

    def getConnection(self):
        return self.connection, self.cursor

    def main(self):  # Cambio aquí
        print("Bienvenido al seleccionador de preferencias de entretenimiento!")

        # Opciones de género
        generos = [
            "family", "reality", "european", "animation", "thriller", "horror", 
            "sport", "documentary", "western", "drama", "fantasy", "crime", 
            "history", "action", "war", "music", "comedy", "romance", "sci-fi"
        ]
        
        # Preguntar al usuario por sus géneros favoritos
        print("Por favor, selecciona tus géneros favoritos de la siguiente lista (separa por comas):")
        for i, genero in enumerate(generos, 1):
            print(f"{i}. {genero}")
        generos_seleccionados = input("Ingresa los números de los géneros que te gustan: ")
        generos_usuario = [generos[int(x) - 1] for x in generos_seleccionados.split(",")]

        # Preguntar si prefiere series, películas o ambas
        tipo_preferido = input("¿Prefieres películas, series o ambos? (ingresa '1' para películas, '2' para series o '3' para ambos): ")
        tipo_preferido = int(tipo_preferido)

        # Preguntar por la duración preferida si eligió películas
        duracion_preferida_peliculas = None
        if tipo_preferido == 1 or tipo_preferido == 3:
            print("¿Qué duración prefieres para las películas?")
            print("1. Menos de 90 minutos")
            print("2. 90 a 120 minutos")
            print("3. Más de 120 minutos")
            print("4. No importa")
            duracion = input("Elige una opción (1, 2, 3, 4): ")
            if duracion == "1":
                duracion_preferida_peliculas = "< 90"
            elif duracion == "2":
                duracion_preferida_peliculas = "Entre 90 i 120"
            elif duracion == "3":
                duracion_preferida_peliculas = "> 120"

        # Preguntar por la duración preferida de episodios si eligió series
        duracion_preferida_series = None
        tipo_series = None
        if tipo_preferido == 2 or tipo_preferido == 3:
            print("¿Qué duración prefieres para los episodios de las series?")
            print("1. Menos de 30 minutos")
            print("2. 30 a 60 minutos")
            print("3. Más de 60 minutos")
            print("4. No importa")
            duracion_series = input("Elige una opción (1, 2, 3, 4): ")
            if duracion_series == "1":
                duracion_preferida_series = "< 30"
            elif duracion_series == "2":
                duracion_preferida_series = "Entre 30 i 60"
            elif duracion_series == "3":
                duracion_preferida_series = "> 60"
            
        # Preguntar si prefiere una serie corta o larga
        if tipo_preferido == 2 or tipo_preferido == 3:
            print("¿Prefieres una serie corta (menos de 4 temporadas) o larga (4 o más temporadas)?")
            print("1. Corta (menos de 4 temporadas)")
            print("2. Larga (4 o más temporadas)")
            print("3. No importa")
            tipo_series = input("Elige una opción (1, 2, 3): ")

        # Preguntar por las plataformas de streaming preferidas
        print("Selecciona las plataformas de streaming que prefieras (separa por comas):")
        plataformas = ["Netflix", "HBOMax", "Amazon", "Paramount TV", "Disney", "HuluTV", "Rakuten"]
        for i, plataforma in enumerate(plataformas, 1):
            print(f"{i}. {plataforma}")
        plataformas_seleccionadas = input("Ingresa los números de las plataformas que prefieras: ")
        plataformas_usuario = [plataformas[int(x) - 1] for x in plataformas_seleccionadas.split(",")]

        # Preguntar por los paises de produccion preferidos
        print("Selecciona los paises de produccion que prefieras (separa por comas):")
        paises = ["US","GB","IN","KR","CA","JP","FR","CN","DE","ES","Otros"]
        for i, pais in enumerate(paises, 1):
            print(f"{i}. {pais}")
        paises_seleccionados = input("Ingresa los números de las paises de produccion que prefieras: ")
        paises_usuario = [paises[int(x) - 1] for x in paises_seleccionados.split(",")]

        # Guardar y mostrar resultados
        print("\nTus preferencias:")
        print("Géneros favoritos:", ", ".join(generos_usuario))
        print("Tipo preferido:", "Películas" if tipo_preferido == 1 else "Series" if tipo_preferido == 2 else "Ambos")
        print("Duración preferida de películas:", duracion_preferida_peliculas if duracion_preferida_peliculas else "No aplicable")
        print("Duración preferida de episodios de series:", duracion_preferida_series if duracion_preferida_series else "No aplicable")
        if tipo_series:
            if tipo_series == "1":
                print("Prefieres una serie corta (menos de 4 temporadas)")
            else:
                print("Prefieres una serie larga (4 o más temporadas)")
        print("Plataformas preferidas:", ", ".join(plataformas_usuario))
        print("Paises de produccion preferidos:", ", ".join(paises_usuario))
        busquedaPosible = 10
        self.queryCondicionada(generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario, paises_usuario, paises, busquedaPosible)  # Cambio aquí

    def queryCondicionada(self, generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario, paises_usuario, paises, busquedaPosible):
        # Query condicionada
        # Base de la consulta
        query = "SELECT movie_serie.title FROM movie_serie "
        print(query)
        # Añadiendo filtro por género
        query += " INNER JOIN " + " produccion_generos " + " ON " + " movie_serie.id = " + " produccion_generos.produccion " 
        query += " INNER JOIN " + " generos " + " ON " + " produccion_generos.generos = " + " generos.id "
        query += " INNER JOIN " + " produccion_plataforma " + " ON " + " produccion_plataforma.produccion = " + " movie_serie.id "
        query += " INNER JOIN " + " plataforma " + " ON " + " produccion_plataforma.plataforma = " + " plataforma.id_plataforma "
        query += " INNER JOIN " + " produccion_pais " + " ON " + " produccion_pais.produccion = " + " movie_serie.id "
        query += " INNER JOIN " + " pais " + " ON " + " produccion_pais.pais = " + " pais.id "
        
        # Añadiendo filtro por género
        where_filters = " OR ".join([f"generos.genre = '{genero}'" for genero in generos_usuario])
        # Añadiendo filtro por plataforma
        where_filters += " AND " + " OR ".join([f"plataforma.plataforma_name = '{plataforma}'" for plataforma in plataformas_usuario])
        # Añadiendo filtro por pais
        if "Otros" in paises_usuario and len(paises_usuario) < 11:
            where_filters += " AND " + "pais.pais NOT IN (" +"".join([f"'{pais}'" for pais in paises if pais != "Otros" and pais not in paises_usuario]) + ")"
        else:
            where_filters += " AND " + " OR ".join([f"pais.pais = '{pais}'" for pais in paises_usuario])
        print(query)

        # Query condicionada para series, a partir de aqui empiezan a diferir
        query2 = query

        # Añadiendo filtro por tipo (series o películas)
        if tipo_preferido == 2 or tipo_preferido == 3:
            where_filters2 = where_filters
            where_filters2 += " AND movie_serie.type = 'show'"
            if duracion_preferida_series:
                if duracion_preferida_series == "Entre 30 i 60":
                    where_filters2 += " AND movie_serie.runtime >= 30 AND movie_serie.runtime <= 60"
                else:
                    where_filters2 += f" AND movie_serie.runtime {duracion_preferida_series}"
        if tipo_preferido == 1 or tipo_preferido == 3:
            where_filters += " AND movie_serie.type = 'movie'"
            if duracion_preferida_peliculas:
                if duracion_preferida_peliculas == "Entre 90 i 120":
                    where_filters += " AND movie_serie.runtime >= 90 AND movie_serie.runtime <= 120"
                else:
                    where_filters += f" AND movie_serie.runtime {duracion_preferida_peliculas}"
                

        # Añadiendo filtro por número de temporadas para series
        if tipo_preferido == 2 or tipo_preferido == 3:
            if tipo_series == "1":
                where_filters2 += " AND movie_serie.seasons < 4"
            else:
                where_filters2 += " AND movie_serie.seasons >= 4"

        if tipo_preferido == 1 or tipo_preferido == 3:
            query += f" WHERE ({where_filters})"
        if tipo_preferido == 2 or tipo_preferido == 3:
            query2 += f" WHERE ({where_filters2})"
        
        print(query)
        print("=====================================")
        print(query2)
       
        resultado = None
        resultado2 = None

        # Ejecutar las consultas, una para peliculas i otra para series
        if self.cursor:
            if tipo_preferido == 1 or tipo_preferido == 3:
                self.cursor.execute(query)
                resultado = self.cursor.fetchall()
                if tipo_preferido == 1:
                    resultado2 = None
            if tipo_preferido == 2 or tipo_preferido == 3:
                self.cursor.execute(query2)
                resultado2 = self.cursor.fetchall()
                if tipo_preferido == 2:
                    resultado = None

        #Filtrar los datos para que no se repitan
        if resultado:
            resultado_filtrado = []
            for i in resultado:
                if i not in resultado_filtrado:
                    resultado_filtrado.append(i)
            resultado = resultado_filtrado

        if resultado2:
            resultado_filtrado2 = []
            for i in resultado2:
                if i not in resultado_filtrado2:
                    resultado_filtrado2.append(i)
            resultado2 = resultado_filtrado2
        
        # Mostrar resultados
        print("\nResultados:")
        print("=============")
        print("Películas:")
        repeticion=0
        if resultado:
            for i,res in enumerate(resultado,1):
                    print(f"{i}. {res}")
        else:
            print("No se encontraron películas con tus preferencias.")
            repeticion+=1
        print("=============")
        print("Series:")
        if resultado2:
            for i,res in enumerate(resultado2,1):
                    print(f"{i}. {res}")
        else:
            print("No se encontraron series con tus preferencias.")
            repeticion+=1

        if repeticion==2:
            while busquedaPosible>1:
                print("")
                print("No se encontraron películas ni series con tus preferencias. Vamos a intentar encontrar algo para ti.")
                self.reconsultaPreferencias(generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario, paises_usuario, paises, busquedaPosible)
        
        print("\n¡Gracias por usar nuestro servicio!")
        exit(0)

    def reconsultaPreferencias(self, generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario, paises_usuario, paises, busquedaPosible):
        print("================================================================")
        print("¿Deseas realizar una nueva búsqueda reduciendo tus preferencias?")
        respuesta = input("Ingresa 's' para sí o 'n' para no: ")
        if respuesta == "s":
            i=1
            print("Tus preferencias anteriores eran:")
            if(generos_usuario):
                print("1.Géneros favoritos: ", ",".join(generos_usuario))
                i+=1
            if(tipo_preferido and tipo_preferido!=3):
                print("2.Tipo preferido:", "Películas" if tipo_preferido == 1 else "Series" if tipo_preferido == 2 else "Ambos")
                i+=1
            if(duracion_preferida_peliculas):
                print("3.Duración preferida de películas: < 90")
                i+=1
            if(duracion_preferida_series):
                print("4.Duración preferida de episodios de series: < 30")
                i+=1
            if tipo_series:
                if tipo_series == "1":
                    print("5.Prefieres una serie corta (menos de 4 temporadas)")
                    i+=1
                else:
                    print("5.Prefieres una serie larga (4 o más temporadas)")
                    i+=1
            if(plataformas_usuario and len(plataformas_usuario)<7):
                print("6.Plataformas preferidas:", ", ".join(plataformas_usuario))
                i+=1
            if(paises_usuario):
                print("7.Paises de produccion preferidos:", ", ".join(paises_usuario))
                i+=1

            # Descartar una preferencia
            print("¿Qué es menos importante para ti?")
            opcion_descartada = input("Elige el número de la preferencia a descartar (1, 2, 3, 4...): ")   
            if opcion_descartada == '1':
                generos_usuario = None
            elif opcion_descartada == '2':
                tipo_preferido = 3
            elif opcion_descartada == '3':
                duracion_preferida_peliculas = None
            elif opcion_descartada == '4':
                duracion_preferida_series = None
            elif opcion_descartada == '5':
                tipo_series = None
            elif opcion_descartada == '6':
                plataformas_usuario = ("Netflix", "HBOMax", "Amazon", "Paramount TV", "Disney", "HuluTV", "Rakuten")
            elif opcion_descartada == '7':
                paises_usuario = ("US","GB","IN","KR","CA","JP","FR","CN","DE","ES","Otros")

            if(i>=1):
                busquedaPosible=i
                self.queryCondicionada(generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario, paises_usuario, paises, busquedaPosible)
            else:
                print("No se puede realizar una nueva búsqueda, ya no quedan parametros para descartar.")
    
        else:
            print("¡Hasta luego!")
            exit(0)

if __name__ == "__main__":
    buscador = Buscador()  # Crear una instancia de la clase Buscador
    buscador.main()  # Llamar al método main() a través de la instancia creada
