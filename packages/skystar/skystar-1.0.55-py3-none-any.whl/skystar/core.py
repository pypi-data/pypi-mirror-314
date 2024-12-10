import weakref
import numpy as np
import contextlib
import skystar
try:
    import cupy
    array_types=(np.ndarray,cupy.ndarray)
    cupy.set_printoptions(precision=4)
except ImportError:
    array_types=(np.ndarray)
np.set_printoptions(precision=4)
TrainingMode = True
def Set_TrainingMode(mode: bool):
    if not isinstance(mode, bool):
        raise ValueError("Mode must be a boolean value (True or False).")
    global TrainingMode
    TrainingMode = mode
    if TrainingMode:
        print('========Setting mode to Training========')
    else:
        print('========Setting mode to Testing========')
def Get_TrainingMode():
    return TrainingMode

class Variable:
    '''--------
    data：输入数据，仅支持ndarray结构
    name:数据名称
    creator:创造输出的函数，该函数具有input和output，其中input==data
    grad：函数节点处的梯度
    generation:数据的辈分，用于反向传播时决定传播的顺序
    '''
    def __init__(self,data,name=None,):
        if data is not None:#如果数据不是ndarray则报错
            if not isinstance(data, array_types):
                raise TypeError('{} is not supposed'.format(type(data)))
        self.data=data
        self.name=name
        self.grad=None
        self.creator=None
        self.generation=0
    '''为每个数据连接函数并辈分'''
    def set_creator(self,func):
        self.creator=func
        self.generation=func.generation+1
    def cleangrad(self):#用以删除传递中间过程产生数据的梯度，释放内存
        self.grad=None
    def unchain(self):#删除数据与函数的链接
        self.creator=None
    def unchain_backward(self):#用于截断时间序列模型的连接（必须使用，不然模型的计算图无限堆叠）
        if self.creator is not None:
            funcs=[self.creator]
            while funcs:
                f=funcs.pop()
                for x in f.inputs:
                    if x.creator is not None:
                        funcs.append(x.creator)
                        x.unchain()
    '''用于把数据用图像展示，采用了matplotlib的接口,暂时取消使用'''
    def img_show(self):
        img=skystar.utils.splicing(self.data)
        img.show()
    def data_to_img_save(self,out_filename=None):
        if out_filename is None and self.name is None:
            out_filename='NoneName'
        img=skystar.utils.splicing(self.data)
        skystar.utils.save_img(img,out_filename)
    def to_cpu(self):
        if self.data is not None:
            self.data=skystar.cuda.as_numpy(self.data)

    def to_gpu(self):
        if self.data is not None:
            self.data=skystar.cuda.as_cupy(self.data)

    def to_float32(self,dtype=None):
        xp=skystar.cuda.get_array_module(self.data)
        dtype=xp.float32
        self.data=self.data.astype(dtype)

    def backward(self,retain_grad=False,create_graph=False):
        '''
        循环结构完成反向传播
        retain_grad:是否保留反向过程中产生的grad
        create_grad:是否启用高阶求导
        '''
        if Config.enable_backprop==False:#反向传播的开关，默认为Ture
            return None
        if self.grad is None:#初始化为Variable，便于计算导数的导数
            xp=skystar.cuda.get_array_module(self.data)
            self.grad=Variable(xp.ones_like(self.data,dtype=xp.float32))#这里把grad变成了
        funcs=[self.creator]
        while funcs:
            f=funcs.pop()
            dys = [output().grad for output in f.outputs]#list，元素为Variable
            with config_using('enable_backprop',create_graph):
                '''如果create_graph为False,在下面的计算中enable_backprop设置为False，由于运算符重载，那么下面的dxs = f.backward(*dys)将会
                调用Function.__call__方法，Function会根据enable_backprop禁止grad（Variable）链接函数f，由此梯度的反向传播无法进行。'''
                dxs = f.backward(*dys)  # 多个值返回元组，一个值返回单个元素，元素为Variable
                if not isinstance(dxs, tuple):
                    dxs = (dxs,)  # 单个值转化为元组，元素为Variable

                '''对每个input设置导数,如果输入两个数据是同一个数据，那么该数据的导数要叠加。这里
                同时会产生一个问题，如果对一个相同的变量反复反向传播，那么它的梯度会叠加，因此需要在
                每次传播后使用self.cleangrad()初始化梯度'''
                for x, dx in zip(f.inputs, dxs):  # x:Variable,dx:Variable
                    # if isinstance(dx, Variable):
                    #     dx.to_float32()
                    # else:
                    #     xp=skystar.cuda.get_array_module(dx)
                    #     dx=dx.astype(xp.float32)
                    if x.grad is None:
                        x.grad = dx
                    else:
                        x.grad = x.grad + dx
                    if x.creator is not None:
                        if x.creator not in funcs:  # 这里避免相同函数的backward被调用两次
                            funcs.append(x.creator)
                            funcs.sort(key=lambda x: x.generation)  # key为函数，指定取待排序元素的哪一项进行排序

                    if not retain_grad:  # 这里删除了中间过程产生的实例变量的grad，释放内存，由用户输入的数据grad的保存了下来
                        for y in f.outputs:
                            y().grad = None
    def reshape(self, *shape):
        if len(shape) == 1 and isinstance(shape[0], (tuple, list)):
            shape = shape[0]
        return reshape(self, shape)

    def transpose(self, *axes):
        if len(axes) == 0:
            axes = None
        elif len(axes) == 1:
            if isinstance(axes[0], (tuple, list) or axes[0] is None):
                axes = axes[0]
        return transpose(self, axes)

    def sum(self,axis=None,keepdims=False):
        return sum(self,axis,keepdims)
    '''静态方法，可以在调用时不加括号，比如x=Variable(np.array),可以直接实现x.shape查看数据形状'''
    @property
    def shape(self):
        return self.data.shape
    @property
    def ndim(self):
        return self.data.ndim
    @property
    def size(self):
        return self.data.size
    @property
    def dtype(self):
        return self.data.dtype
    @property
    def T(self):
        return transpose(self)

    __array_priority__=200#设置运算优先级，防止ndarray与Variable运算时，调用的是numpy的运算符
    def __len__(self):#实现Variable实例直接调用len函数
        return len(self.data)

    def __repr__(self):#改变Variable实例的打印方式
        if self.data is None:
            return 'Variable(None)'
        p=str(self.data).replace('\n','\n'+' '*9)
        return 'Variable('+p+')'

    def __getitem__(self, key):
        # 支持切片读取
        return self.data[key]

    def __setitem__(self, key, value):
        # 支持切片赋值
        self.data[key] = value
    '''重载运算符，实现Variable实例 加减乘除等方式,函数setup_variable也实现了该功能'''

