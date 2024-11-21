#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>

void func5() {
    std::filesystem::path bob("path/to/nowhere");
    std::println("Func5: {}", bob.string().length());
}

