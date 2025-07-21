CC = clang
CFLAGS = -Wall -Wextra -O2
TARGET = main

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) -o $(TARGET) main.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
