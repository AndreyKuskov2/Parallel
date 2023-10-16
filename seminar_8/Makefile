NAME = seminar_8

RM = rm -f

all: ${NAME}

${NAME}:
	cd ex01 && make
	cd ex02 && make

clean:
	cd ex01 && make clean
	cd ex02 && make clean

fclean: clean
	cd ex01 && make fclean
	cd ex02 && make fclean

run_exercise_1:
	cd ex01 && make && echo "START" && ./ex01

run_exercise_2:
	cd ex02 && make && echo "START" && ./ex02

re: fclean all

.PHONY : all clean fclean re
