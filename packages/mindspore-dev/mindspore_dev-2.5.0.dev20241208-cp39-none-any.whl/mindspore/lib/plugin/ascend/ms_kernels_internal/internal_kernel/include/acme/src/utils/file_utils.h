/**
 * Copyright 2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_FILE_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_FILE_UTILS_H_

#include <iostream>
#include <dirent.h>
#include <sys/stat.h>
#include <dlfcn.h>
#include <cstring>
#include <climits>
#include "utils/log/log.h"

namespace mindspore {
namespace acme {
inline std::string BuildPathFromStrings(const std::vector<std::string> &strings) {
  if (strings.empty()) {
    return "";
  }
  std::stringstream ss;
  ss << strings[0];
  for (auto i = 1; i < strings.size(); i++) {
    ss << "/" << strings[i];
  }

  return ss.str();
}

inline bool IsRegularFile(const std::string &file_name) {
  struct stat st;
  if (stat(file_name.c_str(), &st) < 0) {
    MSOP_LOG(ERROR) << "Failed to stat file, file_path: " << file_name;
    return false;
  }

  return S_ISREG(st.st_mode);
}

inline bool IsDir(const std::string &file_name) {
  struct stat st;
  if (stat(file_name.c_str(), &st) < 0) {
    MSOP_LOG(ERROR) << "Failed to stat file, file_path: " << file_name;
    return false;
  }

  return S_ISDIR(st.st_mode);
}

inline std::string GetBaseFileName(const std::string &full_path) {
  auto pos = full_path.find_last_of("/");
  auto start_pos = pos == std::string::npos ? 0 : pos + 1;
  return full_path.substr(start_pos);
}

inline bool IsEndWith(const std::string &path_name, const std::string &suffix) {
  if (path_name.size() < suffix.size()) {
    return false;
  }

  if (path_name.substr(path_name.size() - suffix.size()) != suffix) {
    return false;
  }

  return true;
}

inline bool IsStartWith(const std::string &path_name, const std::string &prefix) {
  auto new_path_name = GetBaseFileName(path_name);
  if (new_path_name.size() < prefix.size()) {
    return false;
  }

  if (new_path_name.substr(0, prefix.size()) != prefix) {
    return false;
  }

  return true;
}

inline bool IsSymLink(const std::string &path_name) {
  struct stat st;
  if (lstat(path_name.c_str(), &st) != 0) {
    MSOP_LOG(ERROR) << "Failed to lstat file: " << path_name;
    return false;
  }
  return S_ISLNK(st.st_mode);
}

inline size_t GetFileSize(const std::string &path_name) {
  struct stat st;
  if (stat(path_name.c_str(), &st) < 0) {
    MSOP_LOG(ERROR) << "Failed to stat file, file_path: " << path_name;
    return 0;
  }

  return st.st_size;
}

std::string GetRealPath(const std::string &path_name);
std::vector<std::string> GetSubItemsInPath(const std::string &path_name, bool is_dir_type);
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_FILE_UTILS_H_