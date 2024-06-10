# Minhas Kamal (minhaskamal024@gmail.com)
# 31 Mar 24

import time

class ChangeDetector:
    _tolerance = 2

    def __init__(self, timeframe=0.5, significance_level=0.05):
        self.timeframe = timeframe
        self.significance_level = significance_level
        self.current_window: list[int] = []
        self.reference_window_avg = -1
        self.start_time = 0
    
    def _reset(self):
        self.start_time = time.time()
        self.current_window.clear()
        return
    
    def _is_passed_timeframe(self):
        curr_time = time.time()
        if curr_time - self.start_time > self.timeframe:
            return True
        return False
    
    def is_changing(self, value: int) -> bool:
        if not self.current_window and self._is_passed_timeframe():
            self._reset()

        self.current_window.append(value)

        if self._is_passed_timeframe():
            current_window_avg = sum(self.current_window) / len(self.current_window)
            if abs(current_window_avg - self.reference_window_avg) < self._tolerance:
                return False

            # print(f"{current_window_avg} - {self.reference_window_avg}")
            self.reference_window_avg = current_window_avg
            self._reset()

        return True
