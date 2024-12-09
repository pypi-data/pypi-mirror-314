import os
import argparse
import aim
import numpy as np
import jittor as jt
import optim as optim_temp 
from MMonitor.mmonitor.monitor import Monitor  
from MMonitor.visualize import Visualization
from data import *
from jittor import nn
from jittor import models
from sklearn.cluster import KMeans

import copy
import datetime

from sklearn.manifold import TSNE
from sklearn.metrics import confusion_matrix
from PIL import Image
from c2net.context import prepare,upload_output
from jittor.dataset import Dataset



# c2net_context = prepare()
cifar_10_python_path = c2net_context.dataset_path

parser = argparse.ArgumentParser(description='PyTorch WideResNet Training')
parser.add_argument('--dataset', default='cifar10', type=str, help='dataset')
parser.add_argument('--model', default='resnet32', type=str, help='model')
parser.add_argument('--num_classes', default=10, type=int, help='the number of dataset classes')
parser.add_argument('--num_meta', type=int, default=1000)
parser.add_argument('--epochs', default=120, type=int, help='number of total epochs to run')
parser.add_argument('--batch_size', '--batch-size', default=100, type=int, help='mini-batch size (default: 100)')
parser.add_argument('--lr', '--learning-rate', default=1e-1, type=float, help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
parser.add_argument('--nesterov', default=True, type=bool, help='nesterov momentum')
parser.add_argument('--weight-decay', '--wd', default=5e-4, type=float, help='weight decay (default: 5e-4)')
parser.add_argument('--prefetch', type=int, default=1, help='Pre-fetching threads.')
parser.add_argument('--corruption_prob', type=float, default=0.4, help='label noise')
parser.add_argument('--corruption_type', '-ctype', type=str, default='unif', help='Type of corruption ("unif" or "flip" or "flip2").')
parser.add_argument('--seed', type=int, default=1)

args = parser.parse_args()

args.cifar_10_python_path = cifar_10_python_path
args.sel_data = list(range(50000))

jt.flags.use_cuda = 1


def build_model():
    model = models.Resnet18(num_classes=args.num_classes)
    return model


class VNet(nn.Module):
    def __init__(self, input, hidden1, output):
        super(VNet, self).__init__()
        self.linear1 = nn.Linear(input, hidden1)
        self.relu1 = nn.ReLU()
        self.linear2 = nn.Linear(hidden1, output)

    def execute(self, x):
        x = self.linear1(x)
        x = self.relu1(x)
        out = self.linear2(x)
        return nn.Sigmoid()(out)


def accuracy(output, target):
    batch_size = target.shape[0]
    pred = np.argmax(output, -1)
    res = ( (pred == target).astype(float).sum() )/batch_size

    return res


def print_lr(optimizer, epoch):
    for param_group in optimizer.param_groups:
        lr = param_group['lr']
        print('\n Epoch:{:.4f}|LR:{:.4f}\n'.format(epoch,lr))
    return lr
  

def adjust_learning_rate(optimizer, epochs):
    lr = args.lr * ((0.1 ** int(epochs >= 80)) * (0.1 ** int(epochs >= 100)))  # For WRN-28-10
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class get_meta1(Dataset):
    def __init__(self, train_data, idx_to_meta_sel):
        self.imgs = train_data.imgs
        self.transform = train_data.transform

        self.idx_to_meta_sel = idx_to_meta_sel

    def __getitem__(self, idx):
        index = self.idx_to_meta_sel[idx]
        with open(self.imgs[index][0], 'rb') as f:
            img = Image.open(f).convert('RGB')
            if self.transform:
                img = self.transform(img)
            return img, self.imgs[index][1], index

    def __len__(self):
        return len(self.idx_to_meta_sel)


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


def test(model, test_loader):
    model.eval()
    correct = 0
    test_loss = 0

    for _, (inputs, targets, _) in enumerate(test_loader):
        inputs, targets = jt.array(inputs), jt.array(targets)
        outputs = model(inputs)
        test_loss += nn.cross_entropy_loss(outputs, targets).detach().item()
        predicted = np.argmax(outputs.detach(), -1) 
        correct += ( (predicted == targets.data).astype(float).sum() )

    test_loss /= len(test_loader)
    accuracy = 100. * correct / len(test_loader)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
        test_loss, correct, len(test_loader),
        accuracy))

    return accuracy

def prepare_config():
    config_mmonitor_resnet18 = {
        nn.BatchNorm:['ForwardOutputMean','ForwardOutputStd','ZeroActivationPrecentage','LinearDeadNeuronNum','BackOutputMean','BackOutputStd'],
        nn.Conv2d:['BackOutputMean','BackOutputStd','WeightNorm']
    }
    config_mmonitor_vnet={
        nn.Linear: ['ZeroActivationPrecentage']
        # nn.ReLU: ['ZeroActivationPercentage']
    }
    return config_mmonitor_resnet18,config_mmonitor_vnet
