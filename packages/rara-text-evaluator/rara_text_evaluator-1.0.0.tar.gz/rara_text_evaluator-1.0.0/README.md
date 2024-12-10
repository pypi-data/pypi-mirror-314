# RaRa Text Evaluator

**`rara-text-evaluator`** is a  Python library for evaluating the quality of text using n-gram models.

---

## ✨ Features  

- **Evaluate text quality** with either pre-built models or create your own.
- **Build** and **train** n-gram models for text quality evaluation.
- Pre-trained models for **Estonian**, **English**, and a **language-agnostic** fallback.
- Easy to extend for other languages or corpora.
---


## ⚡ Quick Start  

Get started with `rara-text-evaluator` in just a few steps:

1. **Install the Package**  
   Ensure you're using Python 3.10 or above, then run:  
   ```bash
   pip install rara-text-evaluator
   ```

2. **Import and Use**  
   Example usage to evaluate text:  

   ```python
   from rara_text_evaluator.quality_evaluator import QualityEvaluator

   evaluator = QualityEvaluator()

   example_text = "Some text here that is over 30 characters long."
   score = evaluator.get_probability(example_text)
   is_valid = evaluator.is_valid(example_text)

   print(f"Text Quality Score: {score}")
   print(f"Text is valid: {is_valid}")
   ```

---

## 💡 Important to note 

- Texts shorter than **30 characters** will result in probability score 0.0 by default. Both the minimum length and the default response can be configured with parameters `length_limit` and `default_response`. See [documentation](DOCUMENTATION.md) to learn more.


## ⚙️ Installation Guide

Follow the steps below to install the `rara-text-evaluator` package, either via `pip` or locally.

---

### Installation via `pip`

<details><summary>Click to expand</summary>

1. **Set Up Your Python Environment**  
   Create or activate a Python environment using Python **3.10** or above.

2. **Install the Package**  
   Run the following command:  
   ```bash
   pip install rara-text-evaluator
   ```
</details>

---

### Local Installation

Follow these steps to install the `rara-text-evaluator` package locally:  

<details><summary>Click to expand</summary>


1. **Clone the Repository**  
   Clone the repository and navigate into it:  
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Git LFS**  
   Ensure you have Git LFS installed and initialized:  
   ```bash
   git lfs install
   ```

3. **Pull Git LFS Files**  
   Retrieve the large files tracked by Git LFS:  
   ```bash
   git lfs pull
   ```

4. **Set Up Python Environment**  
   Create or activate a Python environment using Python 3.10 or above. E.g:
   ```bash
   conda create -n py310 python==3.10
   conda activate py310
   ```

5. **Install Build Package**  
   Install the `build` package to enable local builds:  
   ```bash
   pip install build
   ```

6. **Build the Package**  
   Run the following command inside the repository:  
   ```bash
   python -m build
   ```

7. **Install the Package**  
   Install the built package locally:  
   ```bash
   pip install .
   ```

</details>

---

## 🚀 Testing Guide

Follow these steps to test the `rara-text-evaluator` package.


### How to Test

<details><summary>Click to expand</summary>

1. **Clone the Repository**  
   Clone the repository and navigate into it:  
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Git LFS**  
   Ensure Git LFS is installed and initialized:  
   ```bash
   git lfs install
   ```

3. **Pull Git LFS Files**  
   Retrieve the large files tracked by Git LFS:  
   ```bash
   git lfs pull
   ```

4. **Set Up Python Environment**  
   Create or activate a Python environment using Python 3.10 or above.

5. **Install Build Package**  
   Install the `build` package:  
   ```bash
   pip install build
   ```

6. **Build the Package**  
   Build the package inside the repository:  
   ```bash
   python -m build
   ```

7. **Install with Testing Dependencies**  
   Install the package along with its testing dependencies:  
   ```bash
   pip install .[testing]
   ```

8. **Run Tests**  
   Run the test suite from the repository root:  
   ```bash
   python -m pytest -v tests
   ```

---

</details>


## 📝 Documentation

Documentation can be found [here](DOCUMENTATION.md).

## 🌍 Supported Models  

The `QualityEvaluator` class leverages language-specific pre-built models to assess the quality of provided text. It also supports an automatic fallback model for cases where the specified or detected language is not supported.

### Built-in Models  

The package has built-in support for the following languages:  
- **Estonian**  
- **English**  
- **Language-agnostic fallback model**  

The table below provides details on the corpora used for training each model:

