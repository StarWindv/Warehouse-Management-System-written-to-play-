import os
import time
import shutil
import datetime
import requests
import re
from bs4 import BeautifulSoup
import subprocess
import sys

# 结构定义
class InventoryItem:
    def __init__(self, name, quantity, last_modified, modified_by):
        self.name = name
        self.quantity = quantity
        self.last_modified = last_modified
        self.modified_by = modified_by  # 记录修改用户名

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

RED = "\033[31m"
GOLD = "\033[33m"
BLUE = "\033[34m"
ENDC = "\033[0m"

# 配置
SERVER_URL = "http://minecraftx.ticp.io/一些自己写的代码/cgxt/"
LOCAL_VERSION_FILE = "/count/version.txt"
UPDATE_DIR = "/"
def get_local_version():
    """获取本地版本号"""
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, 'r') as file:
        return file.read().strip()

def get_server_version():
    """从服务器获取最新版本号"""
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            files = response.text.split()
            version_pattern = re.compile(r'v(\d+\.\d+\.\d+)')
            versions = [version_pattern.search(file).group(1) for file in files if version_pattern.search(file)]
            if versions:
                return max(versions, key=lambda v: tuple(map(int, v.split('.'))))
    except Exception as e:
        print(f"获取服务器版本号时发生错误: {e}")
    return None

