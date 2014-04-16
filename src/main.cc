#include <iostream>
#include <v8.h>

using namespace v8;

/*****************************************************************************/
/*!
    \brief  JS callback to print a string.

    Javascript prototype print(value)

    Example:
    \code
    print('Hello world!');
    print(123);
    \endcode
*/
/*****************************************************************************/
void Print(const v8::FunctionCallbackInfo<v8::Value>& args) {
    for (int i =0; i < args.Length(); i++) {
        v8::HandleScope handle_scope(args.GetIsolate());
        v8::String::Utf8Value str(args[i]);
        std::cout << *str;
    }
    printf("\n", NULL);
}

/*****************************************************************************/
/*!
    \brief  JS callback to repeat a string. 

    Javascript prototype: repeat(string, number)

    Example:
    \code
    repeat('I\'m repeating! ', 3);
    \endcode
/*****************************************************************************/
void Repeat(const v8::FunctionCallbackInfo<v8::Value>& args) {
    std::string myStr;
    int count = args[1]->Int32Value();

    for (int i = 0; i < count; i++) {
        v8::HandleScope handle_scope(args.GetIsolate());
        v8::String::Utf8Value str(args[0]);
        myStr += *(str);
    }

    std::cout << myStr.c_str() << std::endl;
}

/*****************************************************************************/
/*!
    \brief  JS callback to add numbers. 

    Javascript prototype: myadd(number, ...)

    Example:
    \code
    myadd(1, 2, 3);
    myadd(4, 5, 6, 7);
    \endcode
*/
/*****************************************************************************/
void Add(const v8::FunctionCallbackInfo<v8::Value>& args) {
    int myVal = 0;
    for (int i =0; i < args.Length(); i++) {
        v8::HandleScope handle_scope(args.GetIsolate());
        myVal += args[1]->Int32Value();
    }
    args.GetReturnValue().Set(v8::Number::New(args.GetIsolate(), myVal));
}

v8::Handle<String> ReadFile(const char* name) {
    // Open the file 
    FILE* file;
    fopen_s(&file, name, "rb");

    // If there is no file, return an empty string.
    if (file == NULL) return v8::Handle<v8::String>();

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

    v8::Handle<v8::String> result = v8::String::NewFromUtf8(Isolate::GetCurrent(), chars, v8::String::kNormalString, size);
    delete[] chars;
    return result;
}

void CreateFunctionsForJS(Handle<v8::Object> global) {
    Isolate *isolate = Isolate::GetCurrent();
    global->Set(v8::String::NewFromUtf8(isolate, "print"), v8::FunctionTemplate::New(isolate, Print)->GetFunction());
    global->Set(v8::String::NewFromUtf8(isolate, "repeat"), v8::FunctionTemplate::New(isolate, Repeat)->GetFunction());
    global->Set(v8::String::NewFromUtf8(isolate, "myadd"), v8::FunctionTemplate::New(isolate, Add)->GetFunction());
}

int main(int argc, char* argv[]) {
    // Get the default Isolate created at startup.	
    Isolate* isolate = Isolate::GetCurrent();

    // Create a stack-allocated handle scope.
    HandleScope handle_scope(isolate);
    
    // Create the global object template 
    Handle<ObjectTemplate> global_template = ObjectTemplate::New();

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

    v8::Handle<v8::String> source = ReadFile(file.c_str());
    if (source.IsEmpty())
    {
        std::cout << "Error reading file" << std::endl;
        std::cout << "Press enter to quit" << std::endl;
        std::cin.get();
        return 0;
    }

    // Compile 
    v8::Handle<v8::Script> script = v8::Script::Compile(source);

    v8::Handle<v8::Value> result;
    for(int i =0; i < n; i++) {
        result = script->Run();
        v8::String::Utf8Value utf8(result);
        std::cout << "Script result: " << *utf8 << std::endl;
    }
    std::cout << "Test completed. Press enty to exit the program.\n";
    std::cin.get();

    return 0;
}