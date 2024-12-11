from bullmq import Queue, Worker, Job
import redis.asyncio as redis
from redis import exceptions
from asyncio import Event
from ..util.common import load_config, config_value


class QueueManager:
    def __init__(self, queue_type='central', queue_name=''):
        """
        指定队列的管理器
        :param queue_type: 队列类型，取值：central 中央队列，local 本地队列
        :param queue_name: 队列名称
        """
        self.queue = None
        self.client = None
        self.config = load_config()
        self.queue_prefix = config_value(self.config, 'queue_common_setting.prefix', 'cv')
        self.retry_times = int(config_value(self.config, 'queue_common_setting.connect_failed_retry_times', '3'))

        if queue_name == '':
            raise ValueError(f"未设置队列名称")
        self.queue_name = queue_name

        if queue_type == 'central':
            self.client = redis.Redis(
                decode_responses=True,
                host = config_value(self.config, 'central_queue.host', ''),
                port = int(config_value(self.config, 'central_queue.port', '6379')),
                db = int(config_value(self.config, 'central_queue.db', '1'))
            )
        elif queue_type == 'local':
            self.client = redis.Redis(
                decode_responses=True,
                host=config_value(self.config, 'local_queue.host', ''),
                port=int(config_value(self.config, 'local_queue.port', '6379')),
                db=int(config_value(self.config, 'local_queue.db', '1'))
            )
        else:
            raise ValueError(f"{queue_type} 是无效的队列类型值，队列类型值包括：central, local")

        retry = 0
        connected = False
        while not connected and retry < self.retry_times:
            try:
                self.queue = Queue(queue_name, {
                    "connection": self.client,
                    "prefix": self.queue_prefix
                })
                connected = True
            except exceptions.ConnectionError:
                retry += 1
                if retry > self.retry_times:
                    print('连接消息队列失败')
                    raise Exception(f"连接 {queue_type} 消息队列失败，队列名称为：{queue_name}")

    async def add_job(self, job_name, job_data, opts=None):
        """
        向队列中添加新任务
        :param job_name: 任务名称
        :param job_data: 任务数据
        :param opts: 任务配置，参见BullMQ中任务配置项
        :return:
        """
        if opts is None:
            await self.queue.add(job_name, job_data)
        else:
            await self.queue.add(job_name, job_data, opts)

    async def receipt(self, task_id, status, result):
        """
        任务执行结果回执
        :param task_id: 任务ID
        :param status: 执行状态，success 成功，fail 失败
        :param result: 返回数据
        :return:
        """
        await self.queue.add('receipt', {"task_id": task_id, "status": status, **result})

    async def start_worker(self, func_process, func_completed=None, func_failed=None):
        """
        启动工作进程消费任务
        :return:
        """
        stop_event = Event()

        def on_completed(job, result):
            if func_completed is not None:
                func_completed(job, result)
            else:
                pass

        def on_failed(job, err):
            if func_failed is not None:
                func_failed(job, err)
            else:
                pass

        worker = Worker(self.queue_name, func_process, {
            "connection": self.client,
            "prefix": self.queue_prefix
        })

        worker.on("completed", on_completed)
        worker.on("failed", on_failed)

        try:
            await stop_event.wait()
        finally:
            await worker.close()
