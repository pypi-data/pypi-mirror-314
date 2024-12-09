# MMonitor-jittor
本工具基于Jittor架构
A simple tool for observing the internal dynamics of neural networks

<h1 align="center"> Debug Tools </h1>

<p align="right">作者：北京航空航天大学复杂关键软件环境全国重点实验室、北京航空航天大学人工智能研究院

>这是一个检测网络训练过程中指标的轻量化工具，即插即用，也可以方便编写自己想要观察地指标
>
>工具的两个重要概念是模块和指标
>
>* 模块是指神经网络中的模块，例如Linear,Conv2d
>* 指标是指想要观察的指标，例如权重范数
>
>可以针对单个模块设置多个观察指标，同一个指标可以被多个模块使用
>
>工具的架构借鉴了软件工程中的三层架构：
>
>1. 数据准备：通过注册hook获取指标计算需要的数据
>2. 指标计算：对上述获得的数据进行二次加工
>3. 界面：用户与工具交互的接口
>
>此外，工具还将指标计算与数据展示解耦，使用者可以使用熟悉的可视化工具将计算得到的数据进行展示(本工具支持将指标保存为json文件以及event file文件保存在本地，可以使用本地提供的可视化，wandb以及使用aim进行可视化)

## 1. 使用方法

### 1.1 安装

```
// 下载源代码
git clone https://openi.pcl.ac.cn/wec/MMonitor-jittor.git
// 进入下载目录
cd 到下载目录，与setup.py文件同级
// 在安装前可以激活你想要安装的环境后运行安装代码
pip install -e ./  或者 python setup.py develop
```

除此之外，该工具已上传到Pypi库上，可以直接下载进行使用
```
//使用pip安装库
pip install MMonitor-jittor==1.0.0
```
此外，在当前包中有两个训练任务：
1. pypi_test/example_local：使用Model-MMonitor库对模型指标进行监控并且使用本地方法进行可视化，用户可以直接运行
2. pypi_test/example_tf：使用Model-MMonitor库对模型指标进行监控并且使用tensorboard可视化，用户可以直接运行
注： 由于wandb需要用户登录，因此无法进行展示
### 1.2 使用

```
# 以使用wandb为例，visualize类默认将指标保存在json文件保存在本地
from MMonitor.MMonitor.monitor import Monitor # 工具接口类
import wandb # 展示工具
from MMonitor.visualize import Visualization,LocalVisualization # 可视化类，其中Visualization默认将指标存储为josn文件并且保存在本地
"""
编写想要观察模块以及对应的观察指标
基本格式：{
	模块1：[[指标1,对应设置],[指标2,对应设置]],
	模块2：[[指标1,对应设置],[指标2,对应设置]]
}
观察模块写法支持  
1. 'fc1'：model中自己定义的模块名称 
2. 'Conv2d':pytorch中的模块类名称的字符串形式  
3. nn.BatchNorm2d：pytorch中的模块类名称

注意： 2，3方式是模糊搜索，会将所有满足条件的模块都进行观察，例如2是模型中所有的卷积模块都观察

观察指标写法支持 
注意：指标的对应设置（例如 linear(5, 2)）是指每隔多少step（minibatch）计算一次指标，linear是指线性（目前仅支持linear方式），5是指每隔5个step计算一次，2是指从第2 个step开始计数也就是第2、7、12...个step的时候进行计算
1. 'MeanTID':指标的类名称的字符串形式,这种形式默认对应设置是linear(0, 0)
2. ['MeanTID']同1
3. ['MeanTID', 'linear(5, 0)']：使用MeanTID指标，这个指标计算从0开始，每隔5个计算一次
由于不同的指标使用不同的Hook因此，在使用组合指标时只能使用相同Hook的指标：
ForwardInputExtension
    InputSndNorm & InputMean & InputStd
    MeanTID & VarTID -> 由于需要使用running_var属性，当前属性只有BatchNormalization才有，所有只有在BN上才能计算上述指标
ForwardOutputExtension:
    RankMe & LinearDeadNeuronNum
ForwardInputEigOfCovExtension
    InputCovStableRank & InputCovMaxEig & InputCovCondition & InputCovCondition20 & InputCovCondition50 & InputCovCondition80
BackwardOutputExtension
    OutputGradSndNorm 
WeightNorm -> 不需要Hook
""" 
config_mmonitor = {
        # nn.Conv2d: ['InputSndNorm']
        nn.BatchNorm2d: [['MeanTID', 'linear(5,0)'],'InputSndNorm']
    }
# prepare model
model = Model(config['w'], config['h'], config['class_num'])  # 假设 Model 已转换为 Jittor
opt = prepare_optimizer(model, config['lr'])
loss_fun = prepare_loss_func()
# 初始化 Monitor 和 Visualization
monitor = Monitor(model, config_mmonitor)
vis = Visualization(monitor, project=config_mmonitor.keys(), name=config_mmonitor.values())
for epoch in range(config['epoch']):
    y_hat = model(x)
    opt.set_input_into_param_group((x, y))
    loss = loss_fun(y_hat, y)
    # 监控和可视化更新
    opt.step(loss) 
    monitor.track(epoch)
    logs = vis.show(epoch)
    print(f"Epoch: {epoch}, Loss: {loss.item()}")
    run_model.track(logs,context={'subset':'train'})
print(monitor.get_output())
```

