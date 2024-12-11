# patcher1337

一个用于处理1337格式补丁文件的Python库。

## 关于.1337补丁格式

.1337是x64dbg调试器使用的补丁格式。补丁文件中的地址是相对虚拟地址(RVA)，需要转换为文件偏移才能应用到目标文件。

补丁文件格式:
```
>target.dll            # 目标文件名
1000:74->EB           # 格式: RVA:原始值->新值
1001:0F->90           # RVA是x64dbg中显示的地址
```

## 安装

```bash
pip install patcher1337
```

## 使用示例

### 基本使用

```python
from patcher1337 import Patcher1337

patcher = Patcher1337()
result = patcher.apply_patch(
    patch_file="example.1337",
    target_file="target.dll"        
)
```

### 批量处理

```python
patcher = Patcher1337(debug=True)
results = patcher.batch_patch(
    patch_files=["patch1.1337", "patch2.1337"],
    target_files=["file1.dll", "file2.dll"],
    offsets=[True, False]  # True表示使用x64dbg的RVA偏移(0xC00)
)
```

### 错误处理

```python
try:
    patcher.apply_patch(...)
except InvalidPatchFile as e:
    print(f"补丁文件格式错误: {e}")  # 补丁文件格式不符合.1337规范
except PatchVerificationError as e:
    print(f"补丁验证失败: {e}")      # 补丁应用后验证失败,可能是文件被修改
except PatchError as e:
    print(f"补丁处理错误: {e}")      # 其他补丁相关错误
```

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。
