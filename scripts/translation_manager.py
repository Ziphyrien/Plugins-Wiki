"""
翻译管理工具

用于管理文档汉化进度
"""

import argparse
import os

# 获取项目根目录 (scripts 的上级目录)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

from version_control import VersionControl

def cmd_status(vc: VersionControl, args):
    """显示翻译状态"""
    if args.detailed:
        vc.print_detailed_status()
    else:
        vc.print_summary()

def cmd_list(vc: VersionControl, args):
    """列出特定状态的文件"""
    status_map = {
        "pending": vc.get_pending_translations,
        "in_progress": vc.get_in_progress_translations,
        "completed": vc.get_completed_translations,
        "outdated": vc.get_outdated_translations,
    }
    
    if args.status not in status_map:
        print(f"未知状态: {args.status}")
        print(f"可用状态: {', '.join(status_map.keys())}")
        return
    
    files = status_map[args.status]()
    
    status_names = {
        "pending": "待翻译",
        "in_progress": "翻译中",
        "completed": "已完成",
        "outdated": "需更新",
    }
    
    print(f"\n📋 {status_names[args.status]} 的文件 ({len(files)} 个):")
    print("-"*50)
    
    for f in sorted(files):
        info = vc.get_file_info(f)
        print(f"  • {f}")
        if args.verbose and info:
            print(f"      原文变更: {info.get('original_modified', 'N/A')}")
            if info.get('translated_at'):
                print(f"      汉化时间: {info['translated_at']}")

def cmd_start(vc: VersionControl, args):
    """标记开始翻译"""
    for file_path in args.files:
        if vc.get_file_info(file_path):
            vc.mark_translation_started(file_path)
        else:
            print(f"  [跳过] 文件未注册: {file_path}")

def cmd_complete(vc: VersionControl, args):
    """标记翻译完成"""
    for file_path in args.files:
        info = vc.get_file_info(file_path)
        if info:
            # 尝试读取翻译后的文件内容
            translated_content = None
            # 兼容 Windows 路径分隔符
            rel_path = file_path.replace("docs/", "docs_zh/").replace("docs\\", "docs_zh\\")
            translated_path = os.path.join(PROJECT_ROOT, rel_path)
            if os.path.exists(translated_path):
                with open(translated_path, 'rb') as f:
                    translated_content = f.read()
            
            vc.mark_translation_completed(file_path, translated_content)
        else:
            print(f"  [跳过] 文件未注册: {file_path}")

def cmd_note(vc: VersionControl, args):
    """添加备注"""
    if vc.get_file_info(args.file):
        vc.add_note(args.file, args.note)
        print(f"  [备注已添加] {args.file}: {args.note}")
    else:
        print(f"  [错误] 文件未注册: {args.file}")

def cmd_info(vc: VersionControl, args):
    """显示文件详细信息"""
    info = vc.get_file_info(args.file)
    if info:
        print(f"\n📄 文件信息: {args.file}")
        print("-"*50)
        print(f"  原文首次获取: {info.get('original_created', 'N/A')}")
        print(f"  原文最后变更: {info.get('original_modified', 'N/A')}")
        print(f"  原文哈希:     {info.get('original_hash', 'N/A')[:16]}...")
        print(f"  翻译状态:     {info.get('translation_status', 'N/A')}")
        print(f"  汉化时间:     {info.get('translated_at', 'N/A')}")
        if info.get('status') == 'deleted':
            print(f"  ⚠️ 状态:       已删除 (Deleted)")
        if info.get('translated_hash'):
            print(f"  译文哈希:     {info['translated_hash'][:16]}...")
        if info.get('notes'):
            print(f"  备注:         {info['notes']}")
    else:
        print(f"  [错误] 文件未注册: {args.file}")

