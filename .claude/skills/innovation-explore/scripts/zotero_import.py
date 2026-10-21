#!/usr/bin/env python3
"""Import project literature PDFs into Zotero, one collection per project.

Subfolders become sub-collections:
  ~/projects/my-paper/papers/flaky_tests/*.pdf  ->  my-paper ▸ flaky_tests

Papers already in Zotero are not imported again: an identical file (same MD5) or
a filename matching an existing title just adds the existing item to the new
collection. Re-running is safe.

Zotero's local HTTP API is read-only, so this script generates a JavaScript
snippet for Zotero's own "Run JavaScript" window. The snippet creates missing
collections, imports new files as stored attachments, and triggers Zotero's
"Retrieve Metadata for PDF" so parent items get real titles/authors.

Usage:
  zotero_import.py ~/projects/my-paper                 # list candidate literature folders, import nothing
  zotero_import.py ~/projects/my-paper/papers          # one project (collection = project name)
  zotero_import.py DIR --collection "my-paper" --exclude "attempt-*" --flat
  zotero_import.py --plan plan.json               # several projects in one snippet

plan.json:
  [{"collection": "flaky-tests", "folders": ["~/projects/a/pdfs", {"path": "~/projects/b", "sub": "子集合名"}],
    "flat": true, "exclude": ["x*"]}, ...]
"""
import argparse
import fnmatch
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys

ZOTERO_DIR = os.path.expanduser(os.environ.get("ZOTERO_DIR", "~/Zotero"))
CANDIDATE_NAMES = ("papers", "paper_pdfs", "pdfs", "literature", "refs", "references", "related_work_papers")
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "worktrees"}


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def existing_hashes():
    """md5 -> attachment key (Zotero storage folders are named by attachment key)."""
    storage = os.path.join(ZOTERO_DIR, "storage")
    out = {}
    if os.path.isdir(storage):
        for key in os.listdir(storage):
            d = os.path.join(storage, key)
            if os.path.isdir(d):
                for name in os.listdir(d):
                    if name.lower().endswith(".pdf"):
                        out[md5(os.path.join(d, name))] = key
    return out


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def zotero_titles():
    db = os.path.join(ZOTERO_DIR, "zotero.sqlite")
    if not os.path.exists(db):
        return []
    con = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
    rows = con.execute("""select i.key, v.value from items i
        join itemData d on d.itemID=i.itemID
        join fields f on f.fieldID=d.fieldID and f.fieldName='title'
        join itemDataValues v on v.valueID=d.valueID
        join itemTypes t on t.itemTypeID=i.itemTypeID
        where t.typeName not in ('attachment','note','annotation')
          and i.itemID not in (select itemID from deletedItems)""").fetchall()
    return [(key, title, words(title)) for key, title in rows if len(words(title)) >= 4]


def suspected_title(pdf, titles):
    """Same paper downloaded separately has a different MD5; match the filename against Zotero titles."""
    joined = " " + " ".join(words(os.path.splitext(os.path.basename(pdf))[0])) + " "
    for key, title, tw in titles:
        if " " + " ".join(tw[:6]) + " " in joined:
            return key, title
    return None


def project_root(path):
    try:
        top = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        if top:
            return top
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    # not a git repo: a literature-named folder belongs to its parent project
    if os.path.basename(path).lower() in CANDIDATE_NAMES:
        return os.path.dirname(path)
    return path


def walk_pdfs(folder, excludes):
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(".")
                       and not any(fnmatch.fnmatch(d, p) for p in excludes)]
        for name in sorted(filenames):
            if name.lower().endswith(".pdf") and not any(fnmatch.fnmatch(name, p) for p in excludes):
                yield os.path.join(dirpath, name)


