# jupyter-README.md-auto-create
Automatically create a README.md when you save your jupyter notebook. (Will also create images if your jupyter notebook have images in there, for example matplotlib plots)

Jupyter can be [set up](https://jupyter-notebook.readthedocs.io/en/stable/config.html) to run many funcitons automatically, and it has a lot of hooks can be used. For example, `FileContentsManager.post_save_hook`  is called after your file is saved. We gonna use this hook to create a markdown file README.md every time you save your jupyter notebook.

> create a configure file if you have not
```
jupyter notebook --generate-config
```
the above command will create a `jupyter_notebook_config.py` file at `~/.jupyter/jupyter_notebook_config.py`


> add the following code into the created file, or if you already have set up this hook, just call this function inside your implementation

```python
import os
import nbformat
from nbconvert.writers import FilesWriter

_md_exporter = None

def script_post_save(model, os_path, contents_manager, **kwargs):
    """convert notebooks to Python script after save with nbconvert
    replaces `ipython notebook --script`
    """
    from nbconvert.exporters.markdown import MarkdownExporter
    log = contents_manager.log

    if model['type'] != 'notebook':
        return

    global _md_exporter

    if _md_exporter is None:
        _md_exporter = MarkdownExporter(parent=contents_manager)

    nb_node = nbformat.read(model['path'], nbformat.NO_CONVERT)
    (output, resources) = _md_exporter.from_notebook_node(nb_node)

    c.FilesWriter.build_directory = os.path.dirname(os_path)
    fw = FilesWriter(config=c)
    fw.write(output, resources, notebook_name="README")

    log.info("Saving README.md & dependencies files%s", os.path.dirname(os_path))

c.FileContentsManager.post_save_hook = script_post_save
```

Try restart your jupyter server, and save your jupyter file, you will see a README.md is created with the same content. 