def download_update(server_version):
    """从服务器下载更新"""
    try:
        file_name = f"仓库.v{server_version}.py"
        file_url = os.path.join(SERVER_URL, file_name)
        file_path = os.path.join(UPDATE_DIR, file_name)
        response = requests.get(file_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            code_content = soup.find('code', {'contenteditable': 'true'}).text
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(code_content)
            return file_path
    except Exception as e:
        print(f"下载更新时发生错误: {e}")
    return None

def delete_old_versions(current_version):
    version_pattern = re.compile(r'v(\d+\.\d+\.\d+)')
    for file_name in os.listdir():
        if version_pattern.search(file_name):
            file_version = version_pattern.search(file_name).group(1)
            if file_version < current_version:
                os.remove(file_name)
                print(f"旧版本{file_name}已删除")



def perform_update():
    """执行更新流程"""
    local_version = get_local_version()
    server_version = get_server_version()

    if server_version and (local_version is None or server_version > local_version):
        print(f"发现新版本: {server_version}，正在下载更新...")
        downloaded_file = download_update(server_version)
        if downloaded_file:
            print("下载完成")
            with open(uc_count_file, 'w', encoding='utf-8') as file:
        	    file.write('')
            with open(LOCAL_VERSION_FILE, 'w') as file:
                file.write(server_version)
                subprocess.Popen([sys.executable, __file__])
        else:
            print("下载更新失败。")
    else:
        print("当前已是最新版本。")

global new_username
new_username = 0

# 文件路径
internal_dir = "source"
count_dir="count"
username_file = os.path.join(internal_dir, "usernames.txt")
password_file = os.path.join(internal_dir, "passwords.txt")
admin_file = os.path.join(internal_dir, "admins.txt")
ram_file = os.path.join(internal_dir, "ram.txt")
uc_count_file = os.path.join(count_dir, "count.txt")
sum_counter_file = os.path.join(count_dir,"sum_count.txt")

#shutil.rmtree(count_dir) #用于清空计数器
# 获取当前时间
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_file(dir,filename,information): #创建文件
    if not os.path.exists(dir):
        os.makedirs(dir)
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(information)
            file.close()
    elif not os.path.exists(filename):
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(information)
            file.close()
    else:
        pass


def increment_counter(): #用于计数
    create_file(count_dir,sum_counter_file,'0')
    create_file(count_dir,uc_count_file,'0')
            
    with open(sum_counter_file, 'r+') as sum_count_file:
        counter = int(sum_count_file.read())
        sum_count_file.seek(0)
        sum_count_file.write(str(counter + 1))
        sum_count_file.truncate()

    with open(uc_count_file, 'r+') as uc_file:
        counter = int(uc_file.read())
        uc_file.seek(0)
        uc_file.write(str(counter + 1))
        uc_file.truncate()

def check_counter(): #获取计数器数据
    with open(sum_counter_file, 'r') as f:
        sum_counter = int(f.read())
    with open(uc_count_file, 'r') as f:
        uc_counter = int(f.read())
        return sum_counter,uc_counter

# 加载数据库
def load_inventory(filename):
    inventory = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:  # 使用 UTF-8 编码
            lines = file.readlines()
            for line in lines:
                name, quantity, last_modified, modified_by = line.strip().split(',')
                inventory[name] = InventoryItem(name, int(quantity), last_modified, modified_by)
    return inventory

# 保存数据到文件
def save_inventory(filename, inventory):
    with open(filename, 'w', encoding='utf-8') as file:  # 使用 UTF-8 编码
        for item in inventory.values():
            file.write(f"{item.name},{item.quantity},{item.last_modified},{item.modified_by}\n")

#替换文件，以做到清空的目的
def instead_file(folder_path,required_files):
    shutil.rmtree(folder_path)
    print(f"文件夹 {folder_path} 已清除，正在重建中...")
    os.makedirs(folder_path)
    for file_name in required_files:
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            print(f"创建文件 {file_path}...")
            creat_file(file_path)
    print("已初始化人员名单\n")

def creat_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('Adminstrator\n')  # 创建
    with open(admin_file, 'w', encoding='utf-8') as file:
        file.write('')  # 清空admins.txt文件内容
        file.close()
    with open(admin_file, 'w', encoding='utf-8') as file:
        file.write('Adminstrator,Adminstrator\n')

def refile(folder_path,required_files):
    for file_name in required_files:
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            print(f"创建文件 {file_path} 中...")
            creat_file(file_path)
        else:
            return False
            
# 加载用户名和密码
def load_credentials(username_file, password_file):
    usernames = {}
    passwords = {}
    if os.path.exists(username_file) and os.path.exists(password_file):
        with open(username_file, 'r', encoding='utf-8') as user_file, open(password_file, 'r', encoding='utf-8') as pass_file:  # 使用 UTF-8 编码
            user_lines = user_file.readlines()
            pass_lines = pass_file.readlines()
            for i, line in enumerate(user_lines):
                usernames[line.strip()] = pass_lines[i].strip()
            pass_file.close()
    return usernames, passwords

# 加载管理员
def load_admins(admin_file):
    admins = []
    if os.path.exists(admin_file):
        with open(admin_file, 'r',encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(',')
                admins.append(Admin(username, password))
            file.close()
    return admins
    
#用户登陆
def login(usernames, admins):
    global current_user, new_username  # 声明为全局变量
    username = input("请输入用户名: ")
    if username == "STv" or username == "stv":
        username = 'StarWindv'
        new_username = username
    if username == "StarWindv":
        #password = input("请输入密码: ")
        #if password == "awsd":
            print("登录成功！\n")
            current_user = username  # 记录当前用户名
            return True, any(admin.username == username for admin in admins)  # 返回是否为管理员
        #else:
            #print(RED + "###输入错误，请检查您的输入###" + ENDC)
    elif username in usernames:
        password = input("请输入密码: ")
        if usernames[username] == password:
            print("登录成功！\n")
            current_user = username  # 记录当前用户名
            return True, any(admin.username == username for admin in admins)  # 返回是否为管理员
        else:
            print("密码错误！")
    else:
        print("用户名不存在！")
    return False, False

# 注册新用户
def register_user(usernames, passwords):
    username = input("请输入用户名: ")
    if username in usernames or username == "StarWindv" or username == "STv" or username == "stv":
        print("用户名已存在，请选择其他用户名。")
        return
    password = input("请输入密码: ")
    if current_user == "StarWindv":
        level=input("请输入用户权限\n\t1.普通用户\n\t2.管理员用户\n\t")
        if level == '1':
            pass
        elif level == '2':
            with open(admin_file,"a",encoding="utf-8") as admin_file_txt:
                admin_file_txt.write(username + "," + password + '\n')
    usernames[username] = password
    passwords[username] = password
    save_credentials(username_file, password_file, usernames, passwords)
    print(RED + "###用户注册成功###\n" + ENDC)

# 保存用户名和密码
def save_credentials(username_file, password_file, usernames, passwords):
    with open(username_file, 'w', encoding="utf-8") as user_file, open(password_file, 'w', encoding="utf-8") as pass_file:
        for username in usernames:
            user_file.write(username + '\n')
            pass_file.write(usernames[username] + '\n')
        pass_file.close()
        user_file.close()
        
def head(current_user):
    list_admins = load_admins(admin_file)
    is_admin = False
    if current_user in [admin.username for admin in list_admins] and current_user != 'StarWindv':
        is_admin = True
    if current_user == "StarWindv":
        quanxian = "王座"
    elif is_admin:
        quanxian = "权杖"
    else:
        quanxian = "护法"
    if current_user != 'StarWindv':
        print(f"当前登录用户:{current_user}\n用户权限: {quanxian}\n\n\t仓库管理系统")
    else:
        print(GOLD + f"当前登录用户:{current_user}\n用户权限: {quanxian}\n\n\t" + ENDC + "仓库管理系统")

def upgrade_log(version,upgrade_information):
    if not os.path.exists(read_me_path):
        with open(read_me_path,"w",encoding="utf-8") as readfile:
            readfile.write(f"[v{version}更新日志]{upgrade_information}")
    elif os.path.exists(read_me_path):
        with open(read_me_path,"r",encoding="utf-8") as readfile:
            be_read_file = readfile.read()
            if upgrade_information not in be_read_file:
                with open(read_me_path,"a",encoding="utf-8") as readfile:
                    readfile.write(f"\n\nv{version}[更新日志]{upgrade_information}")
                    print(RED + "###更新日志已同步###" + ENDC)
                    os.remove(uc_count_file)
            else:
                pass
    else:
        pass

    increment_counter()  # 增加计数器
    sum_count,uc_count = check_counter() # 检查计数器
    if uc_count == 1:
        print(f"v{version}[更新日志]{upgrade_information}")
        print("\n您可以在 ./read_me.txt 中查看本次更新日志\n")
    if os.path.exists(ram_file):
        os.remove(ram_file)
    print(f"你已经启动本系统 {sum_count} 次了")
    print(f"这是你在更新后第 {uc_count} 次使用本系统\n")

required_files = ['admins.txt', 'usernames.txt', 'passwords.txt', 'ram.txt']

# 主程序
def main():
    usernames, passwords = load_credentials(username_file, password_file)
    admins = load_admins(admin_file)

    inside_while = False
    login_while = True
    upgrade_log(version, upgrade_information)

    while True:
        while login_while:
            print("\n\t登录系统")
            print("\t1. 登录")
            print("\t2. 退出")
            choice = input("\t请选择操作(1/2): \n\t")

            if choice == '1':
                is_logged_in, is_admin = login(usernames, admins)
                if is_logged_in:
                    inside_while = True
                    break  # 跳出登录循环
            elif choice == '2':
                print("退出系统。")
                break
            else:
                print("无效的选项，请重新选择。")
        if choice == '2':
            break
        if new_username == 'StarWindv' or current_user in [admin.username for admin in admins]:
            is_admin = True

        if is_logged_in:
            inventory_file = "inventory.txt"
            inventory = load_inventory(inventory_file)

            while inside_while:
                #print(f"登录用户: {current_user}, 是否为管理员: {is_admin}")
                head(current_user)
                print("\t1. 项目管理")
                print("\t2. 增加项目")
                if is_admin:
                    print(RED + "\t3. 注册新用户" + ENDC)
                    print("\t4. 登出")
                    print("\t5. 员工名单")
                    if current_user == "StarWindv":
                        print(GOLD + "\t6. 清空用户" + ENDC)
                        print(f'version:{current_version}\n')
                        choice = input("\t请选择操作(1/2/3/4/5/6): \n\t")
                        print("\n")
                    else:
                        print(f'version:{current_version}\n')
                        choice = input("\t请选择操作(1/2/3/4/5): \n\t")
                        print("\n")
                else:
                    print("\t3. 登出")
                    print("\t4. 员工名单")
                    print(f'version:{current_version}\n')
                    choice = input("\t请选择操作(1/2/3/4): \n\t")
                    print("\n")

                point1=0
                if choice == '3' and not is_admin:
                    choice = '4'
                    point1 = 1 # 如果不是管理员，则跳过注册选项
                if choice == '4' and not is_admin and point1 == 0:
                    choice = "5"
                point1 = 0 # 重定义检查点

                if choice == '1':
                    # 项目管理
                    if not inventory:
                        print(RED + "\n###没有项目。请先增加项目###" + ENDC)
                    else:
                        print("\n当前所有物品的名称、数量、最后修改时间和修改用户:\n")
                        for item in inventory.values():
                            print(
                                f"\t名称: {item.name}\n\t数量: {item.quantity}\n\t最后修改时间: {item.last_modified}\n\t修改用户: {item.modified_by}\n")

                        print("\n\t请选择要操作的项目(输入数字):")
                        for i, item in enumerate(inventory.values()):
                            print(f"\t{i + 1}. {item.name}")
                        choice = input("\n请选择(1-N): ")
                        if choice.isdigit() and 1 <= int(choice) <= len(inventory):
                            selected_item = list(inventory.values())[int(choice) - 1]
                            print(
                                f"\n选择的物品: {selected_item.name}, 当前数量: {selected_item.quantity}, 最后修改时间: {selected_item.last_modified}, 修改用户: {selected_item.modified_by}")

                            # 提供新选项
                            action_choice = input("\n\t请选择操作:\n\t1. 修改数量\n\t2. 删除项目\n\t")
                            if action_choice == '1':
                                new_quantity_input = input(
                                    "请输入新的数量(可以是+N增加，-N减少，或直接输入新数量替换): \n\t")
                                if new_quantity_input.startswith('+') or new_quantity_input.startswith('-'):
                                    try:
                                        change_amount = int(new_quantity_input[1:])  # 提取数字部分
                                        selected_item.quantity += change_amount if new_quantity_input.startswith(
                                            '+') else -change_amount
                                    except ValueError:
                                        print("\n无效的数量输入，请确保输入的是有效的数字。\n")
                                else:
                                    try:
                                        selected_item.quantity = int(new_quantity_input)
                                    except ValueError:
                                        print("\n无效的数量输入，请确保输入的是有效的数字。\n")

                                selected_item.last_modified = get_current_time()
                                selected_item.modified_by = current_user  # 记录当前用户名
                                save_inventory(inventory_file, inventory)
                                print("更新成功!")
                            elif action_choice == '2':
                                delete_choice = input("\t是否删除该项目?(y/n): ").lower()
                                if delete_choice == 'y':
                                    del inventory[selected_item.name]
                                    save_inventory(inventory_file, inventory)
                                    print("项目已删除!\n")
                            else:
                                print("无效的选项，请重新选择。\n")

                elif choice == '2':
                    # 增加项目
                    name = input("\n请输入物品名称: ")
                    quantity = input("\n请输入物品数量: ")
                    if name and quantity.isdigit():
                        new_item = InventoryItem(name, int(quantity), get_current_time(), current_user)  # 传递current_user作为modified_by参数
                        inventory[name] = new_item
                        save_inventory(inventory_file, inventory)
                        print("\n项目已添加!")
                elif choice == '3' and is_admin:
                    register_user(usernames, passwords)
                elif choice == '4':
                    print("退出登录。")
                    inside_while = False
                    is_logged_in = False
                    #break
                elif choice == '5':
                    print("\n员工名单:")
                    usernames, passwords = load_credentials(username_file, password_file)
                    list_admins = load_admins(admin_file)
                    for admin in list_admins:
                        print(f"\t用户名: {admin.username}")
                        if admin.username == 'StarWindv':
                            print("\t权限等级: " + GOLD + "王座\n" + ENDC)
                        else:
                            print("\t权限等级: " + RED + "权杖\n" + ENDC)
                    for username in usernames:
                        if username not in [admin.username for admin in list_admins] and username != 'StarWindv':
                            print(f"\t用户名: {username}")
                            print("\t权限等级: 护法\n")
                elif choice == "6" and current_user == "StarWindv":
                    instead_file(folder_path,required_files)

if __name__ == "__main__":
    folder_path = 'source'
    read_me_path = os.path.join("read_me.txt")

    version = get_local_version()

    upgrade_information = "\n\n1.在这个版本，我们成功做到了热更新！\n不对，我为什么要说们？\n......唯一开发人员：星灿长风v\n\tstarwindv@qq.com"

# 文件夹
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在。创建中...")
        os.makedirs(folder_path)

# 检查 创建
    bool = refile(folder_path,required_files)
    if bool != True:
        for file_name in required_files:
            print(f"文件 {file_name} 已存在")

    perform_update()
    current_version = get_local_version()
    print(f"当前版本: {current_version}")

    try:
        delete_old_versions(current_version)
    except:
        pass
    main()



