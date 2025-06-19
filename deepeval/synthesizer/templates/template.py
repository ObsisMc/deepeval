from typing import Optional


class SynthesizerTemplate:

    @staticmethod
    def generate_text2sql_inputs(context, max_goldens_per_context):
        prompt = f"""Based on the given context, which is a SQL table schema, please generate a list of JSON objects with `input` keys.
        The `input` can either be a question or a statement that can be addressed by the given schema.

        **
        IMPORTANT: Please make sure to only return in JSON format, with the 'data' key as a list of JSON objects.
        You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting repetitive.

        Example context: [
            "Table: Customers",
            "Column: CustomerID, Type: INT, Description: Unique identifier for each customer",
            "Column: FirstName, Type: VARCHAR, Description: First name of the customer",
            "Column: LastName, Type: VARCHAR, Description: Last name of the customer",
            "Column: Email, Type: VARCHAR, Description: Email address of the customer",
            "Column: PhoneNumber, Type: VARCHAR, Description: Contact number of the customer",
            "Column: City, Type: VARCHAR, Description: City where the customer resides"
        ]
        Example max goldens per context: 2
        Example JSON:
        {{
            "data": [
                {{
                    "input": "Show me all the customers who live in New York.",
                }},
                {{
                    "input": "List the first and last names of all customers.",
                }}
            ]  
        }}

        You should NOT incorporate any prior knowledge you have and take each context at face value.
        You MUST include at least one statement as the input.
        `input` MUST be a STRING.
        You MUST TRY to generate {max_goldens_per_context} data points, unless the generated `input` is getting repetitive.
        **

        Max Goldens Per Context:
        {max_goldens_per_context}

        Context:
        {context}

        JSON:
        """
        return prompt

    @staticmethod
    def generate_text2sql_expected_output(input, context):
        return f"""Given the input, which may be a question or a statement addressable by the schema provided in the context,
        generate a JSON object with a key 'sql'. This key should contain the corresponding SQL statement that accurately and efficiently responds to the input.

        **
        IMPORTANT: The output must be in JSON format, with the 'sql' key only.

        Example Context: [
            "Table: Customers",
            "Column: CustomerID, Type: INT, Description: Unique identifier for each customer",
            "Column: FirstName, Type: VARCHAR, Description: First name of the customer",
            "Column: LastName, Type: VARCHAR, Description: Last name of the customer",
            "Column: Email, Type: VARCHAR, Description: Email address of the customer",
            "Column: PhoneNumber, Type: VARCHAR, Description: Contact number of the customer",
            "Column: City, Type: VARCHAR, Description: City where the customer resides"
        ]
        Example Input: "Show me all the customers who live in New York.",
        Example JSON: {{
            "sql": "SELECT * FROM Customers WHERE City = 'New York';"
        }}

        Context:
        {context}

        Input:
        {input}

        JSON:
        """

    def generate_synthetic_expected_output(
        input: str, context: str, expected_output_format: Optional[str]
    ):
        # important_section = (
        #     f"IMPORTANT: Please ensure that the generated response strictly adheres to the following format: {expected_output_format}, and make sure it is concise and straight to the point, using supporting information in context."
        #     if expected_output_format
        #     else "IMPORTANT: Please make sure to generate a response that is concise and straight to the point, and uses supporting information in context."
        # )

        # prompt = f"""Given the input, which may or may not be a question, generate a response using information presented in context.

        # **
        # {important_section}
        # **

        # Context:
        # {context}

        # Input:
        # {input}

        # Generated Response:
        # """

        format_section = (
            f"请确保生成的回应严格遵循以下格式：{expected_output_format}"
        )
        expected_output_style = (
            # "请确保生成的回应简明扼要，并充分利用上下文中的支持信息。"
            "请确保生成的回应充分利用上下文中的支持信息，利用的信息越多越好，回应需要具体和详细。"
        )

        important_section = (
            "重要提示：" + f"{format_section}，"
            if expected_output_format
            else "" + f"{expected_output_style}"
        )

        prompt = f"""根据输入内容（可能是一个问题，也可能不是），使用上下文中提供的信息生成回应。

        **
        {important_section}
        **

        上下文:
        {context}

        输入：
        {input}

        生成的回应：
        """

        return prompt

    @staticmethod
    def generate_synthetic_inputs(
        context: str,
        max_goldens_per_context: str,
        scenario: Optional[str],
        task: Optional[str],
        input_format: Optional[str],
    ):
        # input_format_section = (
        #     f"`input` MUST strictly adhere to the following format: {input_format}."
        #     if input_format
        #     else "`input` MUST be a STRING."
        # )

        # scenario_section = (
        #     f"`input`s MUST be relevant to this specific scenario: ```{scenario}``` (The scenario describes the circumstances under which the inputs are generated and the user’s intent in eliciting a response)."
        #     if scenario
        #     else ""
        # )

        # task_section = (
        #     f"`input`s MUST be framed in a way that evokes a response aligned with the following task: {task} (The task represents the goal or function the entity is expected to achieve when responding)."
        #     if task
        #     else ""
        # )

        # prompt = f"""I want you act as a copywriter. Based on the given context, which is list of strings, please generate a list of JSON objects with a `input` key.
        # The `input` can either be a question or a statement that can be addressed by the given context.

        # **
        # IMPORTANT: Please make sure to only return in JSON format, with the 'data' key as a list of JSON objects.
        # You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting repetitive.

        # Example context: ["Einstein won the Nobel Prize for his discovery of penicillin.", "Einstein won the Nobel Prize in 1968."]
        # Example max goldens per context: 2
        # Example JSON:
        # {{
        #     "data": [
        #         {{
        #             "input": "What was Einstein known for?"
        #         }},
        #         {{
        #             "input": "Einstein was a smart guy huh"
        #         }}
        #     ]
        # }}

        # You should NOT incorporate any prior knowledge you have and take each context at face value.
        # You MUST include at least one statement as the input.
        # {input_format_section}
        # {scenario_section}
        # {task_section}
        # You MUST TRY to generate {max_goldens_per_context} data points, unless the generated `input` is getting repetitive.
        # **

        # Max Goldens Per Context:
        # {max_goldens_per_context}

        # Context:
        # {context}

        # JSON:
        # """

        input_format_section = (
            f"`input` 必须严格遵循以下格式：{input_format}。"
            if input_format
            else "`input` 必须是字符串。"
        )

        scenario_section = (
            f"`input` 必须与此特定场景相关：```{scenario}```（场景描述了生成输入的环境和用户提问的意图）。"
            if scenario
            else ""
        )

        task_section = (
            f"`input` 必须以能够引发与以下任务一致回应的方式提出：{task}（任务代表实体在回应时应实现的目标或功能）。"
            if task
            else ""
        )

        prompt = f"""我希望你扮演一名文案撰写者。基于给定的上下文（一个字符串列表），请生成一个包含 `input` 键的 JSON 对象列表。
        `input` 可以是一个问题，也可以是一个陈述，只要能够由给定上下文回答即可。

        **
        重要提示：请确保只返回 JSON 格式，`data` 键对应一个 JSON 对象列表。
        你必须尽量生成 {max_goldens_per_context} 个数据点，除非 `input` 变得重复。

        示例上下文: ["爱因斯坦因发现青霉素获得了诺贝尔奖。", "爱因斯坦于1968年获得诺贝尔奖。"]
        示例最大金标数: 2
        示例 JSON:
        {{
            "data": [
                {{
                    "input": "爱因斯坦因为什么获得诺贝尔奖？"
                }},
                {{
                    "input": "爱因斯坦真是个聪明的人啊"
                }}
            ]  
        }}

        你不能使用任何先验知识，必须完全基于上下文生成内容。
        你必须至少包含一个陈述句作为 input。
        {input_format_section}
        {scenario_section}
        {task_section}
        你必须尽量生成 {max_goldens_per_context} 个数据点，除非生成的 `input` 变得重复。
        **

        最大金标数:
        {max_goldens_per_context}

        上下文:
        {context}

        JSON:
        """
        return prompt

    @staticmethod
    def rewrite_evolved_input(
        evolved_input: str,
        scenario: Optional[str] = None,
        task: Optional[str] = None,
        input_format: Optional[str] = None,
    ):

        # scenario_section = f'Scenario: "{scenario}"' if scenario else ""

        # task_section = f'Task: "{task}"' if task else ""

        # input_format_section = (
        #     f'Input Format: "{input_format}"' if input_format else ""
        # )

        # return f"""Given the evolved input, which may be a question or a statement, generate a JSON object with a key 'input'. This key should contain a statement or question that fits any provided scenario, aligns with the task's purpose, and matches the required input format (if specified).

        # **
        # IMPORTANT: Try to change the evolved input as little as possible. However, if the evolved input does not align with the provided scenario, task, or input format, it must ultimately be adjusted to fit these requirements. The output must be in JSON format, with the 'input' key only. If necessary, the evolved input should be rewritten to ensure it conforms to the scenario, task, and input format.
        # Use Chinese language for the response if the context is in Chinese, and English language for the `input` if the context is in English.

        # Example Evolved Input: "Is it okay to joke about someone losing their job in front of their coworkers if I'm just trying to lighten the mood?"
        # {f'Example Scenario: "{scenario}"' if scenario else ""}
        # {f'Example Task: "{task}"' if task else ""}
        # {f'Example Input Format: "{input_format}"' if input_format else ""}
        # Example JSON: {{
        #     "input": "How can I joke about someone losing their job without making the situation worse? Is it possible to use humor here without hurting anyone's feelings?"
        # }}

        # Evolved Input:
        # {evolved_input}

        # {scenario_section}
        # {task_section}
        # {input_format_section}

        # JSON:
        # """

        scenario_section = f'场景: "{scenario}"' if scenario else ""

        task_section = f'任务: "{task}"' if task else ""

        input_format_section = (
            f'输入格式: "{input_format}"' if input_format else ""
        )

        return f"""给定进化后的输入（可能是一个问题或陈述），请生成一个包含 'input' 键的 JSON 对象。该键的内容应为一个符合所提供场景、任务目标，并满足指定输入格式（如有）的陈述或问题。

        **
        重要提示：尽量少改动进化后的输入。但如果进化后的输入与场景、任务或输入格式不符，必须进行调整以满足这些要求。输出必须为 JSON 格式，仅包含 'input' 键。如有必要，应重写进化后的输入以确保其符合场景、任务和输入格式。
        如果上下文为中文，请用中文生成回应；如果上下文为英文，请用英文生成 `input`。

        示例进化输入: "在同事面前开玩笑说某人失业可以吗？我只是想活跃气氛。"
        {f'示例场景: "{scenario}"' if scenario else ""}
        {f'示例任务: "{task}"' if task else ""}
        {f'示例输入格式: "{input_format}"' if input_format else ""}
        示例 JSON: {{
            "input": "如何在不伤害他人感情的情况下，用幽默的方式谈论失业？"
        }}

        进化输入:
        {evolved_input}
        
        {scenario_section}
        {task_section}
        {input_format_section}

        JSON:
        """

    @staticmethod
    def rewrite_synthetic_inputs(context, original_query, feedback):
        # return f"""I want you to act as a query rewriter. Based on the provided context, original query, and feedback, generate a rewritten query that improves its clarity and answerability based on the feedback provided.

        # **
        # IMPORTANT: Please make sure to only return in JSON format, with the 'rewritten_input' key.
        # Use Chinese language for the response if the context is in Chinese, and English language for the `input` if the context is in English.

        # Example context: "The Golden Gate Bridge, located in San Francisco, was completed in 1937 and is known for its Art Deco design. It connects the city of San Francisco to Marin County and spans the Golden Gate Strait."
        # Example query: "When was the bridge completed?"
        # Example feedback: "The question asks about the completion of 'the bridge' but does not specify which bridge it refers to. There are many famous bridges, and without specifying the name, the question is too vague. To improve clarity, include the bridge's name."
        # Example JSON:
        # {{
        #     "rewritten_input": "When was the Golden Gate Bridge completed?"
        # }}

        # Example context: "The paper 'Advancements in Quantum Computing' by Dr. Alice Thompson discusses breakthroughs in quantum algorithms and was published in 2022. It explores the potential applications of quantum computing in cryptography and drug discovery."
        # Example query: "What applications of quantum computing are discussed in the paper?"
        # Example feedback: "The query is asking about applications of quantum computing but doesn't specify which paper is being referenced. Since many papers may discuss quantum computing, it would help to specify the title or author of the paper to improve clarity."
        # Example JSON:
        # {{
        #     "rewritten_input": "What applications of quantum computing are discussed in the paper 'Advancements in Quantum Computing' by Dr. Alice Thompson?"
        # }}

        # You should NOT incorporate any prior knowledge and should base the rewritten query only on the context and feedback provided.
        # The `rewritten_input` MUST be a STRING.
        # **

        # Context:
        # {context}

        # Query:
        # {original_query}

        # Feedback:
        # {feedback}

        # JSON:
        # """

        return f"""我希望你充当查询重写者。请根据提供的上下文、原始查询和反馈，生成一个重写后的查询，使其在反馈的基础上更加清晰且易于回答。

        **
        重要提示：请确保只返回 JSON 格式，且仅包含 'rewritten_input' 键。

        示例上下文: "金门大桥位于旧金山，于1937年建成，以其装饰艺术风格著称。它连接了旧金山市和马林县，横跨金门海峡。"
        示例查询: "大桥是什么时候建成的？"
        示例反馈: "问题提到“大桥”，但没有具体说明是哪座桥。著名的桥有很多，如果不指明名称，问题太模糊。为提高清晰度，请包含桥的名称。"
        示例 JSON:
        {{
            "rewritten_input": "金门大桥是什么时候建成的？"
        }}

        示例上下文: "论文《量子计算的进展》由Alice Thompson博士撰写，讨论了量子算法的突破，并于2022年发表。论文还探讨了量子计算在密码学和药物发现中的潜在应用。"
        示例查询: "论文中讨论了量子计算的哪些应用？"
        示例反馈: "该查询询问了量子计算的应用，但没有说明是哪篇论文。由于有许多论文可能涉及量子计算，建议明确论文标题或作者以提高清晰度。"
        示例 JSON:
        {{
            "rewritten_input": "《量子计算的进展》这篇论文中讨论了量子计算的哪些应用？"
        }}

        你不能使用任何先验知识，必须仅根据上下文和反馈重写查询。
        `rewritten_input` 必须是字符串。
        **

        上下文:
        {context}

        查询:
        {original_query}

        反馈:
        {feedback}

        JSON:
        """


