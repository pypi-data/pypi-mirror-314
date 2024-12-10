#!/usr/bin/env python3

import shutil
import re

from subprocess import PIPE, run

class ToolChecker(object):


    @staticmethod
    def find_tool(tool):

        tool_path = None
        tool_version = None

        if tool == "signalp":
            tool_path = shutil.which(tool)
            if tool_path:
                result = run("{} -V".format(tool_path), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                m = re.search(r"^\s*(\S*)\s*(\S*)$", result.stdout.rstrip())
                if m != None:
                    tool_version = m.group(2)
            return tool_path, tool_version

        if tool == "tmhmm":
            tool_path = shutil.which(tool)
            return tool_path, tool_version

        if tool == "targetp":
            tool_path = shutil.which(tool)
            if tool_path:
                result = run("{} -v".format(tool_path), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                m = re.search(r"^\s*(\S*)\s*v(\S*),.*$", result.stdout.rstrip())
                if m != None:
                    tool_version = m.group(2)
            return tool_path, tool_version

        if tool == "effectorp":
            tool_path = shutil.which(tool)
            if tool_path:
                result = run("{} -v".format(tool_path), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                lines = result.stdout.rstrip().split("\n")
                for line in lines:
                    m = re.search(r"^.*EffectorP\s*(\d+.\d*).*$", line)
                    if m != None:
                        tool_version = m.group(1)
            return tool_path, tool_version

