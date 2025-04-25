import os

extensions = ['.py']

def count_lines_in_file(file_path):
    count = 0
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if line.strip():
                count += 1
    return count

def walk_through_folders(root_folder):
    total_lines = 0
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                lines_count = count_lines_in_file(file_path)
                total_lines += lines_count
                print(f"文件：{file_path} --> 行数：{lines_count}")
    return total_lines

if __name__ == "__main__":
    root_folder = '.'
    total_lines = walk_through_folders(root_folder)
    print(f"\nPython源文件总有效代码行数：{total_lines}")
