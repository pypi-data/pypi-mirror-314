class LineIterator:
    """Example usage:
    stream = request.stream
    # The stream may not have the attribute 'readable'.
    # This happens when we get a Body instance from GUnicorn instead of the stream from Flask
    stream = io.TextIOWrapper(stream, encoding='utf-8') if hasattr(stream, 'readable') else LineIterator(stream)

    """

    def __init__(self, body):
        self.body = body

    def __iter__(self):
        return self

    def __next__(self):
        line = self.body.readline()
        if not line:
            raise StopIteration
        return line.decode('utf-8')


class AcquireReleaseCtx:
    def __init__(self, semaphore):
        self.semaphore = semaphore

    def __enter__(self):
        self.semaphore.acquire()
        return self.semaphore

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.semaphore.release()
