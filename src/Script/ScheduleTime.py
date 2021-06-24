from datetime import datetime

class ScheduleTime:
    def __init__(self, sec = None, minu = None, hour = None, days = None, month = None):
        self.mSecond = []
        self.mMinute = []
        self.mHour = []
        self.mDays = []
        self.mMonth = []

        if type(sec) is list: 
            self.mSecond.extend(sec)
        elif sec != None: 
            self.mSecond.append(int(sec))

        if type(minu) is list: 
            self.mMinute.extend(minu)
        elif minu != None: 
            self.mMinute.append(int(minu))

        if type(hour) is list: 
            self.mHour.extend(hour)
        elif hour != None: 
            self.mHour.append(int(hour))

        if type(days) is list: 
            self.mDays.extend(days)
        elif days != None: 
            self.mDays.append(int(days))

        if type(month) is list: 
            self.mMonth.extend(month)
        elif month != None: 
            self.mMonth.append(int(month))
    
    def CheckTime(self, t: datetime):
        if self.mSecond and not t.second in self.mSecond:
            return False
        elif self.mMinute and not t.minute in self.mMinute:
            return False
        elif self.mHour and not t.hour in self.mHour:
            return False
        elif self.mDays and not t.day in self.mDays:
            return False
        elif self.mMonth and not t.month in self.mMonth:
            return False
        return True
    
    @staticmethod
    def Parse(text: str):
        part = text.split(' ')
        if len(part) != 5:
            raise ValueError('invalid schedule format')
        second = [int(x) for x in filter(lambda x: x!='*', part[0].split(','))]
        minute = [int(x) for x in filter(lambda x: x!='*', part[1].split(','))]
        hour = [int(x) for x in filter(lambda x: x!='*', part[2].split(','))]
        days = [int(x) for x in filter(lambda x: x!='*', part[3].split(','))]
        month = [int(x) for x in filter(lambda x: x!='*', part[4].split(','))]
        return ScheduleTime(second, minute, hour, days, month)

    def __str__(self):
        seq = [self.mSecond, self.mMinute, self.mHour, self.mDays, self.mMonth]
        return ' '.join(['*' if len(x)==0 else ','.join([str(y) for y in x]) for x in seq])