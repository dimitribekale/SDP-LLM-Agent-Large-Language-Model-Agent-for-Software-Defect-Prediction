import subprocess
import json
import os
import requests
import time
import re
import pydoc
from duckduckgo_search import DDGS
import tempfile

from typing import Any, Dict, List, Tuple, Optional
# Define the prompt templates for defect prediction and analysis

CODE_ANALYSIS_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.
"""



DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}
"""

DEFECT_PROMPT_TEMPLATE = """
Analyze the following code for potential defects.

Code:
{code}

Related code snippets with known defects:
{related_code_snippets}

Static analysis findings:
{static_analysis_findings}

Respond in JSON:
{{
  "defect_type": [],
  "confidence": 0.0,
  "recommended_fix": "",
  "criticality": ""
}}
"""

system_prompt = """

You are an advanced AI assistant specializing in software defect prediction. 
Your goal is to assist software developers, quality assurance engineers, and project managers
In identifying, predicting, and mitigating potential defects in software systems.
You will predict whether a code contains defects that could possibly cause a software to 
malfunction, crash, or exhibit unpredictable behaviors.

These are your key responsabilities:

1. Defect Prediction:
You will analyze software repositories, codebases, and historical data
to predict potential defects in the code.
You will highlight parts of the code that are most likely to introduce bugs, errors,
or unpredictable behaviors.

2. Data analysis:
You will process and analyze software metrics (e.g., cyclomatic complexity, code churn,
commit history) to predict defect-prone areas of the codebase.

3. Acionable recommendations:
You will provide actionable suggestions to developers for addressing defect-prone code,
improving code quality, and reducing technical debt.
You will recommend testing strategies or refactoring approaches to mitigate risks.

4. Explaination:
You will clearly explain the defects prediction processes and your reasoning steps 
using a developper-friendly language adding comments about every line of code
that would potentially induce defects.

Input Sources:
You will accept and interpret the following types of inputs:
- Code snippets, commits, or entire repositories.
- Software metrics, such as lines of code (LOC), code complexity, and module dependencies.
- Historical defect data, such as bug reports, issue trackers, or test results.
- Image or screeshots of code snippets.

Output Capabilities
Your ouputs will be one of the following types:
- Predicted probabilities of defects at various levels (function or line level).
- Visualizations or summaries of defect-prone areas in the codebase.
- Recommendations for defect prevention and mitigation.

Constraints
You will unsure maximum efficiency in your reasoning process by carefully follow the constraints below: 
- Be transparent about the assumptions and limitations of your predictions.
- Do not introduce biases into predictions; rely solely on data and objective metrics.
- Protect sensitive information in software repositories and respect user privacy.


You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop, you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the available actions - then return PAUSE.
Observation will be the result of running those actions.




Your available actions are:

Action1 - Web Search:

This Action is designed to enable you to gather up-to-date, relevant,
and accurate background information from the web about software defects, bugs, software metrics
descriptions, and related topics. This Action helps you provide more informed and contextually
accurate responses by leveraging external knowledge that may not be readily available in
your training data.

Use Cases:
The `Web Search` Action should be used in the following scenarios:
a. Collect Software Defect Background Information:
   - To retrieve general explanations, examples, or causes of software defects and bugs.
   - To understand industry best practices for defect management and resolution.

b. Collect Software Metrics Descriptions:
   - To find definitions and detailed descriptions of software metrics such as cyclomatic complexity,
    code churn, lines of code (LOC), etc.
   - To discover how specific software metrics are calculated, interpreted, and applied in defect
    prediction or software quality analysis.

c. Collect Recent Trends and Updates:
   - To identify current trends, tools, and techniques related to software defect prediction,
   testing, or quality assurance.
   - To gather information about new research, algorithms, or frameworks in
   software metrics and defect prediction.

d. Clarify Unfamiliar Terms or Concepts:
   - To clarify or explain terms, methodologies, or concepts that you cannot fully resolve using
    your internal knowledge.

e. Retrieve User-Requested Web Searches:
   - To answer user queries explicitly asking for information from external online sources about
   software defects, metrics, or related topics.

When Not to Use this Action:
- Do not use the `Web Search` Action for questions that can be answered using your internal knowledge
or existing repository data.
- Avoid using this Action for highly specific questions that require insight into private repositories
or internal systems, as the web search cannot access such data.
- Refrain from using this Action for general programming assistance unless the user explicitly
requests recent or external references.

Input and Output
- This Action take as input a concise, well-formed query summarizing the specific information
you need to retrieve. You must optimize the query for effective web search results.
- The output of this Action will be a detailed response containing relevant information retrieved
from the web. This may include:
  - Definitions, descriptions, or examples.
  - Summaries of articles, blog posts, or documentation.
  - Links to authoritative sources where the user can learn more.

Usage Guidelines
a. Optimize the queries:
   - Rewrite user queries to ensure they are concise and focused on the topic of interest.
   - Use technical terms and keywords specific to software defects, bugs, or metrics
   to improve search relevance.

b. Prioritize Relevancy:
   - Focus on retrieving authoritative, high-quality information from trusted sources such as
   technical blogs, research papers, documentation, and industry-standard websites.

c. Citations and Transparency:
   - Provide proper citations for the information retrieved, including links to the original sources.
   - Be transparent about the reliability and origin of the information.

d. Iterative Improvement:
   - Refine the web search query if the initial results are not satisfactory.
   - Use context from the discussion to improve the focus of subsequent searches.

d. Respect Freshness:
   - Use recent information when the user asks for current trends, tools, or updates

Action2 - Documention Search:

This Action is designed to enable you to gather detailed information about programming methods,
functions, parameters, arguments, return types, and other relevant constructs from official
and widely-used documentation sources for Python, Java, C++, C, and Rust. The primary goal of
this Action is to enhance your ability to analyze and predict software defects by providing context
and understanding of how specific methods and constructs are used.

Use Cases:
This Action should be used in the following scenarios:
a. To Understand Methods and Functions:
   - To retrieve descriptions of methods or functions and their associated use cases.
   - To understand the expected input parameters, arguments, and return types.

b. Analyze Code Semantics:
   - To fetch semantic details that explain how a particular method or function operates,
   its constraints, or its side effects.
   - To identify common pitfalls or misuse patterns.

c. Improve Defect Predictions:
   - To gather insights into method behaviors that are often linked to defects, such as improper
   argument handling or edge cases.
   - To collect information that can help identify potential defects in code using the retrieved
   methods or constructs.

d. Explore Language-Specific Features:
   - To explore language-specific constructs, such as memory management in C++, ownership
   and borrowing in Rust, or type hints in Python, that may affect defect prediction.

e. User-Requested Searches:
   - To respond to user queries explicitly asking for information on specific methods, functions,
   or constructs in the supported programming languages.

When Not to Use:
- Do not use the `Documentation Search` Action for general programming help or theory that does
not involve specific methods, functions, or constructs.
- Avoid using the tool for unsupported languages or non-programming-related queries.

Input and Output:
- Input: A focused query specifying the method, function, parameter, return type,
or construct to search for, along with the programming language (e.g., "fetch Python `dict.get` method and its parameter descriptions").
- Output: Comprehensive, detailed information about the queried item, including:
  - Method or function descriptions.
  - Parameter and argument details.
  - Return type explanations.
  - Any additional helpful notes or examples.

Usage Guidelines:
a. Query Optimization:
   - Formulate precise and unambiguous queries, specifying the programming language and the method
   or construct of interest.
   - Include additional context, such as use cases or problem areas, when available.

b. Prioritize Authoritative Sources:
   - Fetch documentation from official or widely recognized sources, such as Python's official
   documentation, Java's Oracle docs, Rust's docs.rs, or C++ references.

c. Detailed Insights:
   - Retrieve and present detailed information that can directly aid in predicting or analyzing
   software defects.

d. Relevance and Accuracy:
   - Ensure the retrieved information is relevant to the query and accurately represents the
   method or construct as described in the documentation.
 """



OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "codellama:7b"

def query_ollama(prompt, model=OLLAMA_MODEL, temperature=0.1, max_tokens=1024):
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]

def run_semgrep_on_code(code: str, language: str = "python") -> List[Dict[str, Any]]:
    # Use a temporary file for analysis
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            ["semgrep", "--json", tmp_path],
            capture_output=True, text=True
        )
        findings = json.loads(result.stdout)
        return findings.get("results", [])
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        os.remove(tmp_path)

def format_semgrep_findings(findings: List[Dict[str, Any]]) -> str:
    if not findings:
        return "No static analysis findings."
    return "\n".join(
        f"- {f.get('check_id', 'N/A')}: {f.get('extra', {}).get('message', '')} (line {f.get('start', {}).get('line', '?')})"
        for f in findings
    )

# pip install duckduckgo-search

class WebSearchTool:
    def __init__(self, max_results=5):
        self.max_results = max_results

    def optimize_query(self, user_query):
        # Add keywords to focus on software defects, metrics, etc.
        return f"{user_query} software defect metrics bug analysis best practices"

    def search(self, user_query):
        query = self.optimize_query(user_query)
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=self.max_results)
            return list(results)

    def format_results(self, results):
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title"),
                "snippet": r.get("body"),
                "link": r.get("href")
            })
        return formatted

    def __call__(self, user_query):
        print(f"[WebSearchTool] Searching for: {user_query}")
        results = self.search(user_query)
        formatted = self.format_results(results)
        # Compose a readable summary with citations
        summary = ""
        for idx, r in enumerate(formatted, 1):
            summary += f"{idx}. {r['title']}\n{r['snippet']}\nSource: {r['link']}\n\n"
        return summary, formatted