class Parameter(Variable):#创建子集Parameter，用来存储模型的参数
    pass



class Function:
    '''----------
    inputs：#可以是多个数据，使用加减乘除时必须包含一个Variable实例
    self.inputs：#list，元素为Variable
    self.outputs：#list,元素为Variable实例,使用了弱引用，调用的话需要写为：元素（）
    generation：函数的辈分
    '''
    def __call__(self, *inputs):#添加*号，可以同时输入数据，将多个数据变为元组tuple
        inputs=[as_variable(x) for x in inputs]#将输入变为list,元素为Variable实例
        xs=[x.data for x in inputs]#list,元素为ndarray
        ys=self.forward(*xs)#使用*号解包，传向forward的inputs为元组或单个元素，元素为ndarray
        if not isinstance(ys,tuple):#如果不是元组进行处理
            ys=(ys,)
        outputs=[Variable(as_scalar(y)) for y in ys]#list，元素为Variable

        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self)

        self.inputs=inputs#list,元素为Variable实例
        self.outputs=[weakref.ref(output) for output in outputs]#这里添加了弱引用，减少内存占用，如果要调用列表元素x的值则需要使用x()

        if len(outputs)>1:
            return outputs
        else:
            return outputs[0]#Variable

    def forward(self,x):
        raise NotImplementedError()

    def backward(self,dout):
        raise NotImplementedError()

# =============================================================================
'''四则运算和常用运算'''
# =============================================================================
class Exp(Function):
    def forward(self,x):
        xp=skystar.cuda.get_array_module(x)
        y=xp.exp(x)
        return y
    def backward(self,dout):
        x=self.inputs[0]
        xp=skystar.cuda.get_array_module(dout)
        dout=xp.exp(x)*dout
        return dout
class Square(Function):
    def forward(self,x):
        y=x**2
        return y
    def backward(self,dout):
        dout=2*self.inputs[0]*dout
        return dout
class Add(Function):#加法,实现了广播功能
    def forward(self,x0,x1):
        self.x0_shape,self.x1_shape=x0.shape,x1.shape
        x1=as_scalar(x1)
        return x0+x1
    def backward(self,dout):
        dout0,dout1=dout,dout
        if self.x0_shape != self.x1_shape:
            dout0=skystar.utils.sum_to(dout0,self.x0_shape)
            dout1=skystar.utils.sum_to(dout1,self.x1_shape)
        return dout0,dout1
class Mul(Function):#乘法
    def forward(self,x0,x1):
        self.x0_shape,self.x1_shape=x0.shape,x1.shape
        x1=as_scalar(x1)
        return x0*x1
    def backward(self,dout):
        x0,x1=self.inputs
        if self.x0_shape != self.x1_shape:
            dout0=skystar.utils.sum_to(dout*x1,self.x0_shape)
            dout1=skystar.utils.sum_to(dout*x0,self.x1_shape)
        else:
            dout0 = dout * x1
            dout1 = dout * x0
        return dout0,dout1
class Neg(Function):#负数
    def forward(self,x):
        return -x
    def backward(self,dout):
        return -1*dout
class Sub(Function):#减法
    def forward(self,x0,x1):
        self.x0_shape,self.x1_shape=x0.shape,x1.shape
        return x0-x1
    def backward(self,dout):
        dout0=dout
        dout1=-dout
        if self.x0_shape != self.x1_shape:
            dout0=skystar.utils.sum_to(dout0,self.x0_shape)
            dout1=skystar.utils.sum_to(dout1,self.x1_shape)
        return dout0,dout1
class Div(Function):#除法
    def forward(self,x0,x1):
        self.x0_shape,self.x1_shape=x0.shape,x1.shape
        return x0/x1
    def backward(self,dout):
        x0,x1=self.inputs
        dout1=dout/x1
        dout2=-dout*x0/x1**2
        if self.x0_shape != self.x1_shape:
            dout1=skystar.utils.sum_to(dout1,self.x0_shape)
            dout2=skystar.utils.sum_to(dout2,self.x1_shape)
        return dout1,dout2
class Pow(Function):#幂函数
    def __init__(self,c):
        self.c=c
    def forward(self,x):
        return x**self.c
    def backward(self,dout):
        x=self.inputs[0]
        dout=dout*self.c*x**(self.c-1)
        return dout

def exp(x):
    func=Exp()
    return func(x)
def square(x):
    func=Square()
    return func(x)
def add(x0,x1):
    x1 = as_scalar(x1,skystar.cuda.get_array_module(x0.data))#转换为ndarray，实现Variable与int float的直接运算
    func=Add()
    return func(x0,x1)
def mul(x0,x1):
    x1 = as_scalar(x1,skystar.cuda.get_array_module(x0.data))
    func=Mul()
    return func(x0,x1)
def neg(x):
    func=Neg()
    return func(x)
