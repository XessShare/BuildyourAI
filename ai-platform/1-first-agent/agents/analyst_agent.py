"""
Analyst Agent - Data Analysis and Insights Extraction

Dieser Agent:
- Analysiert Datasets (CSV, JSON, Excel)
- Identifiziert Patterns und Trends
- Führt statistische Analysen durch
- Extrahiert actionable Insights
- Generiert Analytical Reports
- Analysiert Performance Metrics & KPIs
- Vergleicht Datasets über Zeit
"""

from typing import Dict, Any, List, Optional, Union
from .base_agent import BaseAgent
import pandas as pd
import numpy as np
from datetime import datetime
import json


class AnalystAgent(BaseAgent):
    """
    Spezialisiert auf Data Analysis und Insight Extraction

    Features:
    1. Dataset analysis (CSV, JSON, Excel)
    2. Pattern and trend detection
    3. Statistical analysis
    4. Insight extraction
    5. Performance metrics analysis
    6. Comparative analysis
    7. Report generation
    """

    def __init__(self):
        super().__init__(agent_type="analyst")

    def get_system_prompt(self) -> str:
        return """Du bist der Analyst Agent im J-Jeco System.

Deine Mission: Daten analysieren, Patterns erkennen und actionable Insights extrahieren.

ANALYSIS-PRINZIPIEN:

1. DATEN-VERSTÄNDNIS
   - Verstehe die Datenstruktur
   - Identifiziere Key Metrics
   - Erkenne Datenqualität
   - Identifiziere Anomalien

2. PATTERN DETECTION
   - Suche nach Trends
   - Identifiziere Korrelationen
   - Erkenne Saisonalität
   - Finde Outliers

3. STATISTISCHE RIGOROSITÄT
   - Nutze angemessene statistische Methoden
   - Berechne relevante Metriken
   - Bewerte Signifikanz
   - Dokumentiere Annahmen

4. INSIGHT GENERATION
   - Fokus auf Actionable Insights
   - "So what?" - Was bedeutet das?
   - Konkrete Empfehlungen
   - Priorisierung nach Impact

5. KONTEXT & BUSINESS LOGIC
   - Verstehe Business-Kontext
   - Interpretiere Zahlen im Kontext
   - Verbinde Data mit Zielen
   - Denke strategisch

6. KLARHEIT & KOMMUNIKATION
   - Visualisiere komplexe Daten
   - Erkläre für Non-Tech Audience
   - Strukturierte Reports
   - Executive Summaries

ANALYSIS-OUTPUT:
- Executive Summary (Key Findings)
- Detailed Analysis mit Zahlen
- Identified Patterns & Trends
- Statistical Insights
- Actionable Recommendations
- Next Steps & Priorities

SPEZIAL-FOKUS:
- KPI Performance Analysis
- Growth Metrics
- User Behavior Patterns
- Content Performance
- Investment ROI
- Tech Stack Efficiency
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Analyze data based on task type

        Args:
            task: {
                "type": "analyze_dataset" | "identify_patterns" | "analyze_performance",
                "data": DataFrame | dict | list,
                "metrics": ["metric1", "metric2"],  # optional
                "timeframe": "daily" | "weekly" | "monthly"  # optional
            }

        Returns:
            Analysis report with insights and recommendations
        """
        analysis_type = task.get("type", "analyze_dataset")

        if analysis_type == "analyze_dataset":
            return await self.analyze_dataset(task)
        elif analysis_type == "identify_patterns":
            return await self.identify_patterns(task)
        elif analysis_type == "analyze_performance":
            return await self.analyze_performance(task)
        elif analysis_type == "compare_data":
            return await self.compare_data(task)
        elif analysis_type == "calculate_statistics":
            return await self.calculate_statistics(task)
        else:
            return await self.general_analysis(task)

    async def analyze_dataset(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a dataset and extract insights

        Args:
            task: {
                "data": DataFrame or dict/list (will be converted),
                "name": "Dataset name",
                "focus_areas": ["growth", "patterns", "anomalies"]
            }

        Returns:
            Comprehensive dataset analysis
        """
        data = task.get("data")
        dataset_name = task.get("name", "Dataset")
        focus_areas = task.get("focus_areas", ["overview", "patterns", "insights"])

        # Convert data to DataFrame if needed
        df = self._prepare_dataframe(data)

        if df is None:
            return {
                "error": "Could not prepare data for analysis",
                "status": "failed"
            }

        # Generate dataset summary
        summary = self._generate_dataset_summary(df)

        # Build analysis prompt
        query = f"""
Analysiere folgenden Dataset: {dataset_name}

DATASET SUMMARY:
{summary}

FOKUS-BEREICHE:
{chr(10).join(f"- {area}" for area in focus_areas)}

ANALYSE-AUFGABEN:
1. OVERVIEW
   - Was sind die wichtigsten Metriken?
   - Wie ist die Datenqualität?
   - Welche Zeitspanne wird abgedeckt?

2. KEY FINDINGS
   - Was sind die auffälligsten Insights?
   - Welche Trends sind erkennbar?
   - Gibt es Anomalien oder Outliers?

3. PATTERNS & CORRELATIONS
   - Welche Patterns sind erkennbar?
   - Gibt es Korrelationen zwischen Variablen?
   - Saisonalität oder Zyklen?

4. ACTIONABLE INSIGHTS
   - Was bedeuten diese Findings?
   - Welche Handlungsempfehlungen ergeben sich?
   - Was sollte priorisiert werden?

5. NEXT STEPS
   - Welche weiteren Analysen sind sinnvoll?
   - Welche zusätzlichen Daten würden helfen?
   - Quick Wins und Long-term Actions

AUSGABE:
- Executive Summary (2-3 Sätze)
- Detailed Analysis
- Top 3-5 Key Insights
- Recommended Actions
- Next Steps

Sei spezifisch, nutze die konkreten Zahlen aus dem Summary.
"""

        analysis = await self.think(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "dataset_analysis",
            "dataset_name": dataset_name,
            "rows": len(df),
            "columns": list(df.columns),
            "summary": summary,
            "analysis": analysis,
            "analyzed_at": self._get_timestamp()
        }

    async def identify_patterns(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify patterns and trends in data

        Args:
            task: {
                "data": DataFrame or dict/list,
                "metric": "The metric to analyze for patterns",
                "timeframe": "daily" | "weekly" | "monthly"
            }

        Returns:
            Pattern analysis with trends
        """
        data = task.get("data")
        metric = task.get("metric", "value")
        timeframe = task.get("timeframe", "daily")

        df = self._prepare_dataframe(data)

        if df is None or metric not in df.columns:
            return {
                "error": f"Metric '{metric}' not found in data",
                "status": "failed"
            }

        # Calculate basic statistics
        stats = {
            "mean": float(df[metric].mean()),
            "median": float(df[metric].median()),
            "std": float(df[metric].std()),
            "min": float(df[metric].min()),
            "max": float(df[metric].max()),
            "range": float(df[metric].max() - df[metric].min())
        }

        # Identify trends (simple linear trend)
        if len(df) > 1:
            x = np.arange(len(df))
            y = df[metric].values
            trend = np.polyfit(x, y, 1)[0]  # Slope of linear fit
            stats["trend_direction"] = "increasing" if trend > 0 else "decreasing"
            stats["trend_strength"] = abs(float(trend))
        else:
            stats["trend_direction"] = "insufficient_data"
            stats["trend_strength"] = 0

        query = f"""
Pattern-Analyse für Metrik: {metric}

TIMEFRAME: {timeframe}
DATENPUNKTE: {len(df)}

STATISTIKEN:
- Durchschnitt: {stats['mean']:.2f}
- Median: {stats['median']:.2f}
- Standardabweichung: {stats['std']:.2f}
- Min: {stats['min']:.2f}
- Max: {stats['max']:.2f}
- Range: {stats['range']:.2f}
- Trend: {stats['trend_direction']} (Stärke: {stats['trend_strength']:.4f})

PATTERN-ANALYSE:
1. TREND-INTERPRETATION
   - Was sagt der Trend aus?
   - Ist er stark/schwach/stabil?
   - Wie nachhaltig ist er?

2. VARIABILITÄT
   - Wie stabil sind die Werte?
   - Gibt es hohe Volatilität?
   - Ist das normal oder auffällig?

3. PATTERNS
   - Erkennbare Muster?
   - Saisonalität oder Zyklen?
   - Besondere Events?

4. PROGNOSE
   - Wie könnte es weitergehen?
   - Best/Worst Case Scenarios?
   - Risiken und Opportunities?

5. EMPFEHLUNGEN
   - Was sollte man tun?
   - Worauf achten?
   - Welche Interventionen könnten helfen?

Sei konkret und actionable in den Empfehlungen.
"""

        analysis = await self.think(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "pattern_analysis",
            "metric": metric,
            "timeframe": timeframe,
            "data_points": len(df),
            "statistics": stats,
            "analysis": analysis,
            "analyzed_at": self._get_timestamp()
        }

    async def analyze_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance metrics against targets

        Args:
            task: {
                "metrics": {"metric_name": value, ...},
                "targets": {"metric_name": target_value, ...},
                "period": "Month 3" | "Q1" | etc.
            }

        Returns:
            Performance analysis with recommendations
        """
        metrics = task.get("metrics", {})
        targets = task.get("targets", {})
        period = task.get("period", "Current Period")

        if not metrics:
            return {
                "error": "No metrics provided",
                "status": "failed"
            }

        # Calculate performance gaps
        performance = {}
        for metric, value in metrics.items():
            target = targets.get(metric, 0)
            if target > 0:
                achievement = (value / target) * 100
                gap = value - target
                performance[metric] = {
                    "actual": value,
                    "target": target,
                    "achievement_pct": round(achievement, 2),
                    "gap": gap,
                    "status": "on_track" if achievement >= 90 else "behind" if achievement >= 70 else "critical"
                }
            else:
                performance[metric] = {
                    "actual": value,
                    "target": target,
                    "achievement_pct": 0,
                    "gap": value - target,
                    "status": "no_target"
                }

        query = f"""
Performance-Analyse für: {period}

METRIKEN & TARGETS:
{self._format_performance_table(performance)}

PERFORMANCE-ANALYSE:
1. OVERALL PERFORMANCE
   - Wie ist die Gesamt-Performance?
   - Welche Metriken sind on-track?
   - Wo gibt es kritische Gaps?

2. STÄRKEN
   - Was läuft besonders gut?
   - Welche Erfolge sind zu feiern?
   - Best Performers identifizieren

3. SCHWÄCHEN & GAPS
   - Wo sind die größten Lücken?
   - Was sind die Gründe?
   - Welche Metriken brauchen Attention?

4. ROOT CAUSE ANALYSIS
   - Warum werden Targets verfehlt/übertroffen?
   - Systematische vs. einmalige Issues?
   - External vs. internal Faktoren?

5. ACTIONABLE RECOMMENDATIONS
   - Quick Wins (sofort umsetzbar)?
   - Medium-term Optimierungen?
   - Strategic Changes nötig?
   - Resource Reallocation?

6. FORECAST & OUTLOOK
   - Können wir aufholen?
   - Müssen Targets angepasst werden?
   - Was ist realistisch erreichbar?

PRIORITÄT:
Fokus auf die 20% Actions, die 80% Impact haben.
"""

        analysis = await self.think(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "performance_analysis",
            "period": period,
            "metrics_analyzed": len(metrics),
            "performance": performance,
            "analysis": analysis,
            "analyzed_at": self._get_timestamp()
        }

    async def compare_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two datasets or time periods

        Args:
            task: {
                "data_a": DataFrame or dict (Period A),
                "data_b": DataFrame or dict (Period B),
                "label_a": "Period A name",
                "label_b": "Period B name",
                "metrics": ["metric1", "metric2"]  # optional
            }

        Returns:
            Comparative analysis
        """
        data_a = task.get("data_a")
        data_b = task.get("data_b")
        label_a = task.get("label_a", "Period A")
        label_b = task.get("label_b", "Period B")
        metrics = task.get("metrics", [])

        df_a = self._prepare_dataframe(data_a)
        df_b = self._prepare_dataframe(data_b)

        if df_a is None or df_b is None:
            return {
                "error": "Could not prepare data for comparison",
                "status": "failed"
            }

        # If no specific metrics, use all numeric columns
        if not metrics:
            metrics = df_a.select_dtypes(include=[np.number]).columns.tolist()

        # Compare metrics
        comparison = {}
        for metric in metrics:
            if metric in df_a.columns and metric in df_b.columns:
                val_a = df_a[metric].mean()
                val_b = df_b[metric].mean()
                change = val_b - val_a
                change_pct = (change / val_a * 100) if val_a != 0 else 0

                comparison[metric] = {
                    label_a: float(val_a),
                    label_b: float(val_b),
                    "absolute_change": float(change),
                    "percent_change": round(float(change_pct), 2),
                    "trend": "up" if change > 0 else "down" if change < 0 else "stable"
                }

        query = f"""
Vergleichs-Analyse: {label_a} vs {label_b}

METRIKEN-VERGLEICH:
{self._format_comparison_table(comparison)}

COMPARATIVE ANALYSIS:
1. OVERVIEW
   - Was hat sich insgesamt verändert?
   - Positive/negative Entwicklungen?
   - Auffälligste Änderungen?

2. GROWTH & DECLINE
   - Welche Metriken sind gewachsen?
   - Wo gibt es Rückgänge?
   - Growth-Rate Analyse

3. INTERPRETATION
   - Was bedeuten diese Änderungen?
   - Sind sie erwartungsgemäß?
   - Gibt es Überraschungen?

4. INSIGHTS
   - Warum diese Entwicklungen?
   - Korrelationen zwischen Änderungen?
   - Lessons Learned?

5. RECOMMENDATIONS
   - Was sollte verstärkt werden?
   - Was muss korrigiert werden?
   - Next actions?

Fokus auf actionable Insights aus dem Vergleich.
"""

        analysis = await self.think(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "comparative_analysis",
            "label_a": label_a,
            "label_b": label_b,
            "metrics_compared": len(comparison),
            "comparison": comparison,
            "analysis": analysis,
            "analyzed_at": self._get_timestamp()
        }

    async def calculate_statistics(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate detailed statistics for a dataset

        Args:
            task: {
                "data": DataFrame or dict/list,
                "metrics": ["metric1", "metric2"]  # optional
            }

        Returns:
            Statistical analysis
        """
        data = task.get("data")
        metrics = task.get("metrics", [])

        df = self._prepare_dataframe(data)

        if df is None:
            return {
                "error": "Could not prepare data",
                "status": "failed"
            }

        # If no metrics specified, use all numeric columns
        if not metrics:
            metrics = df.select_dtypes(include=[np.number]).columns.tolist()

        statistics = {}
        for metric in metrics:
            if metric in df.columns:
                statistics[metric] = {
                    "count": int(df[metric].count()),
                    "mean": float(df[metric].mean()),
                    "median": float(df[metric].median()),
                    "std": float(df[metric].std()),
                    "min": float(df[metric].min()),
                    "max": float(df[metric].max()),
                    "q25": float(df[metric].quantile(0.25)),
                    "q75": float(df[metric].quantile(0.75))
                }

        self.metrics["tasks_completed"] += 1

        return {
            "type": "statistical_analysis",
            "metrics_analyzed": len(statistics),
            "statistics": statistics,
            "analyzed_at": self._get_timestamp()
        }

    async def general_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        General analysis based on provided query

        Args:
            task: {
                "query": "Analysis question or request",
                "context": "Additional context"
            }

        Returns:
            Analysis response
        """
        query = task.get("query", "")
        context = task.get("context", "")

        if not query:
            return {
                "error": "No query provided",
                "status": "failed"
            }

        full_query = f"{context}\n\n{query}" if context else query
        analysis = await self.think(full_query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "general_analysis",
            "query": query,
            "analysis": analysis,
            "analyzed_at": self._get_timestamp()
        }

    # Helper Methods

    def _prepare_dataframe(self, data: Any) -> Optional[pd.DataFrame]:
        """Convert various data formats to DataFrame"""
        try:
            if isinstance(data, pd.DataFrame):
                return data
            elif isinstance(data, dict):
                return pd.DataFrame([data]) if not isinstance(list(data.values())[0], list) else pd.DataFrame(data)
            elif isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error preparing DataFrame: {e}")
            return None

    def _generate_dataset_summary(self, df: pd.DataFrame) -> str:
        """Generate a text summary of a DataFrame"""
        summary_parts = [
            f"Rows: {len(df)}",
            f"Columns: {len(df.columns)}",
            f"\nColumn Names: {', '.join(df.columns.tolist())}",
            f"\nData Types:\n{df.dtypes.to_string()}",
            f"\n\nBasic Statistics:\n{df.describe().to_string()}"
        ]

        # Check for missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            summary_parts.append(f"\n\nMissing Values:\n{missing[missing > 0].to_string()}")

        return "\n".join(summary_parts)

    def _format_performance_table(self, performance: Dict[str, Dict]) -> str:
        """Format performance data as a readable table"""
        lines = []
        for metric, data in performance.items():
            lines.append(
                f"- {metric}: {data['actual']}/{data['target']} "
                f"({data['achievement_pct']}%) - {data['status'].upper()}"
            )
        return "\n".join(lines)

    def _format_comparison_table(self, comparison: Dict[str, Dict]) -> str:
        """Format comparison data as a readable table"""
        lines = []
        for metric, data in comparison.items():
            # Get the two period labels (exclude calculated fields)
            labels = [k for k in data.keys() if k not in ['absolute_change', 'percent_change', 'trend']]
            if len(labels) >= 2:
                lines.append(
                    f"- {metric}: {data[labels[0]]:.2f} → {data[labels[1]]:.2f} "
                    f"({data['percent_change']:+.1f}%) {data['trend'].upper()}"
                )
        return "\n".join(lines)

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()


# Quick test function
async def test_analyst():
    """Test the Analyst Agent"""
    agent = AnalystAgent()

    print("=" * 60)
    print("Testing AnalystAgent")
    print("=" * 60)

    # Test: Analyze performance metrics
    result = await agent.analyze_performance({
        "metrics": {
            "subscribers": 150,
            "videos": 3,
            "newsletters": 5
        },
        "targets": {
            "subscribers": 100,
            "videos": 2,
            "newsletters": 4
        },
        "period": "Month 3"
    })

    print(f"\n[PERFORMANCE ANALYSIS]")
    print(f"Period: {result['period']}")
    print(f"Metrics Analyzed: {result['metrics_analyzed']}")
    print("\nPerformance Summary:")
    for metric, perf in result['performance'].items():
        print(f"  {metric}: {perf['achievement_pct']}% ({perf['status']})")
    print(f"\nAnalysis Preview (first 400 chars):")
    print(result["analysis"][:400])
    print("...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_analyst())
