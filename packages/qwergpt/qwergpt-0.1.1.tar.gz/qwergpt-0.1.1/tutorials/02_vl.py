import base64
import asyncio

from qwergpt.llms import TongyiLLM
from qwergpt.schema import Message


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


PROMPT: str = """
Convert the following PDF page to markdown.
Return only the markdown with no explanation text.
Do not exclude any content from the page.
"""

PROMPT: str = """
[图片上下文]
{context}
[/图片上下文]

[指令]
根据图片上下文，将图中的红框标注转换为操作步骤列表。
"""


async def main():
    model = 'qwen-vl-max' # qwen-vl-plus
    llm = TongyiLLM(model_name=model)

    image_path = "/Users/leopeng1995/workspaces/promptcn/qwergpt/competition/基于大模型的UBML智能低代码开发创新大赛/docs/training-certification/advance-dev/images/simple_query/simplyquery030.png"

    context = """
##### 2.5.3 针对枚举类型格式化

如果`订单类型``发货状态``订单状态`没有在QO上用表达式进行格式化枚举类型，在这里也可以进行枚举类型的格式化。

```
Stock/Deliver;备货发货/发货订单
Shipped/UnShipped;已发货/未发货
0/1/2/3;制单/提交审批/审批通过/审批不通过
```

以`发货状态`为例进行配置如下所示：
"""
    prompt = PROMPT.format(context=context)

    base64_image = encode_image(image_path)
    message = Message(
        role='user',
        content=[
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
    )

    messages = []
    messages.append(message)

    last_message = None 
    async for chunk in llm.acomplete_stream(messages, max_tokens=2000):
        print(chunk.content, end="", flush=True)
        if chunk.usage:
            last_message = chunk
    
    cost_per_thousand_tokens = 0.02  # 0.02元/千tokens
    if last_message and last_message.usage:
        prompt_tokens = last_message.usage['prompt_tokens']
        completion_tokens = last_message.usage['completion_tokens']
        total_tokens = last_message.usage['total_tokens']
        cost = (total_tokens / 1000) * cost_per_thousand_tokens
        print('\n')
        print(f"本次请求的prompt_tokens数为: {prompt_tokens}")
        print(f"本次请求的completion_tokens数为: {completion_tokens}")
        print(f"本次请求的total_tokens数为: {total_tokens}")
        print(f"本次请求的花费为: {cost:.6f} 元")


if __name__ == "__main__":
    asyncio.run(main())