def train(train_loader, model, vnet, optimizer_model, optimizer_vnet, epoch, meta_lr, epoch_losses, epoch_weight, epoch_uncertainty,monitor_model,monitor_vnet,vis_model,vis_vnet,run_model):
    print('\nEpoch: %d' % epoch)

    train_loss = 0
    meta_loss = 0

    prec_train_all = 0.
    prec_meta_all = 0.

    if epoch < 30:
        for batch_idx, (inputs, targets, index) in enumerate(train_loader):
            model.train()

            outputs = model(inputs)
            loss = ce_loss(outputs, targets)
            
            optimizer_model.step(loss)

            prec_meta = 0.
            prec_train = accuracy(outputs.data, targets.data)

            train_loss += (loss.item() * outputs.shape[0])
            meta_loss += (0. * outputs.shape[0])
            prec_train_all += (prec_train.item() * outputs.shape[0])
            prec_meta_all += (prec_meta * outputs.shape[0])


            with jt.no_grad(no_fuse=1):
                unce = (nn.softmax(outputs, dim=1)).max()

                epoch_losses[index] = ce_loss(outputs, targets, reduce=False)
                epoch_uncertainty[index] = unce
                epoch_weight[index] = jt.ones( len(unce) )


            if (batch_idx + 1) % 50 == 0:
                print('Epoch: [%d/%d]\t'
                    'Iters: [%d/%d]\t'
                    'Loss: %.4f\t'
                    'MetaLoss:%.4f\t'
                    'Prec@1 %.2f\t'
                    'Prec_meta@1 %.2f' % (
                        (epoch + 1), args.epochs, batch_idx + 1, len(train_loader), (train_loss / (batch_idx + 1)),
                        (meta_loss / (batch_idx + 1)), prec_train, prec_meta))
        monitor_model.track(epoch)
        logs = vis_model.show(epoch)
        print(logs)
        run_model.track(logs,context={'subset':'train'})
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
            for j in range( args.num_classes ):
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
            optimizer_vnet.set_input_into_param_group((inputs_val,y_g_hat))
            optimizer_vnet.step(l_g_meta)

            outputs = model(inputs)
            cost_w = ce_loss(outputs, targets, reduce=False).reshape((-1, 1))
            
            with jt.no_grad():
                w_new = vnet(cost_w)

            loss = ((cost_w * w_new).sum())/(w_new.detach().sum())
            optimizer_model.set_input_into_param_group((inputs,outputs))
            optimizer_model.step(loss)

            prec_meta = accuracy(y_g_hat.data, targets_val.data)
            prec_train = accuracy(outputs.data, targets.data)

            train_loss += (loss.item() * outputs.shape[0])
            meta_loss += (l_g_meta.item() * outputs.shape[0])
            prec_train_all += (prec_train.item() * outputs.shape[0])
            prec_meta_all += (prec_meta.item() * outputs.shape[0])


            with jt.no_grad(no_fuse=1):
                # train_loss += loss
                # meta_loss += l_g_meta

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
        monitor_vnet.track(epoch)
        logs_vnet = vis_vnet.show(epoch)
        run_model.track(logs_vnet,context={'subset':'train'})
        monitor_model.track(epoch)
        logs_model = vis_model.show(epoch)
        run_model.track(logs_model,context={'subset':'train'})
        return (train_loss / len(train_loader.dataset)), (meta_loss / len(train_loader.dataset)), \
            (prec_train_all / len(train_loader.dataset)), (prec_meta_all / len(train_loader.dataset)), \
            epoch_losses, epoch_uncertainty, epoch_weight


def extract_features(model, dataloader):
    features = []
    labels = []
    feature_extractor = copy.deepcopy(model)
    feature_extractor.linear=nn.Identity()
    with jt.no_grad():
        for inputs, targets, _ in dataloader:
            output = feature_extractor(inputs)
            features.append(output.reshape(output.shape[0], -1).numpy())
            labels.append(targets.numpy())
    return np.concatenate(features), np.concatenate(labels)


def get_output(model, dataloader):
    pre = jt.zeros( len(train_loader.dataset), args.num_classes )
    labels = jt.zeros( len(train_loader.dataset) ).long()
    feature_extractor = copy.deepcopy(model)
    feature_extractor.eval()
    with jt.no_grad():
        for inputs, targets, index in dataloader:
            output = feature_extractor(inputs)
            
            pre[index] = output            
            labels[index] = targets
    return pre, labels


# load dataset 
train_loader = build_dataset(args)

# load model
model = build_model()
vnet = VNet(1, 100, 1)

optimizer_model = jt.optim.SGD(model.parameters(), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
optimizer_vnet = jt.optim.Adam(vnet.parameters(), 1e-3, weight_decay=1e-4)

current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
tensorboard_log_path = f'./tensorboard_log/{current_time}'



def main():
    best_acc = 0

    train_loss_all = []
    meta_loss_all = []
    prec_train_all = []
    prec_meta_all = []

    epoch_losses = jt.zeros( len(train_loader.dataset) )
    epoch_weight = jt.zeros( len(train_loader.dataset) )
    epoch_uncertainty = jt.zeros( len(train_loader.dataset) )


    out_file_list = []
    config_mmonitor_resnet,config_mmonitor_vnet = prepare_config()
    run_model = aim.Run(repo='aim://203.83.235.100:30058', system_tracking_interval=None, log_system_params=False)
    monitor_resnet = Monitor(model,config_mmonitor_resnet)
    monitor_vnet = Monitor(vnet,config_mmonitor_vnet)
    vis_model = Visualization(monitor_resnet, project=config_mmonitor_resnet.keys(), name=config_mmonitor_resnet.values())
    vis_vnet = Visualization(monitor_vnet, project=config_mmonitor_vnet.keys(), name=config_mmonitor_vnet.values())
    for epoch in range(args.epochs):
        adjust_learning_rate(optimizer_model, epoch)
        meta_lr = print_lr(optimizer_model, epoch)
        train_loss, meta_loss, prec_train, prec_meta, epoch_losses, epoch_uncertainty, epoch_weight = train(train_loader, model, vnet, optimizer_model, optimizer_vnet,epoch, meta_lr, epoch_losses, epoch_weight, epoch_uncertainty,monitor_resnet,monitor_vnet,vis_model,vis_vnet,run_model)
        
        pre, labels = get_output(model, train_loader)
if __name__ == '__main__':
    main()
