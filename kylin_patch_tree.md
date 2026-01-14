文件目录结构中，相关结构为
~/neon_os_patch
├── 第九批信创操作系统漏洞修复说明及操作步骤.wps
├── 系统版本2403
│   ├── 2403漏洞修复检查工具.zip
│   ├── 低危漏洞修复补丁
│   │   ├── 华为品牌专用补丁.zip
│   │   ├── arm架构通用.zip
│   │   └── x86架构通用.zip
│   └── 高危漏洞修复补丁
│       ├── arm架构通用.zip
│       └── x86架构通用.zip
└── 系统版本2503
    ├── 高危漏洞补丁
    │   ├── arm架构通用.zip
    │   └── x86架构通用.zip
    └── 漏洞修复检查工具（2503版本专用）.zip
根据我们获得的$arch_ver和$os_version两个变量，找到对应的高危漏洞补丁并解压到`~/`路径下。
例如，
如果$os_version为2403，同时$arch_ver为x86，
则解压'~/neon_os_patch/系统版本2403/'下的'2403漏洞修复检查工具.zip'，'低危漏洞修复补丁/x86架构通用.zip'，'高危漏洞修复补丁/x86架构通用.zip'
组成一个新的文件目录结构，最高级别的文件夹命名方式为neon_os_patch_{os_version}_{arch_ver}，其中`.deb`文件可多可少，是不确定的：
~/neon_os_patch_2403_x86
├── 2403漏洞修复检查工具.sh
├── 低危漏洞修复补丁
│   ├── x86架构通用
│   │   ├── 第二个
│   │   │   └── kylin-photo-viewer_1.3.1.4-0k5.24update2_amd64.deb
│   │   ├── 第三个
│   │   │   └── peony-rotate-menu-plugin_1.3.1.4-0k5.24update2_amd64.deb
│   │   ├── 第一个
│   │   │   └── libkysdk-qtwidgets_2.4.1.0-0k1.6update3_amd64.deb
│   │   └── 注意：请按照文件夹顺序依次打开安装.txt
└── 高危漏洞修复补丁
    ├── x86架构通用
    └── ├── libkysdk-accounts_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-battery_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-disk_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-filesystem_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-hardware_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-imageproc_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-location_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-logrotate_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-net_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-ocr_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-package_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-powermanagement_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-proc_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-processmanage_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-realtime_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-sysinfo_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-system_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-systemcommon_2.4.1.0-0k1.13update9_amd64.deb
        ├── libkysdk-system-dbus_2.4.1.0-0k1.13update9_amd64.deb
        └── libkysdk-systime_2.4.1.0-0k1.13update9_amd64.deb

