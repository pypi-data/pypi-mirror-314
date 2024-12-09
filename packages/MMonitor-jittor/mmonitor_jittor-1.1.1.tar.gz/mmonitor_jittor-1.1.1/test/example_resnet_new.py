import os
import aim
import argparse
import numpy as np
import jittor as jt
import optim as optim_temp 
from MMonitor.mmonitor.monitor import Monitor  
from MMonitor.visualize import Visualization
from jittor import nn
from jittor import models
import jittor.transform as transform
import copy
from data import *
import datetime
from PIL import Image
from jittor.dataset import Dataset
# from c2net.context import prepare,upload_output
# c2net_context = prepare()
parser = argparse.ArgumentParser(description='PyTorch WideResNet Training')
parser.add_argument('--model', default='resnet32', type=str, help='model')
parser.add_argument('--epochs', default=10, type=int, help='number of total epochs to run')
parser.add_argument('--batch_size', '--batch-size', default=100, type=int, help='mini-batch size (default: 100)')
parser.add_argument('--lr', '--learning-rate', default=1e-1, type=float, help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
parser.add_argument('--weight-decay', '--wd', default=5e-4, type=float, help='weight decay (default: 5e-4)')
parser.add_argument('--prefetch', type=int, default=1, help='Pre-fetching threads.')
parser.add_argument('--seed', type=int, default=1)

args = parser.parse_args()
args.cifar_10_python_path = '/data/wlc/dataset/cifar' 
args.json_file_path = '/home/wlc/wlc/jittor-mmonitor/model'

args.sel_data = list(range(50000))

jt.flags.use_cuda = 1


def build_model():
    model = models.Resnet18(num_classes=args.num_classes)
    return model


def prepare_config():
    config_mmonitor_resnet18 = {
        nn.BatchNorm: ['ForwardInputSndNorm', 'ForwardInputMean', 'ForwardInputStd', 'WeightNorm','WeightMean']

    }
    return config_mmonitor_resnet18


def accuracy(output, target):
    batch_size = target.shape[0]
    pred = np.argmax(output, -1)
    res = ((pred == target).astype(float).sum()) / batch_size

    return res


def adjust_learning_rate(optimizer, epochs):
    lr = args.lr * ((0.1 ** int(epochs >= 80)) * (0.1 ** int(epochs >= 100)))  # For WRN-28-10
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def ce_loss(output, target, reduce=True):
    if len(output.shape) == 4:
        c_dim = output.shape[1]
        output = output.transpose((0, 2, 3, 1))
        output = output.reshape((-1, c_dim))
    target = target.reshape((-1,))
    target = target.broadcast(output, [1])
    target = target.index(1) == target

    output = output - output.max([1], keepdims=True)
    loss = output.exp().sum(1).log()
    loss = loss - (output * target).sum(1)
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
        correct += ((predicted == targets.data).astype(float).sum())

    test_loss /= len(test_loader)
    accuracy = 100. * correct / len(test_loader)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
        test_loss, correct, len(test_loader),
        accuracy))

    return accuracy


def train(train_loader, model, optimizer_model, epoch, epoch_losses, epoch_uncertainty, run_model, monitor_model,
          vis_model):
    current_time = datetime.datetime.now()
    print('\nEpoch: %d, Time: %s' % (epoch, current_time.strftime('%Y-%m-%d %H:%M:%S')))

    train_loss = 0
    prec_train_all = 0.

    for batch_idx, (inputs, targets, index) in enumerate(train_loader):
        jt.sync_all()
        model.train()

        outputs = model(inputs)
        loss = ce_loss(outputs, targets)
        optimizer_model.step(loss)

        prec_train = accuracy(outputs.data, targets.data)

        train_loss += (loss.item() * outputs.shape[0])
        prec_train_all += (prec_train.item() * outputs.shape[0])

        with jt.no_grad(no_fuse=1):
            unce = (nn.softmax(outputs, dim=1)).max()

            epoch_losses[index] = ce_loss(outputs, targets, reduce=False)
            epoch_uncertainty[index] = unce

        if (batch_idx + 1) % 50 == 0:
            print('Epoch: [%d/%d]\t'
                  'Iters: [%d/%d]\t'
                  'Loss: %.4f\t'
                  'Prec@1 %.2f' % (
                      (epoch + 1), args.epochs, batch_idx + 1, len(train_loader), (train_loss / (batch_idx + 1)),
                      prec_train))
        #打印时间戳
    starttime = datetime.datetime.now()
    print("epoch %d start time: %s", epoch, starttime.strftime('%Y-%m-%d %H:%M:%S'))                  
    monitor_model.track(epoch)
    logs = vis_model.show(epoch)

    # writer1.add_scalar('train_loss', train_loss, epoch)
    run_model.track(logs, context={'subset': 'train'})
    #打印时间戳
    endtime = datetime.datetime.now()
    print("epoch %d end time: %s", epoch, endtime.strftime('%Y-%m-%d %H:%M:%S'))
    print('epcho beihang tool 记录消耗时间：', (endtime - starttime).seconds)
    return (train_loss / len(train_loader.dataset)), (
                prec_train_all / len(train_loader.dataset)), epoch_losses, epoch_uncertainty


