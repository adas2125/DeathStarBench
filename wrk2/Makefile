CFLAGS  := -std=c99 -Wall -O2 -D_REENTRANT
LIBS    := -lpthread -lm -lcrypto -lssl

TARGET  := $(shell uname -s | tr '[A-Z]' '[a-z]' 2>/dev/null || echo unknown)

ifeq ($(TARGET), sunos)
	CFLAGS += -D_PTHREADS -D_POSIX_C_SOURCE=200112L
	LIBS   += -lsocket
else ifeq ($(TARGET), darwin)
	# LuaJIT's macOS build expects this to be set. Default to host major.minor.
	MACOSX_DEPLOYMENT_TARGET ?= $(shell sw_vers -productVersion 2>/dev/null | awk -F. '{print $$1 "." $$2}')
	export MACOSX_DEPLOYMENT_TARGET
	# Prefer Homebrew OpenSSL locations on Apple Silicon and Intel Macs.
	OPENSSL_PREFIX ?= $(shell \
		if [ -d /opt/homebrew/opt/openssl@3 ]; then echo /opt/homebrew/opt/openssl@3; \
		elif [ -d /usr/local/opt/openssl@3 ]; then echo /usr/local/opt/openssl@3; \
		fi)
ifneq ($(OPENSSL_PREFIX),)
	CFLAGS  += -I$(OPENSSL_PREFIX)/include
	LDFLAGS += -L$(OPENSSL_PREFIX)/lib
endif
else ifeq ($(TARGET), linux)
        CFLAGS  += -D_POSIX_C_SOURCE=200112L -D_BSD_SOURCE
	LIBS    += -ldl
	LDFLAGS += -Wl,-E
else ifeq ($(TARGET), freebsd)
	CFLAGS  += -D_DECLARE_C99_LDBL_MATH
	LDFLAGS += -Wl,-E
endif

SRC  := wrk.c net.c ssl.c aprintf.c stats.c script.c units.c \
		ae.c zmalloc.c http_parser.c tinymt64.c hdr_histogram.c
BIN  := wrk

ODIR := obj
OBJ  := $(patsubst %.c,$(ODIR)/%.o,$(SRC))

LDIR     = deps/luajit/src
LIBS    := -lluajit $(LIBS)
CFLAGS  += -I$(LDIR)
CFLAGS  += -DWRK_LUA_PATH='"$(CURDIR)/src/wrk.lua"'
LDFLAGS += -L$(LDIR)

all: $(BIN)

clean:
	$(RM) $(BIN) obj/*
	@$(MAKE) -C deps/luajit clean
	rm -f attempted_requests.txt arrivals.csv
	rm -rf output/
	rm sweep.log sweep.pid

$(BIN): $(OBJ)
	@echo LINK $(BIN)
	@$(CC) $(LDFLAGS) -o $@ $^ $(LIBS)

$(OBJ): config.h Makefile $(LDIR)/libluajit.a | $(ODIR)

$(ODIR):
	@mkdir -p $@

$(ODIR)/%.o : %.c
	@echo CC $<
	@$(CC) $(CFLAGS) -c -o $@ $<

$(LDIR)/libluajit.a:
	@echo Building LuaJIT...
	@$(MAKE) -C $(LDIR) BUILDMODE=static

.PHONY: all clean
.SUFFIXES:
.SUFFIXES: .c .o .lua

vpath %.c   src
vpath %.h   src
vpath %.lua scripts

install:
	cp wrk /usr/local/bin
