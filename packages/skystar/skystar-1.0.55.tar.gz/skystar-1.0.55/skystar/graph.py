import numpy as np
import onnx
try:
    import cupy
    inttype = (cupy.int32, cupy.int64, np.int32, np.int64)
except ImportError:
    inttype = (np.int32, np.int64)
from onnx import TensorProto
from onnx.helper import (make_model, make_node, make_graph,
                         make_tensor, make_tensor_value_info)
from onnx.checker import check_model
from onnxsim import simplify

import skystar


class Node:
    def __init__(self, node, generation):
        self.generation = generation
        self.node = node


class Graph:
    def __init__(self):
        self.nodes = []
        self.inputs = []
        self.outputs = []
        self.initializers = []
        self.inputsinfo=[]
        self.last_func_id = None
        self.inputindex = 1

    def add_node(self, node):
        self.nodes.append(node)

    def set_inputs(self, inputs):
        self.inputs = inputs

    def set_outputs(self, outputs):
        self.outputs = outputs


# ===============================================================
# 将graph保存为onnx
# ===============================================================
def save_graph(graph, model_name, file_name='Example.onnx', ifsimplify=False, version=15):
    _graph = make_graph(
        nodes=graph.nodes,
        name=model_name,
        inputs=graph.inputs,
        outputs=graph.outputs,
        initializer=graph.initializers
    )
    onnx_model = make_model(graph=_graph, opset_imports=[onnx.helper.make_opsetid("", version)])  # 指定版本
    check_model(model=onnx_model)
    if ifsimplify:
        model_simplified, check = simplify(onnx_model)
        assert check, "Simplified ONNX model could not be validated"
        onnx.save(model_simplified, file_name)
        print('model saved and simplified successfully--Path:{}'.format(file_name))
    else:
        onnx.save_model(onnx_model, file_name)
        print('model saved successfully--Path:{}'.format(file_name))


# ===============================================================
# 载入和使用onnx模型,（放弃使用）
# ===============================================================
# def load_model(model_name):
#     session = ort.InferenceSession(model_name)
#     return session
#
#
# def model_predict(model, input):
#     input = input.astype(np.float32)
#     inputs = {"input": input}
#     outputs = model.run('output', inputs)
#     return outputs


# ===============================================================
# 创建graph
# ===============================================================
def create_graph(output):
    graph = Graph()
    if isinstance(output, tuple):
        output = output[0]
    fs = [output.creator]
    graph.last_func_id = id(fs[0])
    graph.outputs.append(make_tensor_value_info('Output', TensorProto.FLOAT, list(output.shape)))
    nodes = []
    while fs:
        f = fs.pop()
        generate_initializers(f, graph)  # 先生成initializers
        graph_node = _graph_node(f, graph)  # 后生成nodes
        if graph_node.node not in nodes:
            graph.nodes.append(graph_node)
            nodes.append(graph_node.node)
            for input in f.inputs:
                if input.creator is not None and input.creator not in fs:
                    fs.append(input.creator)
    graph.nodes = sorted(graph.nodes, key=lambda x: x.generation)
    graph.nodes = [i.node for i in graph.nodes]
    return graph


# ===============================================================
# 根据f的名称调用相应的create函数创建节点
# ===============================================================
def _graph_node(f, graph):
    name = f.__class__.__name__
    if name in function_nodes:
        return function_nodes[name](f, graph)
    else:
        print(f'Warning:No such function node: {name}')


# ===============================================================
# 生成输入输出的名称,输入输出是core的Function函数里前向传播的输入输出，大多数create函数可用
# ===============================================================
def generate_names(f, graph):
    inputs_name = []
    if f.generation != 0:
        for input in f.inputs:
            if input.data is not None:  # 考虑到卷积层的b可能为None
                if input.name is not None:
                    inputs_name.append(input.name + f'_{id(input)}')
                else:
                    inputs_name.append(f'mid_{id(input)}')
    else:
        for input in f.inputs:
            if id(input) in graph.inputsinfo:
                continue
            else:
                if input.name is None:
                    index = len(graph.inputs)+1
                    node = make_tensor_value_info(f'Input{index}', TensorProto.FLOAT, list(input.shape))
                    graph.inputs.append(node)
                    inputs_name.append(f'Input{index}')
                else:
                    inputs_name.append(input.name + f'_{id(input)}')

    outputs_name = [f'mid_{id(f.outputs[0]())}']
    if id(f) == graph.last_func_id:
        outputs_name = ['Output']
    return inputs_name, outputs_name

# ===============================================================
# 根据函数的输入生成initializers，如果函数的输入具有name，则将其纳入initializers
# ===============================================================
def generate_initializers(f, graph):
    for input in f.inputs:
        if input.name is None and input.generation==0 and f.generation != 0:
            input.name = 'mid'#这里是对那些除开输入数据外，首次出现的数据进行命名
        if input.name is not None and input.data is not None:
            if isinstance(input.data, inttype):
                datatype=TensorProto.INT32
            else:
                datatype=TensorProto.FLOAT
            initializer = make_tensor(input.name + f'_{id(input)}', datatype, list(input.shape), input.data)
            if initializer not in graph.initializers:
                graph.initializers.append(initializer)

