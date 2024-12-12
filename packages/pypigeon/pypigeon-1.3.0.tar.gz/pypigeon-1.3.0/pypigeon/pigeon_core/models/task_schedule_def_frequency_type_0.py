from enum import Enum


class TaskScheduleDefFrequencyType0(str, Enum):
    DAILY = "daily"
    HOURLY = "hourly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
