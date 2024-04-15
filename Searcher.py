class Buscador:
    def main():
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
        tipo_preferido = input("¿Prefieres series, películas o ambos? (ingresa 'series', 'películas' o 'ambos'): ")

        # Preguntar por la duración preferida si eligió películas
        duracion_preferida_peliculas = None
        if tipo_preferido.lower() == "películas" or tipo_preferido.lower() == "ambos":
            print("¿Qué duración prefieres para las películas?")
            print("1. Menos de 90 minutos")
            print("2. 90 a 120 minutos")
            print("3. Más de 120 minutos")
            duracion = input("Elige una opción (1, 2, 3): ")
            if duracion == "1":
                duracion_preferida_peliculas = "<90 min"
            elif duracion == "2":
                duracion_preferida_peliculas = "90-120 min"
            elif duracion == "3":
                duracion_preferida_peliculas = ">120 min"

        # Preguntar por la duración preferida de episodios si eligió series
        duracion_preferida_series = None
        tipo_series = None
        if tipo_preferido.lower() == "series" or tipo_preferido.lower() == "ambos":
            print("¿Qué duración prefieres para los episodios de las series?")
            print("1. Menos de 30 minutos")
            print("2. 30 a 60 minutos")
            print("3. Más de 60 minutos")
            duracion_series = input("Elige una opción (1, 2, 3): ")
            if duracion_series == "1":
                duracion_preferida_series = "<30 min"
            elif duracion_series == "2":
                duracion_preferida_series = "30-60 min"
            elif duracion_series == "3":
                duracion_preferida_series = ">60 min"
            
            # Preguntar si prefiere una serie corta o larga
            print("¿Prefieres una serie corta (menos de 4 temporadas) o larga (4 o más temporadas)?")
            print("1. Corta (menos de 4 temporadas)")
            print("2. Larga (4 o más temporadas)")
            tipo_series = input("Elige una opción (1, 2): ")

        # Preguntar por las plataformas de streaming preferidas
        print("Selecciona las plataformas de streaming que prefieras (separa por comas):")
        plataformas = ["Netflix", "HBO Max", "Amazon", "Paramount TV", "Disney", "HuluTV", "Rakuten"]
        for i, plataforma in enumerate(plataformas, 1):
            print(f"{i}. {plataforma}")
        plataformas_seleccionadas = input("Ingresa los números de las plataformas que prefieras: ")
        plataformas_usuario = [plataformas[int(x) - 1] for x in plataformas_seleccionadas.split(",")]

        # Guardar y mostrar resultados
        print("\nTus preferencias:")
        print("Géneros favoritos:", ", ".join(generos_usuario))
        print("Tipo preferido:", tipo_preferido)
        print("Duración preferida de películas:", duracion_preferida_peliculas if duracion_preferida_peliculas else "No aplicable")
        print("Duración preferida de episodios de series:", duracion_preferida_series if duracion_preferida_series else "No aplicable")
        if tipo_series:
            if tipo_series == "1":
                print("Prefieres una serie corta (menos de 4 temporadas)")
            else:
                print("Prefieres una serie larga (4 o más temporadas)")
        print("Plataformas preferidas:", ", ".join(plataformas_usuario))
        queryCondicionada(generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario)

    def queryCondicionada(generos_usuario, tipo_preferido, duracion_preferida_peliculas, duracion_preferida_series, tipo_series, plataformas_usuario):
        # Query condicionada
        query = "SELECT * FROM entretenimiento WHERE "
        query += " OR ".join([f"genero = '{genero}'" for genero in generos_usuario])
        query += " AND tipo = 'serie' " if tipo_preferido.lower() == "series" else " AND tipo = 'película' "
        query += f"AND duracion = '{duracion_preferida_peliculas}' " if duracion_preferida_peliculas else ""
        query += f"AND duracion_episodio = '{duracion_preferida_series}' " if duracion_preferida_series else ""
        query += "AND temporadas < 4 " if tipo_series == "1" else "AND temporadas >= 4 " if tipo_series == "2" else ""
        query += " OR ".join([f"plataforma = '{plataforma}'" for plataforma in plataformas_usuario])
        print("\n¡Gracias por usar nuestro servicio!")

    if __name__ == "__main__":
        main()