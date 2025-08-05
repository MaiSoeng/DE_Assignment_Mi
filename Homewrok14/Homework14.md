# Amazon EMR & Spark Homework

This report summarizes the data analysis tasks completed using the Iris flower dataset and the Gutenberg text dataset. It includes step-by-step processes, code snippets, analytical insights, and reflections on challenges encountered.



## Part 1. Iris Dataset Analysis

### Step-by-Step Process and Code Snippets

1. **Download the Dataset**
    Visit the UCI Machine Learning Repository and download the Iris dataset from the link: https://archive.ics.uci.edu/dataset/53/iris

   The dataset schema is also available on the same page and includes the following variables:

   | Variable Name | Type        | Unit | Description                                    |
   | ------------- | ----------- | ---- | ---------------------------------------------- |
   | sepal length  | Continuous  | cm   | Length of sepal                                |
   | sepal width   | Continuous  | cm   | Width of sepal                                 |
   | petal length  | Continuous  | cm   | Length of petal                                |
   | petal width   | Continuous  | cm   | Width of petal                                 |
   | class         | Categorical | –    | Species label (Setosa, Versicolour, Virginica) |

2. **Upload the Dataset to AWS S3**

   - Log into the AWS Console.

   - Navigate to Amazon S3 and create a new bucket. For instance, to complete this assignment, the S3 bucket is called `assignment14irisdatasets`.

   - Upload the `iris.data` file directly into this bucket.

     

3. **Access the Dataset in PySpark**
    After the dataset is uploaded to S3, use the following Python code (with PySpark and Boto3) to programmatically download and process the dataset as a temporary SQL table:

   ```python
   import boto3
   from pyspark.sql import SparkSession
   from pyspark.sql.types import StructType, StructField, StringType, FloatType
   
   spark = SparkSession.builder.appName("S3 iris").getOrCreate()
   sc = spark.sparkContext
   
   # get the iris data from the specific s3 bucket
   s3 = boto3.client("s3")
   bucket_name = "assignment14irisdatasets"
   file_name = "iris.data"
   s3.download_file(bucket_name, file_name, file_name)
   
   # the schema of the iris data
   schema = StructType([
       StructField("sepal_length", FloatType(), True),
       StructField("sepal_width", FloatType(), True),
       StructField("petal_length", FloatType(), True),
       StructField("petal_width", FloatType(), True),
       StructField("class", StringType(), True),
   ])
   
   # read the iris data from the specific s3 bucket as dataframe
   df = spark.read.csv(file_name, header = False, schema = schema)
   
   # turn the dataframe into a temporary table
   df.createOrReplaceTempView("iris")
   ```

4. ****

   **Data Analysis**

   Task 1: To count the number of each species in the dataset, execute the code below:

   ```python
   # run the SQL search
   query = """SELECT class, COUNT(*) as count
              FROM iris 
              GROUP BY class"""
   result = spark.sql(query)
   result.show()
   ```

   The result of the code is shown below:

   ![](H:\DE\DE Lecture\Homewrok14\9430af22536004d24896a46a51f8ae2d.png)

  It can be concluded that the Iris dataset contains three distinct species: *Iris setosa*, *Iris versicolor*, and *Iris virginica*. Each species is equally represented in the dataset, with 50 samples per class.



Task 2: To find the average petal length for each species, execute the code below:

```python
#2. find the average sepal length of each class
query = """
        SELECT class, AVG(petal_length) as avg_petal_length
        FROM iris
        GROUP BY class
        """
result = spark.sql(query)
result.show()
```

The result of the code is shown below:

![](H:\DE\DE Lecture\Homewrok14\65ddcc51111e94c530f009388925c57c.png)

It can be concluded that the average petal lengths for the three Iris species are approximately 5.55 cm for Iris virginica, 1.46 cm for Iris setosa, and 4.26 cm for Iris versicolor.



Task 3: To identify the species with the maximum average sepal width, execute the code below:

