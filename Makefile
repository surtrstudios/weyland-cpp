all: debug release check 

debug: out/Makfile
	$(MAKE) -C out BUILDTYPE=Debug

release: out/Makefile 
	$(MAKE) -C out BUILDTYPE=Release 

check: out/Makefile
	$(MAKE) -C out weyland_tests surtrlog_tests BUILDTYPE=Debug 
	out/Debug/weyland_tests
	out/Debug/surtrlog_tests

.PHONY: check