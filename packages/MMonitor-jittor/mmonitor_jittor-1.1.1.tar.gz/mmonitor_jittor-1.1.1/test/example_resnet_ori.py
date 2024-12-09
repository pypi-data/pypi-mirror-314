import aim
from jittor import nn
import jittor as jt
import copy
from jittor import transform
from MMonitor.mmonitor.monitor import Monitor  
from MMonitor.visualize import Visualization
from jittor.models.resnet import *
from jittor.dataset import Dataset
from jittor.dataset import CIFAR10
from PIL import Image
import numpy as np
class corrupt_train(Dataset):
    def __init__(self, traindata):
        super().__init__()
        self.imgs = traindata.imgs
        self.transform = traindata.transform
        self.sel_data = list(range(50000))

    def __getitem__(self, idx):
        k = self.sel_data[idx]
        with open(self.imgs[k][0], 'rb') as f:
            img = Image.open(f).convert('RGB')
            if self.transform:
                img = self.transform(img)
            return img, self.imgs[k][1], k
    def __len__(self):
        return len(self.imgs)
def build_dataset(cifar10_path,batch_size=100):
    transform_train = transform.Compose([
        transform.RandomHorizontalFlip(),
        transform.RandomCrop(32),
        transform.ToTensor(),
        transform.ImageNormalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    transform_test = transform.Compose([
        transform.ToTensor(),
        transform.ImageNormalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    # 加载数据集
    trainset = CIFAR10(root=cifar10_path,train=True, transform=transform_train,download=False)
    trainloader = trainset.set_attrs(batch_size=batch_size, shuffle=True, num_workers=2)
    return trainloader
def adjust_learning_rate(optimizer, epochs):
    lr = 1e-1
    lr = lr * ((0.1 ** int(epochs >= 80)) * (0.1 ** int(epochs >= 100)))  # For WRN-28-10
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
def prepare_config():
    config_mmonitor = {
        nn.BatchNorm:['ForwardOutputMean','ForwardOutputStd','ZeroActivationPrecentage','LinearDeadNeuronNum'],
        nn.BatchNorm:['BackOutputMean','BackOutputStd'],
        nn.Conv2d:['BackOutputMean','BackOutputStd']
    }
    return config_mmonitor
def ce_loss(output, target, reduce=True):
    if len(output.shape) == 4:
        c_dim = output.shape[1]
        output = output.transpose((0, 2, 3, 1))
        output = output.reshape((-1, c_dim))
    target = target.reshape((-1, ))
    target = target.broadcast(output, [1])
    target = target.index(1) == target
    
    output = output - output.max([1], keepdims=True)
    loss = output.exp().sum(1).log()
    loss = loss - (output*target).sum(1)
    if reduce:
        return loss.mean()
    else:
        return loss


def accuracy(output, target):
    batch_size = target.shape[0]
    pred = np.argmax(output, -1)
    res = ( (pred == target).astype(float).sum() )/batch_size

    return res

def train(model,train_loader,vis,monitor,optimizer,epoch,meta_lr,epoch_losses,epoch_weight,epoch_uncertainty,run_model):
    print('\nEpoch: %d' % epoch)

    train_loss = 0
    meta_loss = 0

    prec_train_all = 0.
    prec_meta_all = 0.

    if epoch < 30:
        for batch_idx, (inputs, targets) in enumerate(train_loader):
            model.train()

            outputs = model(inputs)
            loss = ce_loss(outputs, targets)
            optimizer.set_input_into_param_group((inputs,outputs))
            optimizer.step(loss)
            monitor.track(batch_idx)
            logs = vis.show(batch_idx)
            run_model.track(logs,context={'subset':'train'})
            prec_meta = 0.
            prec_train = accuracy(outputs.data, targets.data)
            train_loss += (loss.item() * outputs.shape[0])
            meta_loss += (0. * outputs.shape[0])
            prec_train_all += (prec_train.item() * outputs.shape[0])
            prec_meta_all += (prec_meta * outputs.shape[0])
            # with jt.no_grad(no_fuse=1):
            #     unce = (nn.softmax(outputs, dim=1)).max()

            #     epoch_losses[index] = ce_loss(outputs, targets, reduce=False)
            #     epoch_uncertainty[index] = unce
            #     epoch_weight[index] = jt.ones( len(unce) )


            if (batch_idx + 1) % 50 == 0:
                print('Epoch: [%d/%d]\t'
                    'Iters: [%d/%d]\t'
                    'Loss: %.4f\t'
                    'MetaLoss:%.4f\t'
                    'Prec@1 %.2f\t'
                    'Prec_meta@1 %.2f' % (
                        (epoch + 1), 120, batch_idx + 1, len(train_loader), (train_loss / (batch_idx + 1)),
                        (meta_loss / (batch_idx + 1)), prec_train, prec_meta))

        return (train_loss / len(train_loader.dataset)), (meta_loss / len(train_loader.dataset)), \
            (prec_train_all / len(train_loader.dataset)), (prec_meta_all / len(train_loader.dataset)), \
            epoch_losses, epoch_uncertainty, epoch_weight
    else:
        model.eval()
        with jt.no_grad(no_fuse=1):
            num_class_all = len( list( set(train_loader.dataset.noise_label) ) )

            all_loss = jt.zeros(len(train_loader.dataset)).float()
            noise_label_all = jt.zeros(len(train_loader.dataset)).long()

            for inputs_u, targets, index in train_loader:
                output_u  = model(inputs_u)
                all_loss[index] = ce_loss(output_u, targets, reduce=False)
                noise_label_all[index] = targets
            noise_label_all = noise_label_all.data.tolist()
            
            idx_to_meta = []
            data_list = {}
            for j in range( 10 ):
                data_list[j] = [i for i, label in enumerate(noise_label_all) if label == j]


            for _, img_id_list in data_list.items():
                _, indexs = jt.topk(all_loss[img_id_list], min(10, len(img_id_list)), largest=False)
                idx_to_meta.extend(((jt.array(img_id_list))[indexs]).tolist())

            train_meta_loader = get_meta1(train_loader, idx_to_meta).set_attrs(num_workers=args.prefetch, batch_size=args.batch_size,shuffle=True)

        train_meta_loader.endless = True
        train_meta_loader_iter = iter(train_meta_loader)
        for batch_idx, (inputs, targets, index) in enumerate(train_loader):
            model.train()

            meta_model = build_model()
            meta_model.load_state_dict(model.state_dict())
            optimizer_temp = optim_temp.SGD(meta_model.parameters(), meta_lr,
                                            momentum=args.momentum, weight_decay=args.weight_decay)

            outputs = meta_model(inputs)
            cost = ce_loss(outputs, targets, reduce=False).reshape((-1,1))
            v_lambda = vnet(cost.detach())
            l_f_meta = ((cost * v_lambda).sum())/(v_lambda.detach().sum())
            optimizer_temp.step(l_f_meta)

            inputs_val, targets_val, _ = next(train_meta_loader_iter)
            y_g_hat = meta_model(inputs_val)
            l_g_meta = nn.cross_entropy_loss(y_g_hat, targets_val)

            optimizer_vnet.step(l_g_meta)

            outputs = model(inputs)
            cost_w = ce_loss(outputs, targets, reduce=False).reshape((-1, 1))
            
            with jt.no_grad():
                w_new = vnet(cost_w)

            loss = ((cost_w * w_new).sum())/(w_new.detach().sum())

            optimizer_model.step(loss)

            prec_meta = accuracy(y_g_hat.data, targets_val.data)
            prec_train = accuracy(outputs.data, targets.data)

            train_loss += (loss.item() * outputs.shape[0])
            meta_loss += (l_g_meta.item() * outputs.shape[0])
            prec_train_all += (prec_train.item() * outputs.shape[0])
            prec_meta_all += (prec_meta.item() * outputs.shape[0])


            with jt.no_grad(no_fuse=1):

                unce = (nn.softmax(outputs, dim=1)).max()

                epoch_losses[index] = cost_w.squeeze(1)
                epoch_uncertainty[index] = unce
                epoch_weight[index] = w_new.squeeze(1)


            if (batch_idx + 1) % 50 == 0:
                print('Epoch: [%d/%d]\t'
                    'Iters: [%d/%d]\t'
                    'Loss: %.4f\t'
                    'MetaLoss:%.4f\t'
                    'Prec@1 %.2f\t'
                    'Prec_meta@1 %.2f' % (
                        (epoch + 1), args.epochs, batch_idx + 1, len(train_loader), (train_loss / (batch_idx + 1)),
                        (meta_loss / (batch_idx + 1)), prec_train, prec_meta))

        return (train_loss / len(train_loader.dataset)), (meta_loss / len(train_loader.dataset)), \
            (prec_train_all / len(train_loader.dataset)), (prec_meta_all / len(train_loader.dataset)), \
            epoch_losses, epoch_uncertainty, epoch_weight


def get_output(model, dataloader):
    pre = jt.zeros( len(train_loader.dataset), 10)
    labels = jt.zeros( len(train_loader.dataset) ).long()
    feature_extractor = copy.deepcopy(model)
    feature_extractor.eval()
    with jt.no_grad():
        for inputs, targets, index in dataloader:
            output = feature_extractor(inputs)
            
            pre[index] = output            
            labels[index] = targets
    return pre, labels

def print_lr(optimizer, epoch):
    for param_group in optimizer.param_groups:
        lr = param_group['lr']
        print('\n Epoch:{:.4f}|LR:{:.4f}\n'.format(epoch,lr))
    return lr

if __name__=='__main__':
    
    cifar_10_python_path = '/data/wlc/dataset/cifar'
    model = Resnet18(pretrained=False,num_classes=10)
    config_mmonitor = prepare_config()
    run_model = aim.Run(repo='aim://203.83.235.100:30058', system_tracking_interval=None, log_system_params=False)
    print('模型已经引入')
    batch_size = 100
    train_loader = build_dataset(cifar_10_python_path,batch_size)
    print('数据已引入')
    epoch_losses = jt.zeros( len(train_loader.dataset) )
    epoch_weight = jt.zeros( len(train_loader.dataset) )
    epoch_uncertainty = jt.zeros( len(train_loader.dataset) )
    num_epochs = 120
    optimizer = jt.optim.SGD(model.parameters(), 1e-1, momentum=0.9, weight_decay=5e-4)
    monitor = Monitor(model,config_mmonitor)
    vis = Visualization(monitor, project=config_mmonitor.keys(), name=config_mmonitor.values())
    for epoch in range(num_epochs):
        adjust_learning_rate(optimizer, epoch)
        meta_lr = print_lr(optimizer, epoch)
        train_loss, meta_loss, prec_train, prec_meta, epoch_losses, epoch_uncertainty, epoch_weight = train(model,train_loader,vis,monitor,optimizer,epoch,meta_lr, epoch_losses, epoch_weight, epoch_uncertainty,run_model)
        
        pre, labels = get_output(model, train_loader)

    