import hashlib
import random
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
import base64
from encoding import EncodingSudoku

def generar_sudoku():
    base = 3
    lado = base * base

    def pattern(r, c): return (base * (r % base) + r // base + c) % lado
    def shuffle(s): return random.sample(s, len(s))

    rBase = range(base)
    filas = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in filas]
    return board

def generar_hash(sudoku): #DEPRECATED
    sudoku_str = ''.join(''.join(map(str, fila)) for fila in sudoku)
    hash_object = hashlib.sha1(sudoku_str.encode())
    return hash_object.hexdigest()

def generar_cadena_bit_packing(sudoku): #DEPRECATED
    # Convertimos la lista de 9x9 en una cadena binaria
    bits = ''.join(f'{num:04b}' for fila in sudoku for num in fila)
    # Convertimos la cadena binaria en bytes
    byte_data = int(bits, 2).to_bytes(len(bits) // 8, byteorder='big')
    # Codificamos en base64 (puedes cambiar a base85 si lo prefieres)
    return base64.b85encode(byte_data).decode('utf-8')


def ocultar_numeros(sudoku, dificultad):
    oculto = [fila[:] for fila in sudoku]  # Copia del sudoku
    bloques_vacios = {i: 0 for i in range(9)}

    while dificultad > 0:
        menos_vacios = min(bloques_vacios.values())
        candidatos = [i for i in bloques_vacios if bloques_vacios[i] == menos_vacios]
        bloque = random.choice(candidatos)

        fila_inicio = (bloque // 3) * 3
        col_inicio = (bloque % 3) * 3
        celdas = [(i, j) for i in range(fila_inicio, fila_inicio + 3) for j in range(col_inicio, col_inicio + 3)]
        random.shuffle(celdas)

        for fila, col in celdas:
            if oculto[fila][col] != 0:
                oculto[fila][col] = 0
                bloques_vacios[bloque] += 1
                dificultad -= 1
                break

    return oculto
    crear_pdf(nombre_pdf, mostrar_solucion, mostrar_barra, dificultad,cantidad_hojas)

def crear_pdf(nombre_archivo, mostrar_solucion, mostrar_barra, dificultad, cantidad_hojas):
    pdf = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho, alto = A4

    #INICIO DE LA HOJA
    # cantidad_hojas
    for sheet in range(cantidad_hojas):
        sudoku = generar_sudoku()
        # sudoku_hash = generar_hash(sudoku)        
        # sudoku_hash = generar_cadena_bit_packing(sudoku)
        es = EncodingSudoku()
        sudoku_hash = es.generar_cadena_base62(sudoku)
        oculto = ocultar_numeros(sudoku, dificultad)

        # Título
        pdf.setFont("Courier", 8)    
        pdf.drawString(60, 800, r'88        88                         88                    88               88                     ')
        pdf.drawString(60, 792, r'88        88                         88                    88               88                     ')
        pdf.drawString(60, 784, r'88        88                         88                    88               88                     ')
        pdf.drawString(60, 776, r'88aaaaaaaa88  ,adPPYYba,  ,adPPYba,  88,dPPYba,    ,adPPYb,88   ,adPPYba,   88   ,d8  88       88  ')
        pdf.drawString(60, 768, r'88""""""""88  ""     `Y8  I8[    ""  88P´    "8a  a8"    `Y88  a8"     "8a  88 ,a8"   88       88  ')
        pdf.drawString(60, 760, r'88        88  ,adPPPPP88   `"Y8ba,   88       88  8b       88  8b       d8  8888[     88       88  ')
        pdf.drawString(60, 752, r'88        88  88,    ,88  aa    ]8I  88       88  "8a,   ,d88  "8a,   ,a8"  88`"Yba,  "8a,   ,a88  ')
        pdf.drawString(60, 744, r'88        88  `"8bbdP"Y8  `"YbbdP"´  88       88   `"8bbdP"Y8   `"YbbdP"`   88   `Y8a  `"YbbdP´Y8  ')
        
        #Subtitulo
        y_offset = 4.5 #cm
        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(ancho / 2, alto - y_offset * cm, f"HASH DEL JUEGO: {sudoku_hash}")
        pdf.drawString(60, 25, 'https://github.com/neocronos666/hashdoku')     
        pdf.drawString(450, 25, f"[Página {sheet+1} de {cantidad_hojas}]")     
        
        # Dibujar Sudoku
        tam_celda = 15  # mm
        tabla_ancho = 9 * tam_celda * mm
        tabla_alto = 9 * tam_celda * mm
        x_offset = (ancho - tabla_ancho) / 2
        y_offset = 680 
        pdf.setFont("Helvetica", 14)
        for i in range(9):
            for j in range(9):
                valor = oculto[i][j]
                if valor != 0:
                    x_pos = x_offset + j * tam_celda * mm + tam_celda * mm / 2
                    y_pos = y_offset - i * tam_celda * mm - tam_celda * mm / 2
                    pdf.drawCentredString(x_pos, y_pos, str(valor))

        # Líneas gruesas para los bloques
        pdf.setLineWidth(2)
        for i in range(0, 10, 3):
            pdf.line(x_offset, y_offset - i * tam_celda * mm, x_offset + tabla_ancho, y_offset - i * tam_celda * mm)
            pdf.line(x_offset + i * tam_celda * mm, y_offset, x_offset + i * tam_celda * mm, y_offset - tabla_alto)

        # Líneas finas para las celdas
        pdf.setLineWidth(0.5)
        for i in range(10):
            pdf.line(x_offset, y_offset - i * tam_celda * mm, x_offset + tabla_ancho, y_offset - i * tam_celda * mm)
            pdf.line(x_offset + i * tam_celda * mm, y_offset, x_offset + i * tam_celda * mm, y_offset - tabla_alto)

        # Solución opcional
        y_offset_solucion = y_offset - tabla_alto - 2 * cm
        if mostrar_solucion:
            tam_celda = 7  # mm
            pdf.setFont("Helvetica", 10)
            
            pdf.drawString(173, y_offset_solucion + 10 , "Solución:")
            for i in range(9):
                for j in range(9):
                    valor = sudoku[i][j]
                    if valor != 0:
                        x_pos = x_offset + j * tam_celda * mm + tam_celda * mm / 2
                        y_pos = y_offset_solucion - i * tam_celda * mm - tam_celda * mm / 2
                        pdf.drawCentredString(x_pos, y_pos, str(valor))        

        
        # Barra de dificultad
        if mostrar_barra:
            pdf.drawString(360, y_offset_solucion + 10 , "Dificultad:")
            posx = 300
            posy = 220
            space = 10
            font_size = 10
            pdf.setFont("Courier", font_size)
            pdf.drawString(posx, posy, f' Celdas Vacias:{dificultad}/81')
            dif = int(dificultad * 28 / 81)
            bar=''
            for i in range(28):
                bar += "#" if i < dif else "."        
            pdf.drawString(posx, posy - font_size - space, f'[{bar}]')
            pdf.drawString(posx, posy - 2 * (font_size + space), r' Facil                Dificil')

        # Nueva Pagina        
        pdf.showPage()    
    pdf.save()

def main():
    # =======DEFAULT SETTINGS=======
    dificultad= 40
    nombre_pdf = 'Hashdokus (100_sudokus).pdf'
    cantidad_hojas = 100
    mostrar_solucion = False
    mostrar_barra = True
    #===============================


    dificultad = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] else dificultad
    nombre_pdf = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else nombre_pdf
    cantidad_hojas = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else cantidad_hojas
    mostrar_solucion = bool(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else mostrar_solucion
    mostrar_barra = bool(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[4] else mostrar_barra
   
    crear_pdf(nombre_pdf, mostrar_solucion, mostrar_barra, dificultad,cantidad_hojas)

if __name__ == "__main__":
    main()

