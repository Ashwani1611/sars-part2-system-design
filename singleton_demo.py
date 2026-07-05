# task 2.3c - singleton database connection, thread safe

import threading


class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):

        #if two threads both check "is instance none" at the same time without a lock, both can pass that check before either one has finished making the object. so you end up with two different instances and whichever one finishes last just overwrites the other one silently. thats the race condition, lock stops it.


        self.connection_string = "postgresql://sars_db:5432/sars"
        print("DatabaseConnection instance created")

    @classmethod
    def get_connection(cls):
        # check without lock first, once instance exists just skip the lock entirely so we're not locking on every single call
        if cls._instance is None:
            with cls._lock:
                # check again inside the lock, another thread might have already made it while we were waiting for the lock
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance


if __name__ == "__main__":
    results = []

    def worker():
        results.append(DatabaseConnection.get_connection())

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    same_instance = all(conn is results[0] for conn in results)
    print(f"All threads got the same instance: {same_instance}")