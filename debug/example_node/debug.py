# -*- coding: utf-8 -*-

import json
from pathlib import Path
from atlas_doc_parser.api import NodeDoc

dir_here = Path(__file__).absolute().parent
path_json = dir_here.joinpath("doc.json")
data = json.loads(path_json.read_text())

node = NodeDoc.from_dict(data, ignore_error=True)
path_md = dir_here.joinpath("page.md")
path_md.write_text(node.to_markdown())
