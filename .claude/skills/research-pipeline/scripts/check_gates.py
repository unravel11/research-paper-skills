#!/usr/bin/env python3
"""File-level gate check for a research-pipeline paper project.

Reads ``research/STATE.md`` to find the current stage ``R<n>``, then checks
whether the artifacts that stage's exit gate requires exist and have the
expected shape: required sections, filled table rows, protocol hashes that
match the working tree, ledger status values from the orchestrator contract,
the orchestrator state file. It never declares a gate passed. A file can exist
and still be wrong, so the report separates what the script verified from
what a person has to judge, and the user confirms every stage transition.

Artifacts are looked up at the default paths of the project skeleton
(``paper/FRAMING.md`` and so on). A project that keeps them elsewhere maps
them in the ``## 阶段产出索引`` section of ``research/STATE.md``::

    - R1：paper/FRAMING.md → paper/latex/FRAMING-ARG.md、STORY_SPINE → paper/latex/SKELETON.md

Left of the arrow (``→``, ``->`` or ``=>``) is the default path or its short
name as listed in ``ARTIFACTS``; right of it is the real path relative to the
project root. A directory on the right is searched with the default file
pattern (for a single file, the default file name). Anything not mapped falls
back to the default path, so a project created by ``init_paper_project.py``
needs no mapping. HTML comments in the section are ignored.

Usage:
    python3 check_gates.py [PROJECT_DIR] [--stage R2] [--json]

Exit codes: 0 every file-level check passed; 1 at least one failed;
2 no readable research/STATE.md and no --stage given.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

STAGE_NAMES = {0: "方向", 1: "主线与故事", 2: "试点与实验协议", 3: "实验执行与结算", 4: "写作", 5: "评审与投稿"}

EVIDENCE_STATUS = {
    "VERIFIED_CURRENT",
    "CONTROLLED_OR_RETROSPECTIVE",
    "EXPLORATORY_OR_CANDIDATE",
    "SUPERSEDED_OR_INVALID",
    "MISSING_OR_UNRESOLVED",
}
CLAIM_STATUS = {"SUPPORTED", "WEAKEN", "ABSTAIN", "REMOVE_FROM_CURRENT_CHAIN"}
STYLE_USABLE = {"PROFILE_SAVED", "TARGET_AUDITED", "STYLE_APPLIED"}
L3_RECOMMENDATIONS = (
    "GO_INTERNAL_REVIEW",
    "GO_AFTER_TARGETED_REVISIONS",
    "NO_GO_MAJOR_REVISION",
    "NO_GO_EVIDENCE_GAP",
    "ABSTAIN_INCOMPLETE_MANUSCRIPT",
)
FRAMING_HEADINGS = ("一句话主张", "读者", "潜力卡", "研究问题", "最强基线", "不主张")
LEDGER_SUFFIXES = {".csv", ".json", ".md"}

SHA_RE = re.compile(r"\b[0-9a-f]{64}\b")
HASH_ROW_RE = re.compile(r"^\|\s*`?([^|`\n]+?)`?\s*\|\s*([0-9a-f]{64})\s*\|", re.M)
STAGE_RE = re.compile(r"当前阶段[:：]\s*R(\d)")
TOKEN_RE = re.compile(r"[㐀-䶿一-鿿豈-﫿]|[A-Za-z0-9]+")
# One "默认路径 → 实际路径" pair inside the 阶段产出索引 section. Items are separated by
# 、 ； ; or line breaks; an annotation in brackets after a path (on either side) is not part of it.
INDEX_PAIR_RE = re.compile(
    r"`?(?P<lhs>[^`、；;：:\s（）()]+)`?(?:（[^）]*）|\([^)]*\))?[ \t]*(?:→|->|=>)[ \t]*`?(?P<rhs>[^`、；;\s（）()]+)`?"
)

# Reference templates whose ```markdown block is what authors copy; a section whose body still
# equals the template's is unfilled even though every keyword is present.
TEMPLATE_FILES = {
    "protocol": Path(__file__).resolve().parents[1] / "references" / "experiment-protocol.md",
    "result": Path(__file__).resolve().parents[1] / "references" / "experiment-run.md",
}

# Research-type profiles under references/methods/; the protocol declares one with "- 研究类型：<name>".
METHOD_DIR = Path(__file__).resolve().parents[1] / "references" / "methods"
METHOD_MANUAL = {
    "quantitative-experiment": "量化实验档案：划分与不碰的评测集、基线调参公平、重复次数与一致性规则、区间与多重比较、环境版本",
    "measurement-study": "测量研究档案：抽样框与分母表、筛选条件人工验证、度量效度、标注信度、主张类型与证据匹配",
    "tool-or-system-evaluation": "工具评估档案：对象集代表性、替代方案公平配置、真值与裁决规则、失败计入分母、消融对应主张",
    "case-study-or-qualitative": "案例与定性档案：选择理由、提纲或问卷为指纹、编码本与分歧处理、饱和与信度、反例搜索、伦理",
    "human-subjects-experiment": "人类参与者实验档案：假设与变量、随机分配、功效与最小可检测效应、操作检查、预注册时间戳、伦理",
    "formal-or-theoretical": "形式化档案：假设清单与必要性、证明义务表、机械化边界、退化情形与反例搜索",
    "replication": "复现档案：复现类型三轴、与原研究差异登记、一致性标准事先定、原作者关系透明",
}
METHOD_RE = re.compile(r"^-?[ \t]*研究类型[^:：\n]*[:：][ \t]*(\S.*)$", re.M)

# Items a person must judge; the script only lists them for the current stage.
MANUAL = {
    0: [
        "用户明确选定排序，并写下前提条件（数据形态、可用信号、算力、不做什么）",
        "已排除的方向各有一句理由",
        "从观察起步的方向：伪像排查先于重要性判断，未排除的写进前提条件，排查与刻画的产出标 exploratory",
    ],
    1: [
        "研究类型选对了：对照 references/methods/README.md 的适用表，两种时主次写明",
        "每个 RQ 有且只有一个主要比较；判定规则写了成立、不成立、不能判定与稳健性要求（按研究类型档案），没有“视情况”；阴性可解释的前提已写",
        "每个主要比较的推算成立：只用已核实的数字加写明的前提，能落进判定规则同一档的不作主要比较；只有下界或跨档的把下界写进了那一列",
        "基线是当前最强版本，版本来源写明",
        "读者、原信念、张力有依据；每个分支的转折是读者会改变判断的发现，不成立分支有退路 venue",
        "潜力卡有前瞻档位；venue 候选的 essential 属性并集已写进 VENUE_PROFILE",
        "建议：paper-review 的 L1 前瞻用法，至少一个 framing 通过且两个分支都有去处",
        "用户确认主张、骨架与 venue 候选",
    ],
    2: [
        "判定规则在接触任何确认性结果之前写定，三种结局都写了；没有“视情况”",
        "稳健性要求按研究类型档案写明；对象与数据的来源、选择、已看过与不碰的部分写清",
        "试做结论已写回潜力卡与骨架分支（或免做理由成立）；试做材料未被用作论文证据",
        "结果中性检查能让阴性结果可解释；协议覆盖 venue 候选的 essential 属性并集",
        "分析脚本也在指纹表里；偏离登记表已建",
        "授权逐项引用用户决定，不由阶段推导",
        "用户确认冻结，冻结时间已记录",
    ],
    3: [
        "每个 RQ 有按协议规则得出的判定（成立 / 不成立 / 不能判定），稳健性要求按档案核对，不挑选；结果中性检查结果已记录",
        "偏离已登记（日期、理由、谁决定、影响），没有以结果为理由的偏离；事后分析带 post hoc 与触发原因，没有升格为协议内结论；结果不如预期已按四类归因",
        "结算选定的分支与台账一致，没有把分支揉在一起；venue 决定写了理由",
        "关键结论登记了复核者，复核者实际重算过",
        "原始数据、模型、日志留在远端；本地只有轻量汇总",
    ],
    4: [
        "本地编译无未定义引用、无 overfull",
        "paper-storytelling 第 4 节症状清单全部为否",
        "每个正文数字可追到台账或输出文件",
        "骨架复核：转折依赖的证据仍是 VERIFIED_CURRENT，章节顺序与骨架一致",
    ],
    5: [
        "L3 最新结论为 GO 或 GO_AFTER_TARGETED_REVISIONS，且修订已做并重新 S4",
        "L3 看过渲染后的 PDF（版面、图表、字号）",
        "接受而不回退的 FAIL 门（如 L2-G1 无独立真值）：STATE.md 有效授权有日期与范围，阻塞 / 待用户决定有补救措施或退路及期限；补救完成后该门重判",
        "artifact 可验证（S6）；作者字段、声明、DOI、投稿材料齐全（S7）",
        "投稿动作由用户执行",
    ],
}


# --- artifact registry and layout --------------------------------------------

@dataclass(frozen=True)
class Artifact:
    """One artifact the gates look for, keyed by its default path as the STATE.md template writes it.

    kind: "file" (one file), "dir" (a directory that must contain files), "glob" (one of
    several files matched by ``pattern`` under ``default_dir``), or "group" (a directory from
    the template index that stands for the ``members`` listed).
    """

    key: str
    kind: str
    stages: tuple[int, ...]
    aliases: tuple[str, ...] = ()
    default_dir: str = ""
    pattern: str = ""
    members: tuple[str, ...] = ()


ARTIFACTS: tuple[Artifact, ...] = (
    Artifact("docs/innovation-log.md", "file", (0,), ("innovation-log",)),
    Artifact("paper/FRAMING.md", "file", (1,), ("FRAMING",)),
    Artifact("paper/STORY_SPINE.md", "file", (1, 3), ("STORY_SPINE",)),
    Artifact("paper/VENUE_PROFILE.md", "file", (1, 3), ("VENUE_PROFILE",)),
    Artifact("experiments/PILOT_<date>.md", "glob", (2,), ("PILOT",), "experiments", "PILOT_*.md"),
    Artifact("experiments/PROTOCOL_<date>.md", "glob", (2,), ("PROTOCOL",), "experiments", "PROTOCOL_*.md"),
    Artifact("reports/<run>/RESULT.md", "glob", (3,), ("RESULT",), "reports", "*/RESULT.md"),
    Artifact("paper/STORY_SPINE_R1_<date>.md", "glob", (3,), ("STORY_SPINE_R1",), "paper", "STORY_SPINE_R1_*.md"),
    Artifact("paper/ledger/evidence_inventory.csv", "glob", (3,), ("evidence_inventory",), "paper/ledger", "evidence_inventory.*"),
    Artifact("paper/ledger/claim_ledger.csv", "glob", (3,), ("claim_ledger",), "paper/ledger", "claim_ledger.*"),
    Artifact("paper/FIGURE_PLAN.md", "file", (4,), ("FIGURE_PLAN",)),
    Artifact(".paper-style/WRITING-CONTRACT.md", "file", (4,), ("WRITING-CONTRACT",)),
    Artifact(".paper-style/STYLE-STATE.json", "file", (4,), ("STYLE-STATE",)),
    Artifact("paper/manuscript/", "dir", (4,), ("manuscript",)),
    Artifact("paper/state.json", "file", (4, 5), ("state.json",)),
    Artifact("paper/review/", "dir", (5,), ("review",)),
    # Directories the template index names that stand for several artifacts.
    Artifact("paper/ledger/", "group", (3,), ("ledger",), members=("paper/ledger/evidence_inventory.csv", "paper/ledger/claim_ledger.csv")),
    Artifact(".paper-style/", "group", (4,), ("paper-style",), members=(".paper-style/WRITING-CONTRACT.md", ".paper-style/STYLE-STATE.json")),
)
ARTIFACT_BY_KEY = {a.key: a for a in ARTIFACTS}


def alias_table() -> dict[str, str]:
    """Lower-cased names the index may use on the left of the arrow, mapped to artifact keys."""
    table: dict[str, str] = {}
    for art in ARTIFACTS:
        bare = art.key.rstrip("/")
        for name in (art.key, bare, bare.rsplit("/", 1)[-1], *art.aliases):
            table[name.lower()] = art.key
    return table


class Layout:
    """Where the artifacts live: skeleton defaults, overridden by STATE.md's 阶段产出索引."""

    def __init__(self, root: Path, pairs: list[tuple[str, str]] | None = None) -> None:
        self.root = root
        self.overrides: dict[str, str] = {}
        self.unknown: list[str] = []
        table = alias_table()
        for lhs, rhs in pairs or []:
            name = re.sub(r"[（(][^（）()]*[）)]$", "", lhs.strip().strip("`")).strip()
            key = table.get(name.lower()) or table.get(name.lower().rstrip("/"))
            value = rhs.strip().strip("`")
            if value.startswith("./"):
                value = value[2:]
            if key is None or not value:
                self.unknown.append(lhs.strip())
                continue
            for target in ARTIFACT_BY_KEY[key].members or (key,):
                self.overrides[target] = value

    def label(self, key: str) -> str:
        """What to call the artifact in the report: the resolved path when the index moved it."""
        if key not in self.overrides:
            return key
        if ARTIFACT_BY_KEY[key].kind == "file":
            return rel(self.root, self.path(key))
        return self.overrides[key]

    def note(self, key: str) -> str:
        return "（按 STATE.md 索引）" if key in self.overrides else ""

    def missing(self, key: str, extra: str = "") -> str:
        text = "缺失（STATE.md 索引指向此路径）" if key in self.overrides else "缺失"
        return f"{text}；{extra}" if extra else text

    def path(self, key: str) -> Path:
        """Resolved path of a file or dir artifact. A directory given for a file artifact means the default file name inside it."""
        art = ARTIFACT_BY_KEY[key]
        if key in self.overrides:
            target = self.root / self.overrides[key]
            if art.kind == "file" and target.is_dir():
                target = target / key.rsplit("/", 1)[-1]
            return target
        return self.root / key

    def files(self, key: str, suffixes: set[str] | None = None) -> list[Path]:
        """Matching files of a glob artifact, sorted by name. An explicit file in the index is taken as is."""
        art = ARTIFACT_BY_KEY[key]
        if key in self.overrides:
            target = self.root / self.overrides[key]
            if target.is_file():
                return [target]
            if not target.is_dir():
                return []
            found = sorted(p for p in target.rglob(art.pattern.rsplit("/", 1)[-1]) if p.is_file())
        else:
            base = self.root / art.default_dir
            found = sorted(p for p in base.glob(art.pattern) if p.is_file()) if base.is_dir() else []
        if suffixes:
            found = [p for p in found if p.suffix.lower() in suffixes]
        return found