```python
#3. find the species with maximum average sepal width
# calculate the average sepal width for each class and order by descending order, then select the top 1
query = """
        SELECT class, AVG(sepal_width) as avg_sepal_width
        FROM iris
        GROUP BY class
        ORDER BY avg_sepal_width DESC
        LIMIT 1
        """
result = spark.sql(query)
result.show()

```

The result of the code is shown below:

![](H:\DE\DE Lecture\Homewrok14\ff5b8628f2b069412d705b0faf1e325c.png)

It can be concluded from the analysis that Iris setosa has the maximum average sepal width, which is approximately 3.42 cm.



5. **Challenges and Solution**

   **Challenge:**
    Initially, when attempting to identify the species with the largest average sepal width, the `MAX` function was applied after calculating the average sepal width. However, this approach only returns the maximum value itself and does not retain the associated species information, making it impossible to determine which species the value belongs to.

   **Solution:**
    To correctly identify the species with the highest average sepal width, the data was first grouped by species and the average sepal width for each group was calculated. The results were then sorted in descending order based on the average sepal width. By selecting the first row of the sorted result, both the maximum value and the corresponding species could be accurately acquired.



## Part 2. Gutenberg Dataset Analysis

### Step-by-Step Process and Code Snippets

1. **Download the Dataset**

   Visit the Gutenberg website: https://www.gutenberg.org/, and randomly choose an e-book and download it in txt format. The book I chose for this analysis is A Room with a View.

2. **Upload the Dataset to AWS S3**
   - Log into the AWS Console.
   - Navigate to Amazon S3 and create a new bucket. For instance, to complete this assignment, the S3 bucket is called `assignment14gutenberg`.
   - Upload the `a_room_with_a_view.txt` file directly into this bucket.

3. **Access the Dataset in PySpark**
    After the dataset is uploaded to S3, use the following Python code (with PySpark and Boto3) to programmatically download and process the dataset as dataframe:

   ```python
   from pyspark.sql import SparkSession
   from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
   from pyspark.sql import functions as f
   from pyspark.ml.feature import StopWordsRemover
   from pyspark.sql import Row
   import boto3
   
   spark = SparkSession.builder.appName("gutenberg").getOrCreate()
   sc = spark.sparkContext
   
   # get gutenberg data from s3
   s3 = boto3.client("s3")
   bucket_name = "assignment14gutenberg"
   file_name = "a_room_with_a_view.txt"
   s3.download_file(bucket_name, file_name, file_name)
   
   # task a
   df = spark.read.text(file_name).withColumnRenamed("value", "text")
   
   # check if the file is read correctly
   df.show(10)
   ```

   

4. ****

   ****

   **Data Analysis**

Task b: To determine the frequency of each unique word within the selected work, execute the following code:

```python
# determine the frequency of each unique word within the text
# first, perform word cleaning
# perform lowercasing, splitting, and removing stop words
df_processed = df.select(f.split(f.lower(f.regexp_replace("text", "[^a-zA-Z0-9]", " ")), r"\s+").alias("text"))
remover = StopWordsRemover(inputCol = "text", outputCol = "text_cleaned")
df_cleaned = remover.transform(df_processed)

# explode the list of words into single word per row and filter out empty words
df_cleaned = df_cleaned.select(f.explode("text_cleaned").alias("words"))
df_cleaned = df_cleaned.drop("text").filter(f.col("words").rlike(r"^[a-z]+$"))

# count the frequency of each word (task b)
count_df = df_cleaned.groupBy("words").count()
count_df.show(10)
```

The result of the code is:

![](H:\DE\DE Lecture\Homewrok14\df81b85440e5062092d964644bff2e89.png)



Task c: Based on the task b, we can extract the top 100 most frequent words by executing the following code:

```python
# sort the words by frequency in descending order (task c)
word_freq = count_df.orderBy(f.col("count").desc()).limit(100)
word_freq.show(100, truncate = False)
```

The complete result of the code can be seen in the gutenberg.ipynb. Part of the result will be shown below:

![](H:\DE\DE Lecture\Homewrok14\e475e40b337f05d2a7c99e7090593783.png)

It can be concluded from the result that prominent character names like "Lucy", "George", "Freddy" appear frequently in the text. Meanwhile, words such as "said", "oh", "say" occur with high frequency in the text as well.

