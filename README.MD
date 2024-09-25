# Large Language Models (LLMs) Workshop - Introduction and Hands-On Examples

👋 Welcome to the **Introductory Workshop on Large Language Models (LLMs)**! This workshop is designed to equip you with the foundational knowledge and practical tools to understand, experiment with, and apply LLMs to a variety of tasks.

🔭 **Workshop Objective:**  
Our aim is twofold:  
1. Introduce the core fundamentals of LLMs.  
2. Provide practical, hands-on code templates (in Python) that will enable you to apply LLMs effectively in your research.

⚙️ **Technologies Used:**  
This workshop will focus on the Hugging Face ecosystem (https://huggingface.co/docs/hub/index) to apply various LLMs. The majority of the code will be executed in **Jupyter Notebooks**, using Python and essential libraries such as `transformers`, `torch`, and `scikit-learn` (some more). The focus will be on integrating LLMs into a variety of NLP tasks.


📝 **Preparation Checklist:**
Before attending the workshop, please ensure you follow the **[installation instructions](https://github.com/FennStatistics/introductory-workshop-in-LLMs/tree/main/Preparation%20Checklist)** provided to
- set up the necessary software and dependencies.  
- generate API keys for accessing LLMs via platforms like Hugging Face.

📢 **Important Note:** 
In this three-hour workshop, we’ll only have time to cover the basics of LLMs. This is a complex and rapidly evolving field, so it’s essential that you as a participant come with a basic understanding of Python. Additionally, I highly recommend reviewing the **[Additional Resources](https://github.com/FennStatistics/introductory-workshop-in-LLMs/tree/main/Additional%20Resources)** section prior to the workshop for a more comprehensive overview. That said, I hope you’re excited to join us for some hands-on learning, where we’ll explore practical and impactful use cases of LLMs (see section below).

💬 **Questions?**  
I’m here to help! If you have any questions, suggestions or would like to discuss potential ideas, feel free to reach out: julius.fenn@psychologie.uni-freiburg.de

## Application Cases Covered in the Workshop:

1. **Text Generation**  
   - Learn how to generate coherent and creative text using pre-trained LLMs.  
   - Experiment with various **prompting techniques** and explore the impact of **hyperparameters** (e.g., temperature, top-k sampling) on output diversity and creativity.

2. **Feature Extraction**  
   - Extract **embeddings** (numerical representations of text meaning) using LLMs and apply them for tasks such as text similarity analysis using cosine similarity.  
   - Explore how embeddings can represent semantic meaning and facilitate other downstream tasks.

3. **Text Classification**  
   - Use extracted embeddings to perform **text classification** with machine learning models like regularized regression or random forests.  
   - Alternatively, explore **fine-tuning LLMs** to classify text (sometimes) more accurately for specific domains.

4. **Summarizing Literature**  
   - Apply LLMs for **summarizing scientific articles** using advanced techniques like **Retrieval-Augmented Generation (RAG)**, which combines LLMs with retrieval mechanisms.  
   - Enhance your summarization by coupling it with **bibliometric analysis** to better understand academic research trends.