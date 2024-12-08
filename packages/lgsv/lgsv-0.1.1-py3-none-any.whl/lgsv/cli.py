"""协程"""

import asyncio

try:
    import luogu
    import setting
except ModuleNotFoundError:
    from lgsv import luogu, setting


async def main():
    """main 函数"""
    setting.parse_args()
    #    await luogu.fetch_csrf_token()
    if setting.global_config["cookie"] is not None:
        luogu.headers["Cookie"] = setting.global_config["cookie"]
    md_src = ""
    problems = []
    trainings = []
    if ("problem" in setting.target) & (setting.target["problem"] is not None):
        for p in setting.target["problem"]:
            problems.append(luogu.Problem(problem_id=p))
    if ("training" in setting.target) & (setting.target["training"] is not None):
        for t in setting.target["training"]:
            trainings.append(luogu.Training(training_id=t))
    async with asyncio.TaskGroup() as tg:
        for t in trainings:
            tg.create_task(t.fetch_resources())
        for p in problems:
            tg.create_task(p.fetch_resources())
    for p in problems:
        md_src += p.get_markdown(setting.global_config["order"])
    for t in trainings:
        md_src += t.get_markdown(setting.global_config["order"])
    with open(file=setting.global_config["output"], mode="w", encoding="utf-8") as f:
        f.write(md_src)


def run():
    """运行 main 函数"""
    asyncio.run(main())


if __name__ == "__main__":
    run()