# ===============================================================
# create函数，创建Function节点
# ===============================================================
def create_node(f, graph, node_type, **kwargs):
    inputs_name, outputs_name = generate_names(f, graph)
    node = make_node(
        node_type,
        inputs_name,
        outputs_name,
        name=f'{node_type}_node_{id(f)}',
        **kwargs
    )
    return Node(node, f.generation)


# ===============================================================
# 创建Function节点
# ===============================================================
def create_add_node(f, graph):
    return create_node(f, graph, 'Add')
def create_matmul_node(f, graph):
    return create_node(f, graph, 'MatMul')
def create_multify_node(f, graph):
    return create_node(f, graph, 'Mul')
def create_relu_node(f, graph):
    return create_node(f, graph, 'Relu')
def create_maxpool_node(f, graph):
    return create_node(f, graph, 'MaxPool', kernel_shape=[f.pool_size, f.pool_size],
                       strides=[f.stride, f.stride], pads=[0, 0, f.pad, f.pad])
def create_AveragePool_node(f, graph):
    return create_node(f, graph, 'AveragePool', kernel_shape=[f.pool_size, f.pool_size],
                       strides=[f.stride, f.stride], pads=[0, 0, f.pad, f.pad])
def create_dropout_node(f, graph):
    return create_node(f, graph, 'Dropout')
def create_conv_node(f, graph):
    '''需要初始化权重'''
    return create_node(f, graph, 'Conv',
                       kernel_shape=[f.inputs[1].shape[2], f.inputs[1].shape[3]],
                       strides=[f.stride, f.stride],
                       pads=[f.pad, f.pad, f.pad, f.pad], )
def create_convtranspose_node(f, graph):
    return create_node(f, graph, 'ConvTranspose', kernel_shape=[f.inputs[1].shape[2], f.inputs[1].shape[3]],
                       strides=[f.stride, f.stride],
                       pads=[f.pad, f.pad, f.pad, f.pad],
                       output_shape=list(f.outputs[0]().shape), )
def create_softmaxcrossentropyloss_node(f, graph):
    '''该节点需要特殊设置'''
    inputs_name = [f'mid_{id(f.inputs[0])}', 'Label']
    graph.inputs.append(make_tensor_value_info('Label', TensorProto.INT64, list(f.inputs[1].shape)))
    f.inputs[1].name = 'Label'
    outputs_name = 'Output'
    node = make_node(
        'SoftmaxCrossEntropyLoss',
        inputs_name,
        outputs_name,
        reduction='mean',
        ignore_index=None,
        name=f'SoftmaxCrossEntropyLoss_node_{id(f)}'
    )
    return Node(node, f.generation)
def create_batchNormalization_node(f, graph):
    return create_node(f, graph, 'BatchNormalization', epsilon=1e-5, momentum=f.momentum, training_mode=0)
def create_sigmoid_node(f, graph):
    return create_node(f, graph, 'Sigmoid')
def create_softmax_node(f, graph):
    return create_node(f, graph, 'Softmax', axis=1)
def create_meansquarederror_node(f, graph):
    pass
def create_gemm_node(f, graph):
    return create_node(f, graph, 'Gemm', alpha=f.alpha, beta=f.beta, transA=f.transA, transB=f.transB)
def create_Concat_node(f, graph):
    return create_node(f, graph, 'Concat', axis=f.axis)
def create_Reshape_node(f, graph):
    return create_node(f,graph,'Reshape')
def create_slice_node(f, graph):
    return create_node(f, graph, 'Slice')
def create_tanh_node(f, graph):
    return create_node(f, graph, 'Tanh')
def create_dic_node(f, graph):
    return create_node(f, graph, 'Div')
def create_transpose_node(f, graph):#矩阵转置,不完善
    return create_node(f, graph, 'Transpose',perm=None)
def create_reducemean_node(f, graph):
    pass
def create_layernorm_node(f,graph):
    return create_node(f, graph, 'LayerNormalization', axis=-1, epsilon=1e-5)
def create_gather_node(f, graph):
    return create_node(f, graph, 'Gather', axis=f.axis)
def create_expand_node(f, graph):
    return create_node(f, graph, 'Expand')
def create_sub_node(f,graph):
    return create_node(f, graph, 'Sub')
# 使用节点的字典
function_nodes = {
    'SoftmaxCrossEntropyLoss': create_softmaxcrossentropyloss_node,
    'Sigmoid': create_sigmoid_node,
    'Relu': create_relu_node,
    'Softmax': create_softmax_node,
    'MeanSquaredError': create_meansquarederror_node,
    'Gemm': create_gemm_node,
    'BatchNormalization': create_batchNormalization_node,
    'Dropout': create_dropout_node,
    'Conv': create_conv_node,
    'ConvTranspose': create_convtranspose_node,
    'MaxPool': create_maxpool_node,
    'Add': create_add_node,
    'Mul': create_multify_node,
    'Dot': create_matmul_node,
    "Concat": create_Concat_node,
    "AveragePool": create_AveragePool_node,
    'Reshape': create_Reshape_node,
    'Slice': create_slice_node,
    'Tanh': create_tanh_node,
    'Div': create_dic_node,
    'Transpose': create_transpose_node,
    'LayerNorm': create_layernorm_node,
    'BroadcastTo':create_expand_node,
    'Gather':create_gather_node,
    'Matmul':create_matmul_node,
    'Sub': create_sub_node,
}
