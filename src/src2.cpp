#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>

void func2() {
    std::string bob("This is some text.");
    std::unordered_map<std::string, int> m;
    m[bob] = 42;
    std::println("Func2: {}", m[bob]);
}

