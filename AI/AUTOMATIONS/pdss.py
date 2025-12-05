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
                    "Project Complexity": ["Low", "Medium"],
                    "Requirements Clarity": ["Clear"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": ["low"],
                    "Risk Tolerance": ["Low"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Innovation Level": ["Low", "Medium"],
                    "Budget": ["Medium", "High"],
                    "Regulatory Compliance": ["low"]
                },
                "Agile": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)", "Very Large (50+)"],
                    "Stakeholder Involvement": ["High"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["High"],
                    "Innovation Level": ["Medium", "High", "Very High"],
                    "Budget": ["Medium", "High", "Very High"],
                    "Regulatory Compliance": ["Low", "Medium"]
                },
                "Iterative": {
                    "Project Complexity": ["Medium", "High"],
                    "Requirements Clarity": ["Evolving"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": ["Medium"],
                    "Risk Tolerance": ["Medium"],
                    "Urgency/Time-to-Market": ["Medium"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Medium", "High"],
                    "Regulatory Compliance": ["Low"]
                },
                "Spiral": {
                    "Project Complexity": ["High", "Very High"],
                    "Requirements Clarity": ["Unclear", "Evolving"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": ["Medium", "High"],
                    "Risk Tolerance": ["High"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Innovation Level": ["High"],
                    "Budget": ["High", "Very High"],
                    "Regulatory Compliance": ["Low", "Medium"]
                },
                "V-Model": {
                    "Project Complexity": ["Medium", "High"],
                    "Requirements Clarity": ["Clear"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": ["Low", "Medium"],
                    "Risk Tolerance": ["Low", "Medium"],
                    "Urgency/Time-to-Market": ["Low", "Medium", "High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Medium", "High"],
                    "Regulatory Compliance": ["High", "Very High"]
                },
                "DevOps Lifecycle": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Requirements Clarity": ["Unclear", "Evolving"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)", "Very Large (50+)"],
                    "Stakeholder Involvement": ["Medium", "High", "Very High"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Medium", "High"],
                    "Regulatory Compliance": ["Low"],
                    "DevOps Implemented": ["Yes"]
                },
                "Rapid Application Development (RAD)": {
                    "Project Complexity": ["Low", "Medium"],
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Stakeholder Involvement": ["Medium", "High"],
                    "Risk Tolerance": ["Low", "Medium"],
                    "Urgency/Time-to-Market": ["High", "Very High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Low", "Medium"],
                    "Regulatory Compliance": ["Low"]
                },
                "Incremental": {
                    "Project Complexity": ["Medium", "High"],
                    "Requirements Clarity": ["Evolving"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"],
                    "Stakeholder Involvement": ["Low", "Medium"],
                    "Risk Tolerance": ["Medium"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Low", "Medium"],
                    "Regulatory Compliance": ["Low"]
                },
                "Big Bang": {
                    "Project Complexity": ["Low"],
                    "Requirements Clarity": ["Unclear"],
                    "Team Size": ["Small (1-5)"],
                    "Stakeholder Involvement": ["Low"],
                    "Risk Tolerance": ["High"],
                    "Urgency/Time-to-Market": ["High"],
                    "Innovation Level": ["Low", "Medium"],
                    "Budget": ["Low"],
                    "Regulatory Compliance": ["Low"]
                },
                "Prototyping": {
                    "Project Complexity": ["Medium", "High"],
                    "Requirements Clarity": ["Unclear", "Evolving"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"],
                    "Stakeholder Involvement": ["High"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Innovation Level": ["High"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Budget": ["Low", "Medium", "High"],
                    "Regulatory Compliance": ["Low"]
                },
                # General/Fallback Recommendations
                "General Recommendation: Low Complexity": {"Project Complexity": ["Low"]},
                "General Recommendation: Medium Complexity": {"Project Complexity": ["Medium"]},
                "General Recommendation: High Complexity": {"Project Complexity": ["High"]},
                "General Recommendation: Very High Complexity": {"Project Complexity": ["Very High"]},
                "General Recommendation: Clear Requirements": {"Requirements Clarity": ["Clear"]},
                "General Recommendation: Evolving Requirements": {"Requirements Clarity": ["Evolving"]},
                "General Recommendation: Unclear Requirements": {"Requirements Clarity": ["Unclear"]},
                "General Recommendation: Low Risk Tolerance": {"Risk Tolerance": ["Low"]},
                "General Recommendation: Medium Risk Tolerance": {"Risk Tolerance": ["Medium"]},
                "General Recommendation: High Risk Tolerance": {"Risk Tolerance": ["High"]},
                "General Recommendation: High Regulatory Compliance": {"Regulatory Compliance": ["High"]},
                "General Recommendation: High Innovation": {"Innovation Level": ["High"]},
                "General Recommendation: Medium Innovation": {"Innovation Level": ["Medium"]},
                "General Recommendation: Low Innovation": {"Innovation Level": ["Low"]},
                "General Recommendation: High Urgency": {"Urgency/Time-to-Market": ["High"]},
                "General Recommendation: Medium Urgency": {"Urgency/Time-to-Market": ["Medium"]},
                "General Recommendation: Low Urgency": {"Urgency/Time-to-Market": ["Low"]},
                "General Recommendation: Small Team": {"Team Size": ["Small (1-5)"]},
                "General Recommendation: Medium Team": {"Team Size": ["Medium (6-20)"]},
                "General Recommendation: Large Team": {"Team Size": ["Large (21-50)"]},
                "General Recommendation: Very Large Team": {"Team Size": ["Very Large (50+)"]},
                "General Recommendation: High Budget": {"Budget": ["High"]},
                "General Recommendation: Very High Budget": {"Budget": ["Very High"]},
                "General Recommendation: Low Budget": {"Budget": ["Low"]},
                "General Recommendation: Medium Budget": {"Budget": ["Medium"]},
                "General Recommendation: High Stakeholder Involvement": {"Stakeholder Involvement": ["High"]},
                "General Recommendation: Medium Stakeholder Involvement": {"Stakeholder Involvement": ["Medium"]},
                "General Recommendation: Low Stakeholder Involvement": {"Stakeholder Involvement": ["Low"]},
                "General Recommendation: DevOps Implemented": {"DevOps Implemented": ["Yes"]},
                "General Recommendation: No DevOps Implemented": {"DevOps Implemented": ["No"]},
                "General Recommendation: MVP Approach": {"Urgency/Time-to-Market": ["High"], "Project Complexity": ["Low", "Medium"]},
            },

            # --- Methodologies/Frameworks ---
            "Methodology": {
                "Scrum": {
                    "Life Cycle": ["Agile"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"],
                    "Stakeholder Involvement": ["High"],
                    "Requirements Clarity": ["Evolving", "Clear"],
                    "Urgency/Time-to-Market": ["High"]
                },
                "Kanban": {
                    "Life Cycle": ["Agile"],
                    "Requirements Clarity": ["Evolving", "Clear"],
                    "Urgency/Time-to-Market": ["High"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "Extreme Programming (XP)": {
                    "Life Cycle": ["Agile"],
                    "Team Size": ["Small (1-5)"],
                    "Requirements Clarity": ["Evolving"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Innovation Level": ["High"]
                },
                "DevOps": {
                    "Life Cycle": ["Agile", "DevOps Lifecycle"],
                    "Urgency/Time-to-Market": ["High"],
                    "Innovation Level": ["Medium", "High"],
                    "DevOps Implemented": ["Yes"],
                    "Scalability Needs": ["High"]
                },
                "PRINCE2": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Regulatory Compliance": ["High"],
                    "Budget": ["Medium", "High", "Very High"],
                    "Project Size": ["Medium", "Large", "Very Large"],
                    "Requirements Clarity": ["Clear"],
                    "Risk Tolerance": ["Low", "Medium"]
                },
                "PMBOK (Project Management Body of Knowledge)": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Project Size": ["Medium", "Large", "Very Large"],
                    "Requirements Clarity": ["Clear"],
                    "Risk Tolerance": ["Low", "Medium"]
                },
                "SAFe (Scaled Agile Framework)": {
                    "Project Size": ["Very Large"],
                    "Life Cycle": ["Agile"],
                    "Team Size": ["Very Large (50+)"],
                    "Stakeholder Involvement": ["High"],
                    "Requirements Clarity": ["Evolving", "Clear"]
                },
                "LeSS (Large Scale Scrum)": {
                    "Project Size": ["Large", "Very Large"],
                    "Life Cycle": ["Agile"],
                    "Team Size": ["Large (21-50)", "Very Large (50+)"],
                    "Stakeholder Involvement": ["High"]
                },
                "Crystal": {
                    "Project Complexity": ["Low", "Medium"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"],
                    "Requirements Clarity": ["Clear", "Evolving"],
                    "Urgency/Time-to-Market": ["Medium", "High"]
                },
                "Feature Driven Development (FDD)": {
                    "Life Cycle": ["Agile"],
                    "Project Complexity": ["Medium", "High"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)"],
                    "Requirements Clarity": ["Evolving"]
                },
                "DSDM (Dynamic Systems Development Method)": {
                    "Life Cycle": ["Agile"],
                    "Project Complexity": ["Medium", "High"],
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Urgency/Time-to-Market": ["High"]
                },
                "RUP (Rational Unified Process)": {
                    "Project Complexity": ["High", "Very High"],
                    "Requirements Clarity": ["Evolving", "Clear"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)"],
                    "Risk Tolerance": ["Medium", "High"]
                },
                "Scrumban": {
                    "Life Cycle": ["Agile"],
                    "Requirements Clarity": ["Evolving"],
                    "Urgency/Time-to-Market": ["High"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"]
                },
                # General/Fallback Recommendations
                "General Recommendation: Agile Methodology": {"Life Cycle": ["Agile"]},
                "General Recommendation: Traditional Methodology": {"Life Cycle": ["Waterfall", "V-Model"]},
                "General Recommendation: Scaled Agile": {"Team Size": ["Large (21-50)", "Very Large (50+)"]},
                "General Recommendation: High Regulatory Compliance": {"Regulatory Compliance": ["High"]},
                "General Recommendation: High Stakeholder Involvement": {"Stakeholder Involvement": ["High"]},
                "General Recommendation: DevOps Practices": {"DevOps Implemented": ["Yes"]},
                "General Recommendation: Rapid Delivery": {"Urgency/Time-to-Market": ["High"]},
                "General Recommendation: Small Team": {"Team Size": ["Small (1-5)"]},
                "General Recommendation: Medium Team": {"Team Size": ["Medium (6-20)"]},
                "General Recommendation: Large Team": {"Team Size": ["Large (21-50)"]},
                "General Recommendation: Very Large Team": {"Team Size": ["Very Large (50+)"]},
                "General Recommendation: MVP Approach": {"Urgency/Time-to-Market": ["High"], "Project Complexity": ["Low", "Medium"]},
            },

            # --- Programming Languages (Simplified mapping) ---
            # ["Web Application", "Mobile App", "Desktop App", "Cross Platform App", "Data Science", "Machine Learning", "Embedded System","Enterprise Applications", "API/Backend Service", "Web Development (Backend)", Web Development (Full-stack), "Game Development", "System Programming", "Engineering", "Other"]

            "Language": {
                "Python": {
                    "Project Type (Implicit)": ["Data Science", "Web Application", "Web Development (Backend)", "Automation", "Scripting", "Machine Learning", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Project Complexity": ["Low", "Medium", "High"],
                    "Budget": ["Low", "Medium"]
                },
                "Java": {
                    "Project Type (Implicit)": ["Enterprise Applications", "Android", "Mobile App", "Large-Scale Systems", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Budget": ["Medium", "High"]
                },
                "JavaScript (with Node.js)": {
                    "Project Type (Implicit)": ["Web Application", "Web Development (Full-stack)", "Real-time Applications", "API/Backend Service", "Cross Platform App"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Project Complexity": ["Low", "Medium", "High"],
                    "Budget": ["Low", "Medium"]
                },
                "Dart (with Flutter)": {
                    "Project Type (Implicit)": ["Real-time Applications", "Cross Platform App"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Project Complexity": ["Low", "Medium", "High"],
                    "Budget": ["Low", "Medium", "High"]
                },
                "TypeScript": {
                    "Project Type (Implicit)": ["Web Application", "Web Development (Full-stack)", "Frontend", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Project Complexity": ["Low", "Medium", "High"],
                    "Budget": ["Low", "Medium"]
                },
                "C# (with Unity)": {
                    "Project Type (Implicit)": [".NET Applications", "Desktop App", "Windows Applications", "Game Development", "Enterprise Applications"],
                    "Urgency/Time-to-Market": ["Low", "Medium", "Very High"],
                    "Project Complexity": ["Medium", "High"],
                    "Budget": ["Medium", "High"]
                },
                "C++": {
                    "Project Type (Implicit)": ["System Programming", "Desktop App", "Game Development", "High-Performance Computing", "Embedded System"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Project Complexity": ["High", "Very High"],
                    "Budget": ["High", "Very High"]
                },
                "Go": {
                    "Project Type (Implicit)": ["Concurrent Applications", "Cloud Infrastructure", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Project Complexity": ["Medium", "High"],
                    "Budget": ["Medium", "High"]
                },
                "Rust": {
                    "Project Type (Implicit)": ["System Programming", "Embedded System", "WebAssembly", "High-Performance Computing"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Project Complexity": ["High", "Very High"],
                    "Budget": ["Medium", "High"]
                },
                "PHP": {
                    "Project Type (Implicit)": ["Web Application", "Web Development (Backend)", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["High"],
                    "Project Complexity": ["Low", "Medium"],
                    "Budget": ["Low", "Medium"]
                },
                "Kotlin": {
                    "Project Type (Implicit)": ["Android", "Mobile App", "Web Application", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["Low", "Medium", "High"],
                    "Project Complexity": ["Medium", "High"],
                    "Budget": ["Medium", "High"]
                },
                "Swift": {
                    "Project Type (Implicit)": ["Mobile App", "iOS", "API/Backend Service"],
                    "Urgency/Time-to-Market": ["Low", "Medium", "High"],
                    "Project Complexity": ["Medium", "High"],
                    "Budget": ["Medium", "High"]
                },
                "R": {
                    "Project Type (Implicit)": ["Data Science", "Statistics", "Machine Learning"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Project Complexity": ["Low", "Medium"],
                    "Budget": ["Low", "Medium"]
                },
                "MATLAB": {
                    "Project Type (Implicit)": ["Data Science", "Simulation", "Engineering"],
                    "Urgency/Time-to-Market": ["Low", "Medium", "High"],
                    "Project Complexity": ["Medium", "High"],
                    "Budget": ["High", "Very High"]
                },
                # General/Fallback Recommendations
                "General Recommendation: Web Application": {"Project Type (Implicit)": ["Web Application"]},
                "General Recommendation: Mobile App": {"Project Type (Implicit)": ["Mobile App"]},
                "General Recommendation: Desktop App": {"Project Type (Implicit)": ["Desktop App"]},
                "General Recommendation: Data Science/ML": {"Project Type (Implicit)": ["Data Science", "Machine Learning"]},
                "General Recommendation: Embedded System": {"Project Type (Implicit)": ["Embedded System"]},
                "General Recommendation: Game": {"Project Type (Implicit)": ["Game Development"]},
                "General Recommendation: Enterprise Software": {"Project Type (Implicit)": ["Enterprise Applications"]},
                "General Recommendation: API/Backend Service": {"Project Type (Implicit)": ["API/Backend Service"]},
                "General Recommendation: Other Project Type": {"Project Type (Implicit)": ["Other"]},
            },

            # --- Architectural Models ---
            "Model (Architectural)": {
                "Microservices": {
                    "Project Complexity": ["High", "Very High"],
                    "Team Size": ["Large (21-50)", "Very Large (50+)"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["High"],
                    "Budget": ["High", "Very High"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Requirements Clarity": ["Unclear"]
                },
                "Monolithic": {
                    "Project Complexity": ["Low", "Medium"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"],
                    "Scalability Needs": ["Low", "Medium"],
                    "Innovation Level": ["Low", "Medium"],
                    "Budget": ["Low", "Medium"],
                    "Urgency/Time-to-Market": ["High"],
                    "Requirements Clarity": ["Clear"]
                },
                "Client-Server": {
                    "Project Complexity": ["Low", "Medium", "High"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Scalability Needs": ["Low", "Medium","High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["High"],
                    "Requirements Clarity": ["Clear"]
                },
                "Event-Driven": {
                    "Project Complexity": ["High"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)", "Large (21-50)"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["High"],
                    "Budget": ["High", "Very High"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Real-time Processing": ["Yes"],
                    "Requirements Clarity": ["Clear"]
                },
                "Serverless": {
                    "Project Complexity": ["Low", "Medium"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["Medium"],
                    "Budget": ["Low", "Medium"],
                    "Urgency/Time-to-Market": ["High"],
                    "Requirements Clarity": ["Clear"]
                },
                "Layered (n-tier)": {
                    "Project Complexity": ["Medium", "High"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Requirements Clarity": ["Clear", "Evolving"]
                },
                "Service-Oriented Architecture (SOA)": {
                    "Project Complexity": ["High", "Very High"],
                    "Team Size": ["Large (21-50)", "Very Large (50+)"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["Medium", "High"],
                    "Budget": ["Medium", "High", "Very High"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Requirements Clarity": ["Clear"]
                },
                "Peer-to-Peer": {
                    "Project Complexity": ["Medium", "High"],
                    "Team Size": ["Very Large (50+)"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["High"],
                    "Budget": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["Low"],
                    "Requirements Clarity": ["Evolving"]
                },
                "Space-Based": {
                    "Project Complexity": ["High", "Very High"],
                    "Scalability Needs": ["High"],
                    "Innovation Level": ["High", "Very High"],
                    "Budget": ["High", "Very High"],
                    "Urgency/Time-to-Market": ["High"],
                    "Requirements Clarity": ["Clear"]
                },
                # General/Fallback Recommendations
                "General Recommendation: High Scalability": {"Scalability Needs": ["High"]},
                "General Recommendation: Real-time Processing": {"Real-time Processing": ["Yes"]},
                "General Recommendation: Low Scalability": {"Scalability Needs": ["Low"]},
                "General Recommendation: Medium Scalability": {"Scalability Needs": ["Medium"]},
                "General Recommendation: Serverless": {"Scalability Needs": ["High"], "Budget": ["Low", "Medium"]},
                "General Recommendation: Layered": {"Project Complexity": ["Medium", "High"]},
                "General Recommendation: Event-Driven": {"Real-time Processing": ["Yes"]},
                "General Recommendation: Monolithic": {"Project Complexity": ["Low", "Medium"]},
                "General Recommendation: Microservices": {"Project Complexity": ["High", "Very High"], "Scalability Needs": ["High"]},
            },

            # --- Timeframe Management ---
            "Timeframe Management": {
                "Fixed Deadline": {
                    "Requirements Clarity": ["Clear"],
                    "Project Complexity": ["Low", "Medium"],
                    "Risk Tolerance": ["Low"],
                    "Urgency/Time-to-Market": ["High"],
                    "Innovation Level": ["Low", "Medium"],
                    "DevOps Implemented": ["No"],
                },
                "Flexible Deadline": {
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Risk Tolerance": ["Low", "Medium"],
                    "Urgency/Time-to-Market": ["Low", "Medium", "High"],
                    "Innovation Level": ["High"],
                    "DevOps Implemented": ["Yes", "No"],

                },
                "Iterative Sprints (e.g., 2-week)": {
                    "Requirements Clarity": ["Evolving", "Clear"],
                    "Project Complexity": ["Low", "Medium"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["High"],
                    "Innovation Level": ["Low", "Medium"],
                    "DevOps Implemented": ["No"],
                    "Life Cycle": ["Agile"],
                },
                "Continuous Delivery": {
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Risk Tolerance": ["Medium", "High", "Very High"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Innovation Level": ["High"],
                    "DevOps Implemented": ["Yes"],
                    "Life Cycle": ["Agile"],
                },
                "Milestone-Based": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Requirements Clarity": ["Clear", "Evolving"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["Low", "Medium"],
                    "Innovation Level": ["Medium", "High"],
                    "DevOps Implemented": ["No"],
                },
                "Rolling Wave Planning": {
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Project Complexity": ["High", "Very High"],
                    "Risk Tolerance": ["Low", "Medium"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Innovation Level": ["Medium"],
                    "DevOps Implemented": ["Yes"],
                },
                "Hybrid (Fixed + Iterative)": {
                    "Requirements Clarity": ["Clear", "Evolving"],
                    "Project Complexity": ["Medium", "High"],
                    "Risk Tolerance": ["Medium", "High"],
                    "Urgency/Time-to-Market": ["Medium", "High"],
                    "Innovation Level": ["Medium", "High"],
                    "DevOps Implemented": ["No"],
                },
                # General/Fallback Recommendations
                "General Recommendation: High Urgency": {"Urgency/Time-to-Market": ["High"]},
                "General Recommendation: Medium Urgency": {"Urgency/Time-to-Market": ["Medium"]},
                "General Recommendation: Low Urgency": {"Urgency/Time-to-Market": ["Low"]},
                "General Recommendation: Evolving Requirements": {"Requirements Clarity": ["Evolving"]},
                "General Recommendation: Unclear Requirements": {"Requirements Clarity": ["Unclear"]},
                "General Recommendation: Clear Requirements": {"Requirements Clarity": ["Clear"]},
                "General Recommendation: DevOps Delivery": {"DevOps Implemented": ["Yes"]},
                "General Recommendation: MVP Approach": {"Urgency/Time-to-Market": ["High"], "Project Complexity": ["Low", "Medium"]},
            },
            # ...existing code...
            "Risk Management": {
                "Proactive Risk Assessment": {
                    "Project Complexity": ["High", "Very High"],
                    "Risk Tolerance": ["Low", "Medium"]
                },
                "Regular Risk Reviews": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "Contingency Planning": {
                    "Risk Tolerance": ["Low", "Medium", "High"],
                    "Budget": ["Medium", "High", "Very High"]
                },
                "General Recommendation: Risk Register": {"Project Complexity": ["Medium", "High", "Very High"]},
                "General Recommendation: Early Stakeholder Engagement": {"Stakeholder Involvement": ["High"]},
            },
            "Testing Strategy": {
                "Automated Testing": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Urgency/Time-to-Market": ["High"],
                    "DevOps Implemented": ["Yes"]
                },
                "Manual Testing": {
                    "Project Complexity": ["Low", "Medium"],
                    "Budget": ["Low", "Medium"]
                },
                "Continuous Integration Testing": {
                    "DevOps Implemented": ["Yes"],
                    "Urgency/Time-to-Market": ["High"]
                },
                "Exploratory Testing": {
                    "Requirements Clarity": ["Unclear", "Evolving"],
                    "Innovation Level": ["High"]
                },
                "General Recommendation: Test Early and Often": {"Project Complexity": ["Medium", "High", "Very High"]},
                "General Recommendation: Regression Testing": {"Project Complexity": ["High", "Very High"]},
            },
            "Deployment": {
                "Continuous Deployment": {
                    "DevOps Implemented": ["Yes"],
                    "Urgency/Time-to-Market": ["High"]
                },
                "Manual Release": {
                    "Project Complexity": ["Low", "Medium"],
                    "Budget": ["Low", "Medium"]
                },
                "Staged Rollout": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Team Size": ["Large (21-50)", "Very Large (50+)"]
                },
                "Blue-Green Deployment": {
                    "Project Complexity": ["High", "Very High"],
                    "Risk Tolerance": ["Low", "Medium"]
                },
                "General Recommendation: Rollback Plan": {"Project Complexity": ["Medium", "High", "Very High"]},
                "General Recommendation: Monitor Deployments": {"DevOps Implemented": ["Yes"]},
            },
            "Documentation": {
                "Comprehensive Documentation": {
                    "Project Complexity": ["High", "Very High"],
                    "Team Size": ["Large (21-50)", "Very Large (50+)"]
                },
                "Lean Documentation": {
                    "Project Complexity": ["Low", "Medium"],
                    "Budget": ["Low", "Medium"]
                },
                "Living Documentation (Wiki)": {
                    "Requirements Clarity": ["Evolving", "Unclear"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "API Documentation": {
                    "Project Type (Implicit)": ["API/Backend Service"],
                    "Urgency/Time-to-Market": ["High"]
                },
                "General Recommendation: Update Documentation Regularly": {"Project Complexity": ["Medium", "High", "Very High"]},
                "General Recommendation: Use Diagrams": {"Project Complexity": ["High", "Very High"]},
            },
            "Collaboration Tools": {
                "Version Control Systems (e.g., Git)": {
                    "Project Complexity": ["Medium", "High", "Very High"],
                    "Team Size": ["Medium (6-20)", "Large (21-50)", "Very Large (50+)"]
                },
                "Collaboration Platforms (e.g., Confluence, Slack)": {
                    "Project Complexity": ["Low", "Medium", "High"],
                    "Team Size": ["Small (1-5)", "Medium (6-20)"]
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
        scores them by number of matches, and returns those with the highest match count.
        """
        kbCategory = self.knowledge_base.get(category_key)
        scored_matches = []
        max_score = 0
        for item, criteria in kbCategory.items():
            score = 0
            total = len(criteria)
            for char_key, char_values in criteria.items():
                # Direct match
                if char_key in self.project_characteristics:
                    user_value = self.project_characteristics[char_key]
                    if user_value in char_values or (
                        char_key == "Life Cycle" and any(lc in char_values for lc in self.recommendations.get("Life Cycle", []))
                    ):
                        score += 1
                # Implicit match
                elif char_key.endswith("(Implicit)"):
                    inferred_key = char_key.replace(" (Implicit)", "")
                    if inferred_key in self.project_characteristics and self.project_characteristics[inferred_key] in char_values:
                        score += 1
                # Special keys
                elif char_key in ["Scalability Needs", "Real-time Processing", "DevOps Implemented"]:
                    if char_key in self.project_characteristics and self.project_characteristics[char_key] in char_values:
                        score += 1
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
            # Write header only if file is new
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
        print("\nResults saved to project_dss_results.csv in the current directory.")


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
    i=1
    while(i):
        dss.get_user_input()
        dss.analyze_and_recommend()
        dss.display_recommendations()
        dss.reset()
        i-=1