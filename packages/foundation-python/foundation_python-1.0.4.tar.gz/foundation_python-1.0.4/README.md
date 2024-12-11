# foundation-python
微服务架构项目的共享库-python版

## foundation-python.logger
日志模块，提供日志记录及日志管理功能
### logger_instance(name) -> Logger
获取日志实例  
__name__ 日志实例名称  

## foundation-python.queue.queue_manager
队列管理模块  
### queue.add_job(job_name, job_data, opts)
向队列添加任务  
__job_name__ 任务名称  
__job_data__ 任务数据  
__opts__ 任务配置项，参见BullMQ任务配置项说明  
### queue.start_worker(process_func)
执行任务消费客户端  
__process_func__ 任务处理方法  

## foundation-python.queue.escalation
向中心服务器发送任务回执  
### escalation.submit(task_id, status, data=None)
向中心服务器提交任务执行回执
__task_id__ 任务ID  
__status__ 任务执行结果，取值：success/fail  
__data__ 回执数据，默认为None  

## foundation-python.util.common
通用工具  
### common.short_uuid()
获取短UUID  
