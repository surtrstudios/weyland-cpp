all: debug release check 

NPROC = $(shell nproc)

debug: out/Makefile
	$(MAKE) -C out BUILDTYPE=Debug -j $(NPROC)

release: out/Makefile 
	$(MAKE) -C out BUILDTYPE=Release -j $(NPROC)

check: out/Makefile
	$(MAKE) -C out weyland_tests surtrlog_tests BUILDTYPE=Debug -j $(NPROC) 
	out/Debug/weyland_tests
	out/Debug/surtrlog_tests

clean: 
	-rm out/Makefile weyland weyland_tests out/$(BUILDTYPE)/weyland
	-find out / -name '*.o' -o -name '*.a' | xargs rm -rf

.PHONY: check