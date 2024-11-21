#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>

void func3() {
    std::string bob("This is some text.");
    std::map<std::string, int> m;
    m[bob] = 42;
    std::println("Func3: {}", m[bob]);
}