Based on the result, the word frequency analysis share significant insights of the text, including:

1. Character-Centric Narrative:

   In the text, prominent character names appear with high occurrence, indicating that multiple individuals play significant part in the text, which may be involved in complex social interactions. "Lucy" appears with highest frequency, implying that it may be the main character of the text.

2. Dialogue-Heavy Structure:

   In the text, words like "said", "oh", "say" appear with high frequency. These words show that the text may be rich in dialogue or internal thought. 

3. Focus on Relationships:

   In the text, relationship-related words such as "mother", "people", "man" appear with high occurrence. It may imply that this text based mostly on social relationships, like family relationship or interpersonal interactions, most likely to be engaged in romantic relationship.



Task d: To find and show the sentences a list of predefined word appear in, execute the following code:

```python
# as for defined words, find and display the sentences they appear in
# split the text into sentences
sentence_df = df.select(f.explode(f.split(f.col("text"), r'[\.\?\!]\s+')).alias("sentence")).filter(f.col("sentence") != "")
sentence_df.show(10, truncate = False)

# find the sentences that contain a list of words
word_list = ["first", "world", "day"]
for word in word_list:
    word_sentence = sentence_df.filter(f.col("sentence").contains(word))
    word_sentence.show(10, truncate = False)
```

The results can be found in gutenberg.ipynb. Part of the results are demonstrated here:

![](H:\DE\DE Lecture\Homewrok14\bfe41bd4c2b36719e20951250297d88a.png)



Task e: To calculate the average word length and distribution of word lengths in the text, execute  the code below:

```python
# calculate the average word length and the distribution of word lengths in the text (task e)
# calculate the average word length
word_length = df_cleaned.withColumn("word_length", f.length("words"))
word_length_avg = word_length.select(f.expr("AVG(word_length) as avg_word_length"))
word_length_avg.show()

# find the distribution of word lengths in the text
word_length_distribution = word_length.groupBy("word_length").count()
word_length_distribution.show()
```

![](H:\DE\DE Lecture\Homewrok14\afb83069f42af1d72de0c4d6d24156d0.png)

It can be concluded from the result that the average word length is approximately 5.77. Meanwhile, words with word length 4, 5, 6 appear more than 5000 times in the text.



Task e: To find the co-occurrence word with a 5-word window, execute the following code:

```python
# Identify word co-occurrences within a 5-word window and analyze their significance
# add sentence_id to the dataframe
sentence_df = sentence_df.withColumn("sentence_id", f.monotonically_increasing_id())

# break down the sentences to each word, and give out the word index
# remove stop words
word_df = sentence_df.select("sentence_id", f.split(f.lower(f.regexp_replace("sentence", "[^a-zA-Z0-9]", " ")), r"\s+").alias("text"))
remover = StopWordsRemover(inputCol = "text", outputCol = "text_cleaned")
word_df = remover.transform(word_df)

# explode the list of words into word index and word, and filter out empty words
word_df = word_df.select("sentence_id", f.posexplode("text_cleaned").alias("word_index", "word")).filter(f.col("word").rlike(r"^[a-z]+$"))

# find the co-occurrences of words within a 5-word window
cooccur_df = word_df.alias("a").join(word_df.alias("b"), \
    on = [f.col("a.sentence_id") == f.col("b.sentence_id"), \
        f.col("a.word_index") < f.col("b.word_index"), \
        f.col("b.word_index") - f.col("a.word_index") <= 5])

cooccur_df = cooccur_df.select(f.col("a.word").alias("word1"), f.col("b.word").alias("word2")) \
    .groupBy("word1", "word2").count()
cooccur_df = cooccur_df.orderBy(f.col("count").desc())
cooccur_df.show()

```

The result of the code is shown below:

![](H:\DE\DE Lecture\Homewrok14\71174f07a489cb12ff75eb8e26f525a9.png)

The word co-occurrence analysis within a 5-word window reveals several significant patterns in the text. Notably, miss-Bartlett, miss-Lavish frequently appear in the 5-word window, suggesting strong character interactions and female social relationships in this text.

