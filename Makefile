CC = gcc
CXX = g++

CFLAGS = -g $(INCLUDES)
CXXFLAGS = -g $(INCLUDES)
INCLUDES = 
TARGET = advent

day = 0
BIN = bin
SRC_DIR = Day$(day)
inc_dir = include
lib_dir = lib

TARGET_BASE = out
TARGET = $(TARGET_BASE)$(day)
# Generate only if not clean. Otherwise produces error messages b/c of Day0
ifneq (clean,$(filter clean,$(MAKECMDGOALS)))
	CPP_SRC = $(shell find $(SRC_DIR) -type f -name "*.cpp")
	C_SRC = $(shell find $(SRC_DIR) -type f -name "*.c")
	SRC_OBJS = $(CPP_SRC:.cpp=.o) $(C_SRC:.c=.o)
	OBJS = $(patsubst $(SRC_DIR)/%,$(BIN)/%,$(SRC_OBJS))
endif

all: $(TARGET)

$(BIN)/%.o: $(SRC_DIR)/%.cpp 
	@mkdir -p $(@D)
	$(CXX) -c $(CXXFLAGS) -o $@ $<

$(BIN)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(@D)
	$(CC) -c $(CFLAGS) -o $@ $<

$(TARGET): $(OBJS)
	$(CXX) -o $@ $^ $(LDFLAGS)
	./$(TARGET)

.PHONY : clean
clean :
	$(RM) $(BIN)/*
	$(RM) $(TARGET_BASE)*
