# -*- encoding=utf8 -*-
__author__ = "UWA"
__title__ = "UWA"
__desc__ = """
该脚本是UWA提供的用于自动化测试的工具包。
提供了较稳定的 apk 安装方法，与 UWA SDK 中的 GOT 模式进行交互的接口，与PocoSDK优化版的交互接口等。
"""

import json
from airtestProject.airtest.core.api import *
from airtestProject.poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtestProject.poco.utils.simplerpc.utils import sync_wrapper

try:
    import run_airtest_config
    import run_got_util

    UWAPPLTest = True
    log("--当前为UWAPPL调试--")
except:
    # log("--当前为本地调试--")
    UWAPPLTest = False

import time
import logging

# log 对象
_logger = logging.getLogger("airtest")
_logger.debug("[UWA] import UWA")


@sync_wrapper
def SetPruningEnabled(pocoHdl, enabled):
    """
    开启或关闭UWA优化后的PocoSDK提供的剪枝优化功能。
    """
    return pocoHdl.agent.c.call("SetPruningEnabled", enabled)


@sync_wrapper
def CollectWeakWhitelist(pocoHdl):
    """
    自动扫描场景物体，检测哪些节点需要保留。在开启剪枝优化功能的情况下，每次切换场景或场景的UI变化比较大时，需要调用一次。
    """
    return pocoHdl.agent.c.call("CollectWeakWhitelist")


@sync_wrapper
def SetBlackList(pocoHdl, *args):
    """
    设置Hierarchy信息节点的黑名单。默认被保留的节点，如果在黑名单里，则会被剔除掉。
    """
    return pocoHdl.agent.c.call("SetBlackList", *args)


@sync_wrapper
def SetWhiteList(pocoHdl, *args):
    """
    设置Hierarchy信息节点的白名单。默认被剔除掉的节点，如果在白名单里，则会被保留。白名单优先于黑名单。
    """
    return pocoHdl.agent.c.call("SetWhiteList", *args)


@sync_wrapper
def SetBlockedAttributes(pocoHdl, *args):
    """
    设置被屏蔽的属性。
    PocoSDK获取到的Hierarchy属性有：
    "name","type","visible","pos","size","scale", "anchorPoint", "zOrders",
    "clickable","text","components",  "texture","tag","_ilayer","layer", "_instanceId"

    推荐屏蔽掉的信息有："Tag","texture", "scale", "clickable", "components", "_ilayer", "layer", "zOrders"

	如果某个属性被屏蔽掉导致脚本运行异常，重新调用该函数设置屏蔽列表即可。
    """

    if UWAPPLTest == True:
        from poco.drivers.std.HierarchyTranslator import translator_agent
        translator_agent.SetBlockAttrs(*args)
    return pocoHdl.agent.c.call("SetBlockedAttributes", *args)


