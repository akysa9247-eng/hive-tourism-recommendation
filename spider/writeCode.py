import os

# 路径A，替换为你的实际路径
path_A = 'C:/Users/allen/Desktop/大数据203班-202010274304-曾利伟-毕设材料-完整版/大数据203班-202010274304-曾利伟-代码/2、数据科学与大数据技术203班-202010274304-曾利伟-毕设论文源程序打包文件/数仓sql'

# 输出的.txt文件名
output_txt = 'sql.txt'

# 确保输出文件是空的（如果已存在）
with open(output_txt, 'w') as f:
    f.write('')

# 遍历路径A下的所有文件和子目录
for root, dirs, files in os.walk(path_A):
    for file in files:
        # 检查文件扩展名是否为.py或.html
        if file.endswith('.sql'):
            # 文件的完整路径
            file_path = os.path.join(root, file)

            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # 将文件名和内容写入到输出文件中
                with open(output_txt, 'a', encoding='utf-8') as out_f:
                    out_f.write(f"==== {file} ====\n")
                    out_f.write(f.read())
                    out_f.write('\n\n')  # 添加两个换行符以便分隔不同的文件内容

print(f"所有文件内容已写入到 {output_txt}")