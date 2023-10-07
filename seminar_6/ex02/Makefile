NAME = ex02

SRC = $(wildcard *.cpp)

OBJ = $(SRC:.cpp=.o)

CPP = c++

all: $(NAME)

.cpp.o:
	$(CPP) -c $< -o $@ -fopenmp

$(NAME): $(OBJ)
	$(CPP) -o exercise_2_sequential exercise_2_sequential.o -fopenmp
	$(CPP) -o exercise_2_for exercise_2_for.o -fopenmp
	$(CPP) -o exercise_2_task exercise_2_task.o -fopenmp

re:	fclean $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f exercise_2_sequential
	rm -f exercise_2_for
	rm -f exercise_2_task

.PHONY: all clean fclean re