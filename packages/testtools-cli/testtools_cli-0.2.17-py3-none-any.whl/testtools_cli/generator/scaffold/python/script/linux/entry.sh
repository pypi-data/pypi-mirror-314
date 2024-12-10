#! /bin/bash

set -exu -o pipefail

# 检查参数数量
if [ "$#" -ne 2 ]; then
  echo "Usage: bash entry.sh <load|run> <file_path>"
  exit 1
fi

# 获取参数
command="$1"
file_path="$2"

# 检查第一个参数是否为 load 或 run
if [[ "$command" != "load" && "$command" != "run" ]]; then
  echo "Error: The first argument must be 'load' or 'run'."
  exit 1
fi

# 检查第二个参数是否为有效的文件路径
if [ ! -f "$file_path" ]; then
  echo "Error: The file '$file_path' does not exist."
  exit 1
fi

export PYTHONUNBUFFERED=1

# 根据第一个参数执行相应的操作
case "$command" in
load)
  echo "Loading testcase with entry file : $file_path"
  python3 /testtools/replace_____me/src/load.py "$file_path"
  ;;
run)
  echo "Running testcase with entry file: $file_path"
  python3 /testtools/replace_____me/src/run.py "$file_path"
  ;;
esac
