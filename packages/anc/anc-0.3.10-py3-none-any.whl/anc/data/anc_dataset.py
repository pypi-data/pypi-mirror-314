import torch
from torch.utils.data.dataset import Dataset
from anc.data.parquet_dataset import ParquetConcateDataset
from anc.data.utils import DataNotReady
from torch.utils.data import IterableDataset
import inspect
import itertools
import logging


class AncDataset(IterableDataset):
    r'''
    A class defines the pipeline of data loading and data transform

    Args:
        filepaths (list of str): files from which to load the data.
        processor (Processor): object that defines the data transform and batch transform logic.
        sampler: object that control the data loader order
        dataset_type (str, optional): the type of dataset that the paths represents (default ``parquet``).
        ds_args (dict, optional): dataset arguments for data loading, such as the columns to load 
            for parquet files, etc (default ``{}``).
        repeat (bool, optional): if set to True, the data will be loaded repeatedly
    '''
    def __init__(self, filepaths, processor, sampler=None, dataset_type="parquet", ds_args={}, repeat=False):
        self.filepaths = filepaths
        self.dataset_type = dataset_type
        self.ds_args = ds_args
        # TODO: support more types of dataset
        self.ds = ParquetConcateDataset(filepaths, columns=ds_args.get("columns"))
        self.processor = processor
        self.sampler = sampler
    
    def set_sampler(self, sampler):
        self.sampler = sampler
    
    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        wid = worker_info.id if worker_info is not None else 0
        num_workers = worker_info.num_workers if worker_info is not None else 1
        logging.debug(f"iter information: len(sampler) - {len(self.sampler)}, worker id - {wid}, num_workers - {num_workers}")
        # use islice to get the iterator of sampler only for current worker
        sampler_iter = itertools.islice(iter(self.sampler), wid, len(self.sampler), num_workers)
        yield from self.get_generator(sampler_iter)

    def get_generator(self, sampler_iter):
        while True:
            indices = next(sampler_iter)
            item_generator = self._getitem(indices)
            is_last = False
            while True:
                try:
                    wid, next_data, is_last = next(item_generator)
                    yield (wid, [next_data], False)
                except StopIteration:
                    if is_last:
                        yield (wid, DataNotReady(), True)
                    break
            if is_last:
                break

    def _getitem(self, idxs):
        worker_info = torch.utils.data.get_worker_info()
        wid = worker_info.id if worker_info is not None else 0
        idxs, is_last_batch = idxs
        if isinstance(idxs, int):
            idxs = [idxs]
        if len(idxs) == 0:
            yield (wid, DataNotReady(), is_last_batch)
            return
        raw_data = [self.ds[idx] for idx in idxs]
        if self.processor.transform:
            processed_data = []
            for data_idx, data in enumerate(raw_data):
                is_last_sample = is_last_batch and data_idx == len(raw_data) - 1
                processed = self.processor.transform(data, is_last_sample)
                if processed is None:
                    continue
                if isinstance(processed, list):
                    processed_data += processed
                else:
                    # processed_data is a generator
                    if self.processor.batch_transform:
                        # batch_processed is a generator too
                        batch_processed = self.processor.batch_transform(processed, is_last_sample)
                        if batch_processed is not None:
                            for batch in batch_processed:
                                yield (wid, batch, is_last_sample)         
        else:
            processed_data = raw_data
        if processed_data and self.processor.batch_transform:
            batch_processed = self.processor.batch_transform(processed_data, is_last_batch)
            if batch_processed is None:
                batch_processed = DataNotReady()
            else:
                assert isinstance(batch_processed, list)
        else:
            batch_processed = []
        for batch in batch_processed:
            yield (wid, batch, is_last_batch)

    def __getstate__(self):
        state = {}
        state['filepaths'] = self.filepaths
        state['dataset_type'] = self.dataset_type
        state['ds_args'] = self.ds_args
        state['processor'] = self.processor.__getstate__()

    def __setstate__(self, state):
        if 'processor' in state:
            processor_state = state.pop('processor')
            self.processor.__setstate__(state['processor'])
        self.__dict__.update(state)

    def __len__(self):
        return len(self.ds)
    
    def get_sub_lengths(self):
        if self.dataset_type == 'parquet':
            level = "row_group"
        else:
            level = "file"
        return self.ds.get_sub_lengths(level)


if __name__ == "__main__":
    from anc.data.anc_processor import AncProcessor
    from anc.data.anc_sampler import AncSampler
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
    ds = AncDataset(files, AncProcessor())
    sampler = AncSampler(ds, 1)
    ds.set_sampler(sampler)
    assert sum([sum(i) for i in ds.get_sub_lengths()]) == len(ds)
    ds_iter = iter(ds)
    for i in range(10):
        wid, data, is_last_batch = next(ds_iter)
        print(data[0][0]['filepath'])

