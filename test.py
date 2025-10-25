import datetime
from zoneinfo import ZoneInfo

now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
print(now)