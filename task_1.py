from multiprocessing.dummy import Pool as ThreadPool
import time
import logging

def send_command(router):
    time.sleep(1)
    logging.info(f'router {router} started.')
    print(f'router {router} command1')
    print(f'router {router} command2')
    print(f'router {router} command3')

def main():
    pool = ThreadPool(1)
    router = list(range(1,11))
    results = pool.map(send_command, router)
    pool.close()
    pool.join()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    main()