def extract_features(model, dataloader):
    features = []
    labels = []
    feature_extractor = copy.deepcopy(model)
    feature_extractor.linear = nn.Identity()
    with jt.no_grad(no_fuse=1):
        for inputs, targets, _ in dataloader:
            output = feature_extractor(inputs)
            features.append(output.reshape(output.shape[0], -1).numpy())
            labels.append(targets.numpy())
    return np.concatenate(features), np.concatenate(labels)


def get_output(model, dataloader):
    pre = jt.zeros(len(dataloader.dataset), args.num_classes)
    labels = jt.zeros(len(dataloader.dataset)).long()
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
args.num_classes = len(train_loader.classes)

# load model
model = build_model()
optimizer_model = jt.optim.SGD(model.parameters(), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)

current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
tensorboard_log_path = f'./tensorboard_log/{current_time}'

# writer1 = SummaryWriter(log_dir=(tensorboard_log_path+'/runs/epoch_model_informations'))
# writer2 = SummaryWriter(log_dir=(tensorboard_log_path+'/runs/epoch_weighting_informations'))
aim_server = os.getenv('TRACKSERVER')
print('aim_server:', aim_server)
#run_model = aim.Run(repo='aim://203.83.235.100:30058', system_tracking_interval=None, log_system_params=False)
run_model = aim.Run(repo=aim_server, system_tracking_interval=None, log_system_params=False)
run_model['id'] = os.getenv('RUNID')
run_model['hparams'] = {
    'learning_rate': args.lr,
    'batch_size': args.batch_size,
    'epochs': args.epochs,
    'momentum': args.momentum
}

