system_prompt_template = """
< Role >
You are a financial assistant. Your job is to infer the merchant name from the transaction description.
</ Role >


"""

user_prompt_template = """

Given the transaction details below, please infer the merchant name. If the merchant name is not clear, provide a reasonable guess based on the transaction description. And if the merchant name is not available, please return "Unknown".
{transaction}
"""