#pragma once

#include "../config.hpp"

#include <filesystem>
#include <string>

namespace nw {

/// Gets the complete suffix of a file name, i.e. "archive.tar.gz" -> "tar.gz"
String complete_file_suffix(const String& filename);

/// Gets user's documents path
std::filesystem::path documents_path();

/// Gets user's home path
std::filesystem::path home_path();

/// Creates randomly named folder in tmp.  Analguous to POSIX ``mkdtemp``.
std::filesystem::path create_unique_tmp_path();

/// Expands path with ~ and environment variables
std::filesystem::path expand_path(const std::filesystem::path& path);

/// Copies and deletes a file to a new location, overwrites existing
bool move_file_safely(const std::filesystem::path& from, const std::filesystem::path& to);

/// Converts path to utf8 string
String path_to_string(const std::filesystem::path& path);

} // namespace nw
