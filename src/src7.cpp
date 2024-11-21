#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>

void func7() {
    std::filesystem::path bob("path/to/nowhere");
    std::println("Func7: {}", bob.string().find('8'));
}

