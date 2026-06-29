import requests

ICS_URL = "https://outlook.live.com/owa/calendar/00000000-0000-0000-0000-000000000000/7b3272d9-59ae-4b21-a6ee-93055d9dabed/cid-7D0F5EF787CF53A7/calendar.ics"

text = requests.get(ICS_URL).text

# 修复微软私有时区
text = text.replace(
    "TZID:Customized Time Zone",
    "TZID:Asia/Shanghai"
)

text = text.replace(
    "TZID=Customized Time Zone",
    "TZID=Asia/Shanghai"
)

# 可选：补一个标准时区声明
text = text.replace(
    "BEGIN:VTIMEZONE\nTZID:Asia/Shanghai",
    """BEGIN:VTIMEZONE
TZID:Asia/Shanghai
X-LIC-LOCATION:Asia/Shanghai"""
)

with open("docs/calendar_1.ics", "w", encoding="utf-8") as f:
    f.write(text)

print("ICS 已更新")