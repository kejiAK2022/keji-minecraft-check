# Minecraft 账户验证系统

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://www.gnu.org/graphics/gplv3-rounded-red-180x60.jpg)

本工具用于批量验证 Minecraft 账户有效性，支持 Mojang 和 OptiFine 双平台验证，提供代理支持和可视化操作界面。

## 功能特性

- 🛡️ 双平台验证
  - Mojang 账户有效性检测
  - OptiFine 账户有效性检测
- 🌐 网络代理支持
  - HTTP/HTTPS/SOCKS 代理
  - 自动代理轮换
- 📁 文件管理
  - 自动保存有效账户
  - 支持中文路径
- 📊 可视化界面
  - 实时验证进度
  - 表格化结果展示
  - 执行耗时统计

## 快速开始

### 环境要求
- Python 3.11+
- 网络连接（可访问 https://optifine.net）

### 安装步骤
```bash
# 克隆仓库
git clone https://github.com/yourusername/minecraft-account-verifier.git
```

### 安装依赖
```bash
python -m pip install mojang
pip install -r requirements.txt
```

## 账户文件格式
创建 `accounts.txt`：

```plaintext
# 格式：邮箱:密码
valid_account@example.com:password123
invalid_account@test.com:wrongpassword
```

## 代理文件格式（可选）
创建 `proxy.txt`：

```plaintext
http://user:pass@127.0.0.1:8080
socks5://192.168.1.100:1080
```

## 使用说明

运行以下命令启动程序：

```bash
python main.py
```

### 控制台交互流程

```plaintext
[是否使用代理？(Y/N)] > y
[请输入代理文件路径] > proxies.txt
[拖放账户文件或输入路径] > accounts.txt
```

### 功能演示
验证界面示例：

```plaintext
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

╔══════════════════════════════════════════════════════╗
│                Minecraft 账户验证系统               │
╠══════════════════╦════════════╦════════╦══════════╣
│ 邮箱             │ 游戏ID     │ OF有效 │ 耗时     │
│ 🌟 valid@test.com │  Player123  │   ✔    │  2.34s  │
│ 💀 bad@test.com  │     -       │   ✘    │    -    │
╚══════════════════════════════════════════════════════╝
```

## 配置选项

| 参数        | 默认值          | 说明                   |
|-------------|-----------------|------------------------|
| 代理文件    | `proxy.txt`     | 代理服务器列表文件     |
| 超时时间    | 5秒             | 网络请求超时时间       |
| 结果文件    | `valid_acc.txt` | 有效账户保存路径       |

## 常见问题

### Q1: 出现 `Missing dependencies` 错误
```bash
pip install -r requirements.txt --force-reinstall
```

### Q2: 代理连接失败
- 检查代理格式是否正确
- 测试代理是否可用
- 关闭防火墙或杀毒软件

### Q3: 验证速度较慢
- 使用高质量代理
- 减少同时验证的账户数量
- 关闭其他占用网络的程序

## 开源协议

本项目采用 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) 协议，您可以在遵循以下条件的前提下自由使用：

1. 保留原始版权声明
2. 修改作品必须开源
3. 分发作品必须使用相同协议

## 贡献指南

欢迎通过 Issue 提交问题或 Pull Request 贡献代码，请确保：

- 遵循现有代码风格
- 包含详细的文档说明
- 通过基础功能测试

> 注意：本工具仅用于教育目的，请勿用于非法用途。使用即表示您知悉相关风险。
