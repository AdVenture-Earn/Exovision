import threading
import multiprocessing
import time
import os
import tempfile

def cpu_hog():
    """Continuously perform a meaningless calculation to max out one CPU core."""
    x = 0
    while True:
        # Some arbitrary math so Python can't optimize it away
        x = (x + 1) * (x - 1) // 3
        if x > 1e6:
            x = 0

def memory_leak():
    """Keep appending to a list to consume RAM over time."""
    data = []
    while True:
        # Append a chunk of bytes to consume memory
        data.append(os.urandom(100_000))  # ~100 KB per iteration
        # Slow it down a tiny bit so you don’t fill RAM instantly
        time.sleep(0.01)

def disk_thrash():
    """Constantly write and discard data on disk."""
    tmp_dir = tempfile.gettempdir()
    i = 0
    while True:
        path = os.path.join(tmp_dir, f"bugfile_{i}.tmp")
        with open(path, 'wb') as f:
            f.write(os.urandom(500_000))   # ~0.5 MB write
        try:
            os.remove(path)
        except OSError:
            pass
        i = (i + 1) % 1000
        # tiny pause so the FS queue backs up
        time.sleep(0.01)

if __name__ == "__main__":
    print("Starting demonstrative bug. Press Ctrl+C to stop.")
    # Spawn CPU‐hogging threads equal to the number of cores
    for _ in range(multiprocessing.cpu_count()):
        t = threading.Thread(target=cpu_hog, daemon=True)
        t.start()

    # One thread for memory leak, one for disk thrash
    threading.Thread(target=memory_leak, daemon=True).start()
    threading.Thread(target=disk_thrash, daemon=True).start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTerminated by user.")
