import logging

TRACE_LOG_LEVEL=0
logging.addLevelName(TRACE_LOG_LEVEL, 'TRACE')

def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LOG_LEVEL):
        self._log(TRACE_LOG_LEVEL, message, args, kws)

logging.Logger.trace = trace
