from pydantic import BaseModel, Field
from typing import List, Dict, Union


class QuestionAnsweringSystemPrompt(BaseModel):
    system_prompt: str = Field(
        default="""You have to answer the user's question based on the information given below.
The information given below is correct -- it has ben sourced by an expert who knows more than you about this topic. Therefore, you must compose an answer which is in accordance with this information.
If possible, quote the information directly instead of rephrasing it. Respond in a way that answers the user's question completely.
Your answer must be direct and to the point.
Do NOT make up any facts.""",
        description="The main system instruction for the prompt.",
    )
    additional_instructions: List[str] = Field(
        default_factory=list, description="Additional instructions."
    )
    context_documents: List[str] = Field(
        default_factory=list, description="Context documents."
    )
    user_query: str = Field(default="", description="The user's query.")

    @property
    def compiled_system_prompt(self):
        return (
            f"{self.system_prompt}\n\n"
            + "\n\n".join(self.context_documents)
            + "\n- ".join(self.additional_instructions)
        )

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.compiled_system_prompt},
            {"role": "user", "content": self.user_query},
        ]

    def compile(self):
        return self.compiled_system_prompt


class SummarisationSystemPrompt(BaseModel):
    text_to_summarise: str
    n_sentences: int

    @property
    def system_prompt(self) -> str:
        return f"""Summarise the user's text into the smallest number of points possible. It must NOT be more than {str(self.n_sentences)} sentences.
Ignore the following from the text:
- If the text contains comments posted by people, ignore such comments.
- If it contains alerts about accepting cookies, information on cookies, etc. ignore such alerts.

Make sure to include the following in your summary:
- Ensure that your summary contains the technical points and language used in the original text.
- Include all the technical points discussed in the user's text.
"""

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.text_to_summarise},
        ]

    def compile(self):
        return self.system_prompt


class QueryRoutingSystemPrompt(BaseModel):
    system_prompt: str = (
        """Return the most suitable option that this request is related to.
Only return the name of the option, and nothing else, or your response will not be parsed correctly!"""
    )
    routes: List[str] = []
    query: str = ""

    @property
    def compiled_system_prompt(self):
        return f"{self.system_prompt}\n- " + "\n- ".join(self.routes)

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.compiled_system_prompt},
            {"role": "user", "content": self.query},
        ]

    def compile(self):
        return self.compiled_system_prompt


class TableDescriptionGenerationSystemPrompt(BaseModel):
    table_to_describe: str
    n_sentences: int

    @property
    def system_prompt(self) -> str:
        return f"""Describe this table in the smallest number of points possible. It must NOT be more than {str(self.n_sentences)} sentences.
In your description, mention the various columns and the type of data populated across rows.
Ensure that your summary contains the technical points and language used in the original text.
"""

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.table_to_describe},
        ]

    def compile(self):
        return self.system_prompt


class TableReformattingSystemPrompt(BaseModel):
    table_to_reformat: str

    @property
    def system_prompt(self) -> str:
        return f"""You are given a table in Markdown format.
There might have been some errors while parsing this table from a document.
Rewrite the table so that these errors are resolved.
- Carefully compare the column headers to the data in the respective columns. Ensure that they are meaningfully aligned.
Eg, if the column data contains years, but there is no column header for year, you can add this column header.

- Ensure that there are no empty columns or rows in your response.
- Ensure that none of the data in the given table is changed.

Your response must contain only the corrected table in Markdown text.
Ensure that your response does not contain anything else, or your response will not be parsed correctly!
"""

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.table_to_reformat},
        ]

    def compile(self):
        return self.system_prompt


class IssueCheckingSystemPrompt(BaseModel):
    question: str
    current_answer: str
    issue: str
    old_answer: str = ""

    additional_instructions: List[str] = Field(
        default_factory=list,
        description="",
    )

    system_prompt_if_old_answer_exists: str = Field(
        default="""You are given a question and two answers. The old answer is known to have a given issue.
Your task is to evaluate whether the currnet answer also has the issue.""",
        description="The main system instruction for the prompt.",
    )

    system_prompt_if_old_answer_does_not_exist: str = Field(
        default="""You are given a question and an answer, along with an issue that may or may not be present in the answer.
Your task is to evaluate whether the answer has the issue.""",
        description="The main system instruction for the prompt.",
    )

    answer_formatting_instructions: str = Field(
        default="""Carefully check whether the given current answer directly contains the issue -- indirect implications do not constitute an issue.
You will respond in a JSON format with the following fields:
- *issue_explanation*: First, you will give a 1-sentence explanation of what the user's mentioned issue actually is.
- *issue_reason*: Then, you will give a 1-sentence explanation of why the issue is present or not present in the current answer.
- *answer_contains_issue*: Then, you will respond with 'YES' if the issue exists in the CURRENT answer, or with 'NO' if the issue is not there. Only respond with 'YES' if the exact issue is 100% present in the current answer!

Here is an example response for the incorrect answer 'The boiling point of water is always 100°C at all places.':

{
"issue_explanation" : "The issue is that the boiling point of water is not 100°C everywhere -- it changes with the atmospheric pressure."
"issue_reason" : "The issue exists because the answer ignores the fact that boiling point of water depends on atmospheric pressure, and is only 100°C at standard atmospheric pressure."
"answer_contains_issue" : "YES",
}

You must make sure that you respond in the above JSON format, or your response will not be parsed correctly!
""",
        description="",
    )

    @property
    def compiled_system_prompt(self):
        if self.old_answer:
            prompt = f"""{self.system_prompt_if_old_answer_exists}
# Question
{self.question}

# Old Answer
{self.old_answer}

# Issue present in old answer
{self.issue}

# Current Answer
{self.current_answer}
"""

        else:
            prompt = f"""{self.system_prompt_if_old_answer_does_not_exist}
# Question
{self.question}

# Current Answer
{self.old_answer}

# Issue to be checked in answer
{self.issue}
"""
        return (
            f"{prompt}\n"
            + "\n\n".join(self.additional_instructions)
            + self.answer_formatting_instructions
        )

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.compiled_system_prompt},
        ]

    def compile(self):
        return self.compiled_system_prompt
