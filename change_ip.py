from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient('192.168.1.10', port=502)
client.connect()

# 第1步：先关闭 CH01（清空手动状态）
client.write_coil(0, False, slave=1)
time.sleep(0.3)

# 第2步：重新设置联动模式，延时为0
client.write_register(0x00, 2, slave=1)  # 模式：联动
time.sleep(0.3)

# 第3步：设置联动模式延时 = 0（用0x63寄存器）
client.write_register(0x63, 2, slave=1)  # 延时 = 0 秒

client.close()
print("现在按 IN1 按钮测试")