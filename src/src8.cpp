#include<iostream>
#include<filesystem>
#include<unordered_map>
#include<vector>
#include<map>
#include<string>
#include<print>
#include<source_location>

void func8() {
    std::println("Func8: {}", std::source_location::current().file_name());
}

