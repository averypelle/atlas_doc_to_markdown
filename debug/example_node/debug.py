# -*- coding: utf-8 -*-

import json
from pathlib import Path
from atlas_doc_parser.api import NodeDoc

dir_here = Path(__file__).absolute().parent
path_source = dir_here.joinpath("source.json")
data = json.loads(path_source.read_text())
node_data = json.loads(list(data.items())[0][1]["body"]["atlas_doc_format"]["value"])
path_doc = dir_here.joinpath("doc.json")
path_doc.write_text(json.dumps(node_data, ensure_ascii=False, indent=4))

node = NodeDoc.from_dict(
    node_data,
    ignore_error=True,
)
path_md = dir_here.joinpath("page.md")
path_md.write_text(
    node.to_markdown(
        ignore_error=True,
    )
)