Frequent pairs like said-miss, said-mr, said-Barlett also indicates that the text is rich in dialogue narratives.

Additionally, frequent pairs like drawing-room, summer-street imply that the text include environmental settings and descriptions.



**Data aggregation analysis:**

Alongside the data analysis mentioned above, other analysis are also conducted to find interesting patterns and insights to this work.

The first analysis is to find the total word count and average word length in each chapter. First, we should divide the book into different chapters and conduct the analysis:

```python
# divide the text into chapter_id, chapter_text
# Concatenate the entire book into a single string
full = df.agg(
    f.concat_ws("\n", f.collect_list("text")).alias("full_text")
)

# Split the text into chapters using regex 
chap_df = full.select(
    f.explode(
        f.split(f.col("full_text"), r"(?=Chapter\s+[IVX]+)")
    ).alias("chapter_text")
)

# Remove empty chapters, content titles, and assign chapter_id
chapter_df = chap_df \
    .filter(f.trim(f.col("chapter_text")) != "") \
    .filter(f.length(f.col("chapter_text")) > 1000) \
    .filter(f.col("chapter_text").rlike(r"Chapter\s+[IVX]+")) \
    .withColumn("chapter_id", f.monotonically_increasing_id()) \
    .select("chapter_id", "chapter_text")
# Display
chapter_df.show(1000, truncate=False)

```

Then, we can do word count and average word length calculation based on different chapters.

```python
# do data aggreation to find interesting patterns or insights specific to the selected work
# find the total word count and average word length used in each chapter, and order by the average word length
# first, explode the chapter_text into words
# format (chapter_id, words)
chapter_word_df = chapter_df.select("chapter_id", \
    f.explode(f.split(f.lower(f.regexp_replace("chapter_text", "[^a-zA-Z0-9]", " ")), r"\s+")).alias("words"))


# then, do the word count and average word length
# format(chapter_id, word_count, avg_word_length)
chapter_word_count = chapter_word_df.groupBy("chapter_id")\
    .agg(f.count(f.col("words")).alias("word_count"), \
        f.avg(f.length(f.col("words"))).alias("avg_word_length"))

# order by the average word length
chapter_word_count = chapter_word_count.orderBy(f.desc("word_count")).show()
```

The results are shown below:

![](H:\DE\DE Lecture\Homewrok14\b86684888e5a2086bcb5ab19396e3657.png)

Based on the result, chapter 17 has 5225 words, which is the longest chapter of the book. This may suggest that this chapter is rich in description, narratives, or plot development. Chapter 16 has the shortest average word length and word count, indicating that it contains more dialogue narratives.



The next analysis is the stop words analysis of each chapter. It is aimed to count the stop words and find the ratio of the stop words in each chapter.

```python
# find the ratio of the stop words used in each chapter
stopwords = StopWordsRemover().getStopWords()
chapter_words = chapter_word_df.withColumn("is_stop_word", f.col("words").isin(stopwords))

# calculate the ratio of the stop words used in each chapter
word_count_ratio = chapter_words.groupBy("chapter_id")\
    .agg(f.count(f.col("words")).alias("total_word_count"), \
        f.sum(f.when(f.col("is_stop_word"), 1).otherwise(0)).alias("stop_word_count")) \
            .select("chapter_id", "total_word_count", "stop_word_count", f.expr("stop_word_count / total_word_count as stop_word_ratio")) 

word_count_ratio.orderBy(f.desc("stop_word_ratio")).show()
```



The result of the code is shown below:

![](H:\DE\DE Lecture\Homewrok14\7876f86f692648d0a9cf0ac9ff98c2d6.png)

Based on the stop word analysis, Chapter 16 has the highest stop word ratio (58.13%), suggesting a more conversational style with frequent use of common stop words. In contrast, Chapter 19 shows the lowest stop word ratio (46.89%), indicating a denser use of meaningful content words. This contrast reflects the diversity of style across chapters, where some are more focused on dialogue, while others emphasize thematic content.



The next analysis is trying to analyze the emotion of each chapter. In this analysis, a dictionary combing positive and negative words with different scores are given to calculate the emotion scores of each chapter:

```python
# build dictionaries with positive and negative words
# positive dictionary
positive_words = [
    Row(words="good", score=2),
    Row(words="excellent", score=3),
    Row(words="happy", score=2),
    Row(words="amazing", score=3),
    Row(words="wonderful", score=3)
]

# negative dictionary
negative_words = [
    Row(words="bad", score=-2),
    Row(words="terrible", score=-3),
    Row(words="sad", score=-2),
    Row(words="awful", score=-3),
    Row(words="horrible", score=-3)
]

# combine the dictionaries and create the dataframe
all_sentiment_words = positive_words + negative_words
sentiment_df = spark.createDataFrame(all_sentiment_words)

# use join to find the emotion words
chapter_emotion_words = chapter_word_df.join(sentiment_df, on = "words", how = "inner")

# calculate the emotion scores
chapter_scores = chapter_emotion_words.groupBy("chapter_id") \
    .agg(f.sum(f.col("score")).alias("chapter_emotion_scores")) \
    .orderBy(f.desc("chapter_emotion_scores"))
chapter_scores.show() 
```

The result of the analysis is shown below:

![](H:\DE\DE Lecture\Homewrok14\b267e821712bee65436d2dc145eb71f7.png)

Based on the emotion analysis, Chapter 7 has the highest emotion scores (31), suggesting a more positive narrative style in the chapter. In contrast, Chapter 14 has the lowest emotion scores (-7), indicating that this chapter may be negative in character emotions or narrative style.



  The final analysis is the sentence analysis on each chapter. To conduct the analysis, execute the following code.

```python
# split the chapter text into sentences
# format (chapter_id, sentences)
chapter_sentences = chapter_df.select("chapter_id", \
    f.explode(f.split(f.col("chapter_text"), r'[\.\?\!]\s+')).alias("sentences")) \
        .filter(f.trim(f.col("sentences")) != "") \

# count the number of chapter sentences, total sentences length, and average length
chapter_sentences = chapter_sentences.groupBy("chapter_id") \
    .agg(f.count("*").alias("num_sentences"), \
        f.sum(f.length("sentences")).alias("sentences_length"), \
        f.avg(f.length("sentences")).alias("avg_length_sentences")) 

chapter_sentences.orderBy(f.desc("num_sentences")).show()
chapter_sentences.orderBy(f.desc("sentences_length")).show()
chapter_sentences.orderBy(f.desc("avg_length_sentences")).show()
```

The result are shown as follows:

![](H:\DE\DE Lecture\Homewrok14\24bccfafdbe5c908ff408503f98fc6fd.png)

![](H:\DE\DE Lecture\Homewrok14\0e524517cdd24b25d6a9ae0ab1108a00.png)

![](H:\DE\DE Lecture\Homewrok14\6e3d8d92d36f0abb78f7f9ba7f47135a.png)

The analysis of sentence lengths reveals stylistic variations across chapters. Chapter 19 stands out with the highest average sentence length (119.48), suggesting a more descriptive style. In contrast, Chapter 11 features the shortest average sentence length (59.70), likely reflecting a dialogue-heavy section. Chapters such as 18, which has the highest number of sentences, indicate a dense narrative structure with moderate sentence complexity.



5. **Challenges and Solution**

**Challenge 1:**
 Initially, when attempting to perform word count, the empty words can always appear at the top of the sorted list.  

**Solution:**
To effectively remove empty words, instead of using a simple inequality check (`f.col("word") != ""`), a regular expression pattern `f.col("word").rlike(r"^[a-z]+$")` was applied.  This approach ensures that only valid lowercase alphabetic tokens are kept, effectively filtering out empty words.



**Challenge 2:**
 Initially, when attempting to split the chapters, the chapter title in the content can always appear at the top of the divided chapter text.  

**Solution:**
To effectively remove the chapter title in the content, a filter expression `filter(f.length(f.col("chapter_text")) > 1000)` is applied. In this way, as the title in the content contains words less than a certain threshold. Therefore, applying a large filter threshold can effectively eliminate the title in the content. 