def list_candidates(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        if os.path.basename(dirpath).lower() in CANDIDATE_NAMES or "related_work" in dirpath.lower():
            n = sum(1 for _ in walk_pdfs(dirpath, []))
            if n:
                found.append((n, dirpath))
                dirnames[:] = []  # counted recursively already
    if not found:
        print("没有找到常见命名的文献目录（papers / literature / pdfs / refs ...），请直接指定目录。")
        return
    print("候选文献目录（PDF 数）：")
    for n, d in sorted(found, key=lambda x: -x[0]):
        print(f"  {n:4d}  {d}")
    print("\n选一个目录重新运行本脚本即可生成导入片段。")


JS_TEMPLATE = r"""// 由 zotero_import.py 生成。Zotero → 工具 → 开发者 → Run JavaScript，勾选 "Run as async function" 后运行。
const FILES = __FILES__;
const libID = Zotero.Libraries.userLibraryID;
const cache = new Map();

async function getColl(name, parentID) {
  const key = (parentID || 0) + "/" + name;
  if (cache.has(key)) return cache.get(key);
  const siblings = parentID ? Zotero.Collections.getByParent(parentID) : Zotero.Collections.getByLibrary(libID);
  let c = siblings.find(x => x.name === name && !x.deleted);
  if (!c) {
    c = new Zotero.Collection();
    c.libraryID = libID;
    c.name = name;
    if (parentID) c.parentID = parentID;
    await c.saveTx();
  }
  cache.set(key, c);
  return c;
}

async function collIDs(paths) {
  const ids = [];
  for (const parts of paths) {
    let c = null;
    for (const p of parts) c = await getColl(p, c ? c.id : null);
    ids.push(c.id);
  }
  return ids;
}

const imported = [], failed = [];
let linked = 0;
for (const f of FILES) {
  try {
    const ids = await collIDs(f.colls);
    if (f.key) {
      let item = Zotero.Items.getByLibraryAndKey(libID, f.key);
      if (!item) throw new Error("existing item not found: " + f.key);
      if (item.isAttachment() && item.parentItem) item = item.parentItem;
      for (const id of ids) item.addToCollection(id);
      await item.saveTx();
      linked++;
    } else {
      imported.push(await Zotero.Attachments.importFromFile({ file: f.path, libraryID: libID, collections: ids }));
    }
  } catch (e) {
    failed.push((f.path || f.key) + " :: " + e);
  }
}
if (imported.length) Zotero.RecognizeDocument.autoRecognizeItems(imported);
return `新导入 ${imported.length} 篇，已有条目加入集合 ${linked} 篇，失败 ${failed.length}。` +
  `元数据识别在后台进行，完成后检查未识别的条目。` + (failed.length ? "\n失败：\n" + failed.join("\n") : "");
"""


def collect(groups, keep_suspected):
    have = existing_hashes()
    titles = [] if keep_suspected else zotero_titles()
    entries, by_hash, report = [], {}, []
    for g in groups:
        stats = {"collection": g["collection"], "new": 0, "same_file": 0, "suspected": [], "subs": set(), "missing": []}
        for folder in g["folders"]:
            fixed = []  # {"path": ..., "sub": "name"} puts the whole folder under one sub-collection
            if isinstance(folder, dict):
                fixed = [folder["sub"]] if folder.get("sub") else []
                folder = folder["path"]
            folder = os.path.abspath(os.path.expanduser(folder))
            if not os.path.isdir(folder):
                stats["missing"].append(folder)
                continue
            for p in walk_pdfs(folder, g.get("exclude", [])):
                rel = os.path.relpath(os.path.dirname(p), folder)
                sub = fixed + ([] if g.get("flat") or rel == "." else rel.split(os.sep))
                coll = [g["collection"], *sub]
                if sub:
                    stats["subs"].add(" ▸ ".join(coll))
                h = md5(p)
                if h in by_hash:  # same file elsewhere in this run: one item, several collections
                    e = by_hash[h]
                    if coll not in e["colls"]:
                        e["colls"].append(coll)
                    continue
                if h in have:
                    e = {"key": have[h], "colls": [coll]}
                    stats["same_file"] += 1
                elif (m := suspected_title(p, titles)):
                    e = {"key": m[0], "colls": [coll]}
                    stats["suspected"].append((os.path.basename(p), m[1]))
                else:
                    e = {"path": p, "colls": [coll]}
                    stats["new"] += 1
                by_hash[h] = e
                entries.append(e)
        report.append(stats)
    return entries, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--plan", help="JSON 计划文件，一次导入多个项目")
    ap.add_argument("--collection", help="顶层集合名，默认为项目（git 根目录）名")
    ap.add_argument("--exclude", action="append", default=[], help="排除的目录/文件名 glob，可重复")
    ap.add_argument("--flat", action="store_true", help="不按子目录建子集合")
    ap.add_argument("--keep-suspected", action="store_true", help="文件名与 Zotero 已有标题相同的也作为新文件导入")
    ap.add_argument("--out", help="JS 输出路径")
    ap.add_argument("--no-copy", action="store_true", help="不复制到剪贴板")
    a = ap.parse_args()

    if a.plan:
        with open(os.path.expanduser(a.plan), encoding="utf-8") as f:
            groups = json.load(f)
        out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.plan)), "zotero-import.js")
    elif a.folder:
        folder = os.path.abspath(os.path.expanduser(a.folder))
        if not os.path.isdir(folder):
            sys.exit(f"不是目录：{folder}")
        root = project_root(folder)
        if folder == root and not a.collection and os.path.basename(folder).lower() not in CANDIDATE_NAMES:
            list_candidates(root)
            return
        groups = [{"collection": a.collection or os.path.basename(root), "folders": [folder],
                   "flat": a.flat, "exclude": a.exclude}]
        out = a.out or os.path.join(root, "docs", "zotero-import.js")
    else:
        ap.error("需要目录或 --plan")

    entries, report = collect(groups, a.keep_suspected)
    for s in report:
        print(f"【{s['collection']}】新导入 {s['new']} 篇，文件已在 Zotero {s['same_file']} 篇，"
              f"疑似同一论文 {len(s['suspected'])} 篇（后两类只加入集合，不重复导入）")
        for sub in sorted(s["subs"]):
            print(f"  子集合：{sub}")
        for name, title in s["suspected"]:
            print(f"  疑似已有：{name}  ≈  {title}")
        for m in s["missing"]:
            print(f"  目录不存在：{m}")
    if not entries:
        print("没有需要处理的文件。")
        return

    js = JS_TEMPLATE.replace("__FILES__", json.dumps(entries, ensure_ascii=False, indent=1))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"\n导入片段：{out}")
    if not a.no_copy:
        if copy_to_clipboard(js):
            print("已复制到剪贴板。")
        else:
            print("没有可用的剪贴板命令，请手动复制上面的文件内容。")
    print("下一步：打开 Zotero → 工具 → 开发者 → Run JavaScript → 勾选 Run as async function → 粘贴 → Run")


def copy_to_clipboard(text: str) -> bool:
    """Copy with the platform's clipboard command; False when none is available."""
    commands = {"darwin": [["pbcopy"]], "win32": [["clip"]]}.get(sys.platform, [["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]])
    for cmd in commands:
        try:
            subprocess.run(cmd, input=text.encode("utf-8"), check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


if __name__ == "__main__":
    main()
