import std;

void func6() {
    std::filesystem::path bob("path/to/nowhere");
    std::println("Func6: {}", bob.string().length());
}