def sub(x0,x1):
    x1=as_scalar(x1,skystar.cuda.get_array_module(x0.data))
    func=Sub()
    return func(x0,x1)
def rsub(x0,x1):
    x1=as_scalar(x1,skystar.cuda.get_array_module(x0.data))
    func=Sub()
    return func(x1,x0)
def div(x0,x1):
    x1=as_scalar(x1,skystar.cuda.get_array_module(x0.data))
    func=Div()
    return func(x0,x1)
def rdiv(x0,x1):
    x1=as_scalar(x1,skystar.cuda.get_array_module(x0.data))
    func=Div()
    return func(x1,x0)
def pow(x,c):
    func=Pow(c)
    return func(x)

# =============================================================================
'''辅助函数'''
# =============================================================================
class Config:#允许反向传播的开关
    enable_backprop=True
@contextlib.contextmanager
def config_using(name, value):
    oldvalue = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield
    finally:
        setattr(Config, name, oldvalue)
def no_grad():
    return config_using('enable_backprop', False)
def as_scalar(x,array_module=np):#把数据变为np.ndarray或者cp.ndarray
    if array_module.isscalar(x):
        return array_module.array(x,dtype=array_module.float32)#把数据转为float32
    return x
def as_variable(x):#把数据变为Variable实例
    if isinstance(x,Variable):
        return x
    return Variable(x)

def setup_variable():#重载运算符
    Variable.__mul__=mul
    Variable.__rmul__=mul
    Variable.__add__ = add
    Variable.__radd__ = add
    Variable.__sub__ = sub
    Variable.__rsub__ = rsub
    Variable.__neg__ = neg
    Variable.__truediv__=div
    Variable.__rtruediv__=rdiv
    Variable.__pow__=pow


# =============================================================================
'''一般函数'''
# =============================================================================
'''
x：函数前向传播的inputs，类型为tuple或单个元素，元素类型为Variable,经__call__方法在forward中变为ndarray
y：函数前向传播的outputs，这里输出类型为ndarray，但会在__call__方法中变为Variable
dout：Variabel实例
self.inputs：#list，元素为Variable
self.outputs：#list,元素为Variable实例,使用了弱引用，调用的话需要写为：元素（）
'''
class Sin(Function):
    def forward(self,x):
        xp=skystar.cuda.get_array_module(x)
        y=xp.sin(x)
        return y
    def backward(self,dout):
        x=self.inputs[0]
        dout=dout*cos(x)
        return dout
def sin(x):
    return Sin()(x)
class Cos(Function):
    def forward(self,x):
        xp=skystar.cuda.get_array_module(x)
        y=xp.cos(x)
        return y
    def backward(self,dout):
        x=self.inputs[0]
        dout=dout*-sin(x)
        return dout
def cos(x):
    return Cos()(x)
class Tanh(Function):
    def forward(self,x):
        xp=skystar.cuda.get_array_module(x)
        y=(xp.exp(x)-xp.exp(-x))/(xp.exp(x)+xp.exp(-x))
        return y
    def backward(self,dout):
        y=self.outputs[0]()
        dout=dout*(1-y*y)
        return dout
def tanh(x):
    return Tanh()(x)
class Reshape(Function):
    def forward(self,x,shape):
        self.x_shape=x.shape
        x=x.reshape(shape)
        return x
    def backward(self,dout):
        dout=dout.reshape(self.x_shape)
        return dout
def reshape(x,shape):
    if isinstance(shape,tuple):
        shape=np.asarray(shape)#这里用cupy无法
    shape = Variable(shape,name='shape')
    if x.shape==shape:
        return as_variable(x)
    return Reshape()(x,shape)
class Dot(Function):#点积
    def forward(self,x0,x1):
        xp=skystar.cuda.get_array_module(x0)
        y=xp.dot(x0,x1)
        return y
    def backward(self,dout):
        x0,x1=self.inputs
        dout0=dot(dout,x1.T)
        dout1=dot(x0.T,dout)
        return dout0,dout1
def dot(x0,x1):
    return Dot()(x0,x1)
class Matmul(Function):
    def forward(self,x0,x1):
        xp=skystar.cuda.get_array_module(x0)
        y=xp.matmul(x0,x1)
        return y
    def backward(self,dout):
        x0,x1=self.inputs
        dout0=matmul(dout,x1.data.swapaxes(-1,-2))#这里直接使用numpy或者cupy的swapaxes方法交换最后两轴
        dout1=matmul(x0.data.swapaxes(-1,-2),dout)
        return dout0,dout1
def matmul(x0,x1):
    return Matmul()(x0,x1)
class Transpose(Function):
    def __init__(self, axes=None):
        self.axes = axes
    def forward(self, x):
        y = x.transpose(self.axes)
        return y
    def backward(self, gy):
        if self.axes is None:
            return transpose(gy)
        # xp=skystar.cuda.get_array_module(gy)
        axes_len = len(self.axes)
        inv_axes = tuple(np.argsort([ax % axes_len for ax in self.axes]))
        return transpose(gy, inv_axes)
def transpose(x, axes=None):
    return Transpose(axes)(x)
class Swapaxis(Function):
    def __init__(self, axis1, axis2):
        self.axis1=axis1
        self.axis2=axis2
    def forward(self, x):
        xp=skystar.cuda.get_array_module(x)
        return xp.swapaxes(x,self.axis1,self.axis2)
    def backward(self, dout):
        dx=dout.data.swapaxes(self.axis1,self.axis2)
        dx=Variable(dx)
        return dx
def swapaxis(x, axis1, axis2):
    return Swapaxis(axis1, axis2)(x)
class Sum(Function):
    def __init__(self,axis,keepdims):
        self.axis=axis
        self.keepdims=keepdims
    def forward(self,x):
        self.x_shape=x.shape
        y=x.sum(axis=self.axis,keepdims=self.keepdims)
        return y
    def backward(self,dout):
        dout=skystar.utils.reshape_sum_backward(dout,self.x_shape,self.axis,self.keepdims)
        dout=broadcast_to(dout,self.x_shape)
        return dout
