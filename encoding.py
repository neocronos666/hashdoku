import string

class EncodingSudoku():
    # Conjunto de caracteres Base62
    BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase + "+-_*@#?=!ñÑ.:,;"

    def __init__(self) -> None:
        pass

    def base_encode(self, num, base_chars=BASE62_CHARS):
        """Convierte un número entero en una cadena en la base dada."""
        base = len(base_chars)
        if num == 0:
            return base_chars[0]
        
        encoded = []
        while num:
            num, rem = divmod(num, base)
            encoded.append(base_chars[rem])
        
        return ''.join(reversed(encoded))

    def base_decode(self, encoded_str, base_chars=BASE62_CHARS):
        """Convierte una cadena baseN de vuelta a un número entero."""
        base = len(base_chars)
        decoded = 0
        for char in encoded_str:
            decoded = decoded * base + base_chars.index(char)
        return decoded

    def sudoku_to_number(self, sudoku):
        """Convierte el Sudoku 9x9 en un solo número grande."""
        sudoku_str = ''.join(str(num) for fila in sudoku for num in fila)
        return int(sudoku_str)

    def number_to_sudoku(self, num):
        """Convierte un número grande de vuelta a un Sudoku 9x9."""
        sudoku_str = str(num).zfill(81)  # Asegura que tenga 81 dígitos
        return [[int(sudoku_str[i*9 + j]) for j in range(9)] for i in range(9)]

    def generar_cadena_base62(self, sudoku):
        """Convierte un Sudoku en una cadena compacta usando Base62."""
        sudoku_number = self.sudoku_to_number(sudoku)
        return self.base_encode(sudoku_number)

    def reconstruir_sudoku_base62(self, cadena_codificada):
        """Convierte una cadena Base62 de vuelta a un Sudoku."""
        sudoku_number = self.base_decode(cadena_codificada)
        return self.number_to_sudoku(sudoku_number)

if __name__ == "__main__":
    # Ejemplo de un Sudoku simple
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    es = EncodingSudoku()

    cadena_base62 = es.generar_cadena_base62(sudoku)
    print(f"Sudoku codificado en Base62: {cadena_base62}")
    print("-------------------------")
    sudoku_recuperado = es.reconstruir_sudoku_base62(cadena_base62)
    print("Sudoku recuperado:", sudoku_recuperado)
    print("-------------------------")
    print(f"base de caracteres:{len(es.BASE62_CHARS)}")
