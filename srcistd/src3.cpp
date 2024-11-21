import std;

void func3() {
    std::string bob("This is some text.");
    std::map<std::string, int> m;
    m[bob] = 42;
    std::println("Func3: {}", m[bob]);
}