@dataclass
class Check:
    label: str
    ok: bool | None  # None means skipped
    detail: str = ""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def visible_length(text: str) -> int:
    """Count CJK characters and Latin words, ignoring punctuation."""
    return len(TOKEN_RE.findall(text))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def has_files(directory: Path) -> bool:
    return directory.is_dir() and any(p.is_file() and p.name != ".gitkeep" for p in directory.rglob("*"))


def dir_check(layout: Layout, key: str, label: str) -> Check:
    """A directory artifact passes when it holds at least one real file."""
    path = layout.path(key)
    if has_files(path):
        return Check(label, True, "有" + layout.note(key))
    return Check(label, False, "目录存在但为空" if path.is_dir() else layout.missing(key))


def parse_md_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def load_rows(path: Path) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    text = read_text(path)
    if suffix == ".csv":
        return [dict(r) for r in csv.DictReader(text.splitlines())]
    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    data = value
                    break
        return [r for r in data if isinstance(r, dict)] if isinstance(data, list) else []
    return parse_md_table(text)


def status_values(rows: list[dict[str, str]]) -> list[str]:
    values: list[str] = []
    for row in rows:
        for key, value in row.items():
            if key and key.strip().lower() in {"status", "状态"}:
                values.append((value or "").strip())
                break
    return values


