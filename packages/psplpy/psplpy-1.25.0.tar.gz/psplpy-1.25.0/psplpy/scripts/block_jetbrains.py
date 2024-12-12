import argparse
import os
import re
from pathlib import Path
import pyshark
from psplpy.serialization_utils import Serializer


class BlockJetBrains:
    def __init__(self, interface: str = 'WLAN'):
        self.interface = interface

    @staticmethod
    def _extract_substring(string: str, search_string: str):
        result = []
        start = 0
        while True:
            index = string.find(search_string, start)
            if index == -1:
                break
            # extract the search string until to the \n
            end_index = string.find('\n', index)
            if end_index == -1:
                end_index = len(string)
            substring = string[index + len(search_string):end_index].strip()
            result.append(substring)
            start = end_index + 1
        return result

    @staticmethod
    def _p_os_system(command: str) -> None:
        print(command)
        os.system(command)

    def _flush_dns(self):
        self._p_os_system('ipconfig /flushdns')

    @staticmethod
    def _remove_ansi_escapes(text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def append_dns_ip(self):
        self._flush_dns()
        s = Serializer(Path(__file__).parent / 'ip.json', data_type=dict)
        current_ip_dict = s.load_json()
        print(f'Current IP: {current_ip_dict}')
        capture_filter = 'dns'
        capture = pyshark.LiveCapture(interface=self.interface, display_filter=capture_filter)
        capture.sniff(timeout=1)

        print('Start capture')
        for packet in capture.sniff_continuously():
            has_added = False
            content = self._remove_ansi_escapes(str(packet))
            if 'Standard query response' in content:
                name_list = self._extract_substring(content, 'Name: ')
                name = None
                if name_list:
                    name = name_list[0]
                ip_result = self._extract_substring(content, ' addr ')
                print(f'{name}: {ip_result}')
                if name in ['www.jetbrains.com', 'account.jetbrains.com']:
                    for ip in ip_result:
                        if not current_ip_dict.get(name):
                            current_ip_dict[name] = []
                        current_ip_list = current_ip_dict[name]
                        if ip not in current_ip_list:
                            current_ip_list.append(ip)
                            print(f'Appended: {ip}')
                            has_added = True
                    if has_added:
                        s.dump_json(current_ip_dict, minimum=False)

                        rule_name = 'jetbrains'
                        total_ip_list = []
                        for ip_list in current_ip_dict.values():
                            total_ip_list.extend(ip_list)
                        self._p_os_system(f'netsh advfirewall firewall delete rule name="{rule_name}"')
                        self._p_os_system(f'netsh advfirewall firewall add rule name="{rule_name}" '
                                          f'dir=out action=block remoteip={",".join(total_ip_list)}')
                        self._p_os_system(f'netsh advfirewall firewall add rule name="{rule_name}" '
                                          f'dir=in action=block remoteip={",".join(total_ip_list)}')
                        self._flush_dns()
        capture.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Block JetBrains IP.')
    parser.add_argument('interface', type=str, help="Current Internet connection's name")
    args = parser.parse_args()

    BlockJetBrains(args.interface).append_dns_ip()
