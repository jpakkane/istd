#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>
#include<regex>

void func10() {
    std::regex rg("a+b");
    std::println("Func10: {}", std::regex_search("bbbbba", rg) ? 1 : 0);
}