def sum(x,axis=None,keepdims=False):
    return Sum(axis,keepdims)(x)
class BroadcastTo(Function):#广播
    def forward(self,x, shape):
        xp=skystar.cuda.get_array_module(x)
        y=xp.broadcast_to(x,shape)
        return y
    def backward(self,dout):
        input= self.inputs[0]
        dout=sum_to(dout,input.shape)
        return dout
def broadcast_to(x,shape):
    # xp=skystar.cuda.get_array_module(x)
    shape=Variable(np.asarray(shape,dtype=np.int32),name='shape')
    if x.shape==shape:
        return as_variable(x)
    return BroadcastTo()(x,shape)


class Gather(Function):#用于嵌入层
    '''本函数的目的是对数组进行映射，映射有两种基本情况，即一个索引映射一个数据或一行数据
    1、映射一行：输入数据满足（batch,row,col）,索引满足（batch,index,1），axis=1，输出（batch,index,col）
    2、映射一个：输入数据满足（batch,col）,索引满足（batch，1），axis=1，输出（batch，1）
    '''
    def __init__(self, axis=1):
        self.axis = axis  # 默认沿着第 0 轴进行 gather 操作
    def forward(self, x, indices):
        xp=skystar.cuda.get_array_module(x)
        return xp.take_along_axis(x, indices, axis=self.axis)
    def backward(self, dout):
        '''暂时只适用于3D输入[batch,num1,dims],输出[batch,num2,1]，axis==1的情况'''
        xp = skystar.cuda.get_array_module(dout)  # 获取合适的库
        x,indices=self.inputs#Variable
        batch,num,dims=x.shape
        indices=indices.data.squeeze()
        dindices=Variable(xp.zeros_like(indices))
        onehot_indice=xp.eye(num)[indices].transpose(0,2,1)
        dx=xp.matmul(onehot_indice,dout.data)
        dx = Variable(dx)
        return dx,dindices
def gather(x, indices,axis=0):
    '''这里输入的x,indices都是Variable'''
    xp=skystar.cuda.get_array_module(x)
    if not isinstance(indices, Variable):
        indices=Variable(xp.asarray(indices,dtype=xp.int32))
    indices.data=indices.data.astype(xp.int32)
    return Gather(axis)(x, indices)

class SumTo(Function):#广播
    def __init__(self,shape):
        self.shape=shape
    def forward(self,x):
        self.x_shape=x.shape
        y=skystar.utils.sum_to(x,self.shape)
        return y
    def backward(self,dout):
        dout=broadcast_to(dout,self.x_shape)
        return dout
def sum_to(x,shape):
    if x.shape==shape:
        return as_variable(x)
    return SumTo(shape)(x)


class Concat(Function):
    def __init__(self, axis=1):
        self.axis = axis  # 指定拼接的维度轴
    def forward(self, x0, x1):
        # 获取所有输入的形状
        self.shapes = [x0.shape,x1.shape]
        xp=skystar.cuda.get_array_module(x0)
        # 在指定轴上拼接输入
        y = xp.concatenate((x0,x1), axis=self.axis)
        return y
    def backward(self, dout):
        # 根据 forward 时记录的形状信息，将 dout 拆分成与 x0 和 x1 形状相同的部分
        axis = self.axis
        xp=skystar.cuda.get_array_module(dout)
        x0_shape, x1_shape = self.shapes
        # 使用 split 将 dout 分割回 x0 和 x1 的大小
        dx0, dx1 = xp.split(dout.data, [x0_shape[axis]], axis=axis)
        return dx0, dx1
def concat(x0, x1, axis=0):
    return Concat(axis)(x0,x1)
class Slice(Function):
    def __init__(self):
        """
        初始化 Slice 函数。输入可谓list 也可为array
        :param starts: 一个一维张量，包含每个维度的起始点，如 [0, 0, 1, 1]。
        :param ends: 一个一维张量，包含每个维度的结束点，如 [1, 3, 3, 3]。
        :param axis: 一个一维张量，指定 starts 和 ends 应用的轴，如 [0, 1, 2, 3]。
        :param stride: 一个一维张量，指定每个轴的步长，如 [1, 1, 1, 1]。
        """
    def forward(self, x, starts, ends, axis, steps):
        """
        前向计算：对输入张量 x 进行切片。
        :param x: 输入张量。
        :return: 切片后的张量。
        """
        self.input_shape = x.shape  # 保存输入形状以便反向传播使用
        slices = [slice(None)] * len(x.shape)  # 初始化所有维度的切片为 ":" (None)
        for ax, start, end, step in zip(axis, starts, ends, steps):
            slices[ax] = slice(start, end, step)  # 按指定轴应用切片
        self.slices = slices  # 保存切片信息供反向传播使用
        y = x[tuple(slices)]  # 应用切片
        return y

    def backward(self, dout):
        """
        反向传播：将 dout 放回原来的形状，并在非切片部分填充 0。
        :param dout: 梯度流。
        :return: 对输入 x 的梯度。
        """
        xp = skystar.cuda.get_array_module(dout)
        dx = xp.zeros(self.input_shape, dtype=dout.dtype)  # 初始化为零的张量，与输入形状相同
        dx[tuple(self.slices)] = dout  # 将 dout 放回切片位置
        return dx

