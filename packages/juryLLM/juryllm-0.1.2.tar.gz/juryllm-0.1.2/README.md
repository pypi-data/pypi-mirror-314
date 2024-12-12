# JuryLLM

## Overview
JuryLLM is an experimental framework that orchestrates multiple language models to work collaboratively, similar to a jury system, to solve complex problems. By leveraging the power of ensemble decision-making, this project aims to demonstrate how smaller, open-source LLM models can work together to produce more robust and intelligent solutions.

The major breakthrough in human intelligence occurred when we learned to communicate more effectively. Unlike other highly intelligent species that went extinct, our ability to communicate and collaborate set us apart. The foundations of our progress have always been rooted in effective communication, teamwork, and collective focus toward shared goals. Even the open-source movement embodies this spirit of collaboration, showcasing how working together can drive innovation and success.

## Key Features
- **Model Ensemble**: Integrates multiple language models to work as a collaborative unit
- **Jury-like Decision Making**: Implements a structured approach for models to deliberate and reach consensus
- **Open Source Focus**: Primarily works with accessible, open-source language models
- **Collaborative Intelligence**: Harnesses diverse model perspectives for enhanced problem-solving

## Purpose
The primary goals of JuryLLM are:
- Explore the potential of collaborative AI decision-making
- Demonstrate how smaller models can achieve superior results through teamwork
- Provide an experimental platform for testing ensemble-based approaches
- Create more reliable and well-rounded AI solutions

## Technical Architecture
The system is designed as a modular framework where:
- Multiple language models act as jury members
- Each model contributes its unique perspective
- A coordinated decision-making process synthesizes various inputs
- The final output represents a collective intelligence solution

## Use Cases
- Complex problem-solving requiring multiple perspectives and using multiple `specialist models`
- Scenarios where consensus-based decision making is valuable
- Tasks benefiting from diverse model capabilities
- Experimental research in collaborative AI systems

## Contributing
We welcome contributions to this experimental project! Whether you're interested in:
- Adding new model integrations
- Improving the consensus mechanism
- Optimising prompts
- Adding better fine-tuned models
- Enhancing the documentation
- Sharing interesting use cases

## License
MIT License

## Documentation

### Architecture
The JuryLLM framework consists of three main components:

1. **Participants (`model.py`)**
   - `BaseParticipant`: Abstract base class for all participants
   - `OllamaParticipant`: Implementation for local Ollama models
   - `OpenAIParticipant`: Implementation for OpenAI API models
   - `Judge`: Specialized participant that evaluates discussions and provides verdicts

2. **Discussion Management (`jury.py`)**
   - `Discussion`: Core class that manages the conversation flow
   - Handles async streaming of responses
   - Manages discussion rounds and verdict checking
   - Formats case prompts and maintains discussion history

3. **Message System**
   - `Message`: Data structure for communication
   - Tracks role, content, and participant information
   - Maintains conversation context

### Setup Instructions

1. **Prerequisites**
   ```bash
   # Install Python 3.8+ and pip
   # Install Ollama (for local models)
   brew install ollama
   ```

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/juryLLM.git
   cd juryLLM

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Pull Required Models**
   ```bash
   # Pull Ollama models
   ollama pull llama2:13b
   ollama pull llama3.2:3b
   ollama pull phi3.5:3.8b
   ```

4. **Configuration**
   - Set environment variables if using OpenAI models:
     ```bash
     export OPENAI_API_KEY=your_api_key
     ```

### Running the Framework

1. **Basic Usage**
   ```python
   # Run the example discussion
   python app.py
   ```

2. **Custom Implementation**
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

   # Run discussion
   async for response in discussion.discuss(your_case_study):
       print(response)
   ```

### Approach and Design Decisions

1. **Asynchronous Processing**
   - Uses `asyncio` for non-blocking operations
   - Implements streaming responses for real-time interaction
   - Handles multiple model responses concurrently

2. **Modular Architecture**
   - Easily extensible for new model types
   - Separation of concerns between participants and discussion management
   - Clean interfaces for adding new functionality

3. **Judge Implementation**
   - Monitors discussion quality and relevance
   - Prevents hallucination and maintains factual accuracy
   - Provides clear verdicts based on discussion context

4. **Error Handling**
   - Graceful handling of model failures
   - Proper context management
   - Clear error messages and logging

### Example Use Cases

1. **Complex Problem Solving**
   ```python
   case_study = """
   Case: Complex mathematical problem with multiple rules
   Rules:
   1. Rule one details...
   2. Rule two details...
   Questions:
   1. Question one...
   2. Question two...
   """
   ```

2. **Decision Making**
   ```python
   case_study = """
   Case: Ethical decision scenario
   Context: [Scenario details]
   Questions to consider:
   1. Ethical implications
   2. Practical considerations
   """
   ```

### Best Practices

1. **Model Selection**
   - Choose models based on task requirements
   - Consider model strengths and weaknesses
   - Balance between performance and resource usage

2. **Prompt Engineering**
   - Provide clear, structured case studies
   - Include relevant context and constraints
   - Define expected output format

3. **Performance Optimization**
   - Use appropriate model sizes
   - Implement proper caching strategies
   - Monitor resource usage

### Troubleshooting

Common issues and solutions:
1. Model loading errors: Ensure Ollama is running and models are pulled
2. Memory issues: Adjust model sizes or reduce participant count
3. Async errors: Check for proper async/await usage
4. API rate limits: Implement proper rate limiting for API calls

---
*Note: This is an experimental project aimed at exploring collaborative AI approaches. The system is under active development and subject to changes.*