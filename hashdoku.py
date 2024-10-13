import hashlib
import random
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas

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

def generar_hash(sudoku):
    sudoku_str = ''.join(''.join(map(str, fila)) for fila in sudoku)
    hash_object = hashlib.sha1(sudoku_str.encode())
    return hash_object.hexdigest()

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

def crear_pdf(nombre_archivo, sudoku, oculto, sudoku_hash, mostrar_solucion):
    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho, alto = A4

    # Título
    c.setFont("Helvetica", 18)
    c.drawCentredString(ancho / 2, alto - 2 * cm, f"Sudoku: {sudoku_hash}")
    
    # Dibujar Sudoku
    tam_celda = 15  # mm
    tabla_ancho = 9 * tam_celda * mm
    tabla_alto = 9 * tam_celda * mm
    x_offset = (ancho - tabla_ancho) / 2
    y_offset = 750
    #y_offset = alto - 5 * cm - tabla_alto / 2

    c.setFont("Helvetica", 14)
    for i in range(9):
        for j in range(9):
            valor = oculto[i][j]
            if valor != 0:
                x_pos = x_offset + j * tam_celda * mm + tam_celda * mm / 2
                y_pos = y_offset - i * tam_celda * mm - tam_celda * mm / 2
                c.drawCentredString(x_pos, y_pos, str(valor))

    # Líneas gruesas para los bloques
    c.setLineWidth(2)
    for i in range(0, 10, 3):
        c.line(x_offset, y_offset - i * tam_celda * mm, x_offset + tabla_ancho, y_offset - i * tam_celda * mm)
        c.line(x_offset + i * tam_celda * mm, y_offset, x_offset + i * tam_celda * mm, y_offset - tabla_alto)

    # Líneas finas para las celdas
    c.setLineWidth(0.5)
    for i in range(10):
        c.line(x_offset, y_offset - i * tam_celda * mm, x_offset + tabla_ancho, y_offset - i * tam_celda * mm)
        c.line(x_offset + i * tam_celda * mm, y_offset, x_offset + i * tam_celda * mm, y_offset - tabla_alto)

    # Solución opcional
    if mostrar_solucion:
        tam_celda = 7  # mm
        c.setFont("Helvetica", 10)


        y_offset_solucion = y_offset - tabla_alto - 2 * cm
        c.drawCentredString(ancho / 2, y_offset_solucion, "Solución:")
        for i in range(9):
            for j in range(9):
                valor = sudoku[i][j]
                if valor != 0:
                    x_pos = x_offset + j * tam_celda * mm + tam_celda * mm / 2
                    y_pos = y_offset_solucion - i * tam_celda * mm - tam_celda * mm / 2
                    c.drawCentredString(x_pos, y_pos, str(valor))

    c.save()

def main():
    dificultad = int(sys.argv[1])
    nombre_pdf = sys.argv[2]
    cantidad_hojas = int(sys.argv[3])
    mostrar_solucion = sys.argv[4] == '1'

    for _ in range(cantidad_hojas):
        sudoku = generar_sudoku()
        sudoku_hash = generar_hash(sudoku)
        oculto = ocultar_numeros(sudoku, dificultad)
        crear_pdf(nombre_pdf, sudoku, oculto, sudoku_hash, mostrar_solucion)

if __name__ == "__main__":
    main()