def md_sections(text: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, body) pairs at '## ' headings; body before the first heading has heading ''."""
    sections: list[tuple[str, str]] = []
    heading, buf = "", []
    for line in text.splitlines():
        if re.match(r"^##\s+", line):
            sections.append((heading, "\n".join(buf)))
            heading, buf = line.strip("# ").strip(), []
        else:
            buf.append(line)
    sections.append((heading, "\n".join(buf)))
    return sections


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


_template_cache: dict[str, dict[str, str]] = {}


def template_sections(kind: str) -> dict[str, str]:
    """Normalized section bodies of a reference template's ```markdown block, keyed by heading; empty if unavailable."""
    if kind not in _template_cache:
        sections: dict[str, str] = {}
        path = TEMPLATE_FILES.get(kind)
        if path is not None and path.is_file():
            block = re.search(r"```markdown\n(.*?)```", read_text(path), re.S)
            if block:
                sections = {h: _norm(b) for h, b in md_sections(block.group(1)) if h}
        _template_cache[kind] = sections
    return _template_cache[kind]


def section_filled(text: str, prefix: str, kind: str) -> bool | None:
    """True when a '## <prefix>…' section exists and its body is neither empty nor the template's own text; None when there is no such heading."""
    for heading, body in md_sections(text):
        if heading.startswith(prefix):
            norm = _norm(body)
            if not norm:
                return False
            template = next((b for h, b in template_sections(kind).items() if h.startswith(prefix)), None)
            return norm != template
    return None


def filled_check(name: str, text: str, prefix: str, kind: str, has_keywords: bool, missing: str) -> Check:
    """Keyword presence plus a filled section; without the heading the keyword test alone decides, as before."""
    if not has_keywords:
        return Check(name, False, missing)
    if section_filled(text, prefix, kind) is False:
        return Check(name, False, f"“{prefix}”节为空或还是模板原文")
    return Check(name, True, "有")