######################################################################################################
##### Filter #########################################################################################
######################################################################################################


class FilterTemplate:

    @staticmethod
    def evaluate_synthetic_inputs(query):

        # return f"""Evaluate the provided synthetic query (which may be a question, task, or instruction) for clarity and answerability, assuming sufficient domain knowledge. Use the following criteria to guide your assessment:

        # 1. **Self-Containment**: Can the query be understood and completed without needing additional context or external references not provided within the query itself? It should be self-sufficient, meaning it doesn't depend on specific documents, tables, or prior knowledge not included in the query.
        # 2. **Clear Objective**: Does the query clearly convey its intent? It should specify what information, action, or response is being requested, allowing for a direct and appropriate answer or execution without ambiguity.

        # Based on these criteria, assign a score between 0 and 1, where:
        # - "1" means the query is clear, self-contained, and answerable.
        # - "0" means the query is vague, relies on external references, or is unclear in its intent.
        # - Scores between 0 and 1 indicate partial clarity or answerability, where the query meets some but not all of the criteria.

        # **
        # IMPORTANT: Please make sure to only return in JSON format, with the 'feedback' and 'score' keys.

        # Example query: "What technological innovations have changed communication over the last 20 years?"
        # Example JSON:
        # {{
        #     "feedback": "The query is somewhat vague as it asks about 'technological innovations' without specifying particular areas of communication (e.g., social media, messaging apps). It could be improved by narrowing the focus to a specific type of innovation or timeframe.",
        #     "score": 0.5
        # }}

        # Example query: "Explain the impact of renewable energy policies in Germany on local economies in 2021."
        # Example JSON:
        # {{
        #     "feedback": "This query clearly specifies the focus (renewable energy policies), the region (Germany), and the timeframe (2021). It is self-contained and answerable without needing additional context, making it clear and effective.",
        #     "score": 1.0
        # }}

        # Example query: "What are the main criticisms of the current education system in the United States?"
        # Example JSON:
        # {{
        #     "feedback": "The question is broad and lacks specificity, as 'main criticisms' could refer to various aspects (e.g., funding, curriculum, access). To improve clarity, it could specify which aspect of the education system is being critiqued.",
        #     "score": 0.4
        # }}

        # Example query: "Discuss the role of AI in healthcare, particularly in diagnostics, as noted in the last report."
        # Example JSON:
        # {{
        #     "feedback": "This question refers to 'the last report' without providing context or details, making it unclear and dependent on external information. It would be clearer if it provided some background on the report or defined what aspects of AI in diagnostics to address.",
        #     "score": 0.3
        # }}

        # The `feedback` MUST be a STRING and `score` must be a float from 0 to 1.
        # **

        # Query:
        # {query}

        # JSON:
        # """

        return f"""请你对给定的合成查询（可能是一个问题、任务或指令）进行清晰度和可回答性评估，假设有足够的领域知识。请参考以下标准：

        1. **自包含性**：该查询是否可以在不依赖额外上下文或未提供的外部信息的情况下被理解和完成？它应当是自足的，不依赖于特定文档、表格或未包含在查询中的先验知识。
        2. **目标明确**：该查询是否清楚地表达了意图？它应当明确说明所需的信息、操作或回应，使得可以直接、准确地回答或执行，无歧义。

        请根据上述标准，给出0到1之间的分数：
        - "1" 表示查询清晰、自包含且可回答。
        - "0" 表示查询模糊、依赖外部信息或意图不明确。
        - 介于0和1之间的分数表示查询部分满足标准，但并非完全清晰或可回答。

        **
        重要提示：请确保只返回JSON格式，包含 'feedback'（反馈）和 'score'（分数）两个键。

        示例查询: "过去20年中，哪些技术创新改变了通信方式？"
        示例JSON:
        {{
            "feedback": "该查询较为宽泛，‘技术创新’未具体说明通信领域的哪些方面（如社交媒体、消息应用等）。可通过聚焦某一类型创新或具体时间段提升清晰度。",
            "score": 0.5
        }}

        示例查询: "请解释2021年德国可再生能源政策对当地经济的影响。"
        示例JSON:
        {{
            "feedback": "该查询明确了关注点（可再生能源政策）、地区（德国）和时间（2021年），内容自包含且易于回答，清晰有效。",
            "score": 1.0
        }}

        示例查询: "美国现行教育体系主要有哪些批评？"
        示例JSON:
        {{
            "feedback": "该问题较为宽泛，‘主要批评’可能涉及多个方面（如资金、课程、机会等）。可通过指定具体批评领域提升清晰度。",
            "score": 0.4
        }}

        示例查询: "请讨论AI在医疗领域，尤其是诊断中的作用，如最近报告所述。"
        示例JSON:
        {{
            "feedback": "该问题提到‘最近的报告’，但未提供具体背景或细节，导致内容不清晰且依赖外部信息。若能补充报告背景或明确诊断方面内容会更清楚。",
            "score": 0.3
        }}

        `feedback` 必须为字符串，`score` 必须为0到1之间的浮点数。
        **

        查询:
        {query}

        JSON:
        """

    @staticmethod
    def evaluate_context(context):
        return f"""请你对给定的上下文进行如下四个维度的评估，并以有效的JSON格式返回结果，每个维度的分数范围为0（最低）到1（最高）：

        - **clarity（清晰度）**：评估信息是否清晰易懂。1表示内容表达清楚、易于理解，0表示内容模糊或难以理解。
        - **depth（深度）**：评估上下文是否有深入分析和独特见解。1表示内容分析透彻、富有启发性，0表示内容浅显、缺乏深度。
        - **structure（结构）**：评估内容组织是否合理、逻辑是否清晰。1表示结构严谨、条理清晰，0表示结构混乱、缺乏逻辑。
        - **relevance（相关性）**：评估内容与主题的相关程度。1表示内容紧扣主题，无无关信息，0表示内容偏离主题或包含无关内容。

        **
        重要提示：请确保只返回JSON格式，包含 'clarity'、'depth'、'structure' 和 'relevance' 四个键。

        示例上下文: "人工智能正在迅速改变各个行业，从医疗到金融，通过提升效率和优化决策。"
        示例JSON:
        {{
            "clarity": 1,
            "depth": 0.8,
            "structure": 0.9,
            "relevance": 1
        }}

        示例上下文: "猫是很棒的宠物。它们喜欢睡觉和玩耍。"
        示例JSON:
        {{
            "clarity": 0.5,
            "depth": 0.3,
            "structure": 0.4,
            "relevance": 0.5
        }}

        示例上下文: "全球化对本地文化的影响是复杂的，既有积极作用，也有消极影响。它可以促进文化交流，但也可能导致本地传统的消失。"
        示例JSON:
        {{
            "clarity": 0.9,
            "depth": 0.8,
            "structure": 0.9,
            "relevance": 1
        }}

        `clarity`、`depth`、`structure` 和 `relevance` 必须为0到1之间的浮点数。
        请确保你的JSON格式合法且正确。
        **

        上下文:
        {context}

        JSON:
        """