def cmd_scan(vc: VersionControl, args):
    """扫描译文目录，自动更新状态"""
    lang_dir = os.path.join(PROJECT_ROOT, args.lang_dir)
    if not os.path.exists(lang_dir):
        print(f"错误: 译文目录不存在: {lang_dir}")
        return

    print(f"正在扫描译文目录: {lang_dir} ...")
    print("-" * 60)
    
    updated_count = 0
    
    # 遍历所有注册的文件
    for file_path, info in vc.metadata["files"].items():
        # 构造预期的译文路径
        # 假设 file_path 是 docs/xxx.md，译文在 docs_zh/xxx.md
        # 或者 file_path 是 docs\xxx.md
        
        # 简单的路径替换逻辑，假设原文都在 docs/ 下
        if file_path.startswith("docs") and (file_path[4] == '/' or file_path[4] == '\\'):
             rel_path = file_path[5:]
             trans_path = os.path.join(lang_dir, rel_path)
        else:
             # 如果不在 docs 下，直接拼接到 lang_dir
             trans_path = os.path.join(lang_dir, file_path)
             
        if os.path.exists(trans_path):
            with open(trans_path, 'rb') as f:
                content = f.read()
            
            # 1. 如果状态是 pending，标记为 completed (或者 in_progress)
            if info["translation_status"] == "pending":
                print(f"  [发现译文] {file_path} -> 标记为已完成")
                vc.mark_translation_completed(file_path, content)
                updated_count += 1
            
            # 2. 如果状态是 completed 或 outdated，检查内容是否变化
            elif info["translation_status"] in ["completed", "outdated"]:
                if vc.update_translation_hash(file_path, content):
                    print(f"  [译文更新] {file_path} -> 更新哈希")
                    # 如果是 outdated，且译文更新了，是否自动改为 completed?
                    # 这里我们保守一点，只提示
                    if info["translation_status"] == "outdated":
                        print(f"    ⚠️  注意: 原文已更新，请确认译文是否已适配，然后手动运行 complete 命令")
                    updated_count += 1
        else:
            # 译文不存在
            if info["translation_status"] == "completed":
                print(f"  [译文丢失] {file_path} (状态是 completed 但文件不存在)")
    
    print("-" * 60)
    print(f"扫描完成，更新了 {updated_count} 个文件的状态。")

def cmd_check(vc: VersionControl, args):
    """检查一致性"""
    print("正在检查一致性...")
    print("-" * 60)
    
    issues_found = False
    
    # 1. 检查孤儿译文 (原文已删除)
    for file_path, info in vc.metadata["files"].items():
        if info.get("status") == "deleted":
            print(f"  ⚠️  [原文已删] {file_path}")
            issues_found = True
            
    # 2. 检查 outdated 状态
    outdated = vc.get_outdated_translations()
    if outdated:
        print(f"\n  ⚠️  [需要更新] 以下 {len(outdated)} 个文件原文有变动:")
        for f in outdated:
            print(f"      - {f}")
        issues_found = True
            
    if not issues_found:
        print("  ✅ 未发现明显问题。")

def main():
    parser = argparse.ArgumentParser(
        description="翻译管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/translation_manager.py status           # 显示摘要
  python scripts/translation_manager.py scan --lang-dir docs_zh  # 扫描译文目录
  python scripts/translation_manager.py check            # 检查一致性
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="显示翻译状态")
    status_parser.add_argument("-d", "--detailed", action="store_true", 
                               help="显示详细状态")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出特定状态的文件")
    list_parser.add_argument("status", 
                             choices=["pending", "in_progress", "completed", "outdated"],
                             help="文件状态")
    list_parser.add_argument("-v", "--verbose", action="store_true",
                             help="显示详细信息")
    
    # start 命令
    start_parser = subparsers.add_parser("start", help="标记开始翻译")
    start_parser.add_argument("files", nargs="+", help="文件路径")
    
    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="标记翻译完成")
    complete_parser.add_argument("files", nargs="+", help="文件路径")
    
    # note 命令
    note_parser = subparsers.add_parser("note", help="添加备注")
    note_parser.add_argument("file", help="文件路径")
    note_parser.add_argument("note", help="备注内容")
    
    # info 命令
    info_parser = subparsers.add_parser("info", help="显示文件详细信息")
    info_parser.add_argument("file", help="文件路径")
    
    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="扫描译文目录")
    scan_parser.add_argument("--lang-dir", default="docs_zh", help="译文目录 (默认: docs_zh)")

    # check 命令
    check_parser = subparsers.add_parser("check", help="检查一致性")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化版本控制 (使用项目根目录)
    vc = VersionControl(PROJECT_ROOT)
    
    # 执行命令
    commands = {
        "status": cmd_status,
        "list": cmd_list,
        "start": cmd_start,
        "complete": cmd_complete,
        "note": cmd_note,
        "info": cmd_info,
        "scan": cmd_scan,
        "check": cmd_check,
    }
    
    commands[args.command](vc, args)

if __name__ == "__main__":
    main()
