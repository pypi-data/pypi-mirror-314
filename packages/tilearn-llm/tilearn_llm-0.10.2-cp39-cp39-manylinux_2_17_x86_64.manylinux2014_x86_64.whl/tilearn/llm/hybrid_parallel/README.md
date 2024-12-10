## TILEARN HYBRID PARALLEL

### usage

```python3
### patch 
import tilearn.llm.hybrid_parallel


### model init
def mian():
    from colossalai.utils import get_current_device
    from colossalai.lazy import LazyInitContext
    init_context = LazyInitContext(default_device=get_current_device())
    #init_context = nullcontext()
    with init_context:
         model = LlamaForCausalLM.from_pretrained(model_args.model_name_or_path, ...)
```

### 2024.3.8 update

HF trainer已经不需要做任何修改, 采用以下方案解决data_iter问题

https://github.com/hpcaitech/ColossalAI/blob/v0.3.4/colossalai/booster/booster.py#L189

版本信息: colosslai==0.3.4, transformers==4.31.0(4.34.0大概率也可以), accelerate==0.21.0(0.24.1大概率也可以)

TODO List:

1) training_args已重载，梯度累积下huggingface training args中batchsize和colossal bs的对应关系需要梳理确认

2）模型初始化还需要手动添加LazyInitContext, 需要分析能否自动添加
```python3
    from colossalai.utils import get_current_device
    from colossalai.lazy import LazyInitContext
    init_context = LazyInitContext(default_device=get_current_device())
    #init_context = nullcontext()
    with init_context:
         model = LlamaForCausalLM.from_pretrained(model_args.model_name_or_path, ...)
```

3）pipeline return loss问题

4）save load问题

5）支持grad ckpt并测试

6）梳理并支持flashattn\RMS\RoPE等cuda kernel接入

7）验证其他transformer\accelerate版本支持情况

8）测试梯度累积

9）端到端验证模型效果

### 2024.3.7 update

1) training_args重载，关掉--deepspeed，传参bs到accelerate.config.bs。处理梯度累积参数mbs，当前是在config写死，且bs需要和启动脚本保持一致

2) 重载trainer.floating_point_ops函数，当前直接注释掉该函数
```python3
    ### boyyang
    #self.current_flos += float(self.floating_point_ops(inputs))
    self.current_flos += float(0.0)
```

3) trainer._inner_training_loop处理for循环dataloader迭代器问题，当前修改方法
```python3
    step = -1
    ### boyyang
    #for step, inputs in enumerate(epoch_iterator):
    inputs = epoch_iterator
    for step in range(len(inputs)):
```

4) save load问题

5) pipeline return loss
