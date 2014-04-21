/******************************************************************************/
/*!
 * @file	main.cc
 * @brief	Defines the main entry point for the Weyland application.
 */
/******************************************************************************/
#include <iostream>
#include <v8.h>
#include "surtrlog/surtrlog.h"
#include "weyland/version.h"

using namespace v8;

/*****************************************************************************/
/*!
    @brief  JS callback to print a string.

    Javascript prototype print(value)

    Example:
    @code
    print('Hello world!');
    print(123);
    @endcode
*/
/*****************************************************************************/
void Print(const v8::FunctionCallbackInfo<v8::Value>& args) {
    for (int i =0; i < args.Length(); i++) {
        v8::HandleScope handle_scope(args.GetIsolate());
        v8::String::Utf8Value str(args[i]);
        std::cout << *str;
    }
    std::cout << std::endl;
}

/******************************************************************************/
/*!
 * @brief	Reads a file into a string.
 */
/******************************************************************************/
std::string ReadFile(const char* name) {
    // Open the file 
    FILE* file = fopen(name, "rb");

    // If there is no file, return an empty string.
    if (file == NULL) return std::string("");

    // Set the pointer to the end of the file
    fseek(file, 0, SEEK_END);

    // Get the size of the file
    int size = ftell(file);

    // Rewind the pointer to the beginning of the stream
    rewind(file);

    // Set up and read into the buffer 
    char* chars = new char[size + 1];
    chars[size] = '\0';
    for (int i =0; i < size;) {
        int read = static_cast<int>(fread(&chars[i], 1, size - i, file));
        i += read;
    }

    // Close the file 
    fclose(file);

    std::string result(chars);
    delete[] chars;
    return result;
}

void CreateFunctionsForJS(Handle<v8::Object> global) {
    Isolate *isolate = Isolate::GetCurrent();
    global->Set(v8::String::NewFromUtf8(isolate, "print"), v8::FunctionTemplate::New(isolate, Print)->GetFunction());
}

int main(int argc, char* argv[]) {
	surtrlog::Logger logger;
	logger.Log<surtrlog::Info>() << "Weyland version " << weyland::Version << surtrlog::endl;

    // Get the default Isolate created at startup.	
    Isolate* isolate = Isolate::GetCurrent();

    // Create a stack-allocated handle scope.
    HandleScope handle_scope(isolate);
    
    // Create a new context 
    Local<Context> context = Context::New(isolate);

    // Enter the context for compiling and running the hello world script.
    Context::Scope context_scope(context);

    Handle<v8::Object> global = context->Global();
    CreateFunctionsForJS(global);

    std::string file = argv[1];
    std::cout << "How many times do you want to run the script? \n" << std::endl;
    int n;
    std::cin >> n;
    std::cout << "" << std::endl;
    std::cin.get();

    std::string source = ReadFile(file.c_str());
    if (source.empty())
    {
    	logger.Log<surtrlog::Error>() << "Error reading file";
        std::cout << "Press enter to quit" << std::endl;
        std::cin.get();
        return 0;
    }

    // Compile 
    v8::Handle<v8::Script> script = v8::Script::Compile(
    		String::NewFromUtf8(isolate, source.c_str()));

    v8::Handle<v8::Value> result;
    for(int i =0; i < n; i++) {
        result = script->Run();
        v8::String::Utf8Value utf8(result);
        logger.Log<surtrlog::Info>() << "Script result: " << *utf8 << "\n";
    }
    std::cout << "Test completed. Press enter to exit the program.\n";
    std::cin.get();

    return 0;
}
