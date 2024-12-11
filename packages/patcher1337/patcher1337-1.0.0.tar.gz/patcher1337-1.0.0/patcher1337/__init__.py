#!/usr/bin/env python
"""
1337 Patch Library - 用于处理1337格式补丁文件的Python库

关于.1337补丁格式:
.1337是x64dbg调试器使用的补丁格式。补丁文件中的地址是相对虚拟地址(RVA)，
需要转换为文件偏移才能应用到目标文件。

补丁文件格式:
>target.dll            # 目标文件名
1000:74->EB           # 格式: RVA:原始值->新值
1001:0F->90           # RVA是x64dbg中显示的地址

使用示例:
1. 基本使用:
    from patcher1337 import Patcher1337
    
    patcher = Patcher1337()
    result = patcher.apply_patch(
        patch_file="example.1337",
        target_file="target.dll"        
    )

2. 批量处理:
    patcher = Patcher1337(debug=True)
    results = patcher.batch_patch(
        patch_files=["patch1.1337", "patch2.1337"],
        target_files=["file1.dll", "file2.dll"],
        offsets=[True, False]  # True表示使用x64dbg的RVA偏移(0xC00)
    )

错误处理:
    try:
        patcher.apply_patch(...)
    except InvalidPatchFile as e:
        print(f"补丁文件格式错误: {e}")  # 补丁文件格式不符合.1337规范
    except PatchVerificationError as e:
        print(f"补丁验证失败: {e}")      # 补丁应用后验证失败,可能是文件被修改
    except PatchError as e:
        print(f"补丁处理错误: {e}")      # 其他补丁相关错误

# PE文件地址类型关系

## 一、本质分类

### 1. RVA为基准
- **RVA** (相对虚拟地址，1337地址)：是最基础的地址表示，也是X64DBG生成补丁时里面填写的地址
- **VA** (虚拟地址)：就是 RVA + ImageBase，这是x64dbg中直接显示的地址，它是程序加载到内存中后的实际地址，通常以0x140000000为基址（64位程序）


### 2. FOA独立
- **FOA** (文件偏移)：实际文件中的位置
- 与RVA的关系：FOA = RVA（1337地址） - 0xC00

## 二、转换公式简化

1. VA = RVA + ImageBase
2. FOA = RVA - 0xC00

因此：
- 所有内存地址（VA、RVA、1337地址）本质上是同一个东西
- 只需要记住RVA和FOA的转换关系即可

## 三、实际应用

1. 看到VA时：先减去ImageBase得到RVA
2. 看到RVA时：直接减0xC00得到FOA
3. 看到1337地址时：就是RVA，按RVA处理
4. 需要FOA时：用上述任何地址最终转成RVA，再减0xC00


补丁工具为什么需要offset参数：当它是true时，表示输入的是RVA（1337地址），需要减去0xC00转换为FOA；当它是false时，表示输入的已经是FOA，无需转换。
"""

import binascii
import shutil
import sys
from datetime import timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
import logging
import os
from enum import Enum, auto

__version__ = "1.0.0"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PatchEntry:
    """补丁条目数据类"""
    offset: int
    original: str
    new: str

class PatchError(Exception):
    """补丁操作相关的异常基类"""
    pass

class InvalidPatchFile(PatchError):
    """无效的补丁文件"""
    pass

class PatchVerificationError(PatchError):
    """补丁验证失败"""
    pass

class PatchStatus(Enum):
    """补丁状态枚举"""
    ALREADY_PATCHED = auto()  # 已经完全修改过
    NEED_PATCH = auto()       # 需要修改（包括全是原始值和部分修改的情况）
    INVALID = auto()          # 文件不匹配

class PatchResult(Enum):
    """补丁操作结果枚举"""
    SUCCESS = auto()           # 补丁应用成功
    ALREADY_PATCHED = auto()   # 文件已经打过补丁
    FILE_NOT_FOUND = auto()    # 文件未找到
    ACCESS_DENIED = auto()     # 访问被拒绝
    INVALID_PATCH = auto()     # 无效的补丁
    VERIFICATION_FAILED = auto() # 验证失败
    UNKNOWN_ERROR = auto()     # 未知错误

