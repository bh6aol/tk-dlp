
# Build

## 1. 创建环境
### 使用 conda 创建 python 环境
```bash
conda create -n tk-dlp python=3.12
```
### 安装依赖
```bash
pip install -r requirements.txt
```

## 2. 运行构建脚本

### Unix / macOS

```bash
./build.sh
```

### Windows

```cmd
build.cmd
```

## 3. 完成

构建完成后即可开始使用 🎉

---

# Misc

## 1. macOS 签名绕过

构建后第一次运行前，可能需要移除隔离属性：

```bash
xattr -dr com.apple.quarantine dist/main.app
```

## 2. macOS 测试运行

```bash
cd dist/main.app/Contents/MacOS/
./main
```
