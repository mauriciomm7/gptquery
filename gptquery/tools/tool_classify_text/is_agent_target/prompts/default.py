# C:\gitprojects\gptquery\gptquery\tools\tool_classify_text\classify_snippets\prompts\default.py
"""
EXTRACTOR prompt template for classifying sentences.

Each prompt template must clearly document its expected parameters - this is the 
"contract" between user and tool.
"""

from .....processing.utils import requires_columns

# STATIC system message for extraction
SNIPPETS_SYSTEM_MESSAGE = """
You are an information extraction expert specializing in classifying text.

# Task
Your goal is to classify whether the entity is the **subject or agent** 
of the sentence (performing an action, being described, or having 
properties attributed to it). Return 1 if the entity is the subject/agent, 
and 0 if it's merely mentioned, referenced indirectly, or discussed in 
relation to other subjects.

# Critical Rules
- Focus on grammatical subject/agent, not just mentions
- If the entity is doing something or being described → 1
- If the text is about someone/something else acting on or 
  discussing the entity → 0
- When uncertain, check: Could you replace the entity with "it/they" 
  as the sentence subject?

# Output Format
You MUST respond with EXACTLY one character: either 0 or 1
- Do NOT include any explanation, reasoning, or additional text
- Do NOT use quotes, punctuation, or whitespace
- Do NOT output anything other than the single digit 0 or 1
- VALID outputs: 0 or 1
- INVALID outputs: "0", "1", 0., 1., "zero", "one", or any text

## Example 1
List of entities:  
Community law

Text: 
Interlinked with the problem of the division of powers there is a further
question, namely the relationship between Community law and national law.

Output: 
1

## Example 2
List of entities: 
the Commission

Text: 
Article 9(1) makes no reference to the authorities but confers upon the
Commission without qualification exclusive jurisdiction for the application of
Article 85(3).

Output:
1

## Example 3
List of entities:
EU law

Text:
The fact that EU law allows a company to avoid certain rules concerning the
conduct of its business would, however, hardly amount to an abuse.

Output:
1 

## Example 4
List of entities:
the Court

Text:
Most likely this is not caused by German judges being more influential than
others but rather by the fact that German lawyers plead more often before the
Court than lawyers of other nationalities.

Output:
0

## Example 5
List of entities:
the Commission

Text:
In one case the Council apparently completely failed to notice that Parliament
had tabled amendments to the Commission proposal.23 In other cases the Council
has merely referred to the reasons given in the preamble to the proposal.

Output:
0
"""


@requires_columns("snippet_text","entities_str")
def prompt_is_agent_target(snippet_text: str, entities_str:str, **kwargs) -> str:
    """ 
    CREATE user_message for classifiying snippets.
    System message handles the detailed instructions; this generates only the dynamic content.
    
    Args:
        snippet_text (str): snippet text string to be classified. 
        entities_str (str): with revelant entities mentioned in snippet to be classified.
        
    Returns:
        str: Formatted user message for GPT (system message handled separately)
            
    """
    user_message = f"""LIST OF RELEVANT ENTITIES:
{entities_str}

TEXT TO ANALYZE:
{snippet_text}"""

    return user_message.strip()
