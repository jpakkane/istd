import std;

void func7() {
    std::filesystem::path bob("path/to/nowhere");
    std::println("Func7: {}", bob.string().find('8'));
}

