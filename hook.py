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