def my_slice(x, starts, ends, axis=None, steps=None):
    if axis is None:
        axis = list(range(len(starts)))  # 默认为所有轴
    if steps is None:
        steps = [1] * len(starts)  # 默认为步长为 1
    xp=skystar.cuda.get_array_module(x)
    starts = Variable(xp.array(starts,dtype=xp.int32),name='starts')
    ends = Variable(xp.array(ends,dtype=xp.int32),name='ends')
    steps = Variable(xp.array(steps,dtype=xp.int32),name='steps')
    axis = Variable(xp.array(axis,dtype=xp.int32),name='axis')
    return Slice()(x,starts, ends, axis, steps)
class Mean(Function):
    def __init__(self, axis=None, keepdims=True):
        self.axis = axis  # 支持传入 axis 参数
        self.keepdims=keepdims
    def forward(self, x):
        xp=skystar.cuda.get_array_module(x)
        self.original_x_shape = x.shape  # 保存原始输入形状
        self.x = x
        # 计算均值
        if self.axis is None:
            mean = xp.mean(x,keepdims=self.keepdims)  # 没有 axis 参数时，计算整个张量的均值
        else:
            mean= xp.mean(x, axis=self.axis, keepdims=self.keepdims)  # 按照指定的 axis 计算均值

        return mean

    def backward(self, dout):
        xp=skystar.cuda.get_array_module(dout)
        N = xp.prod(self.original_x_shape,dtype=xp.float32)  # 计算输入张量的总元素数
        axis_len = xp.prod(xp.array(self.original_x_shape)[self.axis],dtype=xp.float32) if self.axis is not None else N
        # 这里如何不是keepdims=True，则会报错，默认keepdims=True
        dx = xp.ones_like(self.x,dtype=xp.float32) * dout.data / axis_len  # 使用 np.ones_like 保证 dx 形状与 x 相同
        return dx
def my_mean(x, axis=None,keepdims=True):
    return Mean(axis,keepdims=keepdims)(x)


# =============================================================================
'''激活函数'''
# =============================================================================
class Sigmoid(Function):
    def forward(self,x):
        xp=skystar.cuda.get_array_module(x)
        y=1/(1+xp.exp(-x))
        return y
    def backward(self,dout):
        y=self.outputs[0]()
        dout = dout * y * (1 - y)
        return dout
def sigmoid(x):
    func=Sigmoid()
    return func(x)

class Relu(Function):
    def __init__(self):
        self.mask=None
    def forward(self,x):
        self.mask=(x<=0)#标记小于等于0的位置
        y=x.copy()#制作一个副本，避免x被改变
        y[self.mask]=0#小于等于0的值输出0，其它数值原样输出
        return y
    def backward(self,dout):
        dout.data[self.mask]=0
        return dout
def ReLU(x):
    return Relu()(x)

class Softmax(Function):#用于分类的激活函数,用于输出和输入相等
    def __init__(self,axis=None):
        if axis is None:
            self.axis=1
        else:
            self.axis=axis
    def forward(self,x):
        xp = skystar.utils.get_array_module(x)
        c = xp.max(x, axis=self.axis,keepdims=True)  # 求出最大值，避免数据溢出
        x_exp = xp.exp(x - c)  # 利用了广播，每一列的样本减去相同的值,溢出对策
        sum = xp.sum(x_exp, axis=self.axis,keepdims=True)
        y = x_exp / sum
        return y
    def backward(self,dout):
        y=self.outputs[0]()
        return dout*y*(1-y)
def softmax(x,axis=None):
    return Softmax(axis)(x)
# =============================================================================
'''loss函数'''
# =============================================================================
class SoftmaxCrossEntropyLoss(Function):#该函数结合了softmax和loss交叉熵误差函数，可以用作分类问题的最后一个激活函数
    '''y[batch,num_classes,H,W],[batch,index,num_classes],[batch,num_classes]
    t[batch,1,H,W],[batch,index],[batch,]'''
    def __init__(self,axis=None):
        if axis is not None:
            self.axis=axis
        else:self.axis=-1
    def forward(self,x0,x1):
        y=softmax(x0,axis=self.axis)
        loss=skystar.utils.cross_entropy_error(y.data,x1)
        return loss
    def backward(self,dout):#输出层反向传播输入导数1
        x0,t=self.inputs
        y=softmax(x0,axis=self.axis)#Variable
        if t.ndim==1:
            batch,num_class=y.shape
            t=Variable(skystar.utils.onehot(t.data,num_class))#Variable
            dout = (y - t) / batch
        elif t.ndim==2:
            batch, index, num_class = y.shape
            t=Variable(skystar.utils.onehot(t.data,num_class))#Variable
            dout = (y - t) / batch
        elif t.ndim==4:
            t.data=t.data.squeeze(axis=1)
            batch,num_class,H,W = y.shape
            t=Variable(skystar.utils.onehot(t.data,num_class).transpose(0,3,1,2))#Variable
            dout = (y - t) / batch
        else:
            raise ValueError('t.ndim==1 or t.ndim==2 or t.ndim==4')
        return dout
def softmaxwithloss(x,t,axis=None):
    '''t:np.array或者cp.array'''
    xp=skystar.utils.get_array_module(x)
    t=Variable(xp.asarray(t),name='Label')#给t添加名字
    return SoftmaxCrossEntropyLoss(axis)(x, t)

class MeanSquaredError(Function):
    "均方误差，多用于时序模型和一些需要精准预测结果的模型"
    def forward(self,x0,x1):
        diff=x0-x1
        y=(diff**2).sum()/len(diff)
        return y
    def backward(self,dout):
        x0,x1=self.inputs
        diff=x0-x1
        gx0=dout*diff*(2./len(diff))
        gx1=-gx0
        return gx0,gx1
def mean_squared_error(x0,x1):
    return MeanSquaredError()(x0,x1)

