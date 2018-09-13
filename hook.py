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
