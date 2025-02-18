import os
from shutil import copy, rmtree
import random

# 创建文件夹
def mk_file(file_path: str):
    if os.path.exists(file_path):
        # 如果文件夹存在，则先删除原文件夹在重新创建
        rmtree(file_path)
    os.makedirs(file_path)

def main():
    # 保证随机可复现
    random.seed(0)

    # 将数据集中10%的数据划分到验证集中，即训练集：验证集 = 9：1
    split_rate = 0.1

    # 指向你解压后的flower_photos文件夹
    cwd = os.getcwd() # 获取当前工作目录
    data_root = os.path.join(cwd, "flower_data")
    origin_flower_path = os.path.join(data_root, "flower_photos")
    assert os.path.exists(origin_flower_path), "path '{}' does not exist.".format(origin_flower_path)

    flower_class = [cla for cla in os.listdir(origin_flower_path)
                    if os.path.isdir(os.path.join(origin_flower_path, cla))] # 提取所有花卉类别的名称

    # 建立保存训练集的文件夹
    train_root = os.path.join(data_root, "train")
    mk_file(train_root)
    for cla in flower_class:
        # 建立每个类别对应的文件夹
        mk_file(os.path.join(train_root, cla))

    # 建立保存验证集的文件夹
    val_root = os.path.join(data_root, "val")
    mk_file(val_root)
    for cla in flower_class:
        # 建立每个类别对应的文件夹
        mk_file(os.path.join(val_root, cla))

    for cla in flower_class:
        cla_path = os.path.join(origin_flower_path, cla)
        images = os.listdir(cla_path)
        num = len(images)
        # 随机抽取 num*split_rate 张图像的索引作为验证集图像索引
        eval_index = random.sample(images, k=int(num*split_rate))

        # 对每个图像（image）进行遍历，如果它是验证集中的图像（即其文件名在 eval_index 中），就将该图像复制到验证集相应类别的文件夹中
        # 否则复制到训练集相应类别的文件夹中
        for index, image in enumerate(images):
            if image in eval_index:
                # 将分配至验证集中的文件复制到相应目录
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(val_root, cla)
                copy(image_path, new_path)
            else:
                # 将分配至训练集中的文件复制到相应目录
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(train_root, cla)
                copy(image_path, new_path)
            print("\r[{}] processing [{}/{}]".format(cla, index+1, num), end="")  # processing bar
        print()

    print("processing done!")

if __name__ == '__main__':
    main()