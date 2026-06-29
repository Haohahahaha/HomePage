import os
import re
import requests
from datetime import datetime, timedelta

ICS_URL = os.environ["ICS_URL"]

text = requests.get(ICS_URL).text

# 把微软私有时区改掉（虽然最后会删掉 TZID）
text = text.replace(
    "TZID:Customized Time Zone",
    "TZID:Asia/Shanghai"
)

text = text.replace(
    "TZID=Customized Time Zone",
    "TZID=Asia/Shanghai"
)


def convert_to_utc(match):
    """
    DTSTART;TZID=Asia/Shanghai:20260401T080000
    ->
    DTSTART:20260401T000000Z
    """

    field = match.group(1)      # DTSTART 或 DTEND
    dt_str = match.group(2)     # 20260401T080000

    local_time = datetime.strptime(dt_str, "%Y%m%dT%H%M%S")

    # 北京时间 -> UTC
    utc_time = local_time - timedelta(hours=8)

    return f"{field}:{utc_time.strftime('%Y%m%dT%H%M%SZ')}"


# 转换 DTSTART
text = re.sub(
    r"(DTSTART);TZID=Asia/Shanghai:(\d{8}T\d{6})",
    convert_to_utc,
    text
)

# 转换 DTEND
text = re.sub(
    r"(DTEND);TZID=Asia/Shanghai:(\d{8}T\d{6})",
    convert_to_utc,
    text
)

# 删除整个 VTIMEZONE 块（UTC 不需要）
text = re.sub(
    r"BEGIN:VTIMEZONE.*?END:VTIMEZONE\r?\n",
    "",
    text,
    flags=re.DOTALL
)

with open("docs/calendar.ics", "w", encoding="utf-8") as f:
    f.write(text)

print("ICS 已转换为 UTC")