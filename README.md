# jupyter-README.md-auto-create
Automatically create a README.md when you save your jupyter notebook.
Note: pictures will not be created for this version

Jupyter canbe [set up](https://jupyter-notebook.readthedocs.io/en/stable/config.html) for jupyter) to run many funcitons automatically, and it has a lot of hooks can be user. For example, `FileContentsManager.post_save_hook`  is called after your file is saved. We gonna use this hook to create a markdown file README.md every time you save your jupyter notebook.

> create a configure file if you have not
```
jupyter notebook --generate-config
```
the above command will create a `jupyter_notebook_config.py` file at `~/.jupyter/jupyter_notebook_config.py`


> add the following code into the created file, or if you already have set up this hook, just call this function inside your implementation

```python
import io
import os
from notebook.utils import to_api_path

_md_exporter = None

def script_post_save(model, os_path, contents_manager, **kwargs):
    """convert notebooks to Python script after save with nbconvert
    replaces `ipython notebook --script`
    """
    # from nbconvert.exporters.script import ScriptExporter
    from nbconvert.exporters.markdown import MarkdownExporter

    if model['type'] != 'notebook':
        return

    global _md_exporter

    if _md_exporter is None:
        _md_exporter = MarkdownExporter(parent=contents_manager)

    log = contents_manager.log

    script, resources = _md_exporter.from_filename(os_path)
    md_fname = os.path.dirname(os_path) + '/README' + resources.get('output_extension', '.md')
    log.info("Saving README.md /%s", to_api_path(md_fname, contents_manager.root_dir))

    with io.open(md_fname, 'w', encoding='utf-8') as f:
        f.write(script)

c.FileContentsManager.post_save_hook = script_post_save
```

Try restart your jupyter server, and save your jupyter file, you will see a README.md is created with the same content. 
