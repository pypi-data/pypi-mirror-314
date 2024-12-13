CC := g++
CCFLAGS := ${CCFLAGS} -O2 -Wall -Wextra -MMD -fopenmp
LDFLAGS := ${LDFLAGS} -fopenmp
OBJDIR := build
DNNDIR := dnn
BINDIR := bin
TARGET := $(BINDIR)/run_export


INCLUDE_DIRS :=-I. -I./${DNNDIR} -I./${DNNDIR}/include -I./${DNNDIR}/layers -I./${DNNDIR}/parameters
CC_SRCS := $(shell find . -iname "*.cpp")
CC_OBJS := $(patsubst %.cpp, ${OBJDIR}/%.o, ${CC_SRCS})
DEPENDENCIES := $(patsubst %.o, %.d, ${CC_OBJS})

all: build

build: ${CC_OBJS}
	@mkdir -p $(dir ${TARGET})
	${CC} ${CC_OBJS} ${LDFLAGS} -o ${TARGET}

${OBJDIR}/%.o: %.cpp
	@mkdir -p $(dir $@)
	${CC} ${CCFLAGS} ${INCLUDE_DIRS} -c $< -o $@ 

clean:
	if [ -d "$(OBJDIR)" ]; then rm -rf $(OBJDIR); fi
	if [ -d "$(BINDIR)" ]; then rm -rf $(BINDIR); fi


-include $(DEPENDENCIES)
