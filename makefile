# Variables
CC = gcc         
CFLAGS = -Wall
SRC = enlec.c
EXEC = enlec

# Regla por defecto
all: $(EXEC)

# Regla para crear el ejecutable
$(EXEC): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(EXEC)

# Regla para limpiar los archivos generados
clean:
	rm -f $(EXEC)