def l3_recommendation(path: Path, text: str) -> str | None:
    """The L3 recommendation a review file states, or None.

    A JSON review record states it in ``recommendation``. In markdown or text the last line that
    names exactly one recommendation counts; a line listing several (the report template's enum)
    is ignored.
    """
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return None
        value = data.get("recommendation") if isinstance(data, dict) else None
        return value if value in L3_RECOMMENDATIONS else None
    found = None
    for line in text.splitlines():
        tokens = [t for t in L3_RECOMMENDATIONS if t in line]
        if len(tokens) == 1:
            found = tokens[0]
    return found


# --- per-stage checks -------------------------------------------------------

def checks_r0(root: Path, layout: Layout) -> list[Check]:
    key = "docs/innovation-log.md"
    log, name = layout.path(key), layout.label(key)
    if not log.exists():
        return [Check(name, False, layout.missing(key))]
    text = read_text(log)
    out = [Check(name, True, "存在" + layout.note(key))]
    section = re.search(r"##\s*最终选定(.*?)(?=\n##\s|\Z)", text, re.S)
    if section:
        chosen = re.search(r"^-?[ \t]*思路[:：][ \t]*(\S.*)$", section.group(1), re.M)
        out.append(Check("“最终选定”已填写思路", bool(chosen), chosen.group(1).strip()[:60] if chosen else "思路一栏为空"))
    else:
        out.append(Check("“最终选定”小节", False, "缺少 “## 最终选定”"))
    excluded = re.search(r"^-?[ \t]*已排除方向[:：][ \t]*(\S.*)$", text, re.M)
    out.append(Check("研究设定·已排除方向已填写", bool(excluded), excluded.group(1).strip()[:60] if excluded else "为空"))
    anomaly = next((b for h, b in md_sections(text) if h.startswith("异常入口")), None)
    if anomaly is not None and re.search(r"[^\s|:：\-]", re.sub(r"^#.*$|^\|.*$|^-[^:：\n]*[:：]\s*$", "", anomaly, flags=re.M)):
        observation = re.search(r"^-?[ \t]*观察句[^:：\n]*[:：][ \t]*(\S.*)$", anomaly, re.M)
        out.append(Check("异常入口：观察句已填写", bool(observation), observation.group(1).strip()[:60] if observation else "为空"))
        rows = [r for r in parse_md_table(anomaly) if r and list(r.values())[0].strip()]
        results = [next((v for k, v in r.items() if "结果" in k), "") for r in rows]
        pending = [r for r in results if not r.strip() or "未查" in r]
        out.append(Check("异常入口：伪像排查表每行有结果", bool(rows) and not pending, f"{len(rows)} 行，{len(pending)} 行未查或为空" if rows else "排查表为空"))
        unresolved = sum(1 for r in results if "未排除" in r)
        if unresolved:
            out.append(Check("异常入口：未排除的伪像需写进前提条件", None, f"{unresolved} 行未排除"))
        condition = re.search(r"^-?[ \t]*条件[:：][ \t]*(\S.*)$", anomaly, re.M)
        out.append(Check("异常入口：现象卡·条件已填写", bool(condition), condition.group(1).strip()[:60] if condition else "为空"))
    return out


def rq_table(text: str) -> tuple[list[str], list[list[str]]]:
    """Header cells and RQ rows of the FRAMING research-question table."""
    header: list[str] = []
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if cells and cells[0] == "RQ":
            header = cells
        elif header and cells and re.match(r"RQ\s*\d", cells[0]):
            rows.append(cells)
    return header, rows


def derivation_checks(text: str) -> list[Check]:
    """Every main comparison states whether its answer already follows from verified numbers."""
    header, rows = rq_table(text)
    col = next((i for i, h in enumerate(header) if "推出答案" in h), None)
    if col is None:
        return [Check("RQ 表有“不跑实验能否推出答案”列", False, "没有这一列；按 framing-template.md 的表头补上并逐行填写")]
    out: list[Check] = []
    for cells in rows:
        rq, value = cells[0], cells[col] if col < len(cells) else ""
        if not value:
            out.append(Check(f"{rq} 推算已填", False, "“不跑实验能否推出答案”为空；写推算、前提、预测值，以“推不出：”或“能推出：”开头"))
        elif value.startswith("能推出"):
            out.append(Check(f"{rq} 答案不能已由已有数字推出", False, "填了“能推出”：不作主要比较，降为标定或已知发现"))
        else:
            out.append(Check(f"{rq} 推算已填", True, value[:40]))
    return out


def checks_r1(root: Path, layout: Layout) -> list[Check]:
    out: list[Check] = []
    key = "paper/FRAMING.md"
    framing, name = layout.path(key), layout.label(key)
    if framing.exists():
        text = read_text(framing)
        missing = [h for h in FRAMING_HEADINGS if h not in text]
        out.append(Check(f"{name} 必需小节", not missing, "缺少：" + "、".join(missing) if missing else " / ".join(FRAMING_HEADINGS) + " 齐全" + layout.note(key)))
        out.extend(method_checks(text))
        rows = [line for line in text.splitlines() if re.match(r"\|\s*RQ\s*\d", line)]
        complete = [r for r in rows if len([c for c in r.strip().strip("|").split("|") if c.strip()]) >= 5]
        out.append(Check("RQ 表至少一行且主要比较 / 指标 / 判定规则已填", bool(rows) and len(complete) == len(rows), f"{len(complete)}/{len(rows)} 行填写完整"))
        out.extend(derivation_checks(text))
        timing = re.search(r"^-?[ \t]*产生时点[:：][ \t]*(\S.*)$", text, re.M)
        timing_value = timing.group(1).strip() if timing else ""
        ok_timing = bool(re.search(r"事前|事后", timing_value)) and not re.search(r"事前\s*/\s*事后", timing_value)
        out.append(Check("产生时点已标注（事前 / 事后）", ok_timing, timing_value[:40] if timing_value else "未填写"))
    else:
        out.append(Check(name, False, layout.missing(key)))

    key = "paper/STORY_SPINE.md"
    spine = layout.path(key)
    if spine.exists():
        out.extend(spine_branch_checks(read_text(spine), layout.label(key) + layout.note(key)))
    else:
        out.append(Check(layout.label(key), False, layout.missing(key)))

    key = "paper/VENUE_PROFILE.md"
    venue = layout.path(key)
    if venue.exists():
        rows = [r for r in parse_md_table(read_text(venue)) if r and list(r.values())[0].strip()]
        out.append(Check("VENUE_PROFILE 至少一个候选", bool(rows), f"{len(rows)} 行候选" + layout.note(key)))
    else:
        out.append(Check(layout.label(key), False, layout.missing(key)))
    return out