def main():
    best_acc = 0
    # tensorboard_log_path = './'

    train_loss_all = []
    prec_train_all = []

    epoch_losses = jt.zeros(len(train_loader.dataset))
    epoch_uncertainty = jt.zeros(len(train_loader.dataset))

    out_file_list = []
    config_mmonitor_resnet = prepare_config()

    monitor_resnet = Monitor(model, config_mmonitor_resnet)
    vis_model = Visualization(monitor_resnet, project=config_mmonitor_resnet.keys(),
                              name=config_mmonitor_resnet.values())
    for epoch in range(args.epochs):
        adjust_learning_rate(optimizer_model, epoch)
        train_loss, prec_train, epoch_losses, epoch_uncertainty = train(train_loader, model, optimizer_model, epoch,
                                                                        epoch_losses, epoch_uncertainty, run_model,
                                                                        monitor_resnet, vis_model)

        # pre, labels = get_output(model, train_loader)

        # model.save(os.path.join('%s' % you_should_save_here, 'model_resnet18_%d.pkl' % (epoch)))

        # np.save(os.path.join('%s' % you_should_save_here, 'pre_%s.npy' % (epoch)), pre.data, allow_pickle=True,
        #         fix_imports=True)
        # np.save(os.path.join('%s' % you_should_save_here, 'labels_%s.npy' % (epoch)), labels.data, allow_pickle=True,
        #         fix_imports=True)
        print("track metric start time:", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        run_model.track(train_loss, name='Training Loss', epoch=epoch)

        run_model.track(prec_train, name='Training Accuracy', epoch=epoch)
        print("track metric end time:", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        # with jt.no_grad(no_fuse=1):
        #     model.eval()
        #     run_model.track(train_loss, name='Training Loss', epoch=epoch)
        #
        #     run_model.track(prec_train, name='Training Accuracy', epoch=epoch)
        #
        #     train_loss_all.append(train_loss)
        #     prec_train_all.append(prec_train)
        #
        #     plt.figure()
        #     plt.plot(train_loss_all, label='Model Loss')
        #     plt.xlabel('Epoch')
        #     plt.ylabel('Loss')
        #     plt.title('Loss vs Epoch')
        #     plt.legend()
        #     plt.grid(True)
        #
        #     plt.xticks(np.arange(len(train_loss_all)))
        #
        #     plot_filename = (
        #                 tensorboard_log_path + f'/runs/epoch_model_informations/loss_all_for_epoch_{epoch + 1}.png')
        #     # 创建文件夹
        #     os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
        #     plt.savefig(plot_filename)
        #     plt.close()
        #
        #     with Image.open(plot_filename) as img:
        #         img_array = np.array(img)  # 转换为 numpy 数组
        #         aim_image = aim.Image(img_array)  # 使用 Aim 提供的 Image 类型包装图像
        #
        #     # 使用 Aim 记录图像
        #     run_model.track(
        #         aim_image,
        #         name=f'Loss all for Epoch',
        #         epoch=epoch,
        #         context={'model': 'Loss all for Epoch'}
        #     )
        #
        #     out_file_list.append(plot_filename)
        #
        #     # 绘制模型的准确率变化图
        #     plt.figure()
        #     plt.plot(prec_train_all, label='Model Accuracy')
        #     plt.xlabel('Epoch')
        #     plt.ylabel('Accuracy')
        #     plt.title('Accuracy vs Epoch')
        #     plt.legend()
        #     plt.grid(True)
        #
        #     plt.xticks(np.arange(len(prec_train_all)))
        #
        #     plot_filename = (
        #             tensorboard_log_path + f'/runs/epoch_model_informations/accuracy_all_for_epoch_{epoch + 1}.png')
        #     os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
        #     plt.savefig(plot_filename)
        #     plt.close()
        #
        #     with Image.open(plot_filename) as img:
        #         img_array = np.array(img)  # 转换为 numpy 数组
        #         aim_image = aim.Image(img_array)  # 使用 Aim 提供的 Image 类型包装图像
        #
        #     # 使用 Aim 记录图像
        #     run_model.track(
        #         aim_image,
        #         name=f'Accuracy all for Epoch',
        #         epoch=epoch,
        #         context={'model': 'Accuracy all for Epoch'}
        #     )
        #
        #     out_file_list.append(plot_filename)
        #
        #     features, labels = extract_features(model, train_loader)
        #     tsne = TSNE(n_components=2, random_state=42)
        #     features_2d = tsne.fit_transform(features)
        #
        #     class_names = list(range(10))
        #     # 绘制 t-SNE 特征分布图，0 标识颜色深，1 标识颜色浅
        #     colors = plt.cm.tab10(np.linspace(0, 1, 10))
        #
        #     plt.figure(figsize=(10, 10))
        #     for class_idx in range(10):
        #         indices_0 = (labels == class_idx)
        #         # plt.scatter(features_2d[indices_0, 0], features_2d[indices_0, 1], label=f'{class_names[class_idx]} (dark)', cmap='tab10', alpha=0.9)
        #         # plt.scatter(features_2d[indices_1, 0], features_2d[indices_1, 1], label=f'{class_names[class_idx]} (light)', cmap='tab10', alpha=0.3)
        #         plt.scatter(features_2d[indices_0, 0], features_2d[indices_0, 1], color=colors[class_idx],
        #                     label=f'{class_names[class_idx]} (dark)', alpha=0.9)
        #
        #     plt.title('t-SNE Feature Distribution of ResNet32 on CIFAR-10')
        #     plt.xlabel('Dimension 1')
        #     plt.ylabel('Dimension 2')
        #     plt.grid(True)
        #     plt.legend(loc='best')
        #
        #     plot_filename = (
        #             tensorboard_log_path + f'/runs/epoch_model_informations/feature_distribution_for_epoch_{epoch + 1}.png')
        #     os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
        #     plt.savefig(plot_filename)
        #     plt.close()
        #
        #     with Image.open(plot_filename) as img:
        #         img_array = np.array(img)  # 转换为 numpy 数组
        #         aim_image = aim.Image(img_array)  # 使用 Aim 提供的 Image 类型包装图像
        #
        #     # 使用 Aim 记录图像
        #     run_model.track(
        #         aim_image,
        #         name=f'feature Distribution at Epoch',
        #         epoch=epoch,
        #         context={'model': 'feature Distribution at Epoch'}
        #     )
        #
        #     out_file_list.append(plot_filename)
        #
        #     # ##############################################################################################
        #     class_names = list(range(args.num_classes))
        #     all_preds = []
        #     all_labels = []
        #
        #     for inputs, labels, _ in train_loader:
        #         # print('inputs:', labels)
        #         outputs = model(inputs)
        #         preds, _ = outputs.argmax(1)
        #         all_preds.extend(preds.data)
        #         all_labels.extend(labels.data)
        #
        #     conf_matrix = confusion_matrix(all_labels, all_preds)
        #
        #     # 绘制混淆矩阵的热力图
        #     plt.figure(figsize=(10, 8))
        #     sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d',
        #                 xticklabels=class_names, yticklabels=class_names)
        #     plt.xlabel('Predicted Label')
        #     plt.ylabel('True Label')
        #     plt.title('Confusion Matrix for ResNet32 on CIFAR-10')
        #
        #     plot_filename = (
        #             tensorboard_log_path + f'/runs/epoch_model_informations/prediction_distribution_for_epoch_{epoch + 1}.png')
        #     os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
        #     plt.savefig(plot_filename)
        #     plt.close()
        #
        #     with Image.open(plot_filename) as img:
        #         img_array = np.array(img)  # 转换为 numpy 数组
        #         aim_image = aim.Image(img_array)  # 使用 Aim 提供的 Image 类型包装图像
        #
        #     # 使用 Aim 记录图像
        #     run_model.track(
        #         aim_image,
        #         name=f'Prediction Distribution at Epoch',
        #         epoch=epoch,
        #         context={'model': 'Prediction Distribution at Epoch'}
        #     )
        #
        #     plt.figure()
        #
        #     # print('epoch_losses:', type(epoch_losses), epoch_losses.shape, epoch_losses  )
        #     x1, y1 = np.histogram(epoch_losses.numpy(), bins=20, range=(0., epoch_losses.numpy().max().item()))
        #     plt.bar(np.arange(0., 1., 1 / 20), x1, width=0.01, facecolor='Blue')
        #
        #     plt.xlabel('Loss')
        #     plt.ylabel('Sample number')
        #     plt.title(f'Loss Distribution for Epoch')
        #     plt.legend()
        #     plt.grid()
        #
        #     plot_filename = (
        #             tensorboard_log_path + f'/runs/epoch_weighting_informations/loss_distribution_for_epoch_{epoch + 1}.png')
        #     os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
        #     plt.savefig(plot_filename)
        #     plt.close()
        #
        #     with Image.open(plot_filename) as img:
        #         img_array = np.array(img)  # 转换为 numpy 数组
        #         aim_image = aim.Image(img_array)  # 使用 Aim 提供的 Image 类型包装图像
        #
        #     # 使用 Aim 记录图像
        #     run_model.track(
        #         aim_image,
        #         name=f'Loss Distribution at Epoch',
        #         epoch=epoch,
        #         context={'vnet': 'Loss Distribution at Epoch'}
        #     )
        #
        #     out_file_list.append(plot_filename)
        #
        #     plt.figure()
        #
        #     x1, y1 = np.histogram(epoch_uncertainty.numpy(), bins=20, range=(0., epoch_uncertainty.max().item()))
        #     plt.bar(np.arange(0., 1., 1 / 20), x1, width=0.01, facecolor='Blue')
        #
        #     plt.xlabel('Uncertainty')
        #     plt.ylabel('Sample number')
        #     plt.title(f'Uncertainty Distribution for Epoch {epoch + 1}')
        #     plt.legend()
        #     plt.grid()
        #
        #     plot_filename = (
        #             tensorboard_log_path + f'/runs/epoch_weighting_informations/uncertainty_distribution_for_epoch_{epoch + 1}.png')
        #     os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
        #     plt.savefig(plot_filename)
        #     plt.close()
        #
        #     out_file_list.append(plot_filename)
    pre, labels = get_output(model, train_loader)

    # model.save(os.path.join('%s' % you_should_save_here, 'model_resnet18_%d.pkl' % (epoch)))

    # np.save(os.path.join('%s' % you_should_save_here, 'pre_%s.npy' % (epoch)), pre.data, allow_pickle=True,
    #             fix_imports=True)
    # np.save(os.path.join('%s' % you_should_save_here, 'labels_%s.npy' % (epoch)), labels.data, allow_pickle=True,
    #             fix_imports=True)
    # os.rename(os.path.join(you_should_save_here, f'pre_{epoch}.npy'), os.path.join(you_should_save_here, 'pre.pkl'))
    # os.rename(os.path.join(you_should_save_here, f'labels_{epoch}.npy'),
    #           os.path.join(you_should_save_here, 'labels.pkl'))

    # upload_output()


if __name__ == '__main__':
    main()