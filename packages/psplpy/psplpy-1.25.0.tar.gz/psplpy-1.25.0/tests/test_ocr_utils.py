import threading
import paramiko
from tests.__init__ import *
from psplpy.ocr_utils import *

host = 'paddleocr'


def run_ocr_server():
    def _run():
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加和保存远程主机的 SSH 公钥
        ssh.connect(hostname=host, port=22, username='a', password='1')
        stdin, stdout, stderr = ssh.exec_command('pkill python')
        stdin.close()
        dir_path = '/home/a/src/psplpyProject'
        code = (f"import sys; sys.path.append('{dir_path}'); "
                f"from psplpy.ocr_utils import *; OcrServer(workers=10, use_gpu=False).run_server()")
        stdin, stdout, stderr = ssh.exec_command(f'cd {dir_path}; python -c "{code}"')
        print(stdout.read().decode('utf-8'), stderr.read().decode('utf-8'))
        stdin.close()
        ssh.close()
    thread = threading.Thread(target=_run)
    thread.daemon = True
    thread.start()
    time.sleep(3)


def tests():
    run_ocr_server()
    ocr = Ocr(host=host)
    p = PerfCounter()
    result = ocr.get(rc_dir / 'ocr.png', cls=True)
    p.show('ocr')
    print(result)
    assert result == [[[[4.0, 4.0], [221.0, 4.0], [221.0, 25.0], [4.0, 25.0]], '我是左上角Test文本', 0.9756967425346375], [[[355.0, 4.0], [618.0, 4.0], [618.0, 28.0], [355.0, 28.0]], '我是旋转180度Test文本', 0.9985828995704651], [[[773.0, 6.0], [992.0, 6.0], [992.0, 28.0], [773.0, 28.0]], '我是右上角Test文本', 0.9980501532554626], [[[358.0, 58.0], [604.0, 58.0], [604.0, 83.0], [358.0, 83.0]], '本文129T封直垂是', 0.7891653180122375], [[[716.0, 60.0], [901.0, 240.0], [876.0, 266.0], [692.0, 86.0]], '我是旋转45度Test文本', 0.9995959997177124], [[[7.0, 105.0], [36.0, 105.0], [39.0, 358.0], [9.0, 358.0]], '我是旋转90度Test文本', 0.9987719655036926], [[[361.0, 109.0], [607.0, 109.0], [607.0, 134.0], [361.0, 134.0]], '本文129T幡平水', 0.7843223810195923], [[[964.0, 102.0], [996.0, 102.0], [994.0, 372.0], [961.0, 372.0]], '我是旋转270度Test文本', 0.9994610548019409], [[[136.0, 130.0], [165.0, 130.0], [165.0, 328.0], [136.0, 328.0]], '我是竖直Ts文本', 0.9204778671264648], [[[367.0, 271.0], [596.0, 271.0], [596.0, 326.0], [367.0, 326.0]], '我是双凸型Test文本', 0.9981181621551514], [[[384.0, 367.0], [584.0, 382.0], [582.0, 414.0], [382.0, 399.0]], '我是旗形Test文本', 0.9996482729911804], [[[7.0, 472.0], [227.0, 472.0], [227.0, 493.0], [7.0, 493.0]], '我是左下角Test文本', 0.9985069036483765], [[[772.0, 472.0], [992.0, 471.0], [992.0, 493.0], [772.0, 494.0]], '我是右下角Test文本', 0.9985582828521729]]
    DrawResult(rc_dir / 'ocr.png', result, tmp_dir / 'draw_result_ocr.png')
    p.show('draw_result')
    result = ocr.get(rc_dir / 'ocr2.jpg', cls=True)
    p.show('ocr2')
    print(result)
    DrawResult(rc_dir / 'ocr2.jpg', result, tmp_dir / 'draw_result_ocr2.png')
    p.show('draw_result2')


if __name__ == '__main__':
    tests()
