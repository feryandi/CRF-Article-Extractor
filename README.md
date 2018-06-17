# Tool: CRF Article Extractor
This is an experiment on CRF for article content extraction. When you are trying to get clean data from a website, usually the extraction is getting in the way. For example, I want to extract news data from certain online media. It's getting to the point where I need to create automatic content extraction instead of defining XPath for every website out there. This is the goal of the tool, to easily extract article content with minimal errors.

## How to Use
Install all the needed requirement first.

To create a model, use this command
```python generate_model.py```
It will generate model on model folder as well as pickled training-ready data from dataset in pickle folder.

To use it, use the command
```python extract.py --url some.url.com```

Note that this is not production ready thus need more implementation in order to make it ready for use. 

## Experiment
I use CRFSuite with binding for Python (python-crfsuite) implementation for the CRF and using LBFGS as algorithm. The train is only 25 data, validation 10 data, and test 5 data of website that never seen before on train data. While the data is really small, it's have a decent performance overall.

The features are: tag, parent tag, tag chain (tag and parent tag), length text before, length text after, length text content, and word count.

Compared to similar CRF experimentation on [Victor: the Web-Page Cleaning Tool](https://pdfs.semanticscholar.org/5462/d15610592394a5cd305d44003cc89630f990.pdf) this one have greater perfomance (based on precision and recall) and less feature which makes it more general (test data contains 4 different languages) but since the dataset on this one is really small, I couldn't guarantee it.

### Validation Data Result
#### Evaluation
<table>
<colgroup>
  <col style="text-align:left;"/>
  <col style="text-align:left;"/>
</colgroup>
<thead>
<tr>
    <th style="text-align:left;"></th>
    <th style="text-align:left;">%</th>
</tr>
</thead>
<tbody>
<tr>
    <td style="text-align:left;">Precision</td>
    <td style="text-align:left;">96</td>
</tr>
<tr>
    <td style="text-align:left;">Recall</td>
    <td style="text-align:left;">86</td>
</tr>
<tr>
    <td style="text-align:left;">F1</td>
    <td style="text-align:left;">91</td>
</tr>
<tr>
    <td style="text-align:left;">Support</td>
    <td style="text-align:left;">113</td>
</tr>
</tbody>
</table>

#### Confusion Matrix
<table>
<colgroup>
  <col style="text-align:left;"/>
  <col style="text-align:left;"/>
</colgroup>
<thead>
<tr>
    <th style="text-align:left;">content</th>
    <th style="text-align:left;">ignore</th>
</tr>
</thead>
<tbody>
<tr>
    <td style="text-align:left;">97</td>
    <td style="text-align:left;">16</td>
</tr>
<tr>
    <td style="text-align:left;">4</td>
    <td style="text-align:left;">9419</td>
</tr>
</tbody>
</table>

### Test Data Result
#### Evaluation
<table>
<colgroup>
  <col style="text-align:left;"/>
  <col style="text-align:left;"/>
</colgroup>
<thead>
<tr>
    <th style="text-align:left;"></th>
    <th style="text-align:left;">%</th>
</tr>
</thead>
<tbody>
<tr>
    <td style="text-align:left;">Precision</td>
    <td style="text-align:left;">91</td>
</tr>
<tr>
    <td style="text-align:left;">Recall</td>
    <td style="text-align:left;">93</td>
</tr>
<tr>
    <td style="text-align:left;">F1</td>
    <td style="text-align:left;">92</td>
</tr>
<tr>
    <td style="text-align:left;">Support</td>
    <td style="text-align:left;">76</td>
</tr>
</tbody>
</table>

#### Confusion Matrix
<table>
<colgroup>
  <col style="text-align:left;"/>
  <col style="text-align:left;"/>
</colgroup>
<thead>
<tr>
    <th style="text-align:left;">content</th>
    <th style="text-align:left;">ignore</th>
</tr>
</thead>
<tbody>
<tr>
    <td style="text-align:left;">71</td>
    <td style="text-align:left;">5</td>
</tr>
<tr>
    <td style="text-align:left;">7</td>
    <td style="text-align:left;">2640</td>
</tr>
</tbody>
</table>
