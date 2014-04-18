all: debug release check 

debug: out/Makefile
	$(MAKE) -C out BUILDTYPE=Debug

release: out/Makefile 
	$(MAKE) -C out BUILDTYPE=Release 

check: out/Makefile
	$(MAKE) -C out weyland_tests surtrlog_tests BUILDTYPE=Debug 
	out/Debug/weyland_tests
	out/Debug/surtrlog_tests

clean: 
	-rm out/Makefile weyland weyland_tests out/$(BUILDTYPE)/weyland
	-find out / -name '*.o' -o -name '*.a' | xargs rm -rf

.PHONY: check