######################################################################################################
##### Approach similar to https://github.com/nlpxucan/WizardLM/blob/main/Evol_Instruct/depth.py ######
######################################################################################################


class EvolutionTemplate:

    # base_instruction = """I want you to act as an input rewriter.
    # Your object is the rewrite a given `input` and must be factually correct according to the supporting information in `Context`.
    # You MUST complicate the given `Input` using the following method:"""

    base_instruction = """我希望你充当输入重写者。
    你的目标是重写给定的 `输入`，并且必须严格依据 `Context`（上下文）中的支持信息，确保事实准确。
    你必须按照以下方法使给定的 `输入`（输入）变得更复杂："""

    base_constraints = ["`重写输入` 不得超过15个字，能缩写则缩写。"]

    @staticmethod
    def multi_context_evolution(input, context):

        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. `Input` should be rewritten to require readers to use information from all elements of `Context`.
        #     2. `Rewritten Input` must be fully answerable from information in `Context`.
        #     3. `Rewritten Input` should be concise and understandable by humans.
        #     4. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
        #     5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES

        #     Example context:
        #     ["Vaccines introduce a weakened or dead form of the pathogen to the human body.", "This exposure helps the immune system learn to recognize and fight the pathogen in the future."]
        #     Example input:
        #     How do vaccines work?
        #     Example rewritten input:
        #     How does the introduction of a modified pathogen prepare the immune system for future encounters?

        #     --------------------------

        #     Example context:
        #     ["Plants perform photosynthesis, using sunlight to convert carbon dioxide and water into glucose and oxygen.", "Chlorophyll in plant leaves absorbs sunlight, initiating the photosynthesis process.", "Oxygen is a by-product of the photosynthesis process and is released into the atmosphere."]
        #     Example input:
        #     Explain how plants produce oxygen.
        #     Example rewritten input:
        #     Considering chlorophyll's role in sunlight absorption and photosynthesis, how is oxygen produced and released by plants?

        #     --------------------------

        #     Example context:
        #     ["The gravitational pull of the moon on the Earth influences the tides.", "The position of the sun relative to the Earth and the moon also affects tidal patterns."]
        #     Example input:
        #     Tell me about high tides.
        #     Example rewritten input:
        #     Explain how the combined gravitational effects of the moon and the sun's relative positioning influence Earth's tidal phenomena.
        #     **

        #     Context:
        #     {context}
        #     Input:
        #     {input}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. `输入` 应重写为需要读者结合 `上下文` 中所有要素的信息才能作答。
            2. `重写输入` 必须完全可由 `上下文` 信息回答。
            3. `重写输入` 应简明易懂。
            4. `重写输入` 不得包含“根据上下文”或“依据上下文”等表述。

            **
            示例

            示例上下文:
            ["疫苗将减毒或灭活的病原体引入人体。", "这种暴露帮助免疫系统学会识别并抵御未来的病原体。"]
            示例输入:
            疫苗如何起作用？
            示例重写输入:
            减毒病原体如何帮助免疫系统抵御未来感染？

            --------------------------

            示例上下文:
            ["植物通过光合作用利用阳光将二氧化碳和水转化为葡萄糖和氧气。", "叶绿素吸收阳光，启动光合作用。", "氧气是光合作用的副产物并被释放到大气中。"]
            示例输入:
            植物如何产生氧气？
            示例重写输入:
            叶绿素吸收阳光后，植物如何产生并释放氧气？

            --------------------------

            示例上下文:
            ["月球对地球的引力影响潮汐。", "太阳相对于地球和月球的位置也影响潮汐模式。"]
            示例输入:
            什么是高潮？
            示例重写输入:
            月球和太阳的引力如何共同影响地球潮汐现象？
            **

            上下文:
            {context}
            输入:
            {input}
            重写输入:
            """
        )

    @staticmethod
    def reasoning_evolution(input, context):
        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. If `Input` can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning.
        #     2. `Rewritten Input` should require readers to make multiple logical connections or inferences.
        #     3. `Rewritten Input` should be concise and understandable by humans.
        #     4. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
        #     5. `Rewritten Input` must be fully answerable from information in `Context`.
        #     6. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES

        #     Example context:
        #     Chlorophyll allows plants to absorb energy from light, and this energy is used to convert carbon dioxide and water into glucose and oxygen, a process known as photosynthesis.
        #     Example input:
        #     Why are plants green?
        #     Example rewritten input:
        #     How does chlorophyll's role in absorbing light relate to plants' green color and their ability to produce glucose?

        #     --------------------------

        #     Example context:
        #     The greenhouse effect occurs when the Earth's atmosphere traps solar radiation, caused by gases such as carbon dioxide, methane, and water vapor. This process maintains the planet's temperature but can lead to increased global temperatures when exacerbated by human activities.
        #     Example input:
        #     What causes seasons to change?
        #     Example rewritten input:
        #     Given the trapping of solar radiation by atmospheric gases, explain how the enhanced activity impacts Earth's climate.

        #     --------------------------

        #     Example context:
        #     Economic theories suggest that market demand and supply determine prices, but government policies can also influence market dynamics through regulations, taxes, and subsidies.
        #     Example input:
        #     Identify the primary factors that determine the price of goods in a market.
        #     Example rewritten input:
        #     Examine how the interplay of market demand, supply dynamics, and government policy interventions collectively shapes the pricing mechanism of goods within a market ecosystem.
        #     **

        #     Context:
        #     {context}
        #     Input:
        #     {input}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. 如果 `输入` 只需简单思考即可解决，请将其重写为需要多步推理的问题。
            2. `重写输入` 应要求读者进行多步逻辑推理或推断。
            3. `重写输入` 应简明易懂。
            4. `重写输入` 不得包含“根据上下文”或“依据上下文”等表述。
            5. `重写输入` 必须完全可由 `上下文` 信息回答。

            **
            示例

            示例上下文:
            叶绿素使植物能够吸收光能，这些能量用于将二氧化碳和水转化为葡萄糖和氧气，这一过程称为光合作用。
            示例输入:
            为什么植物是绿色的？
            示例重写输入:
            叶绿素吸收光能如何影响植物颜色及其制造葡萄糖的能力？

            --------------------------

            示例上下文:
            温室效应是地球大气层捕获太阳辐射的自然过程，由二氧化碳、甲烷和水蒸气等气体引起。该过程维持了地球温度，但人类活动加剧后会导致全球变暖和气候变化。
            示例输入:
            季节变化的原因是什么？
            示例重写输入:
            大气气体捕获太阳辐射后，活动增强会如何影响地球气候？

            --------------------------

            示例上下文:
            经济理论认为市场需求和供给决定价格，但政府政策也可通过法规、税收和补贴影响市场动态。
            示例输入:
            市场中商品价格的主要决定因素有哪些？
            示例重写输入:
            市场需求、供给与政府政策如何共同影响商品定价机制？
            **

            上下文:
            {context}
            输入:
            {input}
            重写输入:
            """
        )

    @staticmethod
    def concretizing_evolution(input, context):
        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. Rewrite `Input` by replacing general concepts/inquiries with more specific ones.
        #     2. `Rewritten Input` should be concise and understandable by humans.
        #     3. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
        #     4. `Rewritten Input` must be fully answerable from information in `Context`.
        #     5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES
        #     Example context:
        #     Rainforests are home to over half of the world's plant and animal species, making them key to maintaining global biodiversity. The variety of life found in these ecosystems contributes to genetic diversity, which is crucial for adaptation and survival amid changing environmental conditions. This biodiversity also supports ecosystem resilience, enabling forests to recover from disturbances.
        #     The biodiversity in rainforests plays a significant role in human well-being, providing essential services such as air and water purification, disease control, and pollination of crops. Additionally, many medicines are derived from rainforest plants, highlighting the importance of these ecosystems for medical research and healthcare.
        #     Example input:
        #     Why is the biodiversity of rainforests important?
        #     Example rewritten input:
        #     How does the extensive biodiversity found in rainforests, encompassing over half of the world's plant and animal species, contribute to global biodiversity maintenance, and what role does this diversity play in enhancing ecosystem resilience, human health through disease control, crop pollination, and the development of medicines derived from rainforest plants?

        #     --------------------------

        #     Example context:
        #     Bees play a critical role in pollinating flowering plants, including many fruits and vegetables, contributing to the diversity of plant life and the production of crops. Their activity supports the growth of trees, flowers, and other plants, which serve as food and shelter for numerous animals, thus maintaining ecosystem balance.
        #     Beyond their impact on food crops, bees contribute to wild plant growth by pollinating a wide range of plants outside of agricultural settings. This pollination is vital for the reproduction of many plants, affecting entire ecosystems' health and sustainability.
        #     Example input:
        #     What is the role of bees in ecosystems?
        #     Example rewritten input:
        #     How do bees, through their pollination of flowering plants, including a multitude of fruits and vegetables, significantly influence the diversity of plant life and agricultural productivity, and in what ways do their activities extend beyond agricultural settings to support the growth of trees, flowers, and other plants, thereby providing essential resources for various animal species and contributing to the overall balance and sustainability of ecosystems?

        #     --------------------------

        #     Example context:
        #     Solar power generation relies on photovoltaic cells to convert sunlight into electricity. These cells are made of materials that exhibit the photovoltaic effect, which occurs when light photons are absorbed by the material, causing the generation of electrical current.
        #     Solar panels, composed of many photovoltaic cells, collect sunlight and convert it into electrical power. This energy can then be used directly or stored in batteries for later use, providing a renewable and sustainable source of power with minimal environmental impact.
        #     Example input:
        #     What are the principles behind solar power generation?
        #     Example rewritten input:
        #     How do photovoltaic cells work to convert sunlight into electrical power, and what role do solar panels play in this process, including energy storage for sustainable use?
        #     **

        #     Input:
        #     {input}
        #     Context:
        #     {context}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. 将 `输入` 中的泛泛概念/问题替换为更具体的内容。
            2. `重写输入` 应简明易懂。
            3. `重写输入` 不得包含“根据上下文”或“依据上下文”等表述。
            4. `重写输入` 必须完全可由 `上下文` 信息回答。
            **
            示例

            示例上下文:
            热带雨林拥有全球一半以上的动植物物种，是维持全球生物多样性的关键。这些生态系统中的丰富物种促进了遗传多样性，有助于适应和生存。生物多样性还增强了生态系统的恢复力，使森林能从干扰中恢复。
            热带雨林的生物多样性对人类健康也至关重要，提供空气净化、水净化、疾病控制和农作物授粉等服务。许多药物也源自雨林植物，凸显了其在医学研究和医疗中的重要性。
            示例输入:
            为什么热带雨林的生物多样性重要？
            示例重写输入:
            热带雨林丰富的物种如何促进全球生物多样性并增强生态系统恢复力？

            --------------------------

            示例上下文:
            蜜蜂在为开花植物授粉（包括许多水果和蔬菜）方面发挥着关键作用，促进了植物多样性和农作物产量。它们的活动支持了树木、花卉等植物的生长，为众多动物提供食物和栖息地，维持生态平衡。
            除了对农作物的影响外，蜜蜂还通过为野生植物授粉促进了自然生态系统的健康和可持续性。
            示例输入:
            蜜蜂在生态系统中的作用是什么？
            示例重写输入:
            蜜蜂授粉如何影响农作物产量和野生植物多样性，进而维持生态平衡？

            --------------------------

            示例上下文:
            太阳能发电依赖光伏电池将阳光转化为电能。这些电池材料具有光伏效应，吸收光子后产生电流。太阳能板由多个光伏电池组成，收集阳光并转化为电能，可直接使用或储存于电池中，实现可再生、可持续的能源供应，环境影响极小。
            示例输入:
            太阳能发电的原理是什么？
            示例重写输入:
            光伏电池如何将阳光转化为电能？太阳能板在储能中起什么作用？
            **

            输入:
            {input}
            上下文:
            {context}
            重写输入:
            """
        )

    @staticmethod
    def constrained_evolution(input, context):
        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. Rewrite `Input` by adding at least one more constraints/requirements.
        #     2. `Rewritten Input` must be fully answerable from information in `Context`.
        #     5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES
        #     Example context:
        #     Rainforests are home to over half of the world's plant and animal species, making them key to maintaining global biodiversity. The variety of life found in these ecosystems contributes to genetic diversity, which is crucial for adaptation and survival amid changing environmental conditions. This biodiversity also supports ecosystem resilience, enabling forests to recover from disturbances.
        #     The biodiversity in rainforests plays a significant role in human well-being, providing essential services such as air and water purification, disease control, and pollination of crops. Additionally, many medicines are derived from rainforest plants, highlighting the importance of these ecosystems for medical research and healthcare.
        #     Example input:
        #     Why is the biodiversity of rainforests important?
        #     Example rewritten input:
        #     How does the biodiversity of rainforests contribute to ecosystem resilience and recovery from disturbances, and in what ways does it impact human well-being through services such as air and water purification, disease control, and crop pollination?

        #     --------------------------

        #     Example context:
        #     Bees play a critical role in pollinating flowering plants, including many fruits and vegetables, contributing to the diversity of plant life and the production of crops. Their activity supports the growth of trees, flowers, and other plants, which serve as food and shelter for numerous animals, thus maintaining ecosystem balance.
        #     Beyond their impact on food crops, bees contribute to wild plant growth by pollinating a wide range of plants outside of agricultural settings. This pollination is vital for the reproduction of many plants, affecting entire ecosystems' health and sustainability.
        #     Example input:
        #     What is the role of bees in ecosystems?
        #     Example rewritten input:
        #     Considering the pivotal role bees play in pollinating both agricultural crops and wild plants, thereby contributing to the diversity of plant life and supporting the foundation of food chains, analyze how bees influence the growth and sustainability of various ecosystems.

        #     --------------------------

        #     Example context:
        #     Solar power generation relies on photovoltaic cells to convert sunlight into electricity. These cells are made of materials that exhibit the photovoltaic effect, which occurs when light photons are absorbed by the material, causing the generation of electrical current.
        #     Solar panels, composed of many photovoltaic cells, collect sunlight and convert it into electrical power. This energy can then be used directly or stored in batteries for later use, providing a renewable and sustainable source of power with minimal environmental impact.
        #     Example input:
        #     What are the principles behind solar power generation?
        #     Example rewritten input:
        #     Examine the significance of rainforest biodiversity in sustaining ecosystem resilience and providing essential services such as disease control and crop pollination, alongside its critical role in medical research and the development of new medicines. Consider the broader implications of biodiversity loss on global ecological balance and human health.
        #     **

        #     Context:
        #     {context}
        #     Input:
        #     {input}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. 在 `输入` 的基础上增加至少一个额外的约束或要求。
            2. `重写输入` 必须完全可由 `上下文` 信息回答。

            **
            示例

            示例上下文:
            热带雨林拥有全球一半以上的动植物物种，是维持全球生物多样性的关键。这些生态系统中的丰富物种促进了遗传多样性，有助于适应和生存。生物多样性还增强了生态系统的恢复力，使森林能从干扰中恢复。
            热带雨林的生物多样性对人类健康也至关重要，提供空气净化、水净化、疾病控制和农作物授粉等服务。许多药物也源自雨林植物，凸显了其在医学研究和医疗中的重要性。
            示例输入:
            为什么热带雨林的生物多样性重要？
            示例重写输入:
            热带雨林生物多样性如何促进生态恢复力，并在空气净化等方面影响人类健康？

            --------------------------

            示例上下文:
            蜜蜂在为开花植物授粉（包括许多水果和蔬菜）方面发挥着关键作用，促进了植物多样性和农作物产量。它们的活动支持了树木、花卉等植物的生长，为众多动物提供食物和栖息地，维持生态平衡。
            除了对农作物的影响外，蜜蜂还通过为野生植物授粉促进了自然生态系统的健康和可持续性。
            示例输入:
            蜜蜂在生态系统中的作用是什么？
            示例重写输入:
            蜜蜂授粉如何影响农作物产量和野生植物多样性，并维持生态平衡？

            --------------------------

            示例上下文:
            太阳能发电依赖光伏电池将阳光转化为电能。这些电池材料具有光伏效应，吸收光子后产生电流。太阳能板由多个光伏电池组成，收集阳光并转化为电能，可直接使用或储存于电池中，实现可再生、可持续的能源供应，环境影响极小。
            示例输入:
            太阳能发电的原理是什么？
            示例重写输入:
            光伏电池如何将阳光转化为电能？太阳能板在储能和环境保护中起什么作用？
            **

            上下文:
            {context}
            输入:
            {input}
            重写输入:
            """
        )

    @staticmethod
    def comparative_question_evolution(input, context):
        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. Rewrite `Input` to focus on comparing two or more entities, concepts, or processes.
        #     2. `Rewritten Input` should encourage a detailed comparison that highlights similarities and differences.
        #     3. `Rewritten Input` must be fully answerable from information in `Context`.
        #     4. `Rewritten Input` should be concise and understandable by humans.
        #     5. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
        #     6. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES
        #     Example context:
        #     "Water boils at 100°C (212°F) at sea level, but boiling point decreases with altitude due to lower atmospheric pressure. In contrast, alcohol boils at about 78°C (172°F)."
        #     Example input:
        #     What happens to water as it boils?
        #     Example rewritten input:
        #     How does the boiling point of water at sea level compare to that of alcohol, and how does altitude affect water's boiling point?

        #     --------------------------

        #     Example context:
        #     "Photosynthesis in plants involves converting carbon dioxide and water into glucose and oxygen, using sunlight. Cellular respiration in animals converts glucose and oxygen back into carbon dioxide and water, releasing energy."
        #     Example input:
        #     How do plants and animals process energy?
        #     Example rewritten input:
        #     Compare the processes of photosynthesis in plants and cellular respiration in animals, focusing on inputs and outputs of each process.

        #     --------------------------

        #     Example context:
        #     "The Renaissance was a period of significant cultural, artistic, and scientific rebirth that began in the 14th century, primarily in Italy. The Enlightenment, occurring mainly in the 18th century, centered around reason, science, and individualism, significantly influencing European thought."
        #     Example input:
        #     What was the Renaissance?
        #     Example rewritten input:
        #     Contrast the main focuses and impacts of the Renaissance and the Enlightenment on European thought and culture.

        #     --------------------------

        #     Context:
        #     {context}
        #     Input:
        #     {input}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. 将 `输入` 重写为聚焦对两个或多个实体、概念或过程进行比较的问题。
            2. `重写输入` 应鼓励详细比较，突出相似点和不同点。
            3. `重写输入` 必须完全可由 `上下文` 信息回答。
            4. `重写输入` 应简明易懂。
            5. `重写输入` 不得包含“根据上下文”或“依据上下文”等表述。

            **
            示例

            示例上下文:
            "水在海平面上沸点为100°C（212°F），但由于大气压降低，海拔升高时沸点会降低。相比之下，酒精的沸点约为78°C（172°F）。"
            示例输入:
            水沸腾时会发生什么？
            示例重写输入:
            水和酒精的沸点有何不同？海拔变化如何影响水的沸点？

            --------------------------

            示例上下文:
            "植物通过光合作用将二氧化碳和水转化为葡萄糖和氧气，利用阳光。动物的细胞呼吸则将葡萄糖和氧气转化为二氧化碳和水，并释放能量。"
            示例输入:
            植物和动物如何获取能量？
            示例重写输入:
            比较植物光合作用与动物细胞呼吸的输入输出有何异同？

            --------------------------

            示例上下文:
            "文艺复兴是14世纪起源于意大利的重要文化、艺术和科学复兴时期。启蒙运动主要发生在18世纪，强调理性、科学和个人主义，对欧洲思想产生深远影响。"
            示例输入:
            什么是文艺复兴？
            示例重写输入:
            对比文艺复兴与启蒙运动在欧洲思想和文化上的主要影响。

            --------------------------

            上下文:
            {context}
            输入:
            {input}
            重写输入:
            """
        )

    @staticmethod
    def hypothetical_scenario_evolution(input, context):
        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. Rewrite `Input` to include a hypothetical or speculative scenario that is relevant to the `Context`.
        #     2. `Rewritten Input` should encourage the reader to apply knowledge from the `Context` to imagine or deduce outcomes.
        #     3. `Rewritten Input` should be concise, clear, and understandable by humans.
        #     4. `Rewritten Input` should not contain phrases like 'based on the provided context' or 'according to the context'.
        #     5. `Rewritten Input` must be fully answerable from information in `Context`.
        #     6. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES

        #     Example context:
        #     The greenhouse effect is a natural process where the Earth's atmosphere traps some of the Sun's energy, warming the planet to a temperature that supports life. Human activities, particularly the emission of greenhouse gases like carbon dioxide and methane, have intensified this effect, leading to global warming and climate change.
        #     Example input:
        #     What are the consequences of the greenhouse effect?
        #     Example rewritten input:
        #     Imagine a world where greenhouse gas emissions were doubled overnight. How might this intensified greenhouse effect impact global climate patterns and ecosystems?

        #     --------------------------

        #     Example context:
        #     Antibiotics are drugs used to treat bacterial infections. They work by killing bacteria or preventing their growth. However, overuse and misuse of antibiotics have led to the development of antibiotic-resistant bacteria, which are harder to treat because they can withstand the drugs designed to kill them.
        #     Example input:
        #     How do antibiotics work?
        #     Example rewritten input:
        #     In a scenario where a new antibiotic-resistant superbug emerges, how would the principles of antibiotic action and resistance influence our approach to treatment?

        #     --------------------------

        #     Example context:
        #     Quantum computing relies on the principles of quantum mechanics to process information, utilizing quantum bits or qubits. These qubits can exist in multiple states simultaneously, allowing quantum computers to perform complex calculations much faster than traditional computers.
        #     Example input:
        #     What is quantum computing?
        #     Example rewritten input:
        #     Suppose a quantum computer was tasked with solving a problem that currently takes traditional computers centuries to solve. How might the unique capabilities of quantum computing change the outcome?
        #     **

        #     Context:
        #     {context}
        #     Input:
        #     {input}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. 将 `输入` 重写为包含与 `上下文` 相关的假设性或推测性场景。
            2. `重写输入` 应鼓励读者运用 `上下文` 中的知识进行想象或推断结果。
            3. `重写输入` 应简明、清晰且易于理解。
            4. `重写输入` 不得包含“根据上下文”或“依据上下文”等表述。
            5. `重写输入` 必须完全可由 `上下文` 信息回答。

            **
            示例

            示例上下文:
            温室效应是地球大气层捕获部分太阳能量的自然过程，使地球保持适宜生命的温度。人类活动，尤其是二氧化碳和甲烷等温室气体的排放，加剧了这一效应，导致全球变暖和气候变化。
            示例输入:
            温室效应有哪些后果？
            示例重写输入:
            假设温室气体排放量一夜之间翻倍，这种加剧的温室效应将如何影响全球气候模式和生态系统？

            --------------------------

            示例上下文:
            抗生素用于治疗细菌感染，通过杀死细菌或抑制其生长起作用。然而，抗生素的过度和滥用导致了耐药细菌的出现，这些细菌能抵抗原本能杀死它们的药物，治疗难度加大。
            示例输入:
            抗生素如何起作用？
            示例重写输入:
            如果出现一种新的耐药超级细菌，抗生素作用原理和耐药性会如何影响我们的治疗策略？

            --------------------------

            示例上下文:
            量子计算依赖于量子力学原理处理信息，利用量子比特（qubit）。量子比特可同时处于多种状态，使量子计算机能比传统计算机更快地完成复杂运算。
            示例输入:
            什么是量子计算？
            示例重写输入:
            假设量子计算机被用于解决传统计算机需数百年才能完成的问题，其独特能力将如何改变结果？
            **

            上下文:
            {context}
            输入:
            {input}
            重写输入:
            """
        )

    @staticmethod
    def in_breadth_evolution(input, context):
        # return (
        #     EvolutionTemplate.base_instruction
        #     + f"""
        #     1. Rewrite `Input` to create a brand new prompt.
        #     2. `Rewritten Input` should belong to the same domain as the `input` but be even more rare.
        #     3. `Rewritten Input` should be concise, clear, and understandable by humans.
        #     4. `Rewritten Input` should not contain phrases like 'based on the provided context' or 'according to the context'.
        #     5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

        #     **
        #     EXAMPLES

        #     Example context:
        #     Wearable technology has revolutionized personal health monitoring, allowing individuals to track vital signs and activity levels in real time.
        #     Example input:
        #     Explore the impact of wearable technology on personal health management.
        #     Example rewritten input:
        #     Delve into the development of implantable health devices and their potential to transform chronic disease management.

        #     --------------------------

        #     Example context:
        #     Quantum computing leverages the principles of quantum mechanics to process information, offering significant advancements over traditional computing methods.
        #     Example input:
        #     How is quantum computing different from traditional computing?
        #     Example rewritten input:
        #     Explore the potential of quantum cryptography in enhancing cybersecurity measures beyond current encryption standards

        #     --------------------------

        #     Example context:
        #     Virtual reality (VR) offers immersive learning experiences, transforming educational methodologies by providing interactive and engaging ways to acquire knowledge, especially in fields requiring practical skills.
        #     Example input:
        #     What impact does virtual reality (VR) have on education?
        #     Example rewritten input:
        #     Investigate the use of VR simulations in medical training to enhance practical skills and decision-making under pressure.
        #     **

        #     Context:
        #     {context}
        #     Input:
        #     {input}
        #     Rewritten Input:
        #     """
        # )

        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. 将 `输入` 重写为全新的提示语。
            2. `重写输入` 应与原 `输入` 属于同一领域，但更加罕见或冷门。
            3. `重写输入` 应简明、清晰且易于理解。
            4. `重写输入` 不得包含“根据上下文”或“依据上下文”等表述。

            **
            示例

            示例上下文:
            可穿戴技术彻底改变了个人健康监测，使人们能够实时追踪生命体征和活动水平。
            示例输入:
            探讨可穿戴技术对个人健康管理的影响。
            示例重写输入:
            植入式健康设备如何变革慢性病管理？

            --------------------------

            示例上下文:
            量子计算利用量子力学原理处理信息，相较传统计算方法有重大突破。
            示例输入:
            量子计算与传统计算有何不同？
            示例重写输入:
            量子密码学在提升网络安全方面有何潜力？

            --------------------------

            示例上下文:
            虚拟现实（VR）为学习带来沉浸式体验，尤其在需要实践技能的领域，改变了教育方式。
            示例输入:
            虚拟现实对教育有何影响？
            示例重写输入:
            VR仿真在医学培训中如何提升实操与决策能力？
            **

            上下文:
            {context}
            输入:
            {input}
            重写输入:
            """
        )
