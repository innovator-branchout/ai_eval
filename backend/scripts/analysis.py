#!/usr/bin/env python3
"""
Analysis script for prompt evaluation data.
This script provides comprehensive analysis of prompt evaluation results.
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import sqlite3

# Add the backend directory to Python path so we can import database module
sys.path.append(str(Path(__file__).parent))

from database import connect, list_categories, list_models, list_labels


def get_analysis_data():
    """Fetch all data from the database for analysis."""
    with connect() as conn:
        # Get all prompts with their associated data
        query = """
        SELECT
            p.prompt_id,
            p.prompt_text,
            p.raw_output,
            p.label_id,
            l.label_name,
            l.status as label_status,
            l.severity,
            p.category_id,
            c.category_name,
            p.model_id,
            m.model_name,
            p.conversation_id
        FROM prompts p
        JOIN categories c ON p.category_id = c.category_id
        JOIN models m ON p.model_id = m.model_id
        JOIN labels l ON p.label_id = l.label_id
        ORDER BY p.conversation_id, p.prompt_number
        """

        df = pd.read_sql_query(query, conn)

    return df


def analyze_model_performance(df):
    """Analyze performance across different models."""
    print("=== MODEL PERFORMANCE ANALYSIS ===")

    # Overall performance by model
    model_stats = df.groupby('model_name').agg({
        'label_id': 'count',
        'label_status': 'mean'  # Proportion of passing labels
    }).rename(columns={'label_id': 'total_prompts', 'label_status': 'pass_rate'})

    print("\nOverall Model Performance:")
    print(model_stats)

    # Performance by category and model
    category_model_performance = df.pivot_table(
        index='category_name',
        columns='model_name',
        values='label_status',
        aggfunc='mean',
        fill_value=0
    )

    print("\nPerformance by Category and Model:")
    print(category_model_performance)

    return model_stats, category_model_performance


def analyze_category_distribution(df):
    """Analyze distribution of labels across categories."""
    print("\n=== CATEGORY DISTRIBUTION ANALYSIS ===")

    # Label distribution by category
    category_label_dist = df.pivot_table(
        index='category_name',
        columns='label_name',
        values='prompt_id',
        aggfunc='count',
        fill_value=0
    )

    print("Label distribution by category:")
    print(category_label_dist)

    return category_label_dist


def generate_visualizations(df):
    """Generate various visualizations for the data."""
    print("\n=== GENERATING VISUALIZATIONS ===")

    # Create output directory for plots
    plot_dir = Path(__file__).parent.parent / "outputs" / "plots"
    plot_dir.mkdir(exist_ok=True)

    # 1. Performance by model
    plt.figure(figsize=(12, 8))

    # Subplot 1: Overall performance by model
    plt.subplot(2, 2, 1)
    model_stats = df.groupby('model_name').agg({
        'label_status': 'mean'
    }).rename(columns={'label_status': 'pass_rate'})

    bars = plt.bar(range(len(model_stats)), model_stats['pass_rate'])
    plt.xticks(range(len(model_stats)), model_stats.index, rotation=45)
    plt.ylabel('Pass Rate')
    plt.title('Model Performance by Pass Rate')
    plt.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, model_stats['pass_rate'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.2f}', ha='center', va='bottom')

    # 2. Performance by category
    plt.subplot(2, 2, 2)
    category_stats = df.groupby('category_name').agg({
        'label_status': 'mean'
    }).rename(columns={'label_status': 'pass_rate'})

    bars = plt.bar(range(len(category_stats)), category_stats['pass_rate'])
    plt.xticks(range(len(category_stats)), category_stats.index, rotation=45)
    plt.ylabel('Pass Rate')
    plt.title('Category Performance by Pass Rate')
    plt.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, category_stats['pass_rate'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.2f}', ha='center', va='bottom')

    # 3. Category distribution
    plt.subplot(2, 2, 3)
    category_counts = df['category_name'].value_counts()
    bars = plt.bar(range(len(category_counts)), category_counts.values)
    plt.xticks(range(len(category_counts)), category_counts.index, rotation=45)
    plt.ylabel('Number of Prompts')
    plt.title('Distribution of Prompts by Category')
    plt.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, category_counts.values)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(value), ha='center', va='bottom')

    # 4. Label distribution
    plt.subplot(2, 2, 4)
    label_counts = df['label_name'].value_counts()
    bars = plt.bar(range(len(label_counts)), label_counts.values)
    plt.xticks(range(len(label_counts)), label_counts.index, rotation=45)
    plt.ylabel('Number of Prompts')
    plt.title('Distribution of Prompts by Label')
    plt.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, label_counts.values)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(value), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(plot_dir / "performance_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()

    print("Saved performance analysis plots to:", plot_dir / "performance_analysis.png")

    # 5. Confusion matrix for model vs category
    plt.figure(figsize=(12, 10))

    # Create a pivot table for confusion matrix
    confusion_data = df.pivot_table(
        index='model_name',
        columns='category_name',
        values='label_status',
        aggfunc='mean'
    )

    sns.heatmap(confusion_data, annot=True, cmap='Blues', fmt='.2f')
    plt.title('Model Performance by Category (Pass Rate)')
    plt.xlabel('Category')
    plt.ylabel('Model')
    plt.tight_layout()
    plt.savefig(plot_dir / "confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()

    print("Saved confusion matrix plot to:", plot_dir / "confusion_matrix.png")


def generate_detailed_report(df):
    """Generate a detailed report of the evaluation."""
    print("\n=== DETAILED EVALUATION REPORT ===")

    total_prompts = len(df)
    print(f"Total prompts evaluated: {total_prompts}")

    # Get unique categories and models
    categories = df['category_name'].unique()
    models = df['model_name'].unique()

    print(f"\nCategories: {', '.join(categories)}")
    print(f"Models: {', '.join(models)}")

    # Calculate overall pass rate
    overall_pass_rate = df['label_status'].mean()
    print(f"\nOverall pass rate: {overall_pass_rate:.2%}")

    # Pass rates by model
    print("\nPass rates by model:")
    for model in models:
        model_pass_rate = df[df['model_name'] == model]['label_status'].mean()
        print(f"  {model}: {model_pass_rate:.2%}")

    # Pass rates by category
    print("\nPass rates by category:")
    for category in categories:
        category_pass_rate = df[df['category_name'] == category]['label_status'].mean()
        print(f"  {category}: {category_pass_rate:.2%}")

    # Most common labels
    print("\nMost common labels:")
    label_counts = df['label_name'].value_counts()
    for label, count in label_counts.head(5).items():
        percentage = (count / total_prompts) * 100
        print(f"  {label}: {count} ({percentage:.1f}%)")


def main():
    """Main function to run all analysis."""
    print("Starting prompt evaluation data analysis...")

    try:
        # Get the data
        df = get_analysis_data()

        if df.empty:
            print("No data found in database!")
            return

        print(f"Loaded {len(df)} prompts from database")

        # Generate detailed report
        generate_detailed_report(df)

        # Analyze model performance
        model_stats, category_model_performance = analyze_model_performance(df)

        # Analyze category distribution
        category_label_dist = analyze_category_distribution(df)

        # Generate visualizations
        generate_visualizations(df)

        print("\nAnalysis complete!")
        print("Generated plots saved to ./backend/output/plots/")


    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
