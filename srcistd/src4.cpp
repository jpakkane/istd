import std;

void func4() {
    std::string bob("This is some text.");
    std::vector<std::string> arr;
    arr.push_back(bob);
    std::println("Func4: {}", arr.size());
}

