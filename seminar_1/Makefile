NAME = seminar_1

GCC = g++

SRC = main.cpp

OBJ = ${SRC:.c=.o}

RM = rm -f

all: ${NAME}

${NAME}: ${OBJ} 
	${GCC} ${OBJ} -o $(NAME) -fopenmp

%.o: %.cpp
	${GCC} ${GFLAGS} -c $< -o $@ -fopenmp

clean:
	${RM} ${OBJ}

fclean: clean
	${RM} ${NAME}

re: fclean all

.PHONY : all clean fclean re