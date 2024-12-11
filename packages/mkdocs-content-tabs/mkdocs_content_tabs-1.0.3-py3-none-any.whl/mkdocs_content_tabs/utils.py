import re


class ContentTabsParser(object):
    """Class to parse content tabs from markdown and convert them to mkdocs supported admonitions."""

    def _split_blocks(self, markdown):
        """
        Split Markdown text into blocks containing `~~~ tabs` and other blocks.
        """

        # Define a regex pattern to match blocks starting with `~~~ tabs` and ending with `~~~`
        pattern = re.compile(r"(~~~\s*tabs\s*.*?\s*~~~)", re.DOTALL)
        parts = pattern.split(markdown)

        blocks = []
        for part in parts:
            if pattern.match(part):
                blocks.append({"type": "tabs", "content": part})
            else:
                blocks.append({"type": "other", "content": part})

        return blocks

    def _convert_content(self, block):
        rslt = ""
        for line in block.split("\n")[1:-1]:
            if line.strip().startswith("==="):
                label = line.rstrip().split("===")
                if len(label) != 2:
                    rslt += line + "\n"
                    continue

                tab_name = label[1].strip().strip('"')
                label[1] = f' "{tab_name}"'
                rslt += "===".join(label) + "\n"
            else:
                rslt += line + "\n"
            pass
        return rslt
        pass

    def parse(self, markdown: str) -> str:
        rslt = ""
        split_blocks = self._split_blocks(markdown)

        for block in split_blocks:
            type_ = block["type"]
            content_ = block['content']

            if type_ == "tabs":
                rslt += self._convert_content(content_)
            else:
                rslt += content_

        return rslt
