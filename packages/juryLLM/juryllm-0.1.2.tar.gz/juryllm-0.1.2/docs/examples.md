# JuryLLM Examples

This document provides various examples of using JuryLLM for different scenarios.

## 1. Rule-Based Problem Solving

### Example: Mathematical Rules Application

```python
case_study = """
Case: For the following questions you must adhere to these rules:

Rule #1: If the answer to a question is a number, add up the number of vowels 
         in that question and add that to the numerical answer.

Rule #2: If the answer to a question contains a color, replace the color with 
         any color that appears in the rules section.

Rule #3: If its an even-numbered question ignore rules one and four.

Questions:
1. What is 1+4+2+1?
2. What is the sum of 5 and 3?
"""

async def main():
    participants = [
        OllamaParticipant(name="Calculator", model_id="llama3.2:3b"),
        OllamaParticipant(name="Validator", model_id="phi3.5:3.8b")
    ]
    judge = Judge(name="RuleJudge", model_id="llama2:13b")
    
    discussion = Discussion(participants=participants, judge=judge)
    async for response in discussion.discuss(case_study):
        print(response)

asyncio.run(main())
```

## 2. Ethical Decision Making

### Example: Autonomous Vehicle Dilemma

```python
case_study = """
Case: Ethical AI Decision Making

A self-driving car is approaching an unavoidable accident scenario. 
It must choose between:
1. Swerving right, which would impact a group of three elderly pedestrians
2. Swerving left, which would impact a young mother with a baby stroller
3. Continuing straight, which would likely result in the death of its passenger

Consider:
- The value of human life
- Age and potential years of life
- Number of individuals affected
- The car's duty to its passenger
- Legal and ethical implications
"""

async def ethical_discussion():
    participants = [
        OllamaParticipant(name="Ethicist", model_id="llama2:13b"),
        OllamaParticipant(name="Legal", model_id="phi3.5:3.8b")
    ]
    judge = Judge(name="EthicsJudge", model_id="llama2:13b")
    
    discussion = Discussion(participants=participants, judge=judge)
    async for response in discussion.discuss(case_study):
        print(response)
```

## 3. Technical Analysis

### Example: Code Review Discussion

```python
case_study = """
Case: Code Review Analysis

Review the following code snippet and discuss its implications:

```python
def process_data(data: List[Dict]) -> Dict:
    result = {}
    for item in data:
        if item.get('status') == 'active':
            result[item['id']] = item['value']
    return result
```

Consider:
1. Performance implications
2. Error handling
3. Edge cases
4. Best practices
"""

async def code_review():
    participants = [
        OllamaParticipant(name="SecurityExpert", model_id="llama2:13b"),
        OllamaParticipant(name="PerformanceAnalyst", model_id="phi3.5:3.8b")
    ]
    judge = Judge(name="TechLead", model_id="llama2:13b")
    
    discussion = Discussion(participants=participants, judge=judge)
    async for response in discussion.discuss(case_study):
        print(response)
```

## 4. Pattern Recognition

### Example: Data Analysis

```python
case_study = """
Case: Pattern Recognition in Time Series Data

Given the following monthly sales data:
Jan: 100
Feb: 120
Mar: 90
Apr: 110
May: 130
Jun: 95

Questions:
1. What patterns do you observe?
2. What might be causing the fluctuations?
3. What would you predict for July?
"""

async def pattern_analysis():
    participants = [
        OllamaParticipant(name="DataAnalyst", model_id="llama3.2:3b"),
        OllamaParticipant(name="Statistician", model_id="phi3.5:3.8b")
    ]
    judge = Judge(name="AnalyticsLead", model_id="llama2:13b")
    
    discussion = Discussion(participants=participants, judge=judge)
    async for response in discussion.discuss(case_study):
        print(response)
```

## 5. Custom Implementation

### Example: Specialized Discussion Format

```python
class DebateFormat:
    def __init__(self, topic: str, stance_a: str, stance_b: str):
        self.topic = topic
        self.stance_a = stance_a
        self.stance_b = stance_b
    
    def format_case(self) -> str:
        return f"""
        Case: Structured Debate

        Topic: {self.topic}

        Stance A: {self.stance_a}
        Stance B: {self.stance_b}

        Format:
        1. Opening statements
        2. Rebuttals
        3. Final arguments
        """

async def structured_debate():
    debate = DebateFormat(
        topic="Should AI systems be required to explain their decisions?",
        stance_a="Yes, transparency is crucial for trust and accountability",
        stance_b="No, explanation requirements could limit AI capabilities"
    )
    
    participants = [
        OllamaParticipant(name="ProponentA", model_id="llama2:13b"),
        OllamaParticipant(name="ProponentB", model_id="phi3.5:3.8b")
    ]
    judge = Judge(name="Moderator", model_id="llama2:13b")
    
    discussion = Discussion(participants=participants, judge=judge)
    async for response in discussion.discuss(debate.format_case()):
        print(response)
```

## Running the Examples

To run any of these examples:

1. Ensure all required models are pulled:
```bash
ollama pull llama2:13b
ollama pull llama3.2:3b
ollama pull phi3.5:3.8b
```

2. Save the example code in a Python file (e.g., `example.py`)

3. Run the example:
```bash
python example.py
```

## Tips for Creating New Examples

1. **Clear Context**: Provide comprehensive context in the case study
2. **Structured Format**: Use clear sections and formatting
3. **Specific Questions**: Frame precise questions or points for discussion
4. **Appropriate Models**: Choose models suited to the task
5. **Error Handling**: Include proper error handling in implementations