| **Language**       | **Model Name**                     | **Corpora**                                                                           | **Words**   | **Characters** |
|---------------------|-------------------------------------|---------------------------------------------------------------------------------------|-------------|----------------|
| **Estonian**        | `text_validator_ngram_3_et.pkl`    | DIGAR "born digital" articles                                                        | 4,164,975   | 30,630,998     |
| **English**         | `text_validator_ngram_3_en.pkl`    | NLTK corpora ([gutenberg, brown, reuters, webtext](https://www.nltk.org/nltk_data/)) | 5,900,439   | 28,649,578     |
| **Language-agnostic** | `text_validator_ngram_3_fallback.pkl` | Combined DIGAR and NLTK corpora                                                      | 10,065,413  | 59,280,576     |

---

#### Additional Notes
- **Automatic Fallback**: If the target language isn't explicitly supported, the **language-agnostic fallback model** will be used.  
- **N-Gram**: All models currently use a trigrams (`n=3`) approach to evaluate text quality.  

## 🔍 More Usage Examples

This section provides additional examples of possible usage and highlights the roles of some parameters.


### Impact of parameters `length_limit` and `default_response`

<details><summary>Click to expand</summary>

```python
from rara_text_evaluator.quality_evaluator import QualityEvaluator

evaluator = QualityEvaluator()

text = "This is a valid text."
text_length = len(text)

score = evaluator.get_probability(text)

print(f"Text length: {text_length} characters")
print(f"Quality score: {score}")
```

**Output:**

```bash
Text length: 21 characters
Quality score: 0.0
```
As the default `length_limit` param is set to 30, the output score is automatically set to the default value of `default_response` (0.0).

However, we can modify it to allow shorter texts as well:

```python
from rara_text_evaluator.quality_evaluator import QualityEvaluator

evaluator = QualityEvaluator()

text = "This is a valid text."
text_length = len(text)

score = evaluator.get_probability(text, length_limit=20)

print(f"Text length: {text_length} characters")
print(f"Quality score: {score}")
```

**Output:**

```bash
Text length: 21 characters
Quality score: 0.7611294876594459
```

As we see, the method now returns a real quality score, it is just a little bit lower than expected considering the text is actually completely valid. This is why the cut-off was added in the first place - so we can distinguish between texts that actually have low quality opposed to just being short. </details>

### Setting thresholds for binary evaluation

<details><summary>Click to expand</summary>

Let's first inspect the results with default thresholds:

```python
from rara_text_evaluator.quality_evaluator import QualityEvaluator

evaluator = QualityEvaluator()

text_en = "This is more or lesh valihd text but coneins some mistakes."
text_et = "See tekst sishaldap mõnet väjkeset vead, mis võib-olla on okei."

score_en = evaluator.get_probability(text_en)
score_et = evaluator.get_probability(text_et)

is_valid_en = evaluator.is_valid(text_en)
is_valid_et = evaluator.is_valid(text_et)

print(f"text_en is valid: {is_valid_en} (score = {score_en}.")
print(f"text_et is valid: {is_valid_et} (score = {score_et}.")
print(f"Current thresholds for validity:{evaluator.thresholds}")
```

**Output:**

```bash
text_en is valid: True (score = 0.8382394549211963.
text_et is valid: True (score = 0.7840549033157463.
Current thresholds for validity:{'et': 0.7, 'en': 0.7, 'fallback': 0.7}
```

As we can see, both English and Estonian example texts pass the validity check with default thresholds. Let's assume that we want a lot higher quality for our texts in Estonian and set the threshold for that language higher:

```python
from rara_text_evaluator.quality_evaluator import QualityEvaluator

evaluator = QualityEvaluator()

text_en = "This is more or lesh valihd text but coneins some mistakes."
text_et = "See tekst sishaldap mõnet väjkeset vead, mis võib-olla on okei."

# Let's set higher threshold for Estonian
evaluator.set_threshold(lang="et", threshold=0.9)

score_en = evaluator.get_probability(text_en)
score_et = evaluator.get_probability(text_et)

is_valid_en = evaluator.is_valid(text_en)
is_valid_et = evaluator.is_valid(text_et)

print(f"text_en is valid: {is_valid_en} (score = {score_en}.")
print(f"text_et is valid: {is_valid_et} (score = {score_et}.")

print(f"Current thresholds for validity:{evaluator.thresholds}")
```

**Output:**

```bash
text_en is valid: True (score = 0.8382394549211963.
text_et is valid: False (score = 0.7840549033157463.
Current thresholds for validity:{'et': 0.9, 'en': 0.7, 'fallback': 0.7}
```
</details>

### Building and applying a custom language model

<details><summary>Click to expand</summary>

```python
from rara_text_evaluator.ngram_model_builder import NgramModelBuilder
from rara_text_evaluator.quality_evaluator import QualityEvaluator

# Setting class instance parameters
# and creating the class instance
n_gram = 2
language = "klingon"
accepted_chars ="jilnrguhqtmpseybvwaocd.,:;-_!\"()%@1234567890' "

nmb = NgramModelBuilder(n=n_gram, lang=language, accepted_chars=accepted_chars)

# Training and saving the model

#NB! This is just a dummy example! You should use a much bigger corpus!
text_corpus = "'ach cha'logh nItebHa' 'ej mIw vIghoS 'e' vIghoS, 'each vIghoS 'ej cha'logh vIghoS"
model_path = "klingon_ngram.pkl"

nmb.build_model(text_corpus)
nmb.save_model(model_path)

# Using the new model via QualityEvaluator instance

evaluator = QualityEvaluator()
evaluator.add_model(lang="klingon", model_path="klingon_ngram.pkl")

# NB! For custom languages not supported by langdetect,
# it is paramount to pass it along with `lang` parameter!
score = evaluator.get_probability(
    text="vaj nItebHa'vam vIghoS,",
    lang="klingon",
    length_limit=10
)
print(score)
```

**Output:**

```bash
0.99999999999107
```
</details>