class Patcher1337:
    """1337格式补丁文件处理类"""
    
    def __init__(self, debug: bool = False):
        """
        初始化补丁处理器
        
        Args:
            debug: 是否启用调试模式
        """
        self.debug = debug
        if debug:
            logger.setLevel(logging.DEBUG)
    
    def parse_patch_file(self, patch_file: str, target_file: str = None) -> Tuple[str, List[PatchEntry]]:
        """
        解析1337格式补丁文件
        
        Args:
            patch_file: 补丁文件路径
            target_file: 目标文件名（可选），用于只解析特定文件的补丁
            
        Returns:
            Tuple[str, List[PatchEntry]]: 返回目标文件名和补丁条目列表
            
        Raises:
            InvalidPatchFile: 补丁文件格式无效
            FileNotFoundError: 补丁文件不存在
        """
        try:
            with Path(patch_file).open() as f:
                lines = f.readlines()
                
                if not lines or not lines[0].startswith('>'):
                    raise InvalidPatchFile("Invalid 1337 patch file format")
                
                patches = []
                current_file = None
                target_found = False
                matched_file = None  # 存储匹配的文件名
                
                # 修改文件名处理逻辑
                if target_file:
                    target_path = Path(target_file)
                    # 只去掉.tmp后缀，保留原始后缀和大小写
                    if target_path.name.endswith('.tmp'):
                        target_name = target_path.name[:-4]  # 去掉.tmp
                    else:
                        target_name = target_path.name
                else:
                    target_name = None
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith('>'):
                        current_file = line[1:].strip()  # 移除.lower()
                        # 如果找到目标文件，开始收集补丁（使用不区分大小写的比较）
                        if target_name and current_file.lower() == target_name.lower():
                            target_found = True
                            matched_file = current_file  # 保存原始大小写的文件名
                            patches = []  # 清空之前的补丁
                        elif not target_name:
                            # 如果没有指定目标文件，收集所有补丁
                            patches = []
                        else:
                            # 如果不是目标文件，停止收集补丁
                            target_found = False
                        continue
                    
                    # 只收集目标文件的补丁
                    if target_found:
                        try:
                            offset, values = line.split(':')
                            original, new = values.split('->')
                            
                            # 移除偏移量中的前导零
                            offset = offset.lstrip('0')
                            if not offset:
                                offset = '0'
                                
                            patches.append(PatchEntry(
                                offset=int(offset, 16),
                                original=original.strip(),
                                new=new.strip()
                            ))
                        except ValueError as e:
                            logger.error(f"Invalid patch line format: {line}")
                            raise InvalidPatchFile(f"Invalid patch line: {line}") from e
                
                if target_name and not matched_file:
                    raise InvalidPatchFile(f"Target file {target_name} not found in patch")
                    
                # 返回匹配的文件名（如果有）或最后一个文件名
                return matched_file or current_file, patches
                
        except FileNotFoundError:
            logger.error(f"Patch file not found: {patch_file}")
            raise
    
    def backup_file(self, target_file: str, force: bool = False) -> bool:
        """
        备份目标文件
        
        Args:
            target_file: 目标文件路径
            force: 是否强制覆盖已存在的备份
            
        Returns:
            bool: 备份是否成功
        """
        backup_path = Path(target_file + '.origin')
        
        if backup_path.exists() and not force:
            target_mod = Path(target_file).stat().st_mtime
            backup_mod = backup_path.stat().st_mtime
            
            if backup_mod > (target_mod - timedelta(days=7).total_seconds()):
                logger.warning("Recent backup exists. Use force=True to overwrite")
                return False
        
        try:
            shutil.copy2(target_file, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            return False
    
    def restore_backup(self, target_file: str) -> bool:
        """
        从备份恢复文件
        
        Args:
            target_file: 目标文件路径
            
        Returns:
            bool: 恢复是否成功
        """
        backup_path = Path(target_file + '.origin')
        if not backup_path.exists():
            logger.error("No backup file found")
            return False
            
        try:
            shutil.copy2(backup_path, target_file)
            logger.info(f"Restored from backup: {target_file}")
            return True
        except Exception as e:
            logger.error(f"Restore failed: {str(e)}")
            return False
    
    def apply_patch(self, 
                   patch_file: str, 
                   target_file: str, 
                   offset: bool = True,
                   force_backup: bool = False,
                   create_backup: bool = True,
                   strict_mode: bool = True) -> Tuple[bool, Union[PatchStatus, PatchResult]]:
        """
        应用补丁到目标文件
        
        Args:
            patch_file: 补丁文件路径
            target_file: 目标文件路径
            offset: 是否使用x64dbg的RVA偏移(0xC00)
                - True: 将补丁文件中的RVA减去0xC00得到文件偏移，适用于x64dbg补丁
                - False: 直接使用补丁文件中的地址作为文件偏移，使用于其他软件直接生成文件偏移值（即VA）
            force_backup: 是否强制覆盖已存在的备份
            create_backup: 是否创建.origin备份文件
            strict_mode: 是否使用严格模式
                        - True: 任何地址不匹配都会失败
                        - False: 跳过不匹配的地址继续处理
        
        Returns:
            Tuple[bool, Union[PatchStatus, PatchResult]]: 
                - bool: 操作是否成功
                - Union[PatchStatus, PatchResult]: 补丁状态或结果
                    - ALREADY_PATCHED: 文件已经打过补丁
                    - NEED_PATCH: 成功应用了新的补丁
                    - INVALID: 补丁验证失败或文件不匹配
                    - 其他状态见PatchResult枚举
        
        Raises:
            InvalidPatchFile: 补丁文件格式无效
            PatchVerificationError: 补丁验证失败
            PermissionError: 没有文件访问权限
            Exception: 其他未预期的错误
        """
        try:
            if not os.path.exists(target_file):
                return False, PatchResult.FILE_NOT_FOUND
                
            # 解析补丁文件
            try:
                _, patches = self.parse_patch_file(
                    patch_file=patch_file,
                    target_file=Path(target_file).name
                )
            except PermissionError:
                return False, PatchResult.ACCESS_DENIED
            except InvalidPatchFile:
                return False, PatchResult.INVALID_PATCH
                
            # 应用补丁
            offset_value = 0xC00 if offset else 0x0
            
            # 首先检查文件状态
            with open(target_file, "rb") as f:
                all_patched = True
                valid_patches = []  # 存储可以应用的补丁
                
                for patch in patches:
                    location = patch.offset - offset_value
                    f.seek(location)
                    current = f.read(1)
                    current_hex = current.hex().upper()
                    original_hex = patch.original.upper()
                    new_hex = patch.new.upper()
                    
                    if current_hex == new_hex:
                        # 已经是目标值，跳过
                        continue
                    elif current_hex == original_hex:
                        # 是原始值，需要修改
                        all_patched = False
                        valid_patches.append(patch)
                    else:
                        # 不匹配的情况
                        if strict_mode:
                            # 严格模式：立即失败
                            error_msg = (f"File at 0x{location:X} contains unexpected value: "
                                       f"found {current_hex}, expected either {original_hex} or {new_hex}")
                            raise PatchVerificationError(error_msg)
                        else:
                            # 非严格模式：记录警告并继续
                            logger.warning(f"Skipping patch at 0x{location:X}: unexpected value "
                                         f"found {current_hex}, expected either {original_hex} or {new_hex}")
                
                if all_patched:
                    logger.info(f"File already patched: {target_file}")
                    return True, PatchStatus.ALREADY_PATCHED
                
                if not valid_patches:
                    logger.warning("No valid patches to apply")
                    return False, PatchStatus.INVALID

            # 修改备份逻辑
            if create_backup:
                # 如果备份失败，返回错误
                if not self.backup_file(target_file, force_backup):
                    return False, PatchStatus.INVALID
            
            # 在临时文件上进行修改
            temp_file = target_file + '.tmp'
            shutil.copy2(target_file, temp_file)
            
            try:
                # 应用补丁到临时文件
                with open(temp_file, "r+b", buffering=0) as f:
                    # 只应用有效的补丁
                    for patch in valid_patches:
                        location = patch.offset - offset_value
                        f.seek(location)
                        f.write(binascii.unhexlify(patch.new))
                    
                    # 验证修改
                    for patch in valid_patches:
                        location = patch.offset - offset_value
                        f.seek(location)
                        current = f.read(1)
                        if current != binascii.unhexlify(patch.new):
                            raise PatchVerificationError(
                                f"Post-patch verification failed at 0x{location:X}"
                            )
                
                # 所有补丁都成功了
                # # 备份target_file，到.orign中
                # shutil.copy2(target_file, target_file + '.orign')
                # 用临时文件替换目标文件
                shutil.move(temp_file, target_file)
                logger.info(f"Successfully patched: {target_file}")
                return True, PatchStatus.NEED_PATCH
                
            except Exception as e:
                # 如果失败，
                # 删除临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                raise
                
        except PermissionError:
            return False, PatchResult.ACCESS_DENIED
        except PatchVerificationError as e:
            logger.error(f"Verification failed: {str(e)}")
            return False, PatchResult.VERIFICATION_FAILED
        except Exception as e:
            logger.error(f"Patch failed: {str(e)}")
            return False, PatchResult.UNKNOWN_ERROR
    
    def batch_patch(self, 
                   patch_files: List[str], 
                   target_files: List[str], 
                   offsets: Optional[List[bool]] = None,
                   **kwargs) -> Dict[str, bool]:
        """
        批量应用补丁
        
        Args:
            patch_files: 补丁文件路径列表
            target_files: 目标文件路径列表
            offsets: 偏移设置列表
            **kwargs: 传递给apply_patch的其他参数
            
        Returns:
            Dict[str, bool]: 每个文件的补丁结果
        """
        if len(patch_files) != len(target_files):
            raise ValueError("Patch files and target files must have same length")
            
        if offsets is None:
            offsets = [True] * len(patch_files)
        
        results = {}
        for patch_file, target_file, offset in zip(patch_files, target_files, offsets):
            try:
                success, status = self.apply_patch(
                    patch_file=patch_file,
                    target_file=target_file,
                    offset=offset,
                    **kwargs
                )
                results[target_file] = success
            except Exception as e:
                logger.error(f"Failed to patch {target_file}: {str(e)}")
                results[target_file] = False
                
        return results 