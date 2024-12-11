# mkdocs-content-tabs
<!--
[![GitHub latest commit](https://img.shields.io/github/last-commit/sondregronas/mkdocs-callouts)](https://github.com/sondregronas/mkdocs-callouts/commit/)
-->

[![PyPi](https://img.shields.io/pypi/v/mkdocs-callouts)](https://pypi.org/project/mkdocs-callouts/)
![MIT license](https://img.shields.io/github/license/sondregronas/mkdocs-callouts)

This repository is modified from [mkdocs-callouts](https://github.com/sondregronas/mkdocs-callouts).


The plugin converts Obsidian tabs([obsidian-tab-panels](https://github.com/GnoxNahte/obsidian-tab-panels) or [obsidian-html-tabs](https://github.com/ptournet/obsidian-html-tabs)) into [content tabs supported by MkDocs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#content-tabs).



## Setup
Install the plugin using pip:

`pip install mkdocs-content-tabs`

Activate the plugin in `mkdocs.yml`, note that some markdown_extensions are required for this plugin to function correctly:

```yaml
markdown_extensions:
  - nl2br
  - admonition
  - pymdownx.details
  - pymdownx.superfences

plugins:
  - search
  - callouts
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.


## Usage
mkdocs-content-tabs converts the following:


````` text
  ~~~ tabs
    === c++
    ``` cpp
    std::cout << "hello, c++!" << std::endl;
    ```

    === python
    ``` python
    print("hello, python!")
    ```

    === text
    this is a test.
  ~~~
`````


and turns it into:
`````
=== "c++"
``` cpp
std::cout << "hello, c++!" << std::endl;
```
=== "python"
``` python
print("hello, python!")
```

=== "text"
this is a test.
`````