def deletion_test(body: str) -> tuple[bool | None, str]:
    for line in body.splitlines():
        if "章节顺序" not in line:
            continue
        if "是 / 否" in line or "是/否" in line:
            return False, "删除测试还是模板原文，未作答"
        if re.search(r"[:：]\s*是", line):
            return True, "是"
        if re.search(r"[:：]\s*否", line):
            return False, "否：骨架未抓到中心主张"
    return None, "未找到“章节顺序”判断行"


def spine_branch_checks(text: str, source: str = "paper/STORY_SPINE.md") -> list[Check]:
    """Branch-aware checks: only branches with a filled one-sentence story count; at least two must be filled."""
    out: list[Check] = [Check(source, True, "存在")]
    branches = [(h, b) for h, b in md_sections(text) if h.startswith("分支")]
    if not branches:
        # legacy single-spine layout
        story = re.search(r"^-?[ \t]*一句话故事[^:：\n]*[:：][ \t]*(\S.*)$", text, re.M)
        if story:
            length = visible_length(story.group(1))
            out.append(Check("一句话故事 ≤ 40 字", length <= 40, f"{length} 字"))
        else:
            out.append(Check("一句话故事", False, "未填写"))
        ok, detail = deletion_test(text)
        out.append(Check("删除测试为“是”", bool(ok), detail))
        out.append(Check("骨架至少两个分支", False, "没有“## 分支”小节；按 story-spine-template.md 写成立 / 不成立两个分支"))
        return out
    filled = 0
    for heading, body in branches:
        story = re.search(r"^-?[ \t]*一句话故事[^:：\n]*[:：][ \t]*(\S.*)$", body, re.M)
        if not story:
            continue
        filled += 1
        length = visible_length(story.group(1))
        out.append(Check(f"{heading}：一句话故事 ≤ 40 字", length <= 40, f"{length} 字"))
        ok, detail = deletion_test(body)
        out.append(Check(f"{heading}：删除测试为“是”", bool(ok), detail))
        venue = re.search(r"^-?[ \t]*适合的 venue[^:：\n]*[:：][ \t]*(\S.*)$", body, re.M)
        out.append(Check(f"{heading}：有 venue 候选", bool(venue), venue.group(1).strip()[:40] if venue else "未填写"))
    out.append(Check("骨架至少两个填写了的分支", filled >= 2, f"{filled} 个分支填了一句话故事"))
    return out


def settlement_checks(root: Path, layout: Layout) -> list[Check]:
    out: list[Check] = []
    key = "paper/STORY_SPINE.md"
    spine = layout.path(key)
    if spine.exists():
        text = read_text(spine)
        section = next((b for h, b in md_sections(text) if h.startswith("结算")), None)
        if section is None:
            out.append(Check(f"{layout.label(key)} 结算节", False, "缺少“## 结算”"))
        else:
            chosen = re.search(r"^-?[ \t]*选定分支[:：][ \t]*(\S.*)$", section, re.M)
            out.append(Check("结算：选定分支已填写", bool(chosen), chosen.group(1).strip()[:40] if chosen else "为空"))
            basis = re.search(r"^-?[ \t]*依据[^:：\n]*[:：][ \t]*(\S.*)$", section, re.M)
            out.append(Check("结算：依据（证据 ID）已填写", bool(basis), basis.group(1).strip()[:40] if basis else "为空"))
    else:
        out.append(Check(layout.label(key), False, layout.missing(key)))
    key = "paper/STORY_SPINE_R1_<date>.md"
    archived = layout.files(key)
    out.append(Check(f"R1 骨架已归档（{layout.label(key)}）", bool(archived), rel(root, archived[-1]) if archived else layout.missing(key)))
    key = "paper/VENUE_PROFILE.md"
    venue = layout.path(key)
    if venue.exists():
        section = next((b for h, b in md_sections(read_text(venue)) if h.startswith("决定")), None)
        decided = re.search(r"^-?[ \t]*选定 venue[:：][ \t]*(\S.*)$", section or "", re.M)
        out.append(Check("VENUE_PROFILE：决定已填写", bool(decided), decided.group(1).strip()[:40] if decided else "为空"))
    else:
        out.append(Check(layout.label(key), False, layout.missing(key)))
    return out


def declared_methods(text: str) -> list[str]:
    """Profile names declared on the 研究类型 line, normalised to file stems."""
    match = METHOD_RE.search(text)
    if not match:
        return []
    value = re.sub(r"[（(][^（）()]*[）)]", " ", match.group(1)).strip()
    if not value or value.startswith("<"):
        return []
    names = re.split(r"[、,，;；/ ]+", value)
    return [re.sub(r"\.md$", "", n.strip("`（）() ")) for n in names if n.strip("`（）() ")]


def method_checks(text: str) -> list[Check]:
    names = declared_methods(text)
    if not names:
        return [Check("研究类型已声明（- 研究类型：<档案名>）", False, "未声明；可用档案见 references/methods/README.md")]
    out: list[Check] = []
    for name in names:
        exists = (METHOD_DIR / f"{name}.md").is_file()
        out.append(Check(f"研究类型档案存在：{name}", exists, "references/methods/" + name + ".md" if exists else "没有这个档案；按 methods/README.md 的结构新建或改名"))
    return out


