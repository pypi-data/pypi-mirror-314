"""
DO NOT IMPORT ANYTHING OTHER THAN BUIL-INS IN THIS FILE.
THIS COPIED AND RUN AS A STANDALONE SCRIPT
"""
import logging
import random
import time

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def train():
    epoch = 0
    while True:
        sleep_time = random.randint(10, 30)
        time.sleep(sleep_time)
        accuracy_hist_train = random.randint(0, 100) / 100
        accuracy_hist_valid = random.randint(0, 100) / 100
        end = sleep_time
        loss_hist_train = random.choice(range(1, 2, 0.01))
        loss_hist_valid = random.choice(range(1, 2, 0.01))
        dir_name = "test"
        _log = (
            f"[Data-row] {epoch=}, train_acc={accuracy_hist_train*100:.2f}%, "
            + f"test_acc={accuracy_hist_valid*100:.2f}%, time={end:.2f}sec, "
            + f"train_loss={loss_hist_train:.4f}, val_loss={loss_hist_valid:.4f}, {dir_name=}"
        )
        LOGGER.info(_log)
        epoch += 1
