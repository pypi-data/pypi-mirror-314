import os
import time
from torch.utils.data import DataLoader
from anc.data.anc_dataset import AncDataset
from anc.data.anc_sampler import AncSampler
from anc.data.anc_processor import Processor, AncProcessor
from anc.data.utils import DataNotReady
import logging
import datetime


class AncDataLoader:
    r'''
    A wrapper for dataloader, dataset and sampler
    It makes the handling of the data gathering logic in each subprocess easier
    It also helps handle the checkpoint load and resume logic

    Args:
        paths (list of str): files from which to load the data.
        batch_size (int): how many samples per batch to load.
        num_workers (int): how many subprocesses to use for data
            loading. ``0`` means that the data will be loaded in the main process.
        rank (int, optional): data parallel rank of current process (default: ``0``).
        world (int, optional): data parallel world size (default: ``1``).
        processor (Processor, optional): object that defines the data transform and batch transform
            logic (default ``AncProcessor`` instance which just return the input as is for both
            transform and batch transform).
        data_type (str, optional): the type of dataset that the paths represents (default ``parquet``).
        shuffle (bool, optional): set to ``True`` to have the data reshuffled
            at every epoch (default: ``False``).
        drop_last (bool, optional): set to ``True`` to drop the last incomplete batch,
            if the dataset size is not divisible by the batch size. If ``False`` and
            the size of dataset is not divisible by the batch size, then the last batch
            will be smaller. (default: ``False``).
        seed (int, optional): seed for randomness (default: ``0``).
        pin_memory (bool, optional): If ``True``, the data loader will copy Tensors
            into device/CUDA pinned memory before returning them.  If your data elements
            are a custom type, or your :attr:`collate_fn` returns a batch that is a custom type,
            see the example below.
        ds_args (dict, optional): dataset arguments for data loading, such as the columns to load 
            for parquet files, etc (default ``{}``).
        is_train (bool, optional): whether this dataset if for training (default ``True``).
        data_borrow (bool, optional): If ``True``, worker would borrow data from peers when its data is not ready.
            This would do good to performance, but make the bitwise checkpoint harder (default ``True``).
        repeat (bool, optional): If ``True``, data would be loaded repeatedly
        prefetch_factor (int, optional): the prefetch_factor for torch dataloader
    '''
    def __init__(
        self,
        paths,
        batch_size,
        num_workers,
        rank=0,
        world=1,
        processor=AncProcessor(),
        data_type="parquet",
        shuffle=False,
        drop_last=False,
        seed=0,
        pin_memory=True,
        ds_args={},
        is_train=True,
        data_borrow=False,
        repeat=False,
        prefetch_factor=2,
    ):
    # TODO: add support to get rank and world from torch env
        self.paths = paths
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.dataset = AncDataset(paths, processor=processor, dataset_type=data_type, ds_args=ds_args)
        self.sampler = AncSampler(self.dataset, batch_size, world, rank, num_workers, shuffle, seed, drop_last, repeat=repeat)
        self.dataset.set_sampler(self.sampler)
        if data_borrow:
            assert repeat, "repeat must be true if data_borrow is set"
        try:
            self.loader = DataLoader(
                self.dataset,
                num_workers=num_workers,
                pin_memory=pin_memory,
                collate_fn=lambda x: x,
                prefetch_factor=prefetch_factor,
                enable_borrow=data_borrow
            )
        except:
            self.loader = DataLoader(
                self.dataset,
                num_workers=num_workers,
                pin_memory=pin_memory,
                collate_fn=lambda x: x,
                prefetch_factor=prefetch_factor
            )
            logging.warning("Dataloader does not have enable_borrow attribute!")
        self.step = 0
        self.rank = rank
        self.world = world
        self.loader_iter = None
        self.buffer = [[] for _ in range(num_workers)]
        self.last_wid = -1
        self.out_of_data_worker = set()
        self.is_train = is_train
        self.data_borrow = data_borrow

    def __iter__(self):
        logging.debug(f"pid {os.getpid()} rank {self.rank} in iter")
        self.loader_iter = iter(self.loader)
        self.out_of_data_worker = set()
        return self
    
    def __len__(self):
        return len(self.sampler)
    
    def _get_borrow_id(self):
        max_buffer_id = -1
        max_buffer_length = 0
        for i in range(self.num_workers):
            if len(self.buffer[i]) > max_buffer_length:
                max_buffer_length = len(self.buffer[i])
                max_buffer_id = i
        return max_buffer_id

    def __next__(self):
        now = datetime.datetime.now()
        need_logging = self.loader_iter._data_queue.qsize() < 10
        t1 = time.time()
        if len(self.out_of_data_worker) == self.num_workers:
            # TODO: better handle the exception
            raise StopIteration
        # decide which subprocess to get data from
        if self.last_wid < 0:
            cur_wid = self.step % self.num_workers
        else:
            cur_wid = (self.last_wid + 1) % self.num_workers
        if cur_wid in self.out_of_data_worker:
            for i in range(self.num_workers):
                cur_wid = (cur_wid + 1) % self.num_workers
                if cur_wid not in self.out_of_data_worker:
                    break
        data = None
        if len(self.buffer[cur_wid]) > 0:
            data = self.buffer[cur_wid].pop()
        else:
            cnt = 0
            while True:
                item = next(self.loader_iter)
                # since we set batch size=1 for torch dataloader, 
                # the actual batch size is handled by sampler
                # we need to use index 0 to get data out
                # note: cur_data here should be a list of batch data
                cur_data_wid, cur_data, is_last_batch = item[0]
                if is_last_batch:
                    self.out_of_data_worker.add(cur_data_wid)
                if isinstance(cur_data, DataNotReady):
                    logging.info(f"next call get DataNotReady from {cur_data_wid}, is last batch {is_last_batch}")
                    continue
                assert isinstance(cur_data, list)
                if cur_data_wid == cur_wid:
                    data = cur_data[0]
                    self.buffer[cur_data_wid] += cur_data[1:]
                    break
                else:
                    # store the out of order data
                    self.buffer[cur_data_wid] += cur_data
                cnt += 1
                if cnt % self.num_workers == 0:
                    logging.warning(f"{self.rank} Too many loop ({cnt} times) when getting next data for worker {cur_wid} of step {self.step}")
        self.step += 1
        self.last_wid = cur_wid
        consumed_time = time.time() - t1
        need_logging = need_logging or consumed_time > 0.01
        if need_logging:
            logging.info(f"__next__ called time {now} pid {os.getpid()} rank {self.rank} return step {self.step} consumed time {consumed_time} data with buffer {self.loader_iter._data_queue.qsize()}")
        return data

    def __getstate__(self):
        state = {}
        state['paths'] = self.paths
        state['batch_size'] = self.batch_size
        state['num_workers'] = self.num_workers
        state['sampler'] = self.sampler.__getstate__()
        # TODO: add actual subprocess's state
        state['dataset'] = self.dataset.__getstate__()
        state['last_wid'] = self.last_wid
        state['out_of_data_worker'] = self.out_of_data_worker
        state['step'] = self.step

    def __setstate__(self, state):
        if 'dataset' in state:
            dataset_state = state.pop('dataset')
            self.dataset.__setstate__(dataset_state)
        if 'sampler' in state:
            sampler_state = state.pop('sampler')
            self.sampler.__setstate__(sampler_state)
        self.__dict__.update(state)


if __name__ == "__main__":
    folder = "/mnt/personal/parquet_demo_data"
    fnames = [
        "01_0001.parquet",
        "02_0001.parquet",
        "03_0001.parquet",
        "04_0001.parquet",
        "05_0001.parquet",
        "06_0001.parquet",
        "07_0001.parquet"
    ]
    files = [f"{folder}/{fname}" for fname in fnames]
    loader = AncDataLoader(files, 1024, num_workers=4)
    for data in loader:
        print(len(data))
