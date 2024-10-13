from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
import sys

def reconstruir_sudoku(hash_str): #AAAAAACAAAAA NO ANDAAA
    numeros = [int(c) for c in hash_str]
    sudoku = [numeros[i:i + 9] for i in range(0, len(numeros), 9)]
    return sudoku


def crear_pdf_sudoku(nombre_archivo, sudoku):
    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho, alto = A4

    # Dibujar Sudoku
    tam_celda = 15  # mm
    tabla_ancho = 9 * tam_celda * mm
    tabla_alto = 9 * tam_celda * mm
    x_offset = (ancho - tabla_ancho) / 2
    y_offset = alto - 5 * cm

    c.setFont("Helvetica", 14)
    for i in range(9):
        for j in range(9):
            valor = sudoku[i][j]
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

    c.save()

def imprimir_sudoku(sudoku):
    for fila in sudoku:
        print(" ".join(str(num) for num in fila))

def main():
    hash_str = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'dcfe56081b623439c85a9342b2a42c94d226df75'
    sudoku = reconstruir_sudoku(hash_str)
    
    if len(sys.argv) > 2:
        nombre_archivo = sys.argv[2]
        crear_pdf_sudoku(nombre_archivo, sudoku)
    else:
        imprimir_sudoku(sudoku)

if __name__ == "__main__":
    main()
