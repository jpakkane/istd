import std;

void func2() {
    std::string bob("This is some text.");
    std::unordered_map<std::string, int> m;
    m[bob] = 42;
    std::println("Func2: {}", m[bob]);
}

