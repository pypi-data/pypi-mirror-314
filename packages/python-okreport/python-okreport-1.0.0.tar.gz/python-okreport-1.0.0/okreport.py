# -*- coding: utf-8 -*-
import os
import sys
import base64

from jinja2 import Template


class Var:
    """
    Var, where each Var object represents a piece of variable data within a report, have three sources:
    (1) Results, which are the outcomes of the pipeline being run, corresponding to the parameter "result";
    (2) Configuration, which refers to the parameters when running the process, corresponding to the parameter "conf";
    (3) Environment variables, corresponding to the parameter "env".
    """
    def parse(self, result, conf, env):
        raise NotImplementedError


class Image(Var):
    def get_file(self, result, conf, env):
        raise NotImplementedError

    def parse(self, result, conf, env):
        file = self.get_file(result, conf, env)
        if file is None:
            return None
        data = open(file, 'rb').read()
        encoding = sys.getdefaultencoding()
        b64text = base64.b64encode(data).decode(encoding)
        ext = os.path.splitext(file)[1][1:]
        return f'data:image/{ext};base64,{b64text}'


class Paragraph:
    """Paragraph，consists of multiple Vars."""
    def get_template_text(self, result, conf, env):
        return self.__doc__

    def parse(self, result, conf, env):
        data = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            var = getattr(self, name)
            if not isinstance(var, Var):
                continue
            data[name] = var.parse(result, conf, env)
        return data

    def render(self, result, conf, env):
        data = self.parse(result, conf, env)
        template_text = self.get_template_text(result, conf, env)
        template = Template(template_text)
        return template.render(env=env, conf=conf, **data)


class Report:
    """Report，consists of Paragraphs. """
    def get_template_text(self, result, conf, env):
        return self.__doc__

    def render(self, result, conf, env):
        paragraph_texts = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            paragraph = getattr(self, name)
            if not isinstance(paragraph, Paragraph):
                continue
            paragraph_texts[name] = paragraph.render(result, conf, env)
        template_text = self.get_template_text(result, conf, env)
        template = Template(template_text)
        return template.render(env=env, conf=conf, **paragraph_texts)

    def save(self, result, conf, env, file):
        report_text = self.render(result, conf, env)
        with open(file, 'w') as fp:
            fp.write(report_text)
