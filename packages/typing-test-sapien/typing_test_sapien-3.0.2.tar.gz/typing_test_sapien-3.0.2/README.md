# Typing Speed Test with a Knowledge Twist

This project combines a fun typing speed test with an engaging knowledge dataset to measure typing speed (Words Per Minute) and accuracy while learning something new.

## Features
- **Typing Speed Measurement**: Calculates Words Per Minute (WPM) for each test.
- **Accuracy Calculation**: Computes the percentage of correctly typed words.
- **Knowledge Dataset**: Sentences are sourced from a specially curated dataset, including:
  - **Fun Facts**: Trivia that will amaze you.
  - **Health Tips**: Simple tips for a better lifestyle.
  - **Science & Math Wonders**: Discover fascinating facts.
  - **Famous Quotes**: Iconic sayings from great minds.
  - **Movie Dialogues**: Relive legendary cinematic moments.
- **Blind Mode**: Optional feature to hide user input for an added challenge.
- **Bar Chart Visualization**: Summarizes session performance with a bar chart.

## How It Works
1. **Sentence Selection**: Random sentences are selected from the knowledge dataset. [*You’ll absolutely love this!*]
2. **Timing**: Tracks the time taken for the user to type the sentences.
3. **WPM and Accuracy**: Calculates WPM and accuracy based on input.
4. **Session Summary**:
   - Average typing speed.
   - Average accuracy.
   - Final result (PASS or FAIL).

## Installation
Install the required package using pip:
```bash
pip install typing-test-sapien
```
## Execution
```bash
typing-test-sapien

or

typing-test-sapien 5 2 yes
```
   - `5`: Number of tests.
   - `2`: Sentences per test.
   - `yes`: Enables blind mode.

## Example Output
```
Final Results
-------------
Average Accuracy:         85.50%
Average Typing Speed:     72.00 WPM
Result:                   PASS

Session Progress Bar Chart
-------------------------------------------------
WPM       | T1    T2    T3    T4    T5    
-------------------------------------------------
80        |  #     #     #                   
75        |  #     #     #                   
50        |        #     #                   
-------------------------------------------------
```

## Requirements
- Python 3.x
- `getpass` module (comes pre-installed with Python).

## License
This project is licensed under the MIT License.
