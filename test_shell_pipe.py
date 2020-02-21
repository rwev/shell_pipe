# -*- coding: utf-8 -*-

import unittest
from jinja2.utils import generate_lorem_ipsum

from pelican.contents import Page
import pelican.settings

import shell_pipe

# generate one paragraph, enclosed with <p>
TEST_CONTENT = str(generate_lorem_ipsum(n=1))
TEST_OUTPUT = '<<< OUTPUT >>>'
TEST_COMMAND = 'echo \"%s\"' % TEST_OUTPUT


class TestPipe(unittest.TestCase):
    def setUp(self):
        super(TestPipe, self).setUp()

        shell_pipe.register()
        shell_pipe.initialized(None)

    def test_execution_and_replace(self):
        page = Page(**{
            'content': TEST_CONTENT + '<!-- SHELL_BEGIN -->' + TEST_COMMAND + '<!-- SHELL_END -->',
            'context': {
                'localsiteurl': '',
            },
        })
        shell_pipe.run_pipes(page)
        # test both the shell_pipe and the marker removal
        print(page.content)
        self.assertEqual(page.content, TEST_CONTENT + '"%s"\r\n' % TEST_OUTPUT)


if __name__ == '__main__':
    unittest.main()
