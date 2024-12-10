import torch


# for now just return a torch dataloader
# TODO: implement the actual anc dataloader
def create_dataloader(*args, **kwargs):
    return torch.utils.data.DataLoader(*args, **kwargs)
