import std;

void func10() {
    std::regex rg("a+b");
    std::println("Func10: {}", std::regex_search("bbbbba", rg) ? 1 : 0);
}