```
# 使用本地可视化
# 下述方法实现在本地调用指标json文件，使用LineFigure进行可视化
# 默认对当前模块的所有监控指标进行可视化
# 可以通过quantity_name来得到想要可视化的指标，quantity_name为None则可视化所有的指标
# 要求输入monitor
def show_local(monitor,quantity_name=None):
    project = 'BatchNorm2d'
    localvis = LocalVisualization(project=project)
    # quantity_name = 'InputSndNorm'
    localvis.show(monitor,quantity_name=quantity_name,project_name=project)
    print('The result has been saved locally')
```

```
# 使用aim实现可视化
# 需要提前在终端中进行 aim up以打开aim进行可视化
from MMonitor.mmonitor.monitor import Monitor
from MMonitor.visualize import Visualization
from aim import Run
config, config_mmonitor = prepare_config()
model = Model()
# init monitor
monitor = Monitor(model, config_mmonitor)
vis = Visualization(monitor,project=config_mmonitor.keys(),name=config_mmonitor.values())
aim_run = Run()
for epoch in range(config['epoch']):
    y_hat = model(x)
    opt.set_input_into_param_group((x, y))
    loss = loss_fun(y_hat, y)
    # 监控和可视化更新
    opt.step(loss) 
    monitor.track(epoch)
    logs = vis.show(epoch)
    print(f"Epoch: {epoch}, Loss: {loss.item()}")
    aim_run.track(logs,context={'subset':'train'})
print(monitor.get_output()) 
```

## 2. 支持的指标

>指标分为两类一类是singlestep，一类是multistep
>
>singlestep：是指指标计算在一个step内就可以完成的指标
>
>multistep：是指标计算需要多个step结果聚合在一起才能计算完成的指标

### 2.1 Single Step Quantity