def method_manual(text: str) -> list[str]:
    return [METHOD_MANUAL[n] for n in declared_methods(text) if n in METHOD_MANUAL]


def framing_consistency(layout: Layout, protocol_text: str) -> list[Check]:
    """R2 inherits the research type declared in FRAMING at R1; a change is made in FRAMING, not silently in the protocol."""
    key = "paper/FRAMING.md"
    framing = layout.path(key)
    label = "协议研究类型与 FRAMING 一致"
    if not framing.exists():
        return [Check(label, False, layout.missing(key))]
    declared = declared_methods(read_text(framing))
    if not declared:
        return [Check(label, False, f"{layout.label(key)} 没有“- 研究类型：”行；回 R1 补上" + layout.note(key))]
    protocol = declared_methods(protocol_text)
    if protocol == declared:
        return [Check(label, True, "一致：" + "、".join(declared))]
    return [Check(label, False, f"协议 {'、'.join(protocol) or '未声明'}，FRAMING {'、'.join(declared)}；改类型要在协议写理由并修订 FRAMING")]


def checks_r2(root: Path, layout: Layout) -> list[Check]:
    key = "experiments/PROTOCOL_<date>.md"
    protocols = layout.files(key)
    if not protocols:
        return [Check(layout.label(key), False, layout.missing(key))]
    protocol = protocols[-1]
    text = read_text(protocol)
    out = [Check(rel(root, protocol), True, "存在（取名称最新）" + layout.note(key))]
    out.extend(method_checks(text))
    out.extend(framing_consistency(layout, text))
    out.append(Check("协议含指纹（SHA-256）", bool(SHA_RE.search(text)), "有" if SHA_RE.search(text) else "没有任何 64 位十六进制哈希"))
    out.append(filled_check("协议含冻结记录", text, "执行与冻结", "protocol", "冻结" in text, "未出现“冻结”"))
    out.append(filled_check("协议含判定规则的三种结局", text, "判定规则", "protocol", all(k in text for k in ("成立", "不成立", "不能判定")), "缺少“成立 / 不成立 / 不能判定”之一"))
    out.append(filled_check("协议含结果中性检查", text, "结果中性检查", "protocol", "结果中性" in text, "未出现“结果中性检查”"))
    pilot_key = "experiments/PILOT_<date>.md"
    pilots = layout.files(pilot_key)
    # Only a list item that starts with the waiver counts: the checklist quotes the same phrase mid-line.
    waived = re.search(r"^\s*-\s*试点[:：]\s*免做", text, re.M) is not None
    # The reason has to sit on the same line as the waiver; the template mentions 理由 elsewhere.
    waived_with_reason = re.search(r"^\s*-\s*试点[:：]\s*免做[，,、（(]\s*理由[:：]\s*\S", text, re.M) is not None
    if pilots:
        out.append(Check("试点已做", True, rel(root, pilots[-1]) + layout.note(pilot_key)))
    elif waived:
        out.append(Check("试点免做并写了理由", waived_with_reason, "协议写明免做与理由" if waived_with_reason else "写了免做但同一行没有“理由：”"))
    else:
        out.append(Check("试点已做或写明免做理由", False, f"没有 {layout.label(pilot_key)}，协议里也没有“试点：免做，理由：”"))
    unchecked = len(re.findall(r"^\s*-\s*\[ \]", text, re.M))
    checked = len(re.findall(r"^\s*-\s*\[[xX]\]", text, re.M))
    if unchecked + checked:
        out.append(Check("冻结前检查单全部勾选", unchecked == 0, f"{checked}/{checked + unchecked} 已勾选"))
    else:
        out.append(Check("冻结前检查单全部勾选", False, "协议里没有检查单；把 experiment-protocol.md 的冻结前检查单（通用项 + 档案追加项）复制进协议并逐项勾选"))
    for match in HASH_ROW_RE.finditer(text):
        path_text, expected = match.group(1).strip(), match.group(2)
        if path_text.lower() in {"路径", "path", "file", "文件"}:
            continue
        target = root / path_text
        if not target.is_file():
            out.append(Check(f"哈希行文件存在：{path_text}", False, "文件不存在"))
            continue
        actual = sha256(target)
        out.append(Check(f"哈希一致：{path_text}", actual == expected, "一致" if actual == expected else f"不一致（当前 {actual[:12]}…）"))
    return out


def checks_r3(root: Path, layout: Layout) -> list[Check]:
    out: list[Check] = []
    key = "reports/<run>/RESULT.md"
    results = sorted(layout.files(key), key=lambda p: p.stat().st_mtime)
    if results:
        result = results[-1]
        text = read_text(result)
        out.append(Check(rel(root, result), True, "存在（取最近修改）" + layout.note(key)))
        out.append(filled_check("RESULT.md 含判定", text, "判定", "result", "判定" in text, "未出现“判定”"))
        post_hoc = "事后分析" in text or "post hoc" in text.lower()
        out.append(filled_check("RESULT.md 含事后分析节", text, "事后分析", "result", post_hoc, "未出现“事后分析 / post hoc”"))
        hashed = "哈希" in text or "指纹" in text or bool(SHA_RE.search(text))
        out.append(filled_check("RESULT.md 含指纹核对", text, "协议与指纹核对", "result", hashed, "未出现指纹 / 哈希核对"))
        out.append(filled_check("RESULT.md 含偏离登记", text, "偏离登记", "result", "偏离" in text, "未出现“偏离登记”（无偏离也要写“无”）"))
    else:
        out.append(Check(layout.label(key), False, layout.missing(key)))

    for key, name, allowed in (
        ("paper/ledger/evidence_inventory.csv", "evidence_inventory", EVIDENCE_STATUS),
        ("paper/ledger/claim_ledger.csv", "claim_ledger", CLAIM_STATUS),
    ):
        files = layout.files(key, LEDGER_SUFFIXES)
        if not files:
            out.append(Check(layout.label(key), False, layout.missing(key, "也接受 .json / .md")))
            continue
        # Several candidates (e.g. the empty skeleton .csv beside a filled .json): take the first with rows.
        path, rows, parsed = files[0], [], False
        for candidate in files:
            try:
                candidate_rows = load_rows(candidate)
            except Exception as exc:  # noqa: BLE001 - report any parse failure
                out.append(Check(f"{rel(root, candidate)} 可解析", False, str(exc)[:80]))
                continue
            if not parsed or (not rows and candidate_rows):
                path, rows, parsed = candidate, candidate_rows, True
        if not parsed:
            continue
        several = f"；{len(files)} 个候选文件，取有数据行的" if len(files) > 1 else ""
        out.append(Check(f"{rel(root, path)} 有数据行", len(rows) > 0, f"{len(rows)} 行" + layout.note(key) + several))
        if rows:
            values = status_values(rows)
            bad = sorted({v for v in values if v not in allowed})
            if values:
                out.append(Check(f"{name} 状态值符合合同", not bad, "非法值：" + ", ".join(bad) if bad else "全部合法"))
            else:
                out.append(Check(f"{name} 有 status 列", False, "找不到 status / 状态 列"))
    out.extend(settlement_checks(root, layout))
    return out


def find_state_validator() -> Path | None:
    here = Path(__file__).resolve()
    candidates = [here.parents[2] / "paper-writing-orchestrator" / "scripts" / "validate_paper_state.py"]
    for base in (Path.home() / ".claude" / "skills", Path.home() / ".codex" / "skills"):
        candidates.append(base / "paper-writing-orchestrator" / "scripts" / "validate_paper_state.py")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def orchestrator_stage(root: Path, layout: Layout, out: list[Check]) -> str | None:
    key = "paper/state.json"
    state, name = layout.path(key), layout.label(key)
    if not state.exists():
        out.append(Check(name, False, layout.missing(key)))
        return None
    try:
        data = json.loads(read_text(state))
    except json.JSONDecodeError as exc:
        out.append(Check(f"{name} 可解析", False, str(exc)[:80]))
        return None
    stage = data.get("stage") if isinstance(data, dict) else None
    out.append(Check(f"{name} 可解析", True, f"stage={stage}" + layout.note(key)))
    validator = find_state_validator()
    if validator is None:
        out.append(Check("validate_paper_state.py", None, "未找到 paper-writing-orchestrator 的校验脚本，跳过"))
    else:
        proc = subprocess.run([sys.executable, str(validator), str(state)], capture_output=True, text=True)
        message = (proc.stdout + proc.stderr).strip().splitlines()
        out.append(Check("validate_paper_state.py", proc.returncode == 0, (message[-1] if message else "通过")[:120]))
    return stage if isinstance(stage, str) else None


def checks_r4(root: Path, layout: Layout) -> list[Check]:
    out: list[Check] = []
    stage = orchestrator_stage(root, layout, out)
    if stage is not None:
        reached = stage in {"S5_VENUE_REVIEWED", "S6_ARTIFACT_VERIFIED", "S7_SUBMISSION_READY"}
        out.append(Check("orchestrator 阶段 ≥ S5_VENUE_REVIEWED", reached, stage))

    key = "paper/FIGURE_PLAN.md"
    plan = layout.path(key)
    if plan.exists():
        text = read_text(plan)
        rows = [line for line in text.splitlines() if re.match(r"\|\s*(Fig|Tab|图|表)", line)]
        filled = [r for r in rows if len(r.split("|")) > 3 and r.split("|")[3].strip()]
        out.append(Check("FIGURE_PLAN 每行有一句结论", bool(rows) and len(filled) == len(rows), f"{len(filled)}/{len(rows)} 行" + layout.note(key)))
        fig1 = re.search(r"^-[ \t]*图一[^:：\n]*[:：][ \t]*(\S.*)$", text, re.M)
        out.append(Check("图一已确定", bool(fig1), fig1.group(1).strip()[:60] if fig1 else "图一一栏为空"))
    else:
        out.append(Check(layout.label(key), False, layout.missing(key)))

    key = ".paper-style/WRITING-CONTRACT.md"
    contract = layout.path(key)
    out.append(Check(layout.label(key), contract.exists(), "存在" + layout.note(key) if contract.exists() else layout.missing(key, "paper-style-profiler 尚未产出风格合同")))
    key = ".paper-style/STYLE-STATE.json"
    state = layout.path(key)
    if state.exists():
        try:
            status = json.loads(read_text(state)).get("status")
        except (json.JSONDecodeError, AttributeError):
            status = None
        out.append(Check("风格合同状态可用", status in STYLE_USABLE, str(status)))

    key = "paper/manuscript/"
    out.append(dir_check(layout, key, f"{layout.label(key)} 有文件"))
    return out


def checks_r5(root: Path, layout: Layout) -> list[Check]:
    out: list[Check] = []
    key = "paper/review/"
    review = layout.path(key)
    out.append(dir_check(layout, key, f"{layout.label(key)} 有评审记录"))
    if has_files(review):
        latest: tuple[float, str, str] | None = None
        for path in review.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".txt"}:
                continue
            token = l3_recommendation(path, read_text(path))
            if token is None:
                continue
            stamp = path.stat().st_mtime
            if latest is None or stamp > latest[0]:
                latest = (stamp, token, rel(root, path))
        if latest:
            go = latest[1].startswith("GO")
            out.append(Check("最新评审结论为 GO 类", go, f"{latest[1]}（{latest[2]}）"))
        else:
            out.append(Check("评审记录含 L3 结论", False, "未找到只写一个结论的“推荐：”行或 REVIEW-RECORD 的 recommendation（GO / NO_GO / ABSTAIN）"))
    stage = orchestrator_stage(root, layout, out)
    if stage is not None:
        out.append(Check("orchestrator 阶段 = S7_SUBMISSION_READY", stage == "S7_SUBMISSION_READY", stage))
    return out


