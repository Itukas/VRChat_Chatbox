import threading
import time
from pythonosc import udp_client

# === 配置 ===
IP = "127.0.0.1"
PORT = 9000

# === OSC 客户端 ===
class VRCChatboxClient:
    def __init__(self, ip, port):
        self.client = udp_client.SimpleUDPClient(ip, port)
        
    def send_message(self, message, notification=True):
        if message:
            self.client.send_message("/chatbox/input", [message, True, notification])
            print(f" [已发送] {message}")

    def send_typing(self, is_typing):
        self.client.send_message("/chatbox/typing", [is_typing])

def main():
    client = VRCChatboxClient(IP, PORT)
    
    print("-" * 30)
    print(" VRChat Chatbox 启动成功")
    print(" 在下方输入内容并回车发送")
    print(" 输入 'exit' 退出程序")
    print("-" * 30)

    try:
        while True:
            # 获取终端输入
            # 注意：终端模式下很难实时检测"正在打字"，所以这里简化为直接发送
            text = input("> ")
            
            if text.lower() in ["exit", "quit"]:
                print("退出程序...")
                break
            
            if text.strip():
                # 模拟发送前的打字状态（可选，瞬间触发）
                client.send_typing(True)
                time.sleep(0.1) 
                
                # 发送消息
                client.send_message(text)
                
                # 停止打字状态
                client.send_typing(False)
                
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main()
