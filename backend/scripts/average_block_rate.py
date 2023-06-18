import time
from backend.config import SECONDS

from backend.blockchain.main import Blockchain

blockchain = Blockchain()

times = []

for i in range (1000):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS

    times.append(time_to_mine)

    average_time = sum(times) / len(times)
    print(f'Difficulty {blockchain.chain[-1].difficulty}')
    print(f'Time to mine new Block {time_to_mine}')
    print(f'Average time to mine new block {average_time}\n')
