```bash
                                                                                                   
88        88                         88                    88               88                     
88        88                         88                    88               88                     
88        88                         88                    88               88                     
88aaaaaaaa88  ,adPPYYba,  ,adPPYba,  88,dPPYba,    ,adPPYb,88   ,adPPYba,   88   ,d8  88       88  
88""""""""88  ""     `Y8  I8[    ""  88P'    "8a  a8"    `Y88  a8"     "8a  88 ,a8"   88       88  
88        88  ,adPPPPP88   `"Y8ba,   88       88  8b       88  8b       d8  8888[     88       88  
88        88  88,    ,88  aa    ]8I  88       88  "8a,   ,d88  "8a,   ,a8"  88`"Yba,  "8a,   ,a88  
88        88  `"8bbdP"Y8  `"YbbdP"'  88       88   `"8bbdP"Y8   `"YbbdP"'   88   `Y8a  `"YbbdP'Y8  
                                                                                                   
                                                                                                   
```

# 🎉 Hashdoku 📄

Esta app permite generar Documentos en PDF con sudokus, con distintos niveles de dificultad

![Captura_de_pantalla_2024-10-13_20-26-49.png](/screenshots/Captura_de_pantalla_2024-10-13_20-26-49.png)

## 🚀 Características

- **Generación de Sudokus**: Crea tableros de Sudoku válidos a partir de un algoritmo.
- **Guardado en PDF**: Guarda tu Sudoku y su solución en un documento PDF bien formateado.
- **Hash Unico**: Genera un hash único para cada Sudoku, que puedes usar para recrear el mismo tablero.
- **Dificultad Variable**: Oculta números de manera aleatoria según el nivel de dificultad definido.
- **Código QR**: Genera un código QR con el hash del Sudoku.

## 📋 Cómo Empezar

### Requisitos

- Python 3.x
- Librerías: `reportlab`, `qrcode`, `numpy`, `matplotlib`

Instala las dependencias necesarias con:

```sh
pip install reportlab qrcode numpy matplotlib
```
### Clonar el repositorio
Para comenzar, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/neocronos666/hashdoku.git
cd hashdoku
```

### Generación de Sudokus
Ejecuta el siguiente comando para generar un Sudoku y guardarlo en un PDF:

```bash
python sudoku.py [dificultad] [nombre_pdf] [cantidad_hojas] [mostrar_solucion] [mostrar_barra]
```
- `dificultad`: Un número de 0 a 81 que indica la cantidad de números a ocultar.
- `nombre_pdf`: El nombre del archivo PDF que se generará.
- `cantidad_hojas`: La cantidad de Sudokus a generar en el PDF.
- `mostrar_solucion`: Pon 1 si deseas que se muestre la solución en el PDF; de lo contrario, cualquier otro valor.
- `mostrar_barra`: Pon 1 si deseas que se muestre la barra de dificultad de cada juego; de lo contrario, cualquier otro valor o no colocar el parametro.



# Resolución de Sudokus
Ejecuta el siguiente comando para obtener la solución de un Sudoku a partir de un hash:

```bash
python get_solution.py <hash> [nombre_pdf]
```
- `hash`: El hash del Sudoku que quieres resolver.
- `nombre_pdf` (opcional): El nombre del archivo PDF donde se guardará la solución. Si no se proporciona, la solución se imprimirá en la consola.

## 📄 Ejemplo de Uso
Generar Sudoku
```bash
python sudoku.py 30 sudoku_output.pdf 1 1
```
Esto generará un Sudoku con dificultad 30, lo guardará en sudoku_output.pdf y también incluirá la solución en el PDF.

### Generacion con parametros por defecto
Es posible editar unas lineas en `hashdoku.php` para generar el documento unicamente corriendo el script, sin parametros externos. Primero hay que buscar el siguiente bloque:

```python
def main():
    # =======DEFAULT SETTINGS=======
    dificultad = 40
    nombre_pdf = 'sudo.pdf'
    cantidad_hojas = 100
    mostrar_solucion = True
    mostrar_barra = True
    #===============================
```
Completando esas variables al correr el script sin parametros tomara esos valores y generará un documento PDF sobreescribiendo el anterior cada vez que se corra.

### Resolver Sudoku
```bash
python get_solution.py tu_hash_aqui solucion.pdf

```
Esto tomará el hash tu_hash_aqui y generará un PDF llamado solucion.pdf con la solución del Sudoku.



## 🙌 Contribuciones
¡Sientete libre de contribuir! Haz un fork del repositorio y envía tus pull requests.

## 📚 Créditos
Este proyecto fue creado por [Sergio Silvstri](https://github.com/neocronos666) para mi tocaypo Rubén el padre de mi amigo Marco, a quien le gusta resolver Sudokus en papel.

# :muscle: Creditos a terceros
- El título del proyecto fue generado con arte ASCII en [patorjk.com](https://patorjk.com/software/taag/#p=display&f=Univers&t=Hashdoku) usando la fuente "Univers".

## 🛠️ Licencia
Este proyecto está bajo la Licencia GPL-3. Consulta el archivo [LICENSE](LICENSE) para más detalles.


