import collections
import random
import csv
import os


class ProjectDSS:
    def __init__(self):
        self.project_characteristics = {}
        self.recommendations = {
            "Life Cycle": [],
            "Methodology": [],
            "Language": [],
            "Model (Architectural)": [],
            "Timeframe Management": [],
            "Considerations": [], # For additional advice
            "Risk Management": [], # New: For risk mitigation strategies
            "Testing Strategy": [], # New: For recommended testing approaches
            "Deployment": [], # New: For deployment and release strategies
            "Documentation": [], # New: For documentation best practices
            "Collaboration Tools": []
        }
        self.knowledge_base = self._build_knowledge_base()

    def reset(self):
        self.__init__()

    def _build_knowledge_base(self):
        """
        This is the core of the DSS. It maps project characteristics to recommendations.
        It's a simplified representation; in a real system, this would be much more
        sophisticated, potentially using rules engines, machine learning, or a proper
        database.
        """
        kb = {
            # --- Life Cycle Models ---
            "Life Cycle": {
                "Waterfall": {
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Requirements Clarity": [0.2, "Clear"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": [0.1, "low"],
                    "Risk Tolerance": [0.1, "Low"],
                    "Urgency/Time-to-Market": [0.1, "Low", "Medium"],
                    "Innovation Level": [0.1, "Low", "Medium"],
                    "Budget": [0.05, "Medium", "High"],
                    "Regulatory Compliance": [0.05, "low"]
                },
                "Agile": {
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Requirements Clarity": [0.2, "Evolving", "Unclear"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)", "Large (21-50)", "Very Large (50+)"],
                    "Stakeholder Involvement": [0.1, "High"],
                    "Risk Tolerance": [0.1, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.1, "High"],
                    "Innovation Level": [0.1, "Medium", "High", "Very High"],
                    "Budget": [0.05, "Medium", "High", "Very High"],
                    "Regulatory Compliance": [0.05, "Low", "Medium"]
                },
                "Iterative": {
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Requirements Clarity": [0.2, "Evolving"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": [0.1, "Medium"],
                    "Risk Tolerance": [0.1, "Medium"],
                    "Urgency/Time-to-Market": [0.1, "Medium"],
                    "Innovation Level": [0.1, "Medium", "High"],
                    "Budget": [0.05, "Medium", "High"],
                    "Regulatory Compliance": [0.05, "Low"]
                },
                "Spiral": {
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Requirements Clarity": [0.2, "Unclear", "Evolving"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": [0.1, "Medium", "High"],
                    "Risk Tolerance": [0.1, "High"],
                    "Urgency/Time-to-Market": [0.1, "Low", "Medium"],
                    "Innovation Level": [0.1, "High"],
                    "Budget": [0.05, "High", "Very High"],
                    "Regulatory Compliance": [0.05, "Low", "Medium"]
                },
                "V-Model": {
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Requirements Clarity": [0.2, "Clear"],
                    "Team Size": [0.1, "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": [0.1, "Low", "Medium"],
                    "Risk Tolerance": [0.1, "Low", "Medium"],
                    "Urgency/Time-to-Market": [0.1, "Low", "Medium", "High"],
                    "Innovation Level": [0.1, "Medium", "High"],
                    "Budget": [0.05, "Medium", "High"],
                    "Regulatory Compliance": [0.05, "High", "Very High"]
                },
                "DevOps Lifecycle": {
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Requirements Clarity": [0.2, "Unclear", "Evolving"],
                    "Team Size": [0.1, "Medium (6-20)", "Large (21-50)", "Very Large (50+)"],
                    "Stakeholder Involvement": [0.1, "Medium", "High", "Very High"],
                    "Risk Tolerance": [0.1, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.1, "High"],
                    "Innovation Level": [0.1, "Medium", "High"],
                    "Budget": [0.1, "Medium", "High"],
                    "Regulatory Compliance": [0.05, "Low"],
                    "DevOps Implemented": [0.05, "Yes"]
                },
                "Rapid Application Development (RAD)": {
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Requirements Clarity": [0.2, "Evolving", "Unclear"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": [0.1, "Medium", "High"],
                    "Risk Tolerance": [0.1, "Low", "Medium"],
                    "Urgency/Time-to-Market": [0.1, "High", "Very High"],
                    "Innovation Level": [0.1, "Medium", "High"],
                    "Budget": [0.05, "Low", "Medium"],
                    "Regulatory Compliance": [0.05, "Low"]
                },
                "Incremental": {
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Requirements Clarity": [0.2, "Evolving"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)"],
                    "Stakeholder Involvement": [0.1, "Low", "Medium"],
                    "Risk Tolerance": [0.1, "Medium"],
                    "Urgency/Time-to-Market": [0.1, "Medium", "High"],
                    "Innovation Level": [0.1, "Medium", "High"],
                    "Budget": [0.05, "Low", "Medium"],
                    "Regulatory Compliance": [0.05, "Low"]
                },
                "Big Bang": {
                    "Project Complexity": [0.2, "Low"],
                    "Requirements Clarity": [0.2, "Unclear"],
                    "Team Size": [0.1, "Small (1-5)"],
                    "Stakeholder Involvement": [0.1, "Low"],
                    "Risk Tolerance": [0.1, "High"],
                    "Urgency/Time-to-Market": [0.1, "High"],
                    "Innovation Level": [0.1, "Low", "Medium"],
                    "Budget": [0.05, "Low"],
                    "Regulatory Compliance": [0.05, "Low"]
                },
                "Prototyping": {
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Requirements Clarity": [0.2, "Unclear", "Evolving"],
                    "Team Size": [0.1, "Small (1-5)", "Medium (6-20)"],
                    "Stakeholder Involvement": [0.1, "High"],
                    "Risk Tolerance": [0.1, "Medium", "High"],
                    "Innovation Level": [0.1, "High"],
                    "Urgency/Time-to-Market": [0.1, "Medium", "High"],
                    "Budget": [0.05, "Low", "Medium", "High"],
                    "Regulatory Compliance": [0.05, "Low"]
                },
                # General/Fallback Recommendations
                "General Recommendation: Low Complexity": {"Project Complexity": [0.04, "Low"]},
                "General Recommendation: Medium Complexity": {"Project Complexity": [0.04, "Medium"]},
                "General Recommendation: High Complexity": {"Project Complexity": [0.04, "High"]},
                "General Recommendation: Very High Complexity": {"Project Complexity": [0.04, "Very High"]},
                "General Recommendation: Clear Requirements": {"Requirements Clarity": [0.04, "Clear"]},
                "General Recommendation: Evolving Requirements": {"Requirements Clarity": [0.04, "Evolving"]},
                "General Recommendation: Unclear Requirements": {"Requirements Clarity": [0.04, "Unclear"]},
                "General Recommendation: Low Risk Tolerance": {"Risk Tolerance": [0.04, "Low"]},
                "General Recommendation: Medium Risk Tolerance": {"Risk Tolerance": [0.04, "Medium"]},
                "General Recommendation: High Risk Tolerance": {"Risk Tolerance": [0.04, "High"]},
                "General Recommendation: High Regulatory Compliance": {"Regulatory Compliance": [0.04, "High"]},
                "General Recommendation: High Innovation": {"Innovation Level": [0.04, "High"]},
                "General Recommendation: Medium Innovation": {"Innovation Level": [0.04, "Medium"]},
                "General Recommendation: Low Innovation": {"Innovation Level": [0.04, "Low"]},
                "General Recommendation: High Urgency": {"Urgency/Time-to-Market": [0.04, "High"]},
                "General Recommendation: Medium Urgency": {"Urgency/Time-to-Market": [0.04, "Medium"]},
                "General Recommendation: Low Urgency": {"Urgency/Time-to-Market": [0.04, "Low"]},
                "General Recommendation: Small Team": {"Team Size": [0.04, "Small (1-5)"]},
                "General Recommendation: Medium Team": {"Team Size": [0.04, "Medium (6-20)"]},
                "General Recommendation: Large Team": {"Team Size": [0.04, "Large (21-50)"]},
                "General Recommendation: Very Large Team": {"Team Size": [0.04, "Very Large (50+)"]},
                "General Recommendation: High Budget": {"Budget": [0.04, "High"]},
                "General Recommendation: Very High Budget": {"Budget": [0.04, "Very High"]},
                "General Recommendation: Low Budget": {"Budget": [0.04, "Low"]},
                "General Recommendation: Medium Budget": {"Budget": [0.04, "Medium"]},
                "General Recommendation: High Stakeholder Involvement": {"Stakeholder Involvement": [0.04, "High"]},
                "General Recommendation: Medium Stakeholder Involvement": {"Stakeholder Involvement": [0.04, "Medium"]},
                "General Recommendation: Low Stakeholder Involvement": {"Stakeholder Involvement": [0.04, "Low"]},
                "General Recommendation: DevOps Implemented": {"DevOps Implemented": [0.04, "Yes"]},
                "General Recommendation: No DevOps Implemented": {"DevOps Implemented": [0.04, "No"]},
                "General Recommendation: MVP Approach": {"Urgency/Time-to-Market": [0.04, "High"], "Project Complexity": [0.01, "Low", "Medium"]},
            },

            # --- Methodologies/Frameworks ---
            "Methodology": {
                "Scrum": {
                    "Life Cycle": [0.3, "Agile"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)"],
                    "Stakeholder Involvement": [0.2, "High"],
                    "Requirements Clarity": [0.2, "Evolving", "Clear"],
                    "Urgency/Time-to-Market": [0.1, "High"]
                },
                "Kanban": {
                    "Life Cycle": [0.3, "Agile"],
                    "Requirements Clarity": [0.2, "Evolving", "Clear"],
                    "Urgency/Time-to-Market": [0.1, "High"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "Extreme Programming (XP)": {
                    "Life Cycle": [0.3, "Agile"],
                    "Team Size": [0.2, "Small (1-5)"],
                    "Requirements Clarity": [0.2, "Evolving"],
                    "Risk Tolerance": [0.2, "Medium", "High"],
                    "Innovation Level": [0.1, "High"]
                },
                "DevOps": {
                    "Life Cycle": [0.3, "Agile", "DevOps Lifecycle"],
                    "Urgency/Time-to-Market": [0.1, "High"],
                    "Innovation Level": [0.2, "Medium", "High"],
                    "DevOps Implemented": [0.2, "Yes"],
                    "Scalability Needs": [0.2, "High"]
                },
                "PRINCE2": {
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Regulatory Compliance": [0.2, "High"],
                    "Budget": [0.1, "Medium", "High", "Very High"],
                    "Project Size": [0.1, "Medium", "Large", "Very Large"],
                    "Requirements Clarity": [0.2, "Clear"],
                    "Risk Tolerance": [0.2, "Low", "Medium"]
                },
                "PMBOK (Project Management Body of Knowledge)": {
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Project Size": [0.1, "Medium", "Large", "Very Large"],
                    "Requirements Clarity": [0.2, "Clear"],
                    "Risk Tolerance": [0.2, "Low", "Medium"]
                },
                "SAFe (Scaled Agile Framework)": {
                    "Project Size": [0.1, "Very Large"],
                    "Life Cycle": [0.3, "Agile"],
                    "Team Size": [0.2, "Very Large (50+)"],
                    "Stakeholder Involvement": [0.2, "High"],
                    "Requirements Clarity": [0.2, "Evolving", "Clear"]
                },
                "LeSS (Large Scale Scrum)": {
                    "Project Size": [0.1, "Large", "Very Large"],
                    "Life Cycle": [0.3, "Agile"],
                    "Team Size": [0.2, "Large (21-50)", "Very Large (50+)"],
                    "Stakeholder Involvement": [0.2, "High"]
                },
                "Crystal": {
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)"],
                    "Requirements Clarity": [0.2, "Clear", "Evolving"],
                    "Urgency/Time-to-Market": [0.1, "Medium", "High"]
                },
                "Feature Driven Development (FDD)": {
                    "Life Cycle": [0.3, "Agile"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Team Size": [0.2, "Medium (6-20)", "Large (21-50)"],
                    "Requirements Clarity": [0.2, "Evolving"]
                },
                "DSDM (Dynamic Systems Development Method)": {
                    "Life Cycle": [0.3, "Agile"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Requirements Clarity": [0.2, "Evolving", "Unclear"],
                    "Urgency/Time-to-Market": [0.1, "High"]
                },
                "RUP (Rational Unified Process)": {
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Requirements Clarity": [0.2, "Evolving", "Clear"],
                    "Team Size": [0.2, "Medium (6-20)", "Large (21-50)"],
                    "Risk Tolerance": [0.2, "Medium", "High"]
                },
                "Scrumban": {
                    "Life Cycle": [0.3, "Agile"],
                    "Requirements Clarity": [0.2, "Evolving"],
                    "Urgency/Time-to-Market": [0.1, "High"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)", "Large (21-50)"]
                },
                # General/Fallback Recommendations
                "General Recommendation: Agile Methodology": {"Life Cycle": [0.05, "Agile"]},
                "General Recommendation: Traditional Methodology": {"Life Cycle": [0.05, "Waterfall", "V-Model"]},
                "General Recommendation: Scaled Agile": {"Team Size": [0.05, "Large (21-50)", "Very Large (50+)"]},
                "General Recommendation: High Regulatory Compliance": {"Regulatory Compliance": [0.05, "High"]},
                "General Recommendation: High Stakeholder Involvement": {"Stakeholder Involvement": [0.05, "High"]},
                "General Recommendation: DevOps Practices": {"DevOps Implemented": [0.05, "Yes"]},
                "General Recommendation: Rapid Delivery": {"Urgency/Time-to-Market": [0.05, "High"]},
                "General Recommendation: Small Team": {"Team Size": [0.05, "Small (1-5)"]},
                "General Recommendation: Medium Team": {"Team Size": [0.05, "Medium (6-20)"]},
                "General Recommendation: Large Team": {"Team Size": [0.05, "Large (21-50)"]},
                "General Recommendation: Very Large Team": {"Team Size": [0.05, "Very Large (50+)"]},
                "General Recommendation: MVP Approach": {"Urgency/Time-to-Market": [0.05, "High"], "Project Complexity": [0.04, "Low", "Medium"]},
            },

            # --- Programming Languages (Simplified mapping) ---
            # ["Web Application", "Mobile App", "Desktop App", "Cross Platform App", "Data Science", "Machine Learning", "Embedded System","Enterprise Applications", "API/Backend Service", "Web Development (Backend)", Web Development (Full-stack), "Game Development", "System Programming", "Engineering", "Other"]

            "Language": {
                "Python": {
                    "Project Type (Implicit)": [0.4, "Data Science", "Web Application", "Web Development (Backend)", "Automation", "Scripting", "Machine Learning", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Medium", "High"],
                    "Project Complexity": [0.2, "Low", "Medium", "High"],
                    "Budget": [0.2, "Low", "Medium"]
                },
                "Java": {
                    "Project Type (Implicit)": [0.4, "Enterprise Applications", "Android", "Mobile App", "Large-Scale Systems", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium"],
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Budget": [0.2, "Medium", "High"]
                },
                "JavaScript (with Node.js)": {
                    "Project Type (Implicit)": [0.4, "Web Application", "Web Development (Full-stack)", "Real-time Applications", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Medium", "High"],
                    "Project Complexity": [0.2, "Low", "Medium", "High"],
                    "Budget": [0.2, "Low", "Medium"]
                },
                "Dart (with Flutter)": {
                    "Project Type (Implicit)": [0.4, "Real-time Applications", "Cross Platform App"],
                    "Urgency/Time-to-Market": [0.2, "Medium", "High"],
                    "Project Complexity": [0.2, "Low", "Medium", "High"],
                    "Budget": [0.2, "Low", "Medium", "High"]
                },
                "TypeScript": {
                    "Project Type (Implicit)": [0.4, "Web Application", "Web Development (Full-stack)", "Frontend", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Medium", "High"],
                    "Project Complexity": [0.2, "Low", "Medium", "High"],
                    "Budget": [0.2, "Low", "Medium"]
                },
                "C# (with Unity)": {
                    "Project Type (Implicit)": [0.4, ".NET Applications", "Desktop App", "Windows Applications", "Game Development", "Enterprise Applications"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium", "Very High"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Budget": [0.2, "Medium", "High"]
                },
                "C++": {
                    "Project Type (Implicit)": [0.4, "System Programming", "Desktop App", "Game Development", "High-Performance Computing", "Embedded System"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium"],
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Budget": [0.2, "High", "Very High"]
                },
                "Go": {
                    "Project Type (Implicit)": [0.4, "Concurrent Applications", "Cloud Infrastructure", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Medium", "High"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Budget": [0.2, "Medium", "High"]
                },
                "Rust": {
                    "Project Type (Implicit)": [0.4, "System Programming", "Embedded System", "WebAssembly", "High-Performance Computing"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium"],
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Budget": [0.2, "Medium", "High"]
                },
                "PHP": {
                    "Project Type (Implicit)": [0.4, "Web Application", "Web Development (Backend)", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "High"],
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Budget": [0.2, "Low", "Medium"]
                },
                "Kotlin": {
                    "Project Type (Implicit)": [0.4, "Android", "Mobile App", "Web Application", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium", "High"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Budget": [0.2, "Medium", "High"]
                },
                "Swift": {
                    "Project Type (Implicit)": [0.4, "Mobile App", "iOS", "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium", "High"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Budget": [0.2, "Medium", "High"]
                },
                "R": {
                    "Project Type (Implicit)": [0.4, "Data Science", "Statistics", "Machine Learning"],
                    "Urgency/Time-to-Market": [0.2, "Medium", "High"],
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Budget": [0.2, "Low", "Medium"]
                },
                "MATLAB": {
                    "Project Type (Implicit)": [0.4, "Data Science", "Simulation", "Engineering"],
                    "Urgency/Time-to-Market": [0.2, "Low", "Medium", "High"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Budget": [0.2, "High", "Very High"]
                },
                # General/Fallback Recommendations
                "General Recommendation: Web Application": {"Project Type (Implicit)": [0.1, "Web Application"]},
                "General Recommendation: Mobile App": {"Project Type (Implicit)": [0.1, "Mobile App"]},
                "General Recommendation: Desktop App": {"Project Type (Implicit)": [0.1, "Desktop App"]},
                "General Recommendation: Data Science/ML": {"Project Type (Implicit)": [0.1, "Data Science", "Machine Learning"]},
                "General Recommendation: Embedded System": {"Project Type (Implicit)": [0.1, "Embedded System"]},
                "General Recommendation: Game": {"Project Type (Implicit)": [0.1, "Game Development"]},
                "General Recommendation: Enterprise Software": {"Project Type (Implicit)": [0.1, "Enterprise Applications"]},
                "General Recommendation: API/Backend Service": {"Project Type (Implicit)": [0.1, "API/Backend Service"]},
                "General Recommendation: Other Project Type": {"Project Type (Implicit)": [0.1, "Other"]},
            },

            # --- Architectural Models ---
            "Model (Architectural)": {
                "Microservices": {
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Team Size": [0.2, "Large (21-50)", "Very Large (50+)"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15, "High"],
                    "Budget": [0.1, "High", "Very High"],
                    "Urgency/Time-to-Market": [0.05, "Low", "Medium"],
                    "Requirements Clarity": [0.1, "Unclear"]
                },
                "Monolithic": {
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)"],
                    "Scalability Needs": [0.2, "Low", "Medium"],
                    "Innovation Level": [0.15, "Low", "Medium"],
                    "Budget": [0.1, "Low", "Medium"],
                    "Urgency/Time-to-Market": [0.05, "High"],
                    "Requirements Clarity": [0.1, "Clear"]
                },
                "Client-Server": {
                    "Project Complexity": [0.2, "Low", "Medium", "High"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Scalability Needs": [0.2,"Low", "Medium","High"],
                    "Innovation Level": [0.15,"Medium", "High"],
                    "Budget": [0.1,"Medium", "High"],
                    "Urgency/Time-to-Market": [0.05, "High"],
                    "Requirements Clarity": [0.1, "Clear"]
                },
                "Event-Driven": {
                    "Project Complexity": [0.2, "High"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15,"High"],
                    "Budget": [0.1, "High", "Very High"],
                    "Urgency/Time-to-Market": [0.05, "Low", "Medium"],
                    "Real-time Processing": [0.1,"Yes"],
                    "Requirements Clarity": [0.1, "Clear"]
                },
                "Serverless": {
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Team Size": [0.2, "Small (1-5)", "Medium (6-20)"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15,"Medium"],
                    "Budget": [0.1, "Low", "Medium"],
                    "Urgency/Time-to-Market": [0.05, "High"],
                    "Requirements Clarity": [0.1, "Clear"]
                },
                "Layered (n-tier)": {
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Team Size": [0.2, "Medium (6-20)", "Large (21-50)"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15,"Medium", "High"],
                    "Budget": [0.1, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.05, "Medium", "High"],
                    "Requirements Clarity": [0.1, "Clear", "Evolving"]
                },
                "Service-Oriented Architecture (SOA)": {
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Team Size": [0.2, "Large (21-50)", "Very Large (50+)"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15,"Medium", "High"],
                    "Budget": [0.1, "Medium", "High", "Very High"],
                    "Urgency/Time-to-Market": [0.05, "Medium", "High"],
                    "Requirements Clarity": [0.1, "Clear"]
                },
                "Peer-to-Peer": {
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Team Size": [0.2, "Very Large (50+)"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15,"High"],
                    "Budget": [0.1, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.05, "Low"],
                    "Requirements Clarity": [0.1, "Evolving"]
                },
                "Space-Based": {
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Scalability Needs": [0.2, "High"],
                    "Innovation Level": [0.15,"High", "Very High"],
                    "Budget": [0.1, "High", "Very High"],
                    "Urgency/Time-to-Market": [0.05, "High"],
                    "Requirements Clarity": [0.1, "Clear"]
                },
                # General/Fallback Recommendations
                "General Recommendation: High Scalability": {"Scalability Needs": [0.04, "High"]},
                "General Recommendation: Real-time Processing": {"Real-time Processing": [0.04, "Yes"]},
                "General Recommendation: Low Scalability": {"Scalability Needs": [0.04, "Low"]},
                "General Recommendation: Medium Scalability": {"Scalability Needs": [0.04, "Medium"]},
                "General Recommendation: Serverless": {"Scalability Needs": [0.01, "High"], "Budget": [0.04, "Low", "Medium"]},
                "General Recommendation: Layered": {"Project Complexity": [0.04, "Medium", "High"]},
                "General Recommendation: Event-Driven": {"Real-time Processing": [0.04, "Yes"]},
                "General Recommendation: Monolithic": {"Project Complexity": [0.04, "Low", "Medium"]},
                "General Recommendation: Microservices": {"Project Complexity": [0.04, "High", "Very High"], "Scalability Needs": [0.01, "High"]},
            },

            # --- Timeframe Management ---
            "Timeframe Management": {
                "Fixed Deadline": {
                    "Requirements Clarity": [0.25, "Clear"],
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Risk Tolerance": [0.15, "Low"],
                    "Urgency/Time-to-Market": [0.2, "High"],
                    "Innovation Level": [0.1, "Low", "Medium"],
                    "DevOps Implemented": [0.1, "No"]
                },
                "Flexible Deadline": {
                    "Requirements Clarity": [0.2, "Evolving", "Unclear"],
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Risk Tolerance": [0.15, "Low", "Medium"],
                    "Urgency/Time-to-Market": [0.15, "Low", "Medium", "High"],
                    "Innovation Level": [0.15, "High"],
                    "DevOps Implemented": [0.15, "Yes", "No"]
                },
                "Iterative Sprints (e.g., 2-week)": {
                    "Requirements Clarity": [0.2, "Evolving", "Clear"],
                    "Project Complexity": [0.2, "Low", "Medium"],
                    "Risk Tolerance": [0.15, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.2, "High"],
                    "Innovation Level": [0.15, "Low", "Medium"],
                    "DevOps Implemented": [0.05, "No"],
                    "Life Cycle": [0.05, "Agile"]
                },
                "Continuous Delivery": {
                    "Requirements Clarity": [0.2, "Evolving", "Unclear"],
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Risk Tolerance": [0.15, "Medium", "High", "Very High"],
                    "Urgency/Time-to-Market": [0.15, "Low", "Medium"],
                    "Innovation Level": [0.15, "High"],
                    "DevOps Implemented": [0.1, "Yes"],
                    "Life Cycle": [0.05, "Agile"]
                },
                "Milestone-Based": {
                    "Project Complexity": [0.2, "Medium", "High", "Very High"],
                    "Requirements Clarity": [0.2, "Clear", "Evolving"],
                    "Risk Tolerance": [0.15, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.15, "Low", "Medium"],
                    "Innovation Level": [0.15, "Medium", "High"],
                    "DevOps Implemented": [0.15, "No"]
                },
                "Rolling Wave Planning": {
                    "Requirements Clarity": [0.2, "Evolving", "Unclear"],
                    "Project Complexity": [0.2, "High", "Very High"],
                    "Risk Tolerance": [0.15, "Low", "Medium"],
                    "Urgency/Time-to-Market": [0.15, "Medium", "High"],
                    "Innovation Level": [0.15, "Medium"],
                    "DevOps Implemented": [0.15, "Yes"]
                },
                "Hybrid (Fixed + Iterative)": {
                    "Requirements Clarity": [0.2, "Clear", "Evolving"],
                    "Project Complexity": [0.2, "Medium", "High"],
                    "Risk Tolerance": [0.15, "Medium", "High"],
                    "Urgency/Time-to-Market": [0.15, "Medium", "High"],
                    "Innovation Level": [0.15, "Medium", "High"],
                    "DevOps Implemented": [0.15, "No"]
                },
                # General/Fallback Recommendations
                "General Recommendation: High Urgency": {"Urgency/Time-to-Market": [0.04, "High"]},
                "General Recommendation: Medium Urgency": {"Urgency/Time-to-Market": [0.04, "Medium"]},
                "General Recommendation: Low Urgency": {"Urgency/Time-to-Market": [0.04, "Low"]},
                "General Recommendation: Evolving Requirements": {"Requirements Clarity": [0.04, "Evolving"]},
                "General Recommendation: Unclear Requirements": {"Requirements Clarity": [0.04, "Unclear"]},
                "General Recommendation: Clear Requirements": {"Requirements Clarity": [0.04, "Clear"]},
                "General Recommendation: DevOps Delivery": {"DevOps Implemented": [0.04, "Yes"]},
                "General Recommendation: MVP Approach": {"Urgency/Time-to-Market": [0.02, "High"], "Project Complexity": [0.03, "Low", "Medium"]},
            },
            # ...existing code...
            "Risk Management": {
                "Proactive Risk Assessment": {
                    "Project Complexity": [0.6, "High", "Very High"],
                    "Risk Tolerance": [0.4, "Low", "Medium"]
                },
                "Regular Risk Reviews": {
                    "Project Complexity": [0.5, "Medium", "High", "Very High"],
                    "Team Size": [0.5, "Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "Contingency Planning": {
                    "Risk Tolerance": [0.5, "Low", "Medium", "High"],
                    "Budget": [0.5, "Medium", "High", "Very High"]
                },
                "General Recommendation: Risk Register": {"Project Complexity": [0.3, "Medium", "High", "Very High"]},
                "General Recommendation: Early Stakeholder Engagement": {"Stakeholder Involvement": [0.3, "High"]},
            },
            "Testing Strategy": {
                "Automated Testing": {
                    "Project Complexity": [0.4, "Medium", "High", "Very High"],
                    "Urgency/Time-to-Market": [0.3, "High"],
                    "DevOps Implemented": [0.3, "Yes"]
                },
                "Manual Testing": {
                    "Project Complexity": [0.5, "Low", "Medium"],
                    "Budget": [0.5, "Low", "Medium"]
                },
                "Continuous Integration Testing": {
                    "DevOps Implemented": [0.6, "Yes"],
                    "Urgency/Time-to-Market": [0.4, "High"]
                },
                "Exploratory Testing": {
                    "Requirements Clarity": [0.5, "Unclear", "Evolving"],
                    "Innovation Level": [0.5, "High"]
                },
                "General Recommendation: Test Early and Often": {"Project Complexity": [0.2, "Medium", "High", "Very High"]},
                "General Recommendation: Regression Testing": {"Project Complexity": [0.2, "High", "Very High"]},
            },
            "Deployment": {
                "Continuous Deployment": {
                    "DevOps Implemented": [0.6, "Yes"],
                    "Urgency/Time-to-Market": [0.4, "High"]
                },
                "Manual Release": {
                    "Project Complexity": [0.5, "Low", "Medium"],
                    "Budget": [0.5, "Low", "Medium"]
                },
                "Staged Rollout": {
                    "Project Complexity": [0.5, "Medium", "High", "Very High"],
                    "Team Size": [0.5, "Large (21-50)", "Very Large (50+)"]
                },
                "Blue-Green Deployment": {
                    "Project Complexity": [0.5, "High", "Very High"],
                    "Risk Tolerance": [0.5, "Low", "Medium"]
                },
                "General Recommendation: Rollback Plan": {"Project Complexity": [0.3, "Medium", "High", "Very High"]},
                "General Recommendation: Monitor Deployments": {"DevOps Implemented": [0.3, "Yes"]},
            },
            "Documentation": {
                "Comprehensive Documentation": {
                    "Project Complexity": [0.5, "High", "Very High"],
                    "Team Size": [0.5, "Large (21-50)", "Very Large (50+)"]
                },
                "Lean Documentation": {
                    "Project Complexity": [0.5, "Low", "Medium"],
                    "Budget": [0.5, "Low", "Medium"]
                },
                "Living Documentation (Wiki)": {
                    "Requirements Clarity": [0.5, "Evolving", "Unclear"],
                    "Team Size": [0.5, "Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "API Documentation": {
                    "Project Type (Implicit)": [0.5, "API/Backend Service"],
                    "Urgency/Time-to-Market": [0.5, "High"]
                },
                "General Recommendation: Update Documentation Regularly": {"Project Complexity": [0.4, "Medium", "High", "Very High"]},
                "General Recommendation: Use Diagrams": {"Project Complexity": [0.4, "High", "Very High"]},
            },

            "Collaboration Tools": {
                "Version Control Systems (e.g., Git)": {
                    "Project Complexity": [0.5, "Medium", "High", "Very High"],
                    "Team Size": [0.5, "Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "Collaboration Platforms (e.g., Confluence, Slack)": {
                    "Project Complexity": [0.5, "Low", "Medium", "High"],
                    "Team Size": [0.5, "Small (1-5)", "Medium (6-20)"]
                }
            }
        }
        return kb

    def get_user_input(self):
        """Collects project characteristics from the user."""
        print("Please answer the following questions to help us recommend the best options for your project:")

        # Project Characteristics
        self.project_characteristics["Project Size"] = self._get_choice(
            "What is the estimated size of your project?", ["Small", "Medium", "Large", "Very Large"])
        self.project_characteristics["Project Complexity"] = self._get_choice(
            "How complex do you anticipate your project to be?", ["Low", "Medium", "High", "Very High"])
        self.project_characteristics["Requirements Clarity"] = self._get_choice(
            "How clear are your project requirements at this stage?", ["Clear", "Evolving", "Unclear"])
        self.project_characteristics["Team Size"] = self._get_choice(
            "What is your estimated team size?", ["Small (1-5)", "Medium (6-20)", "Large (21-50)", "Very Large (50+)"])
        self.project_characteristics["Stakeholder Involvement"] = self._get_choice(
            "How much involvement do you expect from stakeholders throughout the project?", ["Low", "Medium", "High"])
        self.project_characteristics["Budget"] = self._get_choice(
            "What is your project budget outlook?", ["Low", "Medium", "High", "Very High"])
        self.project_characteristics["Regulatory Compliance"] = self._get_choice(
            "Does your project require significant regulatory compliance?", ["Low", "Medium", "High"])
        self.project_characteristics["Innovation Level"] = self._get_choice(
            "How innovative or novel is your project?", ["Low", "Medium", "High", "Very High"])
        self.project_characteristics["Risk Tolerance"] = self._get_choice(
            "What is your organization's tolerance for project risk?", ["Low", "Medium", "High"])
        self.project_characteristics["Urgency/Time-to-Market"] = self._get_choice(
            "How urgent is it to get this project to market?", ["High", "Medium", "Low"])

        # Implicit characteristics (could be asked directly or inferred)
        project_type = self._get_choice(
            "What is the primary type of software/system you are building?",
            ["Web Application", "Mobile App", "Desktop App", "Cross Platform App", "Data Science", "Machine Learning",
            "Embedded System", "Enterprise Applications", "API/Backend Service", "Web Development (Backend)",
            "Web Development (Full-stack)", "Game Development", "System Programming", "Engineering", "Other"])
        self.project_characteristics["Project Type (Implicit)"] = project_type

        # Scalability Needs
        if project_type in ["Web Application", "Mobile App", "Enterprise Applications", "API/Backend Service"]:
            self.project_characteristics["Scalability Needs"] = self._get_choice(
                "What are your scalability needs for this project?", ["Low", "Medium", "High"])

        # Real-time Processing
        if project_type in ["Data Science", "Machine Learning", "Real-time Applications", "Embedded System"]:
            self.project_characteristics["Real-time Processing"] = self._get_choice(
                "Does your project involve significant real-time data processing?", ["Yes", "No"])

        # DevOps Practices
        devops_implemented = self._get_choice(
            "Do you currently have DevOps practices implemented in your organization?", ["Yes", "No"])
        self.project_characteristics["DevOps Implemented"] = devops_implemented

        # Optionally, ask about Life Cycle preference
        # self.project_characteristics["Life Cycle"] = self._get_choice(
        #     "Do you have a preferred development life cycle?", ["Waterfall", "Agile", "Iterative", "Spiral", "V-Model",
        #     "DevOps Lifecycle", "Rapid Application Development (RAD)", "Incremental", "Big Bang", "Prototyping", "No Preference"])


    def _get_choice(self, prompt, options):
        """Helper to get validated user input for a choice."""
        while True:
            try:
                choice = random.randint(1, len(options))  # Use the correct number of options
                # print(f"\n{prompt}")
                # for i, option in enumerate(options):
                #     print(f"  {i+1}. {option}")
                # print(f"Randomly selected: {choice} ({options[choice-1]})")
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def analyze_and_recommend(self):
        """Analyzes user input against the knowledge base to make recommendations."""
        print("\n--- Analyzing Project Characteristics and Making Recommendations ---")

        # Prioritize matching Life Cycle and Methodologies first as they often drive others
        matched_life_cycles = self._find_matches("Life Cycle")
        if matched_life_cycles:
            self.recommendations["Life Cycle"] = matched_life_cycles
            print(f"Recommended Life Cycles: {', '.join(matched_life_cycles)}")
            self.project_characteristics["Life Cycle"] = matched_life_cycles[0]

        matched_methodologies = self._find_matches("Methodology")
        if matched_methodologies:
            self.recommendations["Methodology"] = matched_methodologies
            print(f"Recommended Methodologies: {', '.join(matched_methodologies)}")

        # Score and recommend for all other categories
        for category in [
            "Language", "Model (Architectural)", "Timeframe Management",
            "Risk Management", "Testing Strategy", "Deployment", "Documentation", "Collaboration Tools"
        ]:
            matched_items = self._find_matches(category)
            if matched_items:
                self.recommendations[category] = matched_items
                print(f"Recommended {category}: {', '.join(matched_items)}")

        self._add_general_considerations()

    def _find_matches(self, category_key):
        """
        Finds all items in the knowledge base that match at least one project characteristic,
        scores them using attribute weights (if present), and returns those with the highest score.
        """
        kbCategory = self.knowledge_base.get(category_key)
        scored_matches = []
        max_score = 0
        for item, criteria in kbCategory.items():
            score = 0.0
            for char_key, char_values in criteria.items():
                # Weighted scoring: if first element is a float, treat as weight
                if isinstance(char_values, list) and len(char_values) > 1 and isinstance(char_values[0], float):
                    weight = char_values[0]
                    values = char_values[1:]
                else:
                    weight = 1.0
                    values = char_values

                # Direct match
                if char_key in self.project_characteristics:
                    user_value = self.project_characteristics[char_key]
                    if user_value in values or (
                        char_key == "Life Cycle" and any(lc in values for lc in self.recommendations.get("Life Cycle", []))
                    ):
                        score += weight
                # Implicit match
                elif char_key.endswith("(Implicit)"):
                    inferred_key = char_key.replace(" (Implicit)", "")
                    if inferred_key in self.project_characteristics and self.project_characteristics[inferred_key] in values:
                        score += weight
                # Special keys
                elif char_key in ["Scalability Needs", "Real-time Processing", "DevOps Implemented"]:
                    if char_key in self.project_characteristics and self.project_characteristics[char_key] in values:
                        score += weight
            if score > 0:
                scored_matches.append((score, item))
                if score > max_score:
                    max_score = score
        # Only return items with the highest score
        best_matches = [item for score, item in scored_matches if score == max_score]
        return best_matches

    def _add_general_considerations(self):
        """Adds concise general advice based on the overall project profile."""
        if self.project_characteristics["Project Complexity"] == "Very High" and "Agile" not in self.recommendations["Life Cycle"]:
            self.recommendations["Considerations"].append("Use agile or iterative methods for complex projects.")
        if self.project_characteristics["Requirements Clarity"] == "Unclear":
            self.recommendations["Considerations"].append("Start with prototyping and frequent feedback.")
        if self.project_characteristics["Team Size"] == "Very Large (50+)":
            self.recommendations["Considerations"].append("Apply scaled agile frameworks for large teams.")
        if self.project_characteristics["Budget"] == "Low":
            self.recommendations["Considerations"].append("Choose open-source and lean solutions.")
        if self.project_characteristics["Urgency/Time-to-Market"] == "High":
            self.recommendations["Considerations"].append("Focus on MVP and fast delivery.")
        if "DevOps" in self.recommendations["Methodology"] or self.project_characteristics["DevOps Implemented"] == "Yes":
            self.recommendations["Considerations"].append("Automate with CI/CD pipelines for efficiency.")


    def save_results_to_csv(self, filename="project_data.csv"):
        """
        Saves user input and top recommendations (max score) to a CSV file in the specified format.
        Columns: Project Size, Project Complexity, Requirements Clarity, Team Size, Budget, Regulatory Compliance,
        Innovation Level, Risk Tolerance, Urgency/Time-to-Market, Life Cycle, Methodology, Language,
        Architectural Model, Timeframe Management
        """
        # Define the columns in order
        columns = [
            "Project Size", "Project Complexity", "Requirements Clarity", "Team Size", "Stakeholder Involvement", "Budget",
            "Regulatory Compliance", "Innovation Level", "Risk Tolerance", "Urgency/Time-to-Market", "Project Type (Implicit)", "DevOps Implemented",
            "Life Cycle", "Methodology", "Language", "Model (Architectural)", "Timeframe Management", "Risk Management", "Testing Strategy", "Deployment", "Documentation", "Collaboration Tools"
        ]
        # Prepare the row: user input + top recommendation for each category
        row = []
        for col in columns:
            if col in self.project_characteristics:
                row.append(self.project_characteristics[col])
            elif col == "Model (Architectural)":
                # Use top architectural recommendation
                items = self.recommendations.get("Model (Architectural)", [])
                row.append(items[0] if items else "")
            elif col == "Timeframe Management":
                items = self.recommendations.get("Timeframe Management", [])
                row.append(items[0] if items else "")
            else:
                # For recommendation categories
                items = self.recommendations.get(col, [])
                row.append(items[0] if items else "")

        # Write to CSV
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            
            writer = csv.writer(csvfile)
            # Write header only if file doesnt exist
            if not file_exists:
                writer.writerow(columns)
            writer.writerow(row)

    def display_recommendations(self):
        """Prints the final recommendations and a table of all user input and recommendations."""
        print("\n----------------------- Final Project Development and Management Recommendations -------------------------")
        print("\n{:<30} | {:<50}".format("Category", "Value"))
        print("-" * 85)
        # Display user input
        for category, items in self.project_characteristics.items():
            print("{:<30} | {:<50}".format(category, str(items)))
        # Display recommendations
        for category, items in self.recommendations.items():
            if items:
                for item in items:
                    print("{:<30} | {:<50}".format(category, str(item)))
            else:
                print("{:<30} | {:<50}".format(category, "No specific recommendations based on current input."))
        # Save to CSV
        self.save_results_to_csv()
        print("\nResults saved to project_data.csv in the current directory.")


        # print("\n--- Important Considerations ---")
        # if self.recommendations["Considerations"]:
        #     for consideration in self.recommendations["Considerations"]:
        #         print(f"  - {consideration}")
        # else:
        #     print("  No specific additional considerations at this time.")

        # print("\n--- Disclaimer ---")
        # print("This is a decision support system providing recommendations based on predefined rules. ")
        # print("Always exercise professional judgment and adapt these recommendations to your specific project context.")

if __name__ == "__main__":
    dss = ProjectDSS()
    i=100000
    while(i):
        dss.get_user_input()
        dss.analyze_and_recommend()
        dss.display_recommendations()
        dss.reset()
        i-=1