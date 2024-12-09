import datetime
import time


# --------------------
## loop until the total elapsed time is greater or equal to the timeout.
# each loop takes delay seconds.
# fixed_adjustment can be used to may each loop time more accurate
#
# @param timeout    (float) the total amount of time (seconds) to loop
# @param delay      (float) the loop time (seconds) to wait
# @param fixed_adjustment (float) the adjustment (seconds) to apply to each loop delay
# @return None
def accurate_wait(timeout: float, delay: float, fixed_adjustment: float = 0.0):
    start_time = datetime.datetime.now().timestamp()
    # uncomment to debug
    # last_time = start_time - delay
    # print(f'last={last_time: >10.6f}')
    count = 1
    elapsed = 0
    while elapsed < timeout:
        elapsed = datetime.datetime.now().timestamp() - start_time
        # yield elapsed, start_time
        yield elapsed, start_time

        expected = start_time + (delay * count)
        last_time = datetime.datetime.now().timestamp()
        adj_delay = expected - last_time - fixed_adjustment
        # print(f'last={last_time: >10.6f} exp={expected: >10.6f} adj={adj_delay: >10.6f}')

        # if the caller's loop took longer than the delay time,
        # adj_delay will be <= 0
        if adj_delay > 0:
            time.sleep(adj_delay)
        count += 1
