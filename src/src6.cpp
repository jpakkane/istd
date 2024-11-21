#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>

void func6() {
    std::filesystem::path bob("path/to/nowhere");
    std::println("Func6: {}", bob.string().length());
}