class GOT_Test():
    """
    GOT Online & GPM 自动化工具类
    """

    ENABLED = True

    @classmethod
    def Connect(cls, poco):
        """
        连接 GOT 进行自动化测试，使 GOT GUI 不可交互，只能通过脚本控制
        :param poco: Unity Poco 实例
        :Example:
            >>> GOT_Test.Connect(poco)
        """
        _logger.debug("[UWA] connect")
        if cls.ENABLED and not poco is None:
            return poco.agent.c.call("UWA.Connect")

    @classmethod
    def Start(cls, poco, mode="default", config=None, platform=True):
        """
        开启 GOT 的某个模式 或者 GPM，支持：overview/mono/resources/lua/gpu/gpm
        :param poco: Unity Poco 实例
        :param mode: 模式分为 overview/mono/resources/lua/gpu/gpm
        :param config: Dict 类型，包含各个模块的配置。如果为 None，则使用默认配置
            config = {
                "overview.mode": 0,                  Overview 模式具体测试模式，0 表示自定义模式，1 表示极简模式，2 表示CPU模式，3 表示内存模式
                "overview.engine_cpu_stack": True,   Overview 模式下，是否开启引擎、C#逻辑代码 CPU 调用堆栈统计
                "overview.lua_cpu_stack": True,      Overview 模式下，是否开启 Lua 逻辑代码 CPU 调用耗时堆栈统计。前置条件：engine_cpu_stack 为 True
                "overview.lua_mem_stack": True,      Overview 模式下，是否开启 Lua 逻辑代码内存占用堆栈统计。前置条件：lua 为 True
                "overview.time_line": True,          Overview 模式下，是否开启 Timeline 统计。前置条件：engine_cpu_stack 为 True
                "overview.stack_detail": 1,          Overview 模式下，堆栈统计的细节控制，0 表示默认细节，1 表示详细细节，2 表示全堆栈（不开放）。前置条件：engine_cpu_stack 为 True
                "overview.unity_api": True,          Overview 模式下，是否开启 Unity API 调用统计。前置条件：engine_cpu_stack 为 True
                "overview.lua": True,                Overview 模式下，是否开启 Lua 测试
                "overview.lua_dump_step": 0,         Overview 模式下，Lua 测试采样间隔，-1 表示不支持Dump，0 表示手动Dump，N自动以N为周期进行Lua Dump。前置条件：lua 为 True
                "overview.resources": True,          Overview 模式下，是否开启资源统计，0 表示完全关闭Resources获取（不可Dump），1 表示只获取资源总数、总内存（可Dump），2 表示获取资源详细信息（可Dump）
                "overview.unity_loading": True,      Overview 模式下，是否开启资源管理功能
                "mono.mono_dump_step": 0,            Mono 模式下，Mono 测试采样间隔，0 表示手动Dump，N自动以N为周期进行Mono Dump
                "resources.unity_loading": True,     Resources 模式下，是否开启资源管理功能
                "lua.lua_dump_step": 0,              Lua 模式下，Lua 测试采样间隔，0 表示手动Dump，N自动以N为周期进行Lua Dump
                "lua.lua_cpu_stack": True,           Lua 模式下，是否开启 Lua 逻辑代码 CPU 调用耗时堆栈统计，固定为 True
                "lua.lua_mem_stack": True,           Lua 模式下，是否开启 Lua 逻辑代码内存占用堆栈统计，固定为 True
                "gpu.texture_analysis": True,        GPU 模式下，是否开启纹理分析
                "gpu.mesh_analysis": True            GPU 模式下，是否开启网格分析
            }
        :param platform: 是否是Android平台
        :Example:
            >>> config={"resources.unity_loading":True}
            >>> GOT_Test.Start(poco, mode="resources", config=config)
            >>> GOT_Test.Start(poco, mode="gpm")
        """

        if UWAPPLTest:
            if run_airtest_config.got_type is not None:
                mode = run_airtest_config.got_type

        if mode == "assets":
            mode = "resources"

        _logger.debug("[UWA] Start " + mode)
        _logger.debug("[UWA] Start Config " + str(config))

        if cls.ENABLED and not poco is None:
            if config is None:
                log("UWA GOT Start")
                res = poco.agent.c.call("UWA.Start", mode)
            else:
                log("UWA GOT Start With Config")
                res = poco.agent.c.call("UWA.Start", mode, json.dumps(config))

            time.sleep(3)
            if platform:
                a_poco = AndroidUiautomationPoco()
                if a_poco("android:id/button1").exists():
                    a_poco("android:id/button1").click()
            return res
        return True

    @classmethod
    def Stop(cls, poco):
        """
        停止 GOT 模式
        :param poco: Unity Poco 实例
        :Example:
            >>> GOT_Test.Stop(poco)
        """
        _logger.debug("[UWA] Stop")
        log("UWA GOT Stop")  # show in the reports

        if cls.ENABLED and not poco is None:
            return poco.agent.c.call("UWA.Stop")
        return True

    @classmethod
    def StatPoco(cls, poco, stat):
        """
        是否在报告中保留 Poco 的额外耗时
        :param poco: Unity Poco 实例
        :param stat: True/False
        :Example:
            >>> GOT_Test.StatPoco(poco, True)
        """
        _logger.debug("[UWA] StatPoco : " + str(stat))
        log("UWA GOT StatPoco")
        if cls.ENABLED and not poco is None:
            return poco.agent.c.call("UWA.StatPoco", stat)

    @classmethod
    def Dump(cls, poco, dump):
        """
        手动 dump，采集更多信息
        :param poco: Unity Poco 实例
        :param dump: 可用dump类型：mono/lua/resources/overdraw，类型为String
        :Example:
            >>> GOT_Test.Dump(poco, "mono")
        """
        _logger.debug("[UWA] Dump : " + dump)
        log("UWA GOT Dump")
        if cls.ENABLED and not poco is None:
            return poco.agent.c.call("UWA.Dump", dump)

    @classmethod
    def Note(cls, poco, note):
        """
        添加备注信息，显示在 UWA官网 对应报告的备注栏。
        :param poco: Unity Poco 实例
        :param note: 备注信息
        :Example:
            >>> GOT_Test.Note(poco, "test")
        """
        _logger.debug("[UWA] Note : " + note)
        log("UWA GOT Note")
        if cls.ENABLED and not poco is None:
            return poco.agent.c.call("UWA.Note", note)

    @classmethod
    def Tag(cls, poco, tag):
        """
        标记测试区间
        :param poco: Unity Poco 实例
        :param tag: 区间标记
        :Example:
            >>> GOT_Test.Tag(poco, "test")
        """
        _logger.debug("[UWA] Tag " + tag)
        log("UWA GOT Tag")
        if cls.ENABLED and not poco is None:
            res = poco.agent.c.call("UWA.Tag", tag)
            return res

    @classmethod
    def Upload(cls, poco, timeLimitS=3600, uploadTimeLimitS=600):
        """
        上传测试数据到 UWA 官网，仅可在UWA Pipeline中使用。
        :param poco: Unity Poco 实例
        :param timeLimitS: 测试时长限制
        :param uploadTimeLimitS: 上传时长限制
        :Example:
            >>> GOT_Test.Upload(poco, 7200, 3000)
        """
        _logger.debug("[UWA] Upload " + str(timeLimitS) + " " + str(uploadTimeLimitS))
        log("UWA GOT Upload With UWA Pipeline")
        if UWAPPLTest:
            run_got_util.UploadWithRecordId(poco, timeLimitS, uploadTimeLimitS)

    @classmethod
    def LocalUpload(cls, poco, account, password, projectID, timeLimitS=3600, uploadTimeLimitS=600):
        """
        本地上传，需要配置好UWA的账号、密码、项目ID等信息。
        :param poco: Unity Poco 实例
        :param account: UWA 账号
        :param password: UWA 账号 密码
        :param projectID: 项目ID
        :param timeLimitS: 测试时长限制,默认3600秒
        :param uploadTimeLimitS: 上传时长限制,默认600秒
        :Example:
            >>> GOT_Test.LocalUpload(poco, "uwa", "111111", 111, 3000)
        """
        log("UWA GOT Upload With Local Test")
        if cls.ENABLED and not poco is None:
            poco.agent.c.call("UWA.StartUploadUserpwd", account, password, projectID, timeLimitS)

            upload_time = 0
            while upload_time < uploadTimeLimitS:
                upload_time += 5
                time.sleep(5)
                res, n = poco.agent.c.call("UWA.CheckUploadResult").wait()
                _logger.debug("[UWA] CheckUploadResult " + str(res))
                if len(res) == 3 and res[0]:
                    return res[1], res[2]

            raise Exception("UWA Upload Timeout")
