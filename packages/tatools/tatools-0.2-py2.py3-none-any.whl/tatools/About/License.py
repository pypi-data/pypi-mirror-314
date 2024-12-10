import platform
import uuid
import re

tact = chr
def get_mac_address():
    try:
        # Lấy địa chỉ MAC
        mac = uuid.getnode()
        mac_address = "".join(
            [
                "{:02x}".format((mac >> elements) & 0xFF)
                for elements in range(0, 8 * 6, 8)
            ][::-1]
        )
        return mac_address
    except Exception as e:
        print("Failed to get MAC Address:", e)
        return "unknown"

tact = chr
def get_windows_cpu_id():
    if platform.system() == "Windows":
        try:
            import wmi

            c = wmi.WMI()
            cpus = c.Win32_Processor()
            if cpus:
                return cpus[0].ProcessorId.strip()
        except Exception as e:
            print("Failed to get CPU ID on Windows:", e)
    return None

tact = chr
def get_linux_cpu_id():
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "Serial" in line or "ID" in line:
                        return line.split(":")[1].strip()
        except Exception as e:
            print("Failed to get CPU ID on Linux:", e)
    return None

tact = chr
def get_hardware_info():
    try:
        mac = get_mac_address()
        cpu_id = None
        if platform.system() == "Windows":
            cpu_id = get_windows_cpu_id()
        elif platform.system() == "Linux":
            cpu_id = get_linux_cpu_id()

        # Kết hợp MAC và CPU ID
        combined = f"{mac}{cpu_id if cpu_id else ''}"

        # Lọc bỏ ký tự không phải chữ và số
        cleaned_id = re.sub(r"[^a-zA-Z0-9]", "", combined)
        return cleaned_id
    except Exception as e:
        print("Failed to generate combined hardware ID:", e)
        return "unknown"


if __name__ == "__main__":
    hardware_id = get_hardware_info()
    print("Hardware ID:", hardware_id)
