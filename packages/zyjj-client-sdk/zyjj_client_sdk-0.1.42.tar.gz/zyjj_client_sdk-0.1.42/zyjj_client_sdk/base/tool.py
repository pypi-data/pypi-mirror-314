import re
import asyncio
import logging
from typing import Any, Callable

import math
import json5
import regex


# 毫秒时间戳格式化
def format_ms(ms: int):
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    # 格式化字符串
    return "{:02d}:{:02d}:{:02d},{:03d}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

# 字幕转字节
def subtitles2srt(subtitles: list) -> bytes:
    srt = ""
    for i, subtitle in enumerate(subtitles):
        srt += f"{i + 1}\n"
        srt += f"{format_ms(subtitle['start'])} --> {format_ms(subtitle['end'])}\n"
        srt += f"{subtitle['text']}\n\n"
    return srt.encode()


async def task_warp(async_fun, err_default, sleep: int = 0, **kwargs):
    try:
        # 延迟固定时间，避免并发太高
        await asyncio.sleep(sleep)
        # 触发我们的实际处理逻辑
        return await async_fun(**kwargs)
    except Exception as e:
        logging.error(f"task error {e}")
        if err_default is not None:
            return err_default
        raise e


async def _async_batch_run(
    data_list: list,
    split_size: int,
    async_fun,
    sleep: int,
    args: dict,
    err_default: dict,
    on_progress: Callable[[int], None] = None,
):
    num_segments = math.ceil(len(data_list) / split_size)
    logging.info(f"segments size {num_segments}")
    task_list = []
    res_list = []
    # 把任务全部添加到任务组里面去
    async with asyncio.TaskGroup() as tg:
        # 依次添加任务
        for i in range(num_segments):
            logging.info(f"start task {i}")
            start = i * split_size
            end = min((i + 1) * split_size, len(data_list))
            logging.info(f"args {args}")
            task_list.append(tg.create_task(task_warp(
                async_fun,
                err_default,
                sleep * i,
                data=data_list[start:end],
                **args
            )))
        # 等待所有任务完成
        for idx in range(num_segments):
            res_list.append(await task_list[idx])
            if on_progress is not None:
                on_progress(int((idx+1) / num_segments * 100))
    return res_list

def async_batch_run(
    data_list: list,
    async_func,
    split_size: int = 1,
    sleep: int = 1,
    args: dict = None,
    err_default: Any = None,
    on_progress: Callable[[int], None] = None,
) -> list:
    if args is None:
        args = {}
    return asyncio.run(_async_batch_run(data_list, split_size, async_func, sleep, args, err_default, on_progress))


def llm_json_parse(data: str) -> dict:
    # 我们使用json5来解析，避免大模型输出多余,
    try:
        return json5.loads(data)
    except Exception as e:
        logging.warning(f"parse json file err {e}")

    # 可以使用正则来匹配json里面的内容
    match = re.search(r'```json\s*([\s\S]*?)```', data)
    if match is not None:
        return llm_json_parse(match.group(1))

    # 最后直接匹配json格式
    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
    objects = pattern.findall(data)
    if len(objects) > 0:
        return llm_json_parse(objects[0])

    raise Exception('no json str found')