实现以上目标的shell脚本代码为：
```bash
#!/bin/bash

# 读取系统信息文件
kyinfo_content=$(cat /etc/.kyinfo 2>/dev/null)

# 检查文件是否存在并可读
if [ -z "$kyinfo_content" ]; then
    echo "无法读取 /etc/.kyinfo 文件"
    exit 1
fi

# 提取麒麟OS版本号（匹配2403或2503）
os_version=""

# 优先匹配2403
if echo "$kyinfo_content" | grep -q "2403"; then
    os_version="2403"
# 如果没找到2403，再匹配2503
elif echo "$kyinfo_content" | grep -q "2503"; then
    os_version="2503"
fi

# 输出麒麟OS版本
if [ -n "$os_version" ]; then
    echo "current version: $os_version"
else
    echo "未找到2403或2503版本信息"
    exit 1
fi

# 获取系统架构信息
uname_output=$(uname -a)
arch_ver=""

# 判断系统架构
if echo "$uname_output" | grep -qi "x86_64\|i386\|i686\|amd64"; then
    arch_ver="x86"
elif echo "$uname_output" | grep -qi "aarch64\|arm64\|arm"; then
    arch_ver="arm"
fi

# 输出系统架构
if [ -n "$arch_ver" ]; then
    echo "architecture: $arch_ver"
else
    echo "无法识别系统架构"
    exit 1
fi

# 将～/桌面/下的zip文件 '附件2：信创操作系统漏洞补丁及手册(1).zip' 解压到 ~/
echo "正在解压漏洞补丁包..."
unzip -o ~/桌面/'附件2：信创操作系统漏洞补丁及手册(1).zip' -d ~/neon_os_patch 2>/dev/null

# 如果解压失败，尝试另一种可能的路径
if [ $? -ne 0 ]; then
    echo "尝试从默认路径解压..."
    unzip -o ~/桌面/附件2：信创操作系统漏洞补丁及手册\(1\).zip -d ~/neon_os_patch 2>/dev/null
fi

if [ $? -ne 0 ]; then
    echo "无法解压补丁包，请确保文件存在: ~/桌面/附件2：信创操作系统漏洞补丁及手册(1).zip"
    exit 1
fi

echo "补丁包解压完成"

# 创建目标目录
target_dir="$HOME/neon_os_patch_${os_version}_${arch_ver}"
echo "创建目标目录: $target_dir"
mkdir -p "$target_dir"

# 定义基础路径
base_path="$HOME/neon_os_patch/系统版本${os_version}"

# 检查工具解压
if [ "$os_version" = "2403" ]; then
    # 2403版本
    check_tool_zip="${base_path}/2403漏洞修复检查工具.zip"
elif [ "$os_version" = "2503" ]; then
    # 2503版本
    check_tool_zip="${base_path}/漏洞修复检查工具（2503版本专用）.zip"
fi

echo "解压检查工具: $check_tool_zip"
if [ -f "$check_tool_zip" ]; then
    unzip -o "$check_tool_zip" -d "$target_dir" 2>/dev/null
    echo "检查工具解压完成"
else
    echo "警告: 检查工具文件不存在: $check_tool_zip"
fi

# 解压低危漏洞补丁（仅2403版本有）
if [ "$os_version" = "2403" ]; then
    low_risk_zip="${base_path}/低危漏洞修复补丁/${arch_ver}架构通用.zip"
    echo "解压低危漏洞补丁: $low_risk_zip"
    
    if [ -f "$low_risk_zip" ]; then
        mkdir -p "$target_dir/低危漏洞修复补丁"
        unzip -o "$low_risk_zip" -d "$target_dir/低危漏洞修复补丁" 2>/dev/null
        echo "低危漏洞补丁解压完成"
    else
        echo "警告: 低危漏洞补丁文件不存在: $low_risk_zip"
    fi
fi

# 解压高危漏洞补丁
if [ "$os_version" = "2403" ]; then
    high_risk_zip="${base_path}/高危漏洞修复补丁/${arch_ver}架构通用.zip"
else
    # 2503版本
    high_risk_zip="${base_path}/高危漏洞补丁/${arch_ver}架构通用.zip"
fi

echo "解压高危漏洞补丁: $high_risk_zip"

if [ -f "$high_risk_zip" ]; then
    mkdir -p "$target_dir/高危漏洞修复补丁"
    unzip -o "$high_risk_zip" -d "$target_dir/高危漏洞修复补丁" 2>/dev/null
    echo "高危漏洞补丁解压完成"
else
    echo "警告: 高危漏洞补丁文件不存在: $high_risk_zip"
fi

# 华为品牌专用补丁（仅2403版本arm架构有）
if [ "$os_version" = "2403" ] && [ "$arch_ver" = "arm" ]; then
    huawei_zip="${base_path}/低危漏洞修复补丁/华为品牌专用补丁.zip"
    echo "解压华为品牌专用补丁: $huawei_zip"
    
    if [ -f "$huawei_zip" ]; then
        # 华为补丁可能也需要解压到特定目录
        mkdir -p "$target_dir/华为品牌专用补丁"
        unzip -o "$huawei_zip" -d "$target_dir/华为品牌专用补丁" 2>/dev/null
        echo "华为品牌专用补丁解压完成"
    else
        echo "注意: 华为品牌专用补丁文件不存在，可能不需要或已包含在其他补丁中"
    fi
fi

# 检查解压结果
echo ""
echo "补丁文件解压完成"
echo "目标目录结构:"
find "$target_dir" -type f -name "*.deb" | head -10 | while read -r file; do
    echo "  - $(basename "$file")"
done

# 统计解压的deb文件数量
deb_count=$(find "$target_dir" -type f -name "*.deb" | wc -l)
echo ""
echo "总共解压了 $deb_count 个 .deb 文件"
echo "补丁目录: $target_dir"

# 列出目录结构
echo ""
echo "目录结构:"
ls -la "$target_dir"
if [ -d "$target_dir/低危漏洞修复补丁" ]; then
    echo "低危漏洞修复补丁目录:"
    ls -la "$target_dir/低危漏洞修复补丁/"
fi
if [ -d "$target_dir/高危漏洞修复补丁" ]; then
    echo "高危漏洞修复补丁目录:"
    ls -la "$target_dir/高危漏洞修复补丁/"
fi

```

下一步，通过cd命令进入到'～/neon_os_patch_{os_version}_{arch_ver}/'目录，
利用`sudo dpkg -i *.deb`依次安装'低危漏洞修复补丁'文件夹和'高危漏洞修复补丁'文件夹中的所有deb文件。

注意，低危漏洞的文件夹需要按照第一个、第二个、第三个顺序依次安装，如果没有第三个文件夹，则忽略。