# =============================================================================
'''层函数'''
# =============================================================================
class Gemm(Function):
    '''
    也叫Affine层
    affine只进行二维矩阵的点积
    x：输入数据，如果输入数据是多维，则先变为2维
    W：参数权重，为二维的Varaible
    b，参数偏置，为一维的Variable
    transA: 是否对x进行转置
    transB：是否对权重w进行转置
    affine层可以单纯由dot与add实现
    '''
    def __init__(self,alpha=1,beta=1,transA=False,transB=False):
        self.alpha=alpha
        self.beta=beta
        self.transA=transA
        self.transB=transB
    def forward(self,x,W,b):
        xp=skystar.cuda.get_array_module(x)
        self.original_x_shape=x.shape
        if self.transA:
            x=x.T
        if self.transB:
            W=W.T
        if b is None:
            y = xp.dot(x, W) * self.alpha
        else:
            y = xp.dot(x, W) * self.alpha + b * self.beta
        return y
    def backward(self,dout):
        x,W,b=self.inputs
        dW=dot(x.T,dout) * self.alpha
        if b is not None:
            db = sum(dout, axis=0) * self.beta
        dout=dot(dout,W.T) * self.alpha
        dout=dout.reshape(*self.original_x_shape)
        if b is None:
            return dout,dW
        else:
            return dout,dW,db
def gemm(x, W, b, alpha=1, beta=1, transA=False, transB=False):
    return Gemm(alpha,beta,transA,transB)(x,W,b)
# =============================================================================
'''BatchNormalization'''
# =============================================================================
class BatchNormalization(Function):
    '''batchnorm 均值和方差是针对特征通道计算的，对于二维数据（N,B），特征通道是B，对于（N,C,H,W），特征通道是C,暂时不考虑3D数据'''
    def __init__(self,momentum=0.9,eps=1e-5):
        self.momentum=momentum#float
        self.xv=None#ndarray
        self.var=None#ndarray
        self.mean=None#ndarray

        self.test_mean=None#ndarray
        self.test_var=None#ndarray
        self.eps=eps
    def forward(self,x,gamma,beta,input_mean,input_var):
        xp=skystar.cuda.get_array_module(x)
        self.test_mean=input_mean
        self.test_var=input_var
        if Get_TrainingMode():#训练时用当前批量输入的均值方差
            if x.ndim==2:
                sum = xp.sum(x, axis=0)
                N = x.shape[0]
                mean = sum / N
                var = xp.sum((x - mean) ** 2, axis=0) / N
            elif x.ndim==4:
                sum = xp.sum(x, axis=(0,2,3))
                N=x.shape[0]*x.shape[2]*x.shape[3]
                mean = sum / N
                var = xp.sum((x - mean.reshape(mean.shape[0],1,1)) ** 2, axis=(0,2,3)) / N
            else:
                raise IndexError
            self.mean = mean
            self.var = var
            '''更新全局均值方差，用于测试用'''
            self.test_mean=self.momentum * self.test_mean + (1 - self.momentum) * self.mean
            self.test_var=self.momentum * self.test_var + (1 - self.momentum) * self.var
        else:#测试用全局均值方差
            mean=self.test_mean
            var=self.test_var
        if x.ndim==4:
            x=x.transpose(0,2,3,1)
            self.xv = ((x - mean) / xp.sqrt(var + self.eps))
            y = gamma * self.xv + beta

            self.xv=self.xv.transpose(0,3,1,2)
            y=y.transpose(0,3,1,2)
            return y
        if x.ndim==2:
            self.xv = (x - mean) / xp.sqrt(var + self.eps)
            y = gamma * self.xv + beta
            return y
    def backward(self,dout):
        xp=skystar.cuda.get_array_module(dout)
        x,gamma,beta=self.inputs[0],self.inputs[1],self.inputs[2]#Variable
        if x.ndim==2:
            N=dout.shape[0]#ndarray
            dgamma=sum(dout*self.xv,axis=0)#Variable
            dbeta=sum(dout,axis=0)#Variable
            dxv=dout*gamma#Variable
            dvar=sum(dxv*(x-self.mean)*xp.power(self.var + self.eps, -1.5)*(-0.5),axis=0)#Variable
            dmean=-1.0*sum(dxv,axis=0)/xp.sqrt(self.var+self.eps)+dvar*sum(-2.0*(x-self.mean),axis=0)/N#Variable
            dx=dxv/xp.sqrt(self.var+self.eps)+dvar*2*(x-self.mean)/N+dmean/N#Variable
        else:
            N=dout.shape[0]*dout.shape[2]*dout.shape[3]
            dgamma=sum(dout*self.xv,axis=(0,2,3))
            dbeta=sum(dout,axis=(0,2,3))

            dout=dout.transpose(0,2,3,1)
            x=x.transpose(0,2,3,1)
            dxv=dout*gamma

            dvar=sum(dxv*(x-self.mean)*xp.power(self.var + self.eps, -1.5)*(-0.5),axis=(0,1,2))#Variable
            dmean=-1.0*sum(dxv,axis=(0,1,2))/xp.sqrt(self.var+self.eps)+dvar*sum(-2.0*(x-self.mean),axis=(0,1,2))/N#Variable
            dx=dxv/xp.sqrt(self.var+self.eps)+dvar*2*(x-self.mean)/N+dmean/N#Variable
            dx=dx.transpose(0,3,1,2)
        return dx,dgamma,dbeta
