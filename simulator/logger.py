'''
this file is for simulator to make trace file.
this file provide a Logger instance.
'''
from typing import Optional, Literal
import os
from datetime import datetime

def ll(thread: str, pid: int, cpu: int, timestamp: int, type: Literal["begin", "B", "end", "E", "count", "C"], name: Optional[str] = None, count: Optional[int] = None, tid: Optional[int] = None) -> str:
    ''' build and return a line for the systrace file.

        line format: {thread}-{pid} [{cpu}] .... {sec}.{us}: tracing_mark_write: {B,E,C}|{pid}|{name}|{count}\n
        timestamp is in us \n
        name and count is optional \n
    '''
    type = type[0].upper()
    if tid is None:
        tid = pid
    if name is not None:
        name = f"|{name}"
    else:
        name = ''
    if (name is not None) and (count is not None):
        count = f"|{count}"
    else:
        count = ''
    return f"{thread}-{tid} [{cpu}] .... {timestamp/(10**6):.6f}: tracing_mark_write: {type}|{pid}{name}{count}\n"

class __Logger:
    ''' a logger to log event into trace file

        usage example:
        1. call Logger.set_file_path(dir, filename) to set file path
        2. call Logger.open() to create file
        3. call Logger.update_timestamp(time) to update the timestamp for logging
        3. call Logger.log(...) when need to log slice or count
        4. call Logger.close() when this file is finish
    '''
    file = None
    file_abs_path = None
    current_timestamp = 0
    previous_timestamp = 0
    single_slice_count = 0

    def set_file_path(self, path: str = f"{__file__}/../../output", name: str = '') -> str:
        ''' set the file's path and return
        '''
        # create dir if not exist yet
        if not os.path.exists( path ):
            os.makedirs( path )
        # set file dir
        file_dir  = path
        # set default file name if not provided
        if not name:
            name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.trace"
        file_name = os.path.basename( os.path.basename(name) )
        # make abs file path
        self.file_abs_path = os.path.abspath( os.path.join(file_dir, file_name) )
        return self.file_abs_path
    def open(self) -> None:
        ''' create trace file if not exist yet and open it
        '''
        if self.file_abs_path and not self.file:
            self.file = open(self.file_abs_path, 'wt')
            self.file.write("# tracer:nop\n")
            self.single_slice_count = 0
        else:
            raise Exception("ERROR: file path not set yet")
    def log(self, thread: str, pid: int, cpu: int, 
            type: Literal["begin", "B", "end", "E", "count", "C"], 
            name: Optional[str] = None, count: Optional[int] = None, 
            tid: Optional[int] = None) -> None:
        ''' log on trace file
        '''
        if self.file:
            self.file.write(
                ll(thread, pid, cpu, self.current_timestamp, type, name, count, tid)
            )
            if type == 'B':
                self.single_slice_count += 1
            elif type == 'E':
                self.single_slice_count -= 1
        else:
            raise Exception("ERROR: file not opened yet")
    def update_timestamp(self, time: int) -> None:
        ''' update the current timestamp used to log
        '''
        if time < self.previous_timestamp:
            raise Exception("ERROR: timestamp earlier than last one")
        self.previous_timestamp = self.current_timestamp
        self.current_timestamp = time
        pass
    def close(self) -> None:
        ''' close the trace file if it is opened
        '''
        if self.file:
            self.file.close()
            self.file = None
            if self.single_slice_count != 0:
                print(f"WARNING: begins and ends are not paired: remains {self.single_slice_count} begin")
    def __del__(self):
        self.close()
    
# Logger
Logger: __Logger = __Logger()


###################################################################
def __test():
    print("===== test logger =====")
    print(Logger.set_file_path(name='test_in_logger.trace'))
    Logger.open()
    Logger.update_timestamp(1); Logger.log(thread="MDLA", tid=0, pid=87, cpu=0, type="B", name='work')
    Logger.update_timestamp(2); Logger.log(thread="MDLA", tid=1, pid=87, cpu=0, type="B", name=0)
    Logger.update_timestamp(2); Logger.log(thread="MDLA", tid=1, pid=87, cpu=0, type="B", name=0)
    Logger.update_timestamp(5); Logger.log(thread="MDLA", tid=0, pid=87, cpu=0, type="E")
    Logger.update_timestamp(6); Logger.log(thread="MDLA", tid=1, pid=87, cpu=0, type="E")
    Logger.close()
if __name__ == '__main__':
    __test()