# ctags.py
#
# Copyright (c) 2011, Micah Carrick All rights reserved.
# Copyright (C) 2020-2021 MATE Developers
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import subprocess
import shlex

def get_ctags_version(executable=None):
    """
    Return the text output from the --version option to ctags or None if ctags
    executable cannot be found. Use executable for custom ctags builds and/or
    path.
    """
    args = shlex.split("ctags --version")
    try:
        p = subprocess.Popen(args, 0, shell=False, stdout=subprocess.PIPE, executable=executable)
        version = p.communicate()[0]
    except:
        version = None
    return version

class Tag(object):
    """
    Represents a ctags "tag" found in some source code.
    """
    def __init__(self, name):
        self.name = name
        self.file = None
        self.ex_command = None
        self.kind = None
        self.fields = {}

class Kind(object):
    """
    Represents a ctags "kind" found in some source code such as "member" or
    "class".
    """
    def __init__(self, name):
        self.name = name
        self.language = None

    def group_name(self):
        """
        Return the kind name as a group name. For example, 'variable' would
        be 'Variables'. Pluralization is complex but this method is not. It
        works more often than not.
        """
        group = self.name

        if self.name[-1] == 's':
            group += 'es'
        elif self.name[-1] == 'y':
            group = self.name[0:-1] + 'ies'
        else:
            group += 's'

        return group.capitalize()

    def icon_name(self):
        """
        Return the icon name in the form of 'source-<kind>'.
        """
        return 'source-' + self.name

class Parser(object):
    """
    Ctags Parser

    Parses the output of a ctags command into a list of tags and a dictionary
    of kinds.
    """
    def has_kind(self, kind_name):
        """
        Return true if kind_name is found in the list of kinds.
        """
        if kind_name in self.kinds:
            return True
        else:
            return False

    def __init__(self):
        self.tags = []
        self.kinds = {}
        self.tree = {}

    def parse(self, command, executable=None):
        """
        Parse ctags tags from the output of a ctags command. For example:
        ctags -n --fields=fiKmnsSzt -f - some_file.php
        """
        #args = [arg.replace('%20', ' ') for arg in shlex.split(command)]
        args = shlex.split(command)
        p = subprocess.Popen(args, 0, shell=False, stdout=subprocess.PIPE, executable=executable)
        symbols = self._parse_text(p.communicate()[0].decode('utf8'))

    def _parse_text(self, text):
        """
        Parses ctags text which may have come from a TAG file or from raw output
        from a ctags command.
        """
        for line in text.splitlines():
            name = None
            file = None
            ex_command = None
            kind = None
            for i, field in enumerate(line.split("\t")):
                if i == 0: tag = Tag(field)
                elif i == 1: tag.file = field
                elif i == 2: tag.ex_command = field
                elif i > 2:
                    if ":" in field:
                        key, value = field.split(":")[0:2]
                        tag.fields[key] = value
                        if key == 'kind':
                            kind = Kind(value)
                            if not kind in self.kinds:
                                self.kinds[value] = kind

            if kind is not None:
                if 'language' in tag.fields:
                    kind.language = tag.fields['language']
                tag.kind = kind

            self.tags.append(tag)

