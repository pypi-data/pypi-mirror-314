# -*- coding: utf-8 -*-
import re
import sys
import logging
import subprocess


class Module:

    def name(self):
        return self.__class__.__name__

    def logger(self):
        return logging.getLogger(f'okmodule.{self.name()}')

    def log(self, message, level=logging.INFO, **kwargs):
        self.logger().log(level, message, **kwargs)

    def main(self):
        raise NotImplementedError

    def __call__(self):
        return self.main()

    def __repr__(self):
        return f'<{self.name()} at 0x{id(self):0x}>'


class Command(Module):

    def path(self):
        return re.sub(r'(?!^)([A-Z]+)', r'-\1', self.name()).lower()  # MyCommand -> my-command

    def args(self):
        raise NotImplementedError

    def env(self):  # noqa
        return None

    def result(self, proc):  # noqa
        return None

    def main(self):
        args = [self.path()]
        args.extend(self.args())
        self.log(f'Running command {" ".join(args)}')
        proc = subprocess.Popen(
            args,
            env=self.env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        enc = sys.getdefaultencoding()
        for raw_line in iter(proc.stdout.readline, b''):
            self.log(raw_line.decode(enc).rstrip())
        returncode = proc.wait()
        if returncode:
            raise subprocess.CalledProcessError(returncode, args)
        return self.result(proc)
