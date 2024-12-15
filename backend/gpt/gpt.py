from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
from pydantic import BaseModel
from openai import OpenAI

from pathlib import Path
import re
import pdfplumber

from dotenv import load_dotenv
import os

load_dotenv()


directory = os.path.join(os.getcwd(), '..', 'uploads')

sources = os.listdir(directory)


text_lst = []
for file in sources:
    file_path = os.path.join(directory, file)
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            text_lst.append(text)
    except Exception as e:
        print(f"Error processing file {file}: {e}")



client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

all_topics = []

for text in text_lst:
  class Topic_Scope(BaseModel):
    topic: str
    scope: list[str]

  class Topic_Output(BaseModel):
    topics: list[Topic_Scope]
    
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": """
        
        You are an expert assistant working as part of a team focused on creating the most effective study materials for students.
          Your role is to analyze the provided text and identify key topics that are most likely to appear on exams for the subject. You will extract the following:

          Key Topics: Select only the topics that are essential for understanding the subject or frequently tested in exams. Avoid irrelevant or non-academic content.
          Topic Scope: For each key topic, provide a concise explanation of its scope within the text—what it covers and why it is significant in the context of the subject.
          Relevance Assessment: Prioritize topics based on their educational value and likelihood of being tested in exams.
          Output Format:
          Return the results in the following structured format:

                {
            "topics": [
            {
              "topic": "Hashing",
              "output": "[Direct Address Tables, Query time complexity, Hash Function, Collisions, Chaining]"
            },
            {
              "topic": "Dijkstra's Algorithm",
              "output": "[Shortest Path Algorithms, Outline of Dijkstra's Algorithm code, Proof Idea of Dijkstra's Algorithm, priority queue for Dijkstra's Algorithm, Dijkstra's Algorithm loop invariants, exit paths]"
            }
        ]
        }

          Focus on topics commonly emphasized in academic curricula and exams.
          Make the topics specific with their own specific scopes
          Avoid trivial or non-academic content unless explicitly relevant to the subject.
          This systematic approach ensures that the study materials generated are targeted, concise, and exam-relevant. Take as long as needed to formulate the bets possible results
        
        """},


        {"role": "user", "content": f"{text}"},
    ],
    response_format=Topic_Output,
  )

  event = completion.choices[0].message.parsed
  all_topics.append(event)

  
def output_to_input(output):
    json_dict = []

    for i in range(len(output)):
        document_topic_output = output[i]

        document_topic_output_dict = {'topics': []}


        for topic in document_topic_output.topics:
            temp_dict = {}
            temp_dict['topic'] = topic.topic
            temp_dict['scope'] = topic.scope
            document_topic_output_dict['topics'].append(temp_dict)


        json_dict.append(document_topic_output_dict)
    
    return str(json_dict)

t_lsit = output_to_input(all_topics)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class Topic_Latex(BaseModel):
    topic: str
    latex: str

class Latex_Output(BaseModel):
    topics: list[Topic_Latex]

t_list = output_to_input(all_topics)

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": """
        
        You are a LaTeX code generator specializing in creating content for cheat sheets. Your task is to generate 12 blocks of detailed LaTeX code based on a provided string
        that maps topics to their scope. Each block should focus on one topic and present all critical information compactly while remaining visually structured and engaging.
        
        Requirements:
        Analyze the input string to extract key topics and their scopes.
        Include comprehensive and relevant details for each topic while ensuring they fit well within the context of a cheat sheet.
        Optimize for clarity and visual organization by utilizing lists, tables, and equations wherever appropriate to enhance readability and conserve space.
        Ensure a balanced output length for each block, maintaining a minimum of 8-10 lines of LaTeX code per block.
        Use compact formatting without unnecessary whitespace or excessively large text but ensure all information remains legible and well-structured.
        Constraints:
        Do not include big headers, bullet points with excessive spacing, or irrelevant details.
        Ensure that the overall design prioritizes a dense, readable format suitable for a cheat sheet.
        Validate that all blocks maintain clarity, completeness, and consistency.
        Output format: Only include LaTeX code. Do not include explanations, headers, or any additional text.


        """},

        {"role": "user", "content": f"{t_list}"},
    ],
    max_tokens = 10000,

    response_format=Latex_Output,
)
    
event = completion.choices[0].message.parsed

    
def latex_output_to_input(output):
    json_dict = []

    for topic in output.topics:
        temp_dict = {}
        temp_dict['topic'] = topic.topic
        temp_dict['latex'] = topic.latex
        
        json_dict.append(temp_dict)
    
    return json_dict

latex_maps = latex_output_to_input(event)


template = r""" 



