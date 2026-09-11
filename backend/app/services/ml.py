import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any, Tuple

class ProductivityAnalyticsEngine:
    def __init__(self):
        # IsolationForest model for unsupervised anomaly detection
        # contamination=0.1 assumes roughly 10% of high-stress outlier states warrant burnout alerts
        self.anomaly_detector = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )

    def match_tasks_to_circadian_rhythm(
        self, 
        tasks: List[Dict[str, Any]], 
        hourly_energy_profile: Dict[int, float]
    ) -> List[Dict[str, Any]]:
        """
        Circadian matching algorithm:
        Sorts tasks by cognitive_load descending and assigns them to the highest-energy available hours.
        """
        if not tasks or not hourly_energy_profile:
            return tasks

        # Sort available hours by energy level descending
        sorted_hours = sorted(hourly_energy_profile.items(), key=lambda item: item[1], reverse=True)
        
        # Sort tasks by cognitive load descending (deepest focus first)
        sorted_tasks = sorted(tasks, key=lambda t: t.get("cognitive_load", 0.5), reverse=True)

        scheduled_tasks = []
        for index, task in enumerate(sorted_tasks):
            assigned_hour = sorted_hours[index % len(sorted_hours)][0]
            task_copy = dict(task)
            task_copy["scheduled_hour"] = assigned_hour
            scheduled_tasks.append(task_copy)

        return scheduled_tasks

    def detect_burnout_risk(self, historical_logs: List[Dict[str, Any]]) -> Tuple[bool, float, str]:
        """
        Evaluates fatigue telemetry [hours_worked_today, energy_level] via IsolationForest.
        Returns: (is_anomaly, risk_score, explanatory_message)
        """
        # Baseline training data if user history is short (< 5 logs)
        # Features: [hours_worked_today, energy_level (1-5)]
        default_baseline = np.array([
            [4.0, 4], [6.0, 4], [7.5, 3], [8.0, 3], [5.0, 5],
            [6.5, 4], [7.0, 3], [8.5, 2], [9.0, 2], [3.0, 5]
        ])

        if len(historical_logs) >= 5:
            feature_matrix = np.array([
                [log["hours_worked_today"], log["energy_level"]]
                for log in historical_logs
            ])
        else:
            feature_matrix = default_baseline

        # Fit model on baseline distributions
        self.anomaly_detector.fit(feature_matrix)

        # Evaluate the most recent observation
        latest = historical_logs[-1] if historical_logs else {"hours_worked_today": 9.5, "energy_level": 1}
        current_sample = np.array([[latest["hours_worked_today"], latest["energy_level"]]])

        prediction = self.anomaly_detector.predict(current_sample)[0]  # -1 for anomaly, 1 for normal
        decision_score = self.anomaly_detector.decision_function(current_sample)[0]

        # Convert decision function score to a 0.0 - 1.0 risk index
        risk_score = round(float(np.clip(0.5 - decision_score, 0.0, 1.0)), 2)
        is_burnout = bool(prediction == -1 and latest["energy_level"] <= 2)

        if is_burnout:
            message = "High burnout anomaly detected: sustained high workload combined with depleted energy reserves."
        elif risk_score > 0.6:
            message = "Elevated cognitive load warning. Consider scheduling decompression intervals."
        else:
            message = "Cognitive workload and recovery rhythms are balanced."

        return is_burnout, risk_score, message

# Singleton instance
analytics_engine = ProductivityAnalyticsEngine()