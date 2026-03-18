from __future__ import annotations

from automation.engine.registry import TaskRegistry

from automation.packs.core_fs.copy import CopyFileTask
from automation.packs.core_process.echo import EchoTask
from automation.packs.data_ops.quality_bridge import DataHealthRunTask
from automation.packs.web_automation.http_check import HttpCheckTask


def default_registry() -> TaskRegistry:
    reg = TaskRegistry(tasks={})
    reg.register(EchoTask())
    reg.register(CopyFileTask())
    reg.register(HttpCheckTask())
    reg.register(DataHealthRunTask())
    return reg