\documentclass{article}
\usepackage[landscape]{geometry}
\usepackage{url}
\usepackage{multicol}
\usepackage{amsmath}
\usepackage{esint}
\usepackage{amsfonts}
\usepackage{tikz}
\usetikzlibrary{decorations.pathmorphing}
\usepackage{amsmath,amssymb}

\usepackage{colortbl}
\usepackage{xcolor}
\usepackage{mathtools}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\makeatletter

\newcommand*\bigcdot{\mathpalette\bigcdot@{.5}}
\newcommand*\bigcdot@[2]{\mathbin{\vcenter{\hbox{\scalebox{#2}{$\m@th#1\bullet$}}}}}
\makeatother

\title{Title Cheat Sheet}
\usepackage[brazilian]{babel}
\usepackage[utf8]{inputenc}

\advance\topmargin-.8in
\advance\textheight3in
\advance\textwidth3in
\advance\oddsidemargin-1.5in
\advance\evensidemargin-1.5in
\parindent0pt
\parskip2pt
\newcommand{\hr}{\centerline{\rule{3.5in}{1pt}}}
%\colorbox[HTML]{e4e4e4}{\makebox[\textwidth-2\fboxsep][l]{texto}
\begin{document}

\begin{center}{\huge{\textbf{Title Cheat Sheet}}}\\
\end{center}
\begin{multicols*}{3}

\tikzstyle{mybox} = [draw=black, fill=white, very thick,
    rectangle, rounded corners, inner sep=10pt, inner ysep=10pt]
\tikzstyle{fancytitle} =[fill=black, text=white, font=\bfseries]

%------------ page 1 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
   box1
   
\end{minipage}
};
%------------ page 1  Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 1};
\end{tikzpicture}

%------------ page 2  ---------------
\begin{tikzpicture}
\node [mybox] (box) {%
    \begin{minipage}{0.3\textwidth}
       box2
    \end{minipage}
};
%------------ page 2  Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 2};
\end{tikzpicture}

%------------ page 3 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
    box3
    \end{minipage}
};
%------------ page 3 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 3};
\end{tikzpicture}

%------------ page 4 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
   box4
    \end{minipage}
};
%------------ page 4 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 4};
\end{tikzpicture}
%------------ page 5 ---------------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
    	box5
    \end{minipage}
};
%------------ page 5 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 5};
\end{tikzpicture}

%------------ page 6 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}  
   box6
    \end{minipage}
};
%------------ page 6 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 6};
\end{tikzpicture}

%------------ page 7 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
    box7
    \end{minipage}
};
%------------ page 7 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 7};
\end{tikzpicture}


%------------ page 8 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
box8
    \end{minipage}
};
%------------ page 8 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 8};
\end{tikzpicture}
\
%------------ page 9 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
    box9
    \end{minipage}
};
%------------ page 9 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 9};
\end{tikzpicture}
%------------ page 10 ---------------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
	box10
	\end{minipage}
};
%------------ page 10 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 10};
\end{tikzpicture}
\\
\\
\\
\\

%------------ page 11 ---------------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
   box11
	\end{minipage}
};
%------------ page 11 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 11};
\end{tikzpicture}

%------------ page 12 ---------------
\begin{tikzpicture}
\node [mybox] (box){%
    \begin{minipage}{0.3\textwidth}
    box12
    \end{minipage}
};
%------------ page 12 Header ---------------------
\node[fancytitle, right=10pt] at (box.north west) {page 12};
\end{tikzpicture}
\end{multicols*}
\end{document}"""

for i in range(12):
    topic_latex_section = latex_maps[i]
    topic_name = topic_latex_section['topic'] 
    topic_latex = topic_latex_section['latex'] 

    template = template.replace(f"box{i+1}", topic_latex)
    template = template.replace(f"page {i+1}", topic_name)


file_name = "output.tex"

file_path = os.path.join(os.getcwd(), file_name)

with open(file_path, "w") as file:
    file.write(template)