|    Name                 |           描述                 |                                                       实现       |           Extension                    |                                                            cite  |
| ------------------- | -------------------------- | ------------------------------------------------------------ | ----------------------------- | -----------------------------------------------------------: |
| InputCovMaxEig      | 输入协方差矩阵的最大特征值 | 1. data = module.input.cov_matrix_eigs 2. Max Eig value      | ForwardInputEigOfCovExtension | [https://arxiv.org/pdf/2002.10801.pdf](https://arxiv.org/pdf/2207.12598.pdf) |
| InputCovStableRank  | 输入协方差矩阵的稳定秩     | 1. data = module.input.cov_matrix_eigs 2. Eigs sum / Max Eig | ForwardInputEigOfCovExtension |                                                              |
| InputCovCondition20 | 输入协方差矩阵的20%条件数  | 1. data = module.input.cov_matrix_eigs 2. top20% Eig values  | ForwardInputEigOfCovExtension | [https://arxiv.org/pdf/2002.10801.pdf](https://arxiv.org/pdf/2207.12598.pdf) |
| InputCovCondition50 | 输入协方差矩阵的50%条件数  | 1. data = module.input.cov_matrix_eigs 2. top50% Eig values  | ForwardInputEigOfCovExtension | [https://arxiv.org/pdf/2002.10801.pdf](https://arxiv.org/pdf/2207.12598.pdf) |
| InputCovCondition80 | 输入协方差矩阵的80%条件数  | 1. data = module.input.cov_matrix_eigs 2. top80% Eig values  | ForwardInputEigOfCovExtension | [https://arxiv.org/pdf/2002.10801.pdf](https://arxiv.org/pdf/2207.12598.pdf) |
| WeightNorm          | 权重二范数                 | 1. data = module.weight 2. norm(2)                           |                               |                                                              |
| InputMean           | 输入的每个channel的均值    | 1. data = module.input 2. mean                               | ForwardInputExtension         |                                                              |
| OutputGradSndNorm   | 输出梯度二范数             | 1. data = module.output_grad 2. norm(2)                      | BackwardOutputExtension       |                                                              |
| InputSndNorm        | 输出二范数                 | 1. data = module.input 2. norm(2)                            | ForwardInputExtension         |                                                              |
| InputStd | 输入的标准差 | 1. data = module.input 2.std | ForwardInputExtension | |
| InputNorm | 输入的二阶范数 | 1. data = module.input     2. norm(2) | ForwardInputExtension | |
| RankMe | 基于输出数据的奇异值分解（SVD）来计算一个与秩相关的度量值 | 1. data = module.output  2.svd | ForwardOutputExtension | |
| InputCovCondition | 输入协方差矩阵的条件数 | data = module.input.cov_matrix_eigs | ForwardInputEigOfCovExtension | |

### 2.2 Multi Step Quantity

| Name            | 描述                                       | 实现                                                         | Extension             | cite                             |
| --------------- | ------------------------------------------ | ------------------------------------------------------------ | --------------------- | -------------------------------- |
| MeanTID         | BN模块中batch的训练和推理时mean的差异      | 1.data = module.input 2.datas = [data.mean] 3.diff_data = [d-module.running_mean for d in datas] 4. stack diff_data 5. diff_data.norm(-1)/(sqrt(running_var).norm(-1)) 6. mean (思路详见论文公式) | ForwardInputExtension | https://arxiv.org/abs/2210.05153 |
| VarTID          | BN模块中batch的训练和推理时var的差异       | 1. data = input 2. datas = [sqrt(data.var(1))] 3. sigma = sqrt(running_var) 4. diff_data = [d-sigma for d in datas] 5. stack diff_data 6. diff_data(-1)/(sigma.norm(-1)) 7. mean(思路详见论文公式) | ForwardInputExtension | https://arxiv.org/abs/2210.05153 |
| WeightParamJump | 监控模型权重参数在不同时间步之间的跳变情况 | 1. data = module_weight 2. jump_num = [d * d_p < 0 for d, d_p in zip(self.cache[-1], self.cache[-2])] 3. sum(jump_num) |                       |                                  |

## 3. 开发者

### 3.1 Extension

#### 3.1.1 Forward Extension

| Name                          | 描述                       | 实现                                            |
| ----------------------------- | -------------------------- | ----------------------------------------------- |
| ForwardInputExtension         | 获取模块的输入             | 1.return input[0]                               |
| ForwardOutputExtension        | 获取模块的输出             | 1.return output[0]                              |
| ForwardInputEigOfCovExtension | 获取输入协方差矩阵的特征值 | 1.cal_cov_matrix(data) 2.retrun cal_eig(matrix) |

#### 3.1.2 Backward Extension

| Name                            | 描述                               | 实现                                                     |
| ------------------------------- | ---------------------------------- | -------------------------------------------------------- |
| BackwardInputExtension          | 获取模块输入的梯度                 | 1. return grad_input[0]                                  |
| BackwardOutputExtension         | 获取模块输出的梯度                 | 1. return grad_output[0]                                 |
| BackwardOutputEigOfCovExtension | 获取模块输出梯度协方差矩阵的特征值 | 1. cal_cov_matrix(grad_output) 2. return cal_eig(matrix) |

#### 3.1.3 utils

| Function       | 描述                 | 实现                              |
| -------------- | -------------------- | --------------------------------- |
| cal_cov_matrix | 计算数据的协方差矩阵 | return torch.cov(data.T)          |
| cal_eig        | 计算数据的特征值     | return torch.linalg.eigvals(data) |

### 3.2 Visualization

>Visualization主要包括：
>
>1. 本地可视化：Monitor类会将指标存储为json文件并且存在本地，可以使用LocalVisualization完成可视化
>2. 使用Wandb：在运行之前开始wandb
>3. 使用aim：提前打开aim之后直接运行相关文件，结果可以在aim可视化工具中实时显示指标变化

```
# 具体保存json为格式为：
output:
	BatchNorm2d(模块名称):
		bn_InputSndNorm(指标名称)：
			xxx.json
# 本地可视化图片的保存路径：
output:
	picture:
		bn_InputSndNorm_result.png
```




