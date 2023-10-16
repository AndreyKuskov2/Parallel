NAME = seminar_7

RM = rm -f

all: ${NAME}

${NAME}:
	cd ex01 && make
	cd ex02 && make
	cd ex03 && make
	cd ex04 && make

clean:
	cd ex01 && make clean
	cd ex02 && make clean
	cd ex03 && make clean
	cd ex04 && make clean

fclean: clean
	cd ex01 && make fclean
	cd ex02 && make fclean
	cd ex03 && make fclean
	cd ex04 && make fclean

run_exercise_1:
	cd ex01 && make && echo "START" && ./ex01

run_exercise_2:
	cd ex02 && make && echo "START" && ./ex02

run_exercise_3:
	cd ex03 && make && echo "START" && ./ex03

run_exercise_4:
	cd ex04 && make && echo "START" && ./ex04

re: fclean all

.PHONY : all clean fclean re
