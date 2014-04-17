devenv weyland.sln /Build Debug
devenv weyland.sln /Build Release
devenv deps\surtrlog\surtrlog.sln /Build Debug 
devenv deps\surtrlog\surtrlog.sln /Build Release 

Debug\weyland_tests.exe
deps\surtrlog\Debug\surtrlog_tests.exe