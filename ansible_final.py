# เราจะเปลี่ยนไฟล์นี้ให้ทำงานด้วย Netmiko แทน Ansible
from netmiko import ConnectHandler
from pprint import pprint

# นำการตั้งค่าการเชื่อมต่อมาจาก netmiko_final.py
# อย่าลืมเปลี่ยน IP ให้ถูกต้อง
device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
    "conn_timeout": 20, # เพิ่ม timeout เพื่อความเสถียร
}


# นี่คือฟังก์ชัน showrun เวอร์ชันใหม่ของเรา
def showrun(student_id, router_name):
    
    # สร้างชื่อไฟล์เหมือนเดิม
    filename = f"show_run_{student_id}_{router_name}.txt"
    
    try:
        print("Attempting to connect to device for showrun...")
        with ConnectHandler(**device_params) as ssh:
            # 1. รันคำสั่ง show running-config
            print("Connection successful. Getting running-config...")
            running_config = ssh.send_command("show running-config")
            
            # 2. บันทึกผลลัพธ์ลงไฟล์
            print(f"Saving config to {filename}...")
            with open(filename, 'w') as f:
                f.write(running_config)
            
            print("File saved successfully.")
            # 3. ถ้าทุกอย่างสำเร็จ ให้คืนค่า 'ok' และชื่อไฟล์
            return "ok", filename

    except Exception as e:
        print(f"!!! AN ERROR OCCURRED in ansible_final.py (Netmiko version) !!!")
        print(e)
        # 4. ถ้ามีปัญหา ให้คืนค่า Error
        return "Error: Could not get running-config via Netmiko", None