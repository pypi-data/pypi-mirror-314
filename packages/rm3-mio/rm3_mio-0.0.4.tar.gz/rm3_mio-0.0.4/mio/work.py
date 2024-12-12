########################
# TIME MATH
########################

# # TIME
# from time import time as epoch
# EPOCH_MS = lambda: int(epoch() * 1000)
# EPOCH = lambda: int(epoch())


def time(timeRangeString):
    times = timeRangeString.split("-")
    a = Time.fromString(times[0])
    b = Time.fromString(times[1])
    return a - b


class Time:
    def __init__(self, hour:int, minute:int):
        self.hours = hour
        self.minutes = minute
        self.military = hour*60+minute

    @classmethod
    def fromString(cls, timeString):
        if ":" in timeString:
            h,m = timeString.split(":")
            return cls( int(h), int(m) )
        else:
            return cls( int(timeString), 0 )

    def __gt__(self, other):
        if type(other)!=Time: raise TypeError
        return self.military > other.military

    def __repr__(self):
        return f"{self.hours}:{self.minutes}"

    def __sub__(self, other):
        if type(other)!=Time: raise TypeError

        # am / pm crossover (convert to military)
        if other < self: other.hours += 12

        deltaHour = other.hours - self.hours
        deltaMinute = other.minutes - self.minutes
        if deltaMinute < 0:
            deltaHour -= 1
            deltaMinute += 60
 
        return round(deltaHour + deltaMinute/60, 3)