# =============================================================================
'''LayerNorm'''
# =============================================================================
class LayerNorm(Function):
    '''只考虑了3D输入的情况（batch，seqlen，embedding_nidm）'''
    def __init__(self, epsilon=1e-5):
        self.epsilon = epsilon  # 防止除零的小常数

    def forward(self, x, gamma, beta):
        xp=skystar.cuda.get_array_module(x)
        # 计算均值和方差,对最后一维进行归一化，这里与batchnorm不同
        self.mean = xp.mean(x, axis=-1, keepdims=True)
        self.var = xp.var(x, axis=-1, keepdims=True)
        # 归一化
        self.x_hat = (x - self.mean) / xp.sqrt(self.var + self.epsilon)
        # 缩放和平移
        out = gamma * self.x_hat + beta
        return out

    def backward(self, dout):
        xp=skystar.cuda.get_array_module(dout)
        x,gamma,beta=self.inputs
        # 计算梯度
        Bath,N, D = dout.shape  # 输入的样本数量和特征维度
        dx_hat = dout * gamma  # 先计算归一化的梯度
        # 计算方差和均值的梯度
        dvar = xp.sum(dx_hat.data * (self.x_hat * -0.5) * xp.power(self.var + self.epsilon, -1.5), axis=-1, keepdims=True)
        dmean = xp.sum(dx_hat.data * -1 / xp.sqrt(self.var + self.epsilon), axis=-1, keepdims=True) + dvar * xp.mean(-2 * self.x_hat, axis=-1, keepdims=True)
        # 计算输入的梯度
        dx = Variable(dx_hat.data / xp.sqrt(self.var + self.epsilon) + dvar * 2 * self.x_hat / D + dmean / D)
        dgamma = Variable(xp.sum(dout.data * self.x_hat, axis=(0,1)))#
        dbeta = Variable(xp.sum(dout.data, axis=(0,1)))#
        # 返回梯度
        return dx, dgamma, dbeta
def layernorm(x,gamma,beta,epsilon=1e-5):
    return LayerNorm(epsilon)(x,gamma,beta)
# =============================================================================
'''Dropout'''
# =============================================================================
class Dropout(Function):
    '''训练时随机删除神经元节点，有效避免过拟合'''
    def __init__(self):
        self.mask=None
    def forward(self,x, ratio, training_mode):
        xp=skystar.cuda.get_array_module(x)
        if Get_TrainingMode():
            rand = xp.random.rand(*x.shape)  # 生成与x形状相同的随机数
            self.mask = (rand < ratio)
            y = x.copy()
            y[self.mask] = 0#被标记的神经元
            y/=(1.0 - ratio)#缩放处理，保持输出一致性
        else:
            y=x#测试时不对数据进行缩放，因为所有神经元都要输出
        return y
    def backward(self, dout):
         dout.data[self.mask]=0
         return dout
def dropout(x,ratio=0.5,training_mode=False):
    xp=skystar.cuda.get_array_module(x)
    ratio = Variable(xp.array([ratio],dtype=xp.float32),name='ratio')
    training_mode = Variable(xp.array([Get_TrainingMode()],dtype=xp.int32),name='training_mode')
    return Dropout()(x,ratio,training_mode)

# =============================================================================
'''卷积网络层函数'''
# =============================================================================
class Conv(Function):
    '''
    卷积层
    W：Variable,四维shape(out_channel,in_channel,FH,FW)
    B：Variable,一维shape(out_channel,)
    stride:步长
    pad:填充
    to_affine:如果下一层是affine层，将输出调整为矩阵，而不是四维张量
    '''
    def __init__(self,stride=1,pad=0):
        self.stride=stride#int
        self.pad=pad#int

        # 中间数据（backward时使用）
        self.col = None#array,shape(N*oh*ow, c*fh*fw)
        self.col_W = None#array,shape(c*fh*fw,FN)
    def forward(self,x,Weight,b):
        xp=skystar.cuda.get_array_module(x)
        N,C,H,W=x.shape
        FN,C,FH,FW=Weight.shape
        out_h=int((H+2*self.pad-FH)//self.stride+1)
        out_w=int((W+2*self.pad-FW)//self.stride+1)
        self.col=skystar.utils.im2col(x,FH,FW,stride=self.stride,pad=self.pad)#shape(N*oh*ow, c*fh*fw)
        self.col_W=Weight.reshape(FN,-1).T#shape(c*fh*fw,FN)

        out = xp.dot(self.col, self.col_W)
        if b is not None:
            out +=b  # shape(N*oh*ow,FN))
        out=out.reshape(N,out_h,out_w,-1).transpose(0,3,1,2)#shape(N,FN,oh,ow)
        return out

    def backward(self,dout):
        x,W,b=self.inputs[0],self.inputs[1],self.inputs[2]
        FN, C, FH, FW = W.shape
        dout = dout.transpose(0, 2, 3, 1).reshape(-1, FN)#(N*oh*ow,FN)

        dw = dot(self.col.T, dout).transpose(1,0).reshape(FN,C,FH,FW)

        dcol = dot(dout, self.col_W.T)#Variable(N*oh*ow,c*fh*fw)
        dx = skystar.utils.col2im(dcol.data, x.shape, FH, FW, self.stride, self.pad)#shape(N,C,H,W)
        dx=Variable(dx)
        if b is not None:
            db = sum(dout, axis=0)  # (FN,)
            return dx, dw, db
        return dx, dw
def convolution(x,W,b,stride=1,pad=0):
    return Conv(stride,pad)(x,W,b)

class ConvTranspose(Function):
    def __init__(self,stride=1,pad=0):
        self.stride=stride#int
        self.pad=pad#int

        # 中间数据（backward时使用）
        self.col = None#array,shape(N*oh*ow, c*fh*fw)
        self.col_W = None#array,shape(c*fh*fw,FN)
    def forward(self,x,Weight,b):
        '''2*2-->填充k=3,s=2,p=0--> 7*7-->标准卷积k=3,s=1,p=0-->5*5
        o' = s(i' - 1) + k-2p ，i'为原输入尺寸，o'为输出尺寸 （s=32,p=16,k=64）适合图像尺寸224*224卷积为7*7的网络反卷积'''
        '''注意，ConvTranspose的权重形状为（in_channels,out_channels,H,W）
        输入为（N,in_channels,H，W）,因此需要对权重进行轴的调换'''
        xp=skystar.cuda.get_array_module(x)#3*3
        Weight=Weight.transpose(1,0,2,3)
        out_channel, in_channel, FH, FW = Weight.shape
        reWeight = xp.flip(Weight, axis=(2, 3))  # 对权重矩阵进行翻转
        x=skystar.utils.transconv_pad(x,stride=self.stride,kernel_size=FH,pad=self.pad)#对x进行反卷积的填充，7*7
        N, C, H, W = x.shape
        self.shape=x.shape

        #标准卷积
        out_h=int((H+2*0-FH)//1+1)#5
        out_w=int((W+2*0-FW)//1+1)#5
        self.col=skystar.utils.im2col(x,FH,FW,stride=1,pad=0)#shape(N*oh*ow, c*fh*fw)
        self.col_W=reWeight.reshape(out_channel,-1).T#shape(c*fh*fw,out_channel)
        out=xp.dot(self.col, self.col_W)
        if b is not None:
            out += b  # shape(N*oh*ow,FN)
        out=out.reshape(N,out_h,out_w,-1).transpose(0,3,1,2)#shape(N,out_channel,oh,ow)5*5

        return out
    def backward(self,dout):
        x,W,b=self.inputs[0],self.inputs[1],self.inputs[2]#这里的W是Variable实例
        xp = skystar.cuda.get_array_module(x)
        W=W.transpose(1,0,2,3)
        out_channel, in_channel, FH, FW = W.shape
        dout = dout.transpose(0, 2, 3, 1).reshape(-1, out_channel)#(N*oh*ow,out_channel)

        dw = dot(self.col.T, dout).transpose(1, 0).reshape(out_channel, in_channel, FH, FW)#这里得到的梯度是翻转后W的梯度，因此梯度需要翻转
        dw = Variable(xp.flip(dw.data.transpose(1, 0, 2, 3), axis=(2, 3)))

        dcol = dot(dout, self.col_W.T)#Variable(N*oh*ow,c*fh*fw)
        dx = skystar.utils.col2im(dcol.data, self.shape, FH, FW, stride=1,pad=0)#shape(N,C,H,W)
        dx=Variable(skystar.utils.back_transcov_pad(dx,stride=self.stride,kernel_size=FH,pad=self.pad))
        if b is not None:
            db = sum(dout, axis=0)  # (FN,)
            return dx, dw, db
        return dx,dw
def transposed_convolution(x,weight,b,stride=1,pad=0):
    return ConvTranspose(stride=stride, pad=pad)(x, weight, b)

class MaxPool(Function):
    '''池化层，取池化窗口的最大值'''
    def __init__(self, pool_size, stride=1, pad=0):
        self.pool_size = pool_size#int
        self.stride = stride#int
        self.pad = pad#int
        self.arg_max = None#array

    def forward(self, x):
        xp=skystar.cuda.get_array_module(x)
        N, C, H, W = x.shape
        out_h = int(1 + (H - self.pool_size) / self.stride)
        out_w = int(1 + (W - self.pool_size) / self.stride)

        '''展开为二维数组'''
        col = skystar.utils.im2col(x, self.pool_size, self.pool_size, self.stride, self.pad)
        col = col.reshape(-1, self.pool_size * self.pool_size)

        '''计算最大值'''
        out = xp.max(col, axis=1)
        self.arg_max = xp.argmax(col, axis=1)  # 记录最大值的位置
        '''转换为四维数组'''
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

        return out

    def backward(self, dout):
        xp=skystar.cuda.get_array_module(dout)
        x = self.inputs[0]
        dout = dout.transpose(0, 2, 3, 1)

        pool_size = self.pool_size * self.pool_size
        dmax = xp.zeros((dout.size, pool_size))
        dmax[xp.arange(self.arg_max.size), self.arg_max.flatten()] = dout.data.flatten()
        dmax = dmax.reshape(dout.shape + (pool_size,))

        dcol = dmax.reshape(dmax.shape[0] * dmax.shape[1] * dmax.shape[2], -1)
        dx = skystar.utils.col2im(dcol, x.shape, self.pool_size, self.pool_size, self.stride, self.pad)
        dx = Variable(dx)
        return dx
def maxpool(x,pool_size,stride=1,pad=0):
    return MaxPool(pool_size,stride,pad)(x)

class AveragePool(Function):
    '''平均池化层，取池化窗口的平均值'''
    def __init__(self, pool_size, stride=1, pad=0):
        self.pool_size = pool_size  # int
        self.stride = stride  # int
        self.pad = pad  # int
    def forward(self, x):
        xp = skystar.cuda.get_array_module(x)
        N, C, H, W = x.shape
        out_h = int(1 + (H - self.pool_size) / self.stride)
        out_w = int(1 + (W - self.pool_size) / self.stride)
        # 展开为二维数组
        col = skystar.utils.im2col(x, self.pool_size, self.pool_size, self.stride, self.pad)
        col = col.reshape(-1, self.pool_size * self.pool_size)
        # 计算平均值
        out = xp.mean(col, axis=1)
        # 转换为四维数组
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)
        return out
    def backward(self, dout):
        x = self.inputs[0]
        dout = dout.transpose(0, 2, 3, 1)
        # 计算反向传播
        pool_size = self.pool_size * self.pool_size
        dmean = dout / pool_size
        dmean = Variable(dmean.data.repeat(pool_size, axis=-1))

        dcol = dmean.reshape(dmean.shape[0] * dmean.shape[1] * dmean.shape[2], -1)
        dx = skystar.utils.col2im(dcol.data, x.shape, self.pool_size, self.pool_size, self.stride, self.pad)
        dx = Variable(dx)
        return dx
def avgpool(x,pool_size,stride=1,pad=0):
    return AveragePool(pool_size,stride,pad)(x)

# class Gather(Function):
#     def __init__(self, shape):
#         pass
#     def forward(self, x):
#         pass

