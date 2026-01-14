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
unzip ~/桌面/'附件2：信创操作系统漏洞补丁及手册(1).zip' -d ~/neon_os_patch

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

# 进入目标目录并安装补丁
echo ""
echo "进入目标目录并安装补丁..."
cd "$target_dir" || {
    echo "无法进入目录: $target_dir"
    exit 1
}

echo "当前目录: $(pwd)"

# 安装低危漏洞修复补丁（如果存在）
if [ -d "低危漏洞修复补丁" ]; then
    echo ""
    echo "开始安装低危漏洞修复补丁..."
    
    # 进入低危漏洞修复补丁目录
    cd "低危漏洞修复补丁" || {
        echo "无法进入低危漏洞修复补丁目录"
        exit 1
    }
    
    echo "当前目录: $(pwd)"
    
    # 根据架构进入对应的架构目录
    arch_dir="${arch_ver}架构通用"
    if [ -d "$arch_dir" ]; then
        cd "$arch_dir" || {
            echo "无法进入架构目录: $arch_dir"
            exit 1
        }
        
        echo "进入架构目录: $(pwd)"
        
        # 按照第一个、第二个、第三个的顺序安装
        for order in "第一个" "第二个" "第三个"; do
            if [ -d "$order" ]; then
                echo ""
                echo "安装 $order 文件夹中的补丁..."
                cd "$order" || {
                    echo "无法进入目录: $order"
                    continue
                }
                
                # 检查是否有deb文件
                deb_files=$(find . -maxdepth 1 -name "*.deb" -type f)
                if [ -n "$deb_files" ]; then
                    echo "正在安装 $(pwd) 中的补丁..."
                    sudo dpkg -i *.deb 2>/dev/null
                    
                    # 检查安装是否成功
                    if [ $? -ne 0 ]; then
                        echo "$order 文件夹中的补丁安装出现问题，尝试修复依赖..."
                        sudo apt-get install -f -y
                    fi
                else
                    echo "$order 文件夹中没有找到.deb文件"
                fi
                
                # 返回架构目录
                cd ..
            else
                echo "$order 文件夹不存在，跳过"
            fi
        done
        
        # 返回低危漏洞修复补丁目录
        cd ..
    else
        echo "架构目录不存在: $arch_dir"
    fi
    
    # 返回目标目录
    cd ..
else
    echo "低危漏洞修复补丁目录不存在，跳过安装"
fi

# 安装高危漏洞修复补丁（如果存在）
if [ -d "高危漏洞修复补丁" ]; then
    echo ""
    echo "开始安装高危漏洞修复补丁..."
    
    # 进入高危漏洞修复补丁目录
    cd "高危漏洞修复补丁" || {
        echo "无法进入高危漏洞修复补丁目录"
        exit 1
    }
    
    echo "当前目录: $(pwd)"
    
    # 根据架构进入对应的架构目录
    arch_dir="${arch_ver}架构通用"
    if [ -d "$arch_dir" ]; then
        cd "$arch_dir" || {
            echo "无法进入架构目录: $arch_dir"
            exit 1
        }
        
        echo "进入架构目录: $(pwd)"
        
        # 检查是否有deb文件
        deb_files=$(find . -maxdepth 1 -name "*.deb" -type f)
        if [ -n "$deb_files" ]; then
            echo "正在安装高危漏洞修复补丁..."
            sudo dpkg -i *.deb 2>/dev/null
            
            # 检查安装是否成功
            if [ $? -ne 0 ]; then
                echo "高危漏洞修复补丁安装出现问题，尝试修复依赖..."
                sudo apt-get install -f -y
            fi
        else
            echo "高危漏洞修复补丁目录中没有找到.deb文件"
        fi
        
        # 返回高危漏洞修复补丁目录
        cd ..
    else
        echo "架构目录不存在: $arch_dir"
    fi
    
    # 返回目标目录
    cd ..
else
    echo "高危漏洞修复补丁目录不存在，跳过安装"
fi

# 安装华为品牌专用补丁（如果存在）
if [ -d "华为品牌专用补丁" ]; then
    echo ""
    echo "开始安装华为品牌专用补丁..."
    
    # 进入华为品牌专用补丁目录
    cd "华为品牌专用补丁" || {
        echo "无法进入华为品牌专用补丁目录"
        exit 1
    }
    
    echo "当前目录: $(pwd)"
    
    # 检查是否有deb文件
    deb_files=$(find . -maxdepth 1 -name "*.deb" -type f)
    if [ -n "$deb_files" ]; then
        echo "正在安装华为品牌专用补丁..."
        sudo dpkg -i *.deb 2>/dev/null
        
        # 检查安装是否成功
        if [ $? -ne 0 ]; then
            echo "华为品牌专用补丁安装出现问题，尝试修复依赖..."
            sudo apt-get install -f -y
        fi
    else
        echo "华为品牌专用补丁目录中没有找到.deb文件"
    fi
    
    # 返回目标目录
    cd ..
else
    echo "华为品牌专用补丁目录不存在，跳过安装"
fi

# 安装完成后进行依赖修复
echo ""
echo "正在进行最终依赖修复..."
sudo apt-get install -f -y

# 检查安装结果
echo ""
echo "补丁安装完成，检查已安装的包..."
echo "已安装的补丁包:"
dpkg -l | grep -E "kylin|kysdk|peony" | head -20

# 显示安装统计
echo ""
echo "安装统计:"
total_installed=$(find "$target_dir" -name "*.deb" -type f | wc -l)
echo "总共尝试安装 $total_installed 个补丁包"
echo "请重启系统以确保所有补丁生效"