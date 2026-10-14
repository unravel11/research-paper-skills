#!/usr/bin/env python3
"""List Zotero items (title / year / venue / PDF path) from the local zotero.sqlite.

Opens the database read-only in immutable mode so it works while Zotero is running.

Usage:
  zotero_list.py                       # list collections with item counts
  zotero_list.py --collection "EA"     # items in a collection (recursive)
  zotero_list.py --search "authorization"   # title/abstract substring match
  zotero_list.py --collection "EA" --json   # machine-readable output
"""
import argparse
import json
import os
import sqlite3
import sys

ZOTERO_DIR = os.path.expanduser(os.environ.get("ZOTERO_DIR", "~/Zotero"))
DB = os.path.join(ZOTERO_DIR, "zotero.sqlite")


def connect():
    if not os.path.exists(DB):
        sys.exit(f"zotero.sqlite not found at {DB} (set ZOTERO_DIR)")
    return sqlite3.connect(f"file:{DB}?immutable=1", uri=True)


def field(con, item_id, name):
    row = con.execute(
        """select v.value from itemData d
           join fields f on f.fieldID=d.fieldID
           join itemDataValues v on v.valueID=d.valueID
           where d.itemID=? and f.fieldName=?""",
        (item_id, name),
    ).fetchone()
    return row[0] if row else ""


def first_author(con, item_id):
    row = con.execute(
        """select c.lastName from itemCreators ic
           join creators c on c.creatorID=ic.creatorID
           where ic.itemID=? order by ic.orderIndex limit 1""",
        (item_id,),
    ).fetchone()
    return row[0] if row else ""


def pdf_path(con, item_id):
    for att_id, link_mode, path in con.execute(
        """select itemID, linkMode, path from itemAttachments
           where parentItemID=? and contentType='application/pdf'""",
        (item_id,),
    ):
        if not path:
            continue
        if path.startswith("storage:"):
            key = con.execute("select key from items where itemID=?", (att_id,)).fetchone()[0]
            return os.path.join(ZOTERO_DIR, "storage", key, path[len("storage:"):])
        return path
    return ""


def collection_ids(con, name):
    rows = con.execute(
        "select collectionID from collections where collectionName=? collate nocase", (name,)
    ).fetchall()
    ids = [r[0] for r in rows]
    frontier = list(ids)
    while frontier:  # include sub-collections
        cid = frontier.pop()
        kids = [r[0] for r in con.execute(
            "select collectionID from collections where parentCollectionID=?", (cid,))]
        ids.extend(kids)
        frontier.extend(kids)
    return ids


def regular_items(con, where="", params=()):
    # exclude attachments, notes and deleted items
    return [r[0] for r in con.execute(
        f"""select i.itemID from items i
            join itemTypes t on t.itemTypeID=i.itemTypeID
            where t.typeName not in ('attachment','note','annotation')
              and i.itemID not in (select itemID from deletedItems) {where}""",
        params)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection")
    ap.add_argument("--search")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    con = connect()

    if not a.collection and not a.search:
        for cid, name, parent in con.execute(
                "select collectionID, collectionName, parentCollectionID from collections order by parentCollectionID, collectionName"):
            n = con.execute("select count(*) from collectionItems where collectionID=?", (cid,)).fetchone()[0]
            print(f"{'  ' if parent else ''}{name}  ({n})")
        return

    if a.collection:
        ids = collection_ids(con, a.collection)
        if not ids:
            sys.exit(f"collection not found: {a.collection}")
        q = ",".join("?" * len(ids))
        items = regular_items(con, f"and i.itemID in (select itemID from collectionItems where collectionID in ({q}))", tuple(ids))
    else:
        items = [i for i in regular_items(con)
                 if a.search.lower() in (field(con, i, "title") + " " + field(con, i, "abstractNote")).lower()]

    out = []
    for n, i in enumerate(items, 1):
        out.append({
            "id": n,
            "author": first_author(con, i),
            "year": field(con, i, "date")[:4],
            "title": field(con, i, "title"),
            "venue": field(con, i, "publicationTitle") or field(con, i, "proceedingsTitle") or field(con, i, "conferenceName"),
            "doi": field(con, i, "DOI"),
            "pdf": pdf_path(con, i),
        })

    if a.json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        return
    for r in out:
        print(f"[{r['id']}] {r['author']} {r['year']} · {r['title']}")
        if r["venue"]:
            print(f"    {r['venue']}")
        print(f"    pdf: {r['pdf'] or '(none)'}")


if __name__ == "__main__":
    main()
