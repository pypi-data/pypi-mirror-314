# JuryLLM Usage Guide

## Getting Started

### Installation

1. **System Requirements**
   - Python 3.8+
   - Ollama (for local models)
   - 16GB+ RAM recommended

2. **Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Model Setup**
   ```bash
   # Pull required Ollama models
   ollama pull llama2:13b
   ollama pull llama3.2:3b
   ollama pull phi3.5:3.8b
   ```

## Basic Usage

### Simple Discussion

```python
from juryLLM.model import OllamaParticipant, Judge
from juryLLM.jury import Discussion

# Create participants
participants = [
    OllamaParticipant(name="Model1", model_id="llama2:13b"),
    OllamaParticipant(name="Model2", model_id="phi3.5:3.8b")
]

# Create judge
judge = Judge(name="Judge", model_id="llama2:13b")

# Initialize discussion
discussion = Discussion(participants=participants, judge=judge)

# Define case study
case_study = """
Case: [Your case description]
Questions:
1. [Question 1]
2. [Question 2]
"""

# Run discussion
async for response in discussion.discuss(case_study):
    print(response)
```

## Advanced Usage

### Custom Participants

Create specialized participants for specific tasks:

```python
class SpecialistParticipant(BaseParticipant):
    def __init__(self, name: str, model_id: str, expertise: str):
        super().__init__(name)
        self.model_id = model_id
        self.expertise = expertise
        self.context.append(
            Message(
                role="system",
                content=f"You are a specialist in {expertise}."
            )
        )
```

### Custom Judge Logic

Implement specialized verdict criteria:

```python
class ConsensusJudge(Judge):
    def __init__(self, name: str, model_id: str, consensus_threshold: float = 0.8):
        super().__init__(name, model_id)
        self.consensus_threshold = consensus_threshold
        
    async def evaluate_consensus(self, responses: List[str]) -> bool:
        # Custom consensus evaluation logic
        pass
```

## Case Study Format

### Basic Format
```python
case_study = """
Case: [Brief description]
Context: [Additional information]
Questions:
1. [Question 1]
2. [Question 2]
"""
```

### Complex Format
```python
case_study = """
Case: Complex Problem Solving
Rules:
1. [Rule 1]
2. [Rule 2]

Context:
[Detailed background]

Questions:
1. [Specific question]
2. [Follow-up question]

Constraints:
- [Constraint 1]
- [Constraint 2]
"""
```

## Best Practices

### 1. Model Selection
- Choose models based on task requirements
- Consider model strengths and weaknesses
- Balance between performance and resource usage

### 2. Prompt Engineering
- Provide clear, structured case studies
- Include relevant context and constraints
- Define expected output format

### 3. Performance Optimization
- Use appropriate model sizes
- Implement proper caching strategies
- Monitor resource usage

## Common Issues and Solutions

### 1. Model Loading Errors
```python
# Ensure Ollama is running
ollama list  # Check available models
ollama pull model_name  # Pull missing models
```

### 2. Memory Issues
```python
# Reduce model size or participant count
participants = [
    OllamaParticipant(name="Model1", model_id="llama2:7b"),  # Use smaller model
]
```

### 3. Async Errors
```python
# Proper async usage
async def main():
    async for response in discussion.discuss(case_study):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Topics

### 1. Custom Response Processing
```python
async def process_responses(responses: List[str]) -> str:
    # Custom processing logic
    return processed_result
```

### 2. Discussion Monitoring
```python
class DiscussionMonitor:
    def __init__(self, discussion: Discussion):
        self.discussion = discussion
        self.metrics = {}
    
    async def monitor_round(self, round_num: int):
        # Monitoring logic
        pass
```

### 3. State Management
```python
class DiscussionState:
    def __init__(self):
        self.history = []
        self.metrics = {}
    
    def save_state(self, filepath: str):
        # State saving logic
        pass
    
    @classmethod
    def load_state(cls, filepath: str):
        # State loading logic
        pass
```
