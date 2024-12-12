import sys
sys.path.append("./src/")

from mkdocs_content_tabs.plugin import ContentTabsPlugin


def convert(input: str) -> str:
    """For readability: Parse the input string using the plugin"""
    return ContentTabsPlugin().on_page_markdown(input, None, None, None)


def test():
    mkdown = """ \
# hi

Publish your public notes with MkDocs

> [!INFO]\n> Unitled block

## test

~~~ tabs

=== cpp
``` cpp
std::cout << "hello c++!" << std::endl;
```

=== python
``` python
print("hello python!")
```

=== c
``` c
printf("hello, c!");
```

=== latex

$$ \alpha \to \beta $$

=== text
this is a test!

~~~



``` cpp
std::cout << "hello c++!" << std::endl;
```


``` c
printf("hello, c!");
```


    """

    rslt = convert(mkdown)
    with open("rslt.md", 'w') as fw:
        fw.write(rslt)

    pass


if __name__ == "__main__":
    test()
    pass