CHECKS = {0: checks_r0, 1: checks_r1, 2: checks_r2, 3: checks_r3, 4: checks_r4, 5: checks_r5}


# --- STATE.md ---------------------------------------------------------------

@dataclass
class StateInfo:
    exists: bool = False
    stage: int | None = None
    last_checked: str = ""
    next_steps: list[str] = field(default_factory=list)
    index: list[tuple[str, str]] = field(default_factory=list)


def parse_index(text: str) -> list[tuple[str, str]]:
    """Return the (默认路径, 实际路径) pairs written in the 阶段产出索引 section; HTML comments are ignored."""
    section = next((b for h, b in md_sections(text) if h.startswith("阶段产出索引")), "")
    section = re.sub(r"<!--.*?-->", "", section, flags=re.S)
    return [(m.group("lhs"), m.group("rhs")) for m in INDEX_PAIR_RE.finditer(section)]


def parse_state(root: Path) -> StateInfo:
    state = root / "research" / "STATE.md"
    if not state.exists():
        return StateInfo()
    text = read_text(state)
    match = STAGE_RE.search(text)
    checked = re.search(r"最近核对[:：][ \t]*(\S.*)$", text, re.M)
    section = re.search(r"##\s*下一步(.*?)(?=\n##\s|\Z)", text, re.S)
    next_steps = []
    if section:
        next_steps = [line.strip()[1:].strip() for line in section.group(1).splitlines() if line.strip().startswith("-") and line.strip()[1:].strip()]
    return StateInfo(
        exists=True,
        stage=int(match.group(1)) if match else None,
        last_checked=checked.group(1).strip() if checked else "",
        next_steps=next_steps,
        index=parse_index(text),
    )


def index_notices(root: Path, layout: Layout, stage: int) -> list[Check]:
    """Index problems the stage checks would not surface: unknown names, and mapped paths of other stages that do not exist."""
    out = [Check(f"STATE.md 索引：“{name}”不是已知产物名", None, "忽略；可用名见 check_gates.py 的 ARTIFACTS") for name in layout.unknown]
    for key, value in layout.overrides.items():
        if stage not in ARTIFACT_BY_KEY[key].stages and not (root / value).exists():
            out.append(Check(f"STATE.md 索引：{key} → {value}", None, "路径不存在（非本阶段产物，仅提示）"))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_dir", nargs="?", default=".", help="paper project root (default: current directory)")
    parser.add_argument("--stage", help="override the stage to check, e.g. R2 (default: read research/STATE.md)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    root = Path(args.project_dir).expanduser().resolve()
    info = parse_state(root)
    layout = Layout(root, info.index)
    if args.stage:
        match = re.fullmatch(r"R?(\d)", args.stage.strip(), re.I)
        if not match or int(match.group(1)) not in STAGE_NAMES:
            print("error: --stage must be R0..R5", file=sys.stderr)
            return 2
        stage = int(match.group(1))
    elif info.stage is None:
        if info.exists:
            print("error: research/STATE.md 没有可解析的“- 当前阶段：R<n> <名称>”行", file=sys.stderr)
        else:
            print(
                f"error: {root} 下没有 research/STATE.md。新项目运行 init_paper_project.py 建骨架；"
                "已有自己文件布局的项目运行 init_paper_project.py --state-only 只建 STATE.md 与 PROGRESS.md，"
                "再在 STATE.md 的阶段产出索引里写“默认路径 → 实际路径”",
                file=sys.stderr,
            )
        return 2
    else:
        stage = info.stage

    checks = index_notices(root, layout, stage) + CHECKS[stage](root, layout)
    manual = list(MANUAL[stage])
    if stage in (2, 3):
        protocols = layout.files("experiments/PROTOCOL_<date>.md")
        framing = layout.path("paper/FRAMING.md")
        source = protocols[-1] if protocols else (framing if framing.exists() else None)
        if source is not None:
            manual.extend(method_manual(read_text(source)))
    failed = [c for c in checks if c.ok is False]
    passed = [c for c in checks if c.ok is True]
    exit_code = 1 if failed else 0

    if args.json:
        payload = {
            "project": str(root),
            "stage": f"R{stage}",
            "stage_name": STAGE_NAMES[stage],
            "last_checked": info.last_checked,
            "layout": layout.overrides,
            "index_unknown": layout.unknown,
            "checks": [asdict(c) for c in checks],
            "manual": manual,
            "next_steps": info.next_steps,
            "file_level_passed": not failed,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return exit_code

    suffix = f"（STATE.md 最近核对：{info.last_checked}）" if info.last_checked else "（--stage 指定）" if args.stage else ""
    print(f"阶段：R{stage} {STAGE_NAMES[stage]}{suffix}")
    print(f"项目：{root}")
    if layout.overrides:
        here = {k: v for k, v in layout.overrides.items() if stage in ARTIFACT_BY_KEY[k].stages}
        others = len(layout.overrides) - len(here)
        tail = f"（另有 {others} 条属于其他阶段）" if others else ""
        print(f"STATE.md 索引覆盖的默认路径{tail}：")
        for key, value in here.items():
            print(f"  {key} → {value}")
    print("文件级核对（文件存在不等于门槛已过）：")
    for check in checks:
        mark = "x" if check.ok else "-" if check.ok is None else " "
        detail = f" — {check.detail}" if check.detail else ""
        print(f"  [{mark}] {check.label}{detail}")
    print("需人工核对：")
    for item in manual:
        print(f"  - {item}")
    if info.next_steps:
        print("STATE.md 下一步：")
        for step in info.next_steps:
            print(f"  - {step}")
    print(f"结论：文件级核对 {len(passed)}/{len(passed) + len(failed)} 通过；人工项 {len(manual)} 条待判断。R{stage} 门槛是否已过由用户确认。")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
