import subprocess

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator


def initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG

    DEFAULT_CONFIG.setdefault('SHELL_BEGIN',
                              '<!-- SHELL_BEGIN -->')
    DEFAULT_CONFIG.setdefault('SHELL_END',
                              '<!-- SHELL_END -->')

    if pelican:
        pelican.settings.setdefault('SHELL_BEGIN',
                                    '<!-- SHELL_BEGIN -->')
        pelican.settings.setdefault('SHELL_END',
                                    '<!-- SHELL_END -->')


def run_pipes(instance):
    if not instance._content:
        return

    content = instance._update_content(instance._content, instance.settings['SITEURL'])

    shell_begin_index = content.find(instance.settings['SHELL_BEGIN'])
    shell_end_index = content.find(instance.settings['SHELL_END'])

    code_start = shell_begin_index + len(instance.settings['SHELL_BEGIN'])
    code_end = shell_end_index

    if code_start < 0 or code_end < 0:
        return

    code_str = content[code_start: code_end].strip()

    if not len(code_str):
        return

    output = subprocess.check_output(code_str, shell=True).decode('utf-8')

    instance._content = content.replace(
        content[
        shell_begin_index:
        shell_end_index + len(instance.settings['SHELL_END'])
        ],
        "<div class=\"shell-pipe\"><p class=\"code\">%s</p><p        class=\"output\">%s</p>"% (code_str, output)
    )


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                run_pipes(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                run_pipes(page)


def register():
    signals.initialized.connect(initialized)
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        signals.content_object_init.connect(run_pipes)
