import std;

void func5() {
    std::filesystem::path bob("path/to/nowhere");
    std::println("Func5: {}", bob.string().length());
}

