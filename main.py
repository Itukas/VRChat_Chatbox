import time
from datetime import datetime
from pythonosc import udp_client

# === 配置 ===
IP = "127.0.0.1"
PORT = 9000


# === 终端颜色代码 (让界面更好看) ===
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# === OSC 客户端 ===
class VRCChatboxClient:
    def __init__(self, ip, port):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def send_message(self, message, notification=True):
        if message:
            # 发送给 VRChat
            self.client.send_message("/chatbox/input", [message, True, notification])

            # 获取当前时间
            current_time = datetime.now().strftime("%H:%M:%S")

            # 打印带时间戳和颜色的日志
            print(f"{Color.GREEN}[{current_time}] 已发送: {Color.END}{message}")

    def send_typing(self, is_typing):
        self.client.send_message("/chatbox/typing", [is_typing])


def main():
    client = VRCChatboxClient(IP, PORT)

    print(f"{Color.CYAN}{'-' * 40}{Color.END}")
    print(f"{Color.BOLD} VRChat Chatbox{Color.END}")
    print(f" {Color.YELLOW}•{Color.END} 输入内容并回车发送")
    print(f" {Color.YELLOW}•{Color.END} 输入 'exit' 或 'quit' 或直接关闭退出")
    print(f"{Color.CYAN}{'-' * 40}{Color.END}")

    try:
        while True:
            # 获取输入，使用稍微醒目一点的箭头
            try:
                text = input(f"{Color.BLUE}>{Color.END} ")
            except EOFError:
                break

            # 退出命令
            if text.strip().lower() in ["exit", "quit"]:
                print(f"{Color.RED}退出程序...{Color.END}")
                break

            # 只要不是空消息就处理
            if text.strip():
                # 1. 瞬间触发打字状态
                client.send_typing(True)
                time.sleep(0.05)

                # 2. 发送消息
                client.send_message(text)

                # 3. 停止打字状态
                client.send_typing(False)

    except KeyboardInterrupt:
        print(f"\n{Color.RED}程序已停止 (KeyboardInterrupt){Color.END}")


if __name__ == "__main__":
    main()