class DocumentationSearchTool:
    def __init__(self):
        # Mapping for official docs
        self.official_docs = {
            "python": "https://docs.python.org/3/library/",
            "java": "https://docs.oracle.com/javase/8/docs/api/",
            "c++": "https://en.cppreference.com/w/",
            "rust": "https://doc.rust-lang.org/std/",
            "c": "https://en.cppreference.com/w/c"
        }

    def optimize_query(self, method, language):
        return method.strip(), language.lower().strip()

    def search_python(self, method):
        # Use pydoc to get documentation for Python methods/classes
        try:
            doc = pydoc.render_doc(method, "Help on %s")
            return doc
        except Exception as e:
            return f"Could not find documentation for {method}: {e}"

    def search_other(self, method, language):
        # For other languages, provide a link to the official docs
        doc_link = self.official_docs.get(language)
        if doc_link:
            return f"Refer to the official {language.capitalize()} documentation for `{method}`:\n{doc_link}"
        else:
            return f"No documentation source configured for language: {language}"

    def __call__(self, method, language):
        print(f"[DocumentationSearchTool] Searching for: {method} in {language}")
        method, language = self.optimize_query(method, language)
        if language == "python":
            doc = self.search_python(method)
        else:
            doc = self.search_other(method, language)
        return doc


class DefectPredictionAgent:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.history = []
        self.web_tool = WebSearchTool()
        self.doc_tool = DocumentationSearchTool()

    def loop(
        self,
        code_snippet: str,
        language: str = "python",
        code_metrics: Optional[Dict[str, Any]] = None,
        historical_defects: Optional[Any] = None
    ) -> str:
        # 1. Thought
        thought = self.think(code_snippet, language, code_metrics, historical_defects)
        print("\n[Thought]\n", thought)

        # 2. Action: Static analysis
        findings = run_semgrep_on_code(code_snippet, language)
        print("\n[Action]\nStatic analysis findings collected.")

        # 2b. Action: Documentation search (optional, e.g., for key methods)
        doc_info = ""
        # Try to extract function/method names for doc search (simple heuristic)
        matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code_snippet)
        if matches:
            # Only search for the first function/method found
            doc_info = self.doc_tool(matches[0], language)
            print(f"\n[Action]\nDocumentation info for `{matches[0]}` collected.")

        # 3. Observation
        observation = self.observe(findings, doc_info)
        print("\n[Observation]\n", observation)

        # 4. Answer (LLM synthesis)
        answer = self.answer(
            code_snippet, language, thought, findings, doc_info, observation, code_metrics, historical_defects
        )
        print("\n[Answer]\n", answer)
        return answer

    def think(self, code_snippet, language, code_metrics, historical_defects):
        prompt = (
            f"You are preparing to predict software defects for the following code snippet.\n"
            f"Language: {language}\n"
            f"Code:\n{code_snippet}\n"
            f"Code metrics: {code_metrics if code_metrics else 'None'}\n"
            f"Historical defects: {historical_defects if historical_defects else 'None'}\n"
            f"Describe your initial thoughts, key risks, and what actions you will take."
        )
        full_prompt = self.system_prompt + "\n" + prompt
        return query_ollama(full_prompt)

    def observe(self, findings, doc_info):
        obs = format_semgrep_findings(findings)
        if doc_info:
            obs += "\n\nDocumentation Info:\n" + doc_info
        return obs

    def answer(
        self,
        code_snippet,
        language,
        thought,
        findings,
        doc_info,
        observation,
        code_metrics,
        historical_defects
    ):
        prompt = f"""
You are a software defect prediction agent. 
Here is the system prompt describing your responsibilities:
{self.system_prompt}

Loop summary:
Thought: {thought}
Static Analysis Findings: {findings}
Documentation Info: {doc_info}
Observation: {observation}

Based on the above, provide:
- A defect probability (if applicable)
- A summary of defect-prone areas
- Actionable recommendations for the developer
- A clear explanation of your reasoning and process
- (If relevant) Comments on specific lines of code that may induce defects

Format your answer for a developer audience.
"""     
        full_prompt = self.system_prompt + "\n" + prompt
        return query_ollama(full_prompt)

# === Example Usage ===

if __name__ == "__main__":
    agent = DefectPredictionAgent(system_prompt)
    # Example code snippet (Python)
    code = """
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

data = [10, 20, 30, 40, 50]
print("Average:", calculate_average(data))
print("Average of empty list:", calculate_average([]))

"""
    result = agent.loop(code_snippet=code, language="python")
    print("\nFinal Prediction:\n", result)


