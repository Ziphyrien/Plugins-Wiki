"""
版本控制系统

跟踪信息：
- original_created: 原文首次获取时间
- original_modified: 原文最后变更时间（来自 sitemap lastmod）
- translated_at: 汉化完成时间
- translation_status: 翻译状态 (pending/in_progress/completed/outdated)
- original_hash: 原文内容哈希，用于检测内容变化
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

VERSION_FILE = "version_metadata.json"

class VersionControl:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.version_file = os.path.join(base_dir, VERSION_FILE)
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """加载版本元数据"""
        if os.path.exists(self.version_file):
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Warning: Could not load {self.version_file}, creating new one.")
        return {"files": {}, "last_updated": None}
    
    def _save_metadata(self):
        """保存版本元数据"""
        self.metadata["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def compute_hash(content: bytes) -> str:
        """计算内容的 MD5 哈希值"""
        return hashlib.md5(content).hexdigest()
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """获取文件的版本信息"""
        return self.metadata["files"].get(file_path)
    
    def register_original(self, file_path: str, content: bytes, 
                          remote_lastmod: Optional[str] = None):
        """
        注册/更新原文文件信息
        
        Args:
            file_path: 文件相对路径
            content: 文件内容
            remote_lastmod: 远程 sitemap 中的 lastmod 时间
        """
        now = datetime.now(timezone.utc).isoformat()
        content_hash = self.compute_hash(content)
        
        existing = self.metadata["files"].get(file_path)
        
        if existing is None:
            # 新文件
            self.metadata["files"][file_path] = {
                "original_created": now,
                "original_modified": remote_lastmod or now,
                "original_hash": content_hash,
                "translated_at": None,
                "translated_hash": None,
                "translation_status": "pending",
                "notes": ""
            }
            print(f"  [NEW] Registered new file: {file_path}")
        else:
            # 检查是否有更新
            if existing["original_hash"] != content_hash:
                existing["original_modified"] = remote_lastmod or now
                existing["original_hash"] = content_hash
                
                # 如果已翻译，标记为过期
                if existing["translation_status"] == "completed":
                    existing["translation_status"] = "outdated"
                    print(f"  [OUTDATED] Original updated, translation needs review: {file_path}")
                else:
                    print(f"  [UPDATED] Original content changed: {file_path}")
            else:
                print(f"  [UNCHANGED] No changes detected: {file_path}")
        
        self._save_metadata()
    
    def mark_translation_started(self, file_path: str):
        """标记开始翻译"""
        if file_path in self.metadata["files"]:
            self.metadata["files"][file_path]["translation_status"] = "in_progress"
            self._save_metadata()
            print(f"  [IN PROGRESS] Translation started: {file_path}")
    
    def mark_translation_completed(self, file_path: str, translated_content: Optional[bytes] = None):
        """
        标记翻译完成
        
        Args:
            file_path: 文件路径
            translated_content: 翻译后的内容（用于计算哈希）
        """
        if file_path in self.metadata["files"]:
            now = datetime.now(timezone.utc).isoformat()
            self.metadata["files"][file_path]["translated_at"] = now
            self.metadata["files"][file_path]["translation_status"] = "completed"
            
            if translated_content:
                self.metadata["files"][file_path]["translated_hash"] = self.compute_hash(translated_content)
            
            self._save_metadata()
            print(f"  [COMPLETED] Translation completed: {file_path}")

    def mark_file_deleted(self, file_path: str):
        """标记原文已删除"""
        if file_path in self.metadata["files"]:
            if self.metadata["files"][file_path].get("status") != "deleted":
                self.metadata["files"][file_path]["status"] = "deleted"
                # 保留翻译状态以便恢复或参考，但可以添加标记
                self._save_metadata()
                print(f"  [DELETED] Original file marked as deleted: {file_path}")

    def restore_file(self, file_path: str):
        """恢复被标记为删除的文件"""
        if file_path in self.metadata["files"]:
            if self.metadata["files"][file_path].get("status") == "deleted":
                del self.metadata["files"][file_path]["status"]
                self._save_metadata()
                print(f"  [RESTORED] File restored: {file_path}")

    def update_translation_hash(self, file_path: str, content: bytes):
        """更新译文哈希（用于检测手动修改）"""
        if file_path in self.metadata["files"]:
            new_hash = self.compute_hash(content)
            old_hash = self.metadata["files"][file_path].get("translated_hash")
            
            if new_hash != old_hash:
                self.metadata["files"][file_path]["translated_hash"] = new_hash
                # 如果之前是 outdated，且译文内容变了，可能意味着用户修复了
                # 这里我们保守一点，不自动改状态，除非用户明确要求
                # 但我们可以记录最后一次检测到译文变化的时间
                self.metadata["files"][file_path]["translated_modified"] = datetime.now(timezone.utc).isoformat()
                self._save_metadata()
                return True
        return False
    
    def add_note(self, file_path: str, note: str):
        """添加备注"""
        if file_path in self.metadata["files"]:
            self.metadata["files"][file_path]["notes"] = note
            self._save_metadata()
    
    def get_pending_translations(self) -> List[str]:
        """获取待翻译的文件列表"""
        return [
            path for path, info in self.metadata["files"].items()
            if info["translation_status"] == "pending"
        ]
    
    def get_outdated_translations(self) -> List[str]:
        """获取需要更新翻译的文件列表（原文已更新）"""
        return [
            path for path, info in self.metadata["files"].items()
            if info["translation_status"] == "outdated"
        ]
    
    def get_in_progress_translations(self) -> List[str]:
        """获取正在翻译的文件列表"""
        return [
            path for path, info in self.metadata["files"].items()
            if info["translation_status"] == "in_progress"
        ]
    
    def get_completed_translations(self) -> List[str]:
        """获取已完成翻译的文件列表"""
        return [
            path for path, info in self.metadata["files"].items()
            if info["translation_status"] == "completed"
        ]
    
    def print_summary(self):
        """打印版本控制摘要"""
        total = len(self.metadata["files"])
        pending = len(self.get_pending_translations())
        in_progress = len(self.get_in_progress_translations())
        completed = len(self.get_completed_translations())
        outdated = len(self.get_outdated_translations())
        
        print("\n" + "="*60)
        print("📊 翻译进度摘要")
        print("="*60)
        print(f"  📁 总文件数:     {total}")
        print(f"  ⏳ 待翻译:       {pending}")
        print(f"  🔄 翻译中:       {in_progress}")
        print(f"  ✅ 已完成:       {completed}")
        print(f"  ⚠️  需要更新:     {outdated}")
        print("="*60)
        
        if self.metadata.get("last_updated"):
            print(f"  最后更新: {self.metadata['last_updated']}")
        print()
    
    def print_detailed_status(self):
        """打印详细状态"""
        self.print_summary()
        
        status_icons = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "outdated": "⚠️"
        }
        
        print("\n详细文件列表:")
        print("-"*60)
        
        for path, info in sorted(self.metadata["files"].items()):
            icon = status_icons.get(info["translation_status"], "❓")
            status = info["translation_status"]
            
            print(f"{icon} [{status:12}] {path}")
            print(f"    原文变更: {info['original_modified'] or 'N/A'}")
            print(f"    汉化时间: {info['translated_at'] or 'N/A'}")
            if info.get("notes"):
                print(f"    备注: {info['notes']}")
            print()


def check_needs_update(vc: VersionControl, file_path: str, 
                       content: bytes, remote_lastmod: Optional[str] = None) -> tuple:
    """
    检查是否需要更新文件
    
    Returns:
        (should_download, reason, is_new)
    """
    existing = vc.get_file_info(file_path)
    
    if existing is None:
        return True, "新文件", True
    
    content_hash = vc.compute_hash(content)
    if existing["original_hash"] != content_hash:
        return True, "内容已变更", False
    
    return False, "无变化", False
