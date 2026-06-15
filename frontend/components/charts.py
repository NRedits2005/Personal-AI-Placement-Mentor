import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_readiness_gauge(score: float):
    """Generates a premium Gauge chart representing the AI Readiness Score."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall AI Readiness Index", 'font': {'size': 20, 'color': "#e2e8f0"}},
        number = {'font': {'color': "#00f2fe", 'size': 48}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#00f2fe"},
            'bgcolor': "rgba(30, 41, 59, 0.5)",
            'borderwidth': 2,
            'bordercolor': "#475569",
            'steps': [
                {'range': [0, 50], 'color': '#ef4444'},
                {'range': [50, 80], 'color': '#f59e0b'},
                {'range': [80, 100], 'color': '#22c55e'}
            ],
            'threshold': {
                'line': {'color': "#ffffff", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e2e8f0", 'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_skill_gap(skills_list: list):
    """Generates a horizontal bar chart showing skill gaps and priorities."""
    if not skills_list:
        return None
        
    df = pd.DataFrame(skills_list)
    # Color mapping for priorities
    color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"}
    
    fig = px.bar(
        df,
        y="skill",
        x=[1]*len(df), # equal width bars
        color="priority",
        orientation="h",
        text="status",
        color_discrete_map=color_map,
        title="Expected Skill Gaps by Priority",
        labels={"skill": "Skill Topic", "priority": "Priority Level"}
    )
    
    fig.update_traces(textposition='inside', textfont_size=12)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e2e8f0", 'family': "Inter"},
        xaxis_visible=False,
        yaxis={'categoryorder':'total ascending'},
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_coding_progress(solved_count: int):
    """Generates a radial/donut chart showing coding solve ratios."""
    labels = ['Solved Questions', 'Practice Targets']
    values = [solved_count, max(15 - solved_count, 0)] # Target is 15 questions
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.5,
        marker=dict(colors=['#10b981', '#3b82f6'])
    )])
    
    fig.update_layout(
        title="DSA Coding Milestone Progress",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e2e8f0", 'family': "Inter"},
        height=250,
        showlegend=True,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    return fig

def plot_readiness_trend(trend_data: list):
    """Generates a trend line chart showing weighted readiness components over time."""
    if not trend_data:
        return None
        
    df = pd.DataFrame(trend_data)
    df["Date"] = pd.to_datetime(df["timestamp"]).dt.strftime('%b %d %H:%M')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["overall_score"], name="Overall Readiness", line=dict(color="#00f2fe", width=4)))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["resume_score"], name="Resume Score", line=dict(color="#f59e0b", dash='dash')))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["coding_score"], name="Coding Accuracy", line=dict(color="#10b981", dash='dash')))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["technical_score"], name="Technical Mock", line=dict(color="#8b5cf6", dash='dash')))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["hr_score"], name="HR Mock", line=dict(color="#ec4899", dash='dash')))
    
    fig.update_layout(
        title="AI Readiness Improvement Trend",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30, 41, 59, 0.3)',
        font={'color': "#e2e8f0", 'family': "Inter"},
        yaxis=dict(title="Score (0-100)", range=[0, 105], gridcolor="#334155"),
        xaxis=dict(title="Progress Log", gridcolor="#334155"),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_weekly_progress(tasks_dict: dict):
    """Plots completion metrics per study plan week."""
    if not tasks_dict:
        return None
        
    weeks = []
    completion_rates = []
    
    for week_name, task_list in tasks_dict.items():
        weeks.append(week_name.split(":")[0]) # Shorten name (e.g. Week 1)
        total = len(task_list)
        completed = sum(1 for t in task_list if t.get("completed", False))
        rate = (completed / total * 100.0) if total > 0 else 0.0
        completion_rates.append(rate)
        
    df = pd.DataFrame({"Week": weeks, "Completion %": completion_rates})
    
    fig = px.bar(
        df,
        x="Week",
        y="Completion %",
        color="Completion %",
        color_continuous_scale="Viridis",
        title="Weekly Roadmap Task Completion Rates",
        range_y=[0, 105]
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e2e8f0", 'family': "Inter"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
