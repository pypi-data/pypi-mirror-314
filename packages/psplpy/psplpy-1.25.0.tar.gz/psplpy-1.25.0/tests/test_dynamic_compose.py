from tests.__init__ import *
from psplpy.dynamic_compose import DynamicCompose

dc_rc_dir = rc_dir / 'dynamic_compose'
dc_compose_dir = dc_rc_dir / '.compose'
compose_dumped_file = dc_compose_dir / 'compose-dumped.yml'
dockerfile_dumped_file = dc_compose_dir / 'dumped-Dockerfile'
dockerfile_dumped_file2 = dc_compose_dir / 'dumped-Dockerfile2'


def lines_rstrip(text: str) -> str:
    lines = text.splitlines()
    stripped_lines = [line.rstrip() for line in lines]
    result = '\n'.join(stripped_lines)
    return result


def tests():
    dc = DynamicCompose(cwd=dc_rc_dir)
    dc.env['GPU'] = '''    
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]'''
    dc.env['IMAGE'] = 'python:3.10'
    dc.env['software'] = 'git'
    print(dc.env)

    dc.fd_all().up()

    assert compose_dumped_file.read_text().strip() == lines_rstrip((dc.cwd / 'compose.yml').read_text().strip())
    assert dockerfile_dumped_file.read_text().strip() == lines_rstrip((dc.cwd / 'Dockerfile').read_text().strip())
    assert dockerfile_dumped_file2.read_text().strip() == lines_rstrip((dc.cwd / 'Dockerfile2').read_text().strip())


if __name__ == '__main__':
    tests()
