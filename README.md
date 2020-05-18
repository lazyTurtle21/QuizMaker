# QuizMaker
> An app for automatic quiz generation

![Who wants to become a linear algebra expert?](https://i.imgur.com/GV1w2xI.jpg)

## How to run
```sh
pip install -r requirements.txt
jupyter notebook
```

Then, it depends on what you want:
* see the performance of NER model - run **ner_model_linear_algebra.ipynb**
* see a quiz generation using a Knowledge Graph approach - run **knowledge_graph_approach.ipynb**
* see a quiz generation using a Feature extraction approach - run **feature_extraction_approach.ipynb**

In both *_aproach.ipynb notebooks, you can choose the chapter for quiz generation. It can be done by replacing the parameter *chapter_number* in function *get_one_chapter_strang*. <br>
Also, you're able to choose a number of questions for the quiz. The variable *n = 10* is responsible for it.

## Team
* Olya Prots
* Sophia Kholod
