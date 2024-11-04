import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Define skills lists
ai_ml_skills = [
    "Machine Learning Algorithms", "Data Preprocessing", "Model Evaluation and Tuning",
    "Feature Engineering", "Hyperparameter Optimization", "Natural Language Processing (NLP)", "Deep Learning",
    "Large Language Models", "RAG and Fine Tuning", "Data Visualization", "MLOps", "LLMOps",
    "Computer Vision", "Conversational AI", "AI Governance, Ethics and Fairness"
]

pm_skills = [
    "Feature Specification and Prioritization", "Product Delivery", "Validation and Quality Assurance",
    "Fluency with Data", "Voice of Customer", "User Experience (UX) Design", 
    "Business Outcome Ownership", "Product Vision and Roadmapping", "Strategic Impact",
    "Managing Up", "Stakeholder Engagement", "Team Leadership"
]

# Title and intro
st.title("AI Product Manager Skill Competencies Shape")

# Skill selection with checkboxes and sliders
skill_scores = {}

# AI/ML Skills Section with "Select All" option
st.sidebar.header("AI/ML Skills")
select_all_ai = st.sidebar.checkbox("Select All AI/ML Skills", value=False)
for skill in ai_ml_skills:
    col1, col2 = st.sidebar.columns([2, 1])
    with col1:
        selected = col1.checkbox(skill, key=f"ai_{skill}", value=select_all_ai)
    with col2:
        if selected:
            skill_scores[skill] = col2.slider(f"Score for {skill}", 1, 10, 5, key=f"slider_ai_{skill}")

# Product Management Skills Section with "Select All" option
st.sidebar.header("Product Management Skills")
select_all_pm = st.sidebar.checkbox("Select All Product Management Skills", value=False)
for skill in pm_skills:
    col1, col2 = st.sidebar.columns([2, 1])
    with col1:
        selected = col1.checkbox(skill, key=f"pm_{skill}", value=select_all_pm)
    with col2:
        if selected:
            skill_scores[skill] = col2.slider(f"Score for {skill}", 1, 10, 5, key=f"slider_pm_{skill}")

# Placeholder for spider chart
def plot_spider_chart(skill_scores):
    # Separate AI/ML and PM skills for color differentiation
    ai_labels = [skill for skill in skill_scores.keys() if skill in ai_ml_skills]
    pm_labels = [skill for skill in skill_scores.keys() if skill in pm_skills]
    
    ai_values = [skill_scores[skill] for skill in ai_labels]
    pm_values = [skill_scores[skill] for skill in pm_labels]

    labels = ai_labels + pm_labels
    values = ai_values + pm_values
    
    # Radar chart setup
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Closing the circle for each set separately, with safe indexing
    ai_angles = angles[:len(ai_labels)] + [angles[0]] if ai_labels else []
    pm_angles = angles[len(ai_labels):] + [angles[len(ai_labels)]] if pm_labels else []
    ai_values_circle = ai_values + [ai_values[0]] if ai_values else []
    pm_values_circle = pm_values + [pm_values[0]] if pm_values else []
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plot AI/ML skills in pink if available
    if ai_angles and ai_values_circle:
        ax.fill(ai_angles, ai_values_circle, color='pink', alpha=0.25)
        ax.plot(ai_angles, ai_values_circle, color='pink', linewidth=2, label="AI/ML Skills")
    
    # Plot PM skills in blue if available
    if pm_angles and pm_values_circle:
        ax.fill(pm_angles, pm_values_circle, color='blue', alpha=0.25)
        ax.plot(pm_angles, pm_values_circle, color='blue', linewidth=2, label="Product Management Skills")
    
    # Customize labels without any degree symbols
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels([])  # Remove angle tick labels

    # Position labels outside the plot and avoid rotating text
    label_radius = 11
    for i, label in enumerate(labels):
        angle_rad = angles[i]
        ha = "right" if np.pi / 2 <= angle_rad <= 3 * np.pi / 2 else "left"  # Align text based on position

        ax.text(
            angle_rad, label_radius, label, ha=ha, va="center",
            rotation_mode='anchor', fontsize=10, color="black"
        )

    # Add legend
    ax.legend(loc="upper right", bbox_to_anchor=(1.7, 1.7))
    
    st.pyplot(fig)

# Generate spider chart if any skills are selected
if skill_scores:
    plot_spider_chart(skill_scores)
else:
    st.warning("Please select and score at least one skill to generate the chart.")
