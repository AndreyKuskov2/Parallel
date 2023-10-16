NAME = ex01

SRC = $(wildcard *.cpp)

OBJ = $(SRC:.cpp=.o)

CPP = x86_64-w64-mingw32-gcc

all: $(NAME)

.cpp.o:
	$(CPP) -c $< -o $@ -fopenmp

$(NAME): $(OBJ)
	$(CPP) -o $(NAME) $(OBJ) -fopenmp

re:	fclean $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

.PHONY: all clean fclean re