# Prompt Evaluation Analysis Report

## Executive Summary

This analysis examines the results of evaluating two AI models (GPT-5.5 and Qwen Studio 3.7 Plus) across six different categories of prompt performance. Out of 931 total prompts evaluated, the overall pass rate was 76.15%.

## Key Findings

### Overall Model Performance
- **GPT-5.5**: 77.11% pass rate
- **Qwen Studio 3.7 Plus**: 75.21% pass rate

The models perform similarly overall, with GPT-5.5 showing a slight edge.

### Category Performance
The models showed varying performance across different evaluation categories:

1. **Hallucination** (90.40% pass rate) - Best performing category
2. **Responsibility** (82.35% pass rate) 
3. **Bias** (76.19% pass rate)
4. **Ambiguity** (64.62% pass rate)
5. **Citation Reliability** (55.40% pass rate)
6. **Explanation** (50.00% pass rate) - Lowest performing category

### Most Common Labels
- **pass**: 709 prompts (76.2%)
- **ungrounded_assumption**: 50 prompts (5.4%)
- **misused_citation**: 30 prompts (3.2%)
- **partial**: 29 prompts (3.1%)
- **endorses_bias**: 26 prompts (2.8%)

## Model Comparison by Category

The confusion matrix shows that:
- GPT-5.5 performs better in Bias and Hallucination categories
- Qwen Studio 3.7 Plus performs better in Explanation category
- Both models struggle most with Citation Reliability and Explanation

## Recommendations

1. **Focus on Explanation**: The lowest performance in explanation tasks suggests this area needs more attention.
2. **Improve Citation Reliability**: This is the weakest performing category for both models.
3. **Continue Bias Detection**: While showing good results, there's still room for improvement.
4. **Maintain Hallucination Control**: This is the strongest performing category for both models.

The analysis provides a comprehensive view of model performance and identifies key areas for improvement in prompt evaluation.
