import os, sys
import subprocess, threading, time

from airtestProject.manager.LogManager import LogManager, catch_error

LIBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(LIBASE_DIR)

log_manager = LogManager(logfile=None)


# 指定目录执行cmd指令，阻塞进程
@catch_error
def run_command(command, cwd="."):
    data = ({})
    try:
        p = subprocess.Popen(command, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out, std_err = p.communicate()
        ret_code = p.returncode

        data.update({"dir": cwd,
                     "cmd": command,
                     "code": ret_code,
                     "std_out": std_out,
                     "std_err": std_err,
                     })
        return data
    except Exception as e:
        import traceback
        log_manager.log_error(traceback.format_exc())
        return data


def _thread_run_command(command, log_file, cwd=".", ):
    try:
        p = subprocess.Popen(command, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            std_out = p.stdout.readline()
            if std_out is not None and len(std_out) > 0:
                with open(log_file, "ab") as file_obj:
                    file_obj.write(std_out)
    except Exception as e:
        import traceback
        log_manager.log_error(traceback.format_exc())


def random_string(length):
    import random, string
    if length > 0:
        max_once = 62
        if length > max_once:
            ret = "".join(random.sample(string.ascii_letters + string.digits, max_once)) \
                  + random_string(length - max_once)
        else:
            ret = "".join(random.sample(string.ascii_letters + string.digits, length))
        return ret
    else:
        return ""


# 指定目录执行cmd指令，异步执行不阻塞进程
# 执行结果输出到指定日志，返回值为日志路径
def run_command_async(command, cwd=".", log_name=None):
    crd = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                       "log",
                       "tmp")

    if not os.path.isdir(crd):
        os.makedirs(crd)

    if log_name is None:
        log_name = "run_%s_%s.log" % (time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time() + 60 * 60 * 8)),
                                      random_string(10).lower())

    log_file = os.path.join(crd, log_name)

    t = threading.Thread(target=_thread_run_command, args=(command, log_file, cwd))
    t.setDaemon(False)  # 设置为守护线程,主线程结束,同时全部子线程被终止

    t.start()

    return log_file



def adb_shell(cmd, device_id=None):
    if not device_id:
        run_cmd = f'adb shell {cmd}'
        result = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[
            0].decode("utf-8").strip()
        return result

    if type(device_id) != list:
        device_id = [device_id]
    for id in device_id:
        run_cmd = f'adb -s {id} shell {cmd}'
        result = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[
            0].decode("utf-8").strip()

    return True


if __name__ == "__main__":
    s = adb_shell("ps | filter findstr com.global.bcslg", "d1236ad8")
    print(111, s)
