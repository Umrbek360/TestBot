import json
import os
from typing import Dict, List, Any, Optional


class TestManager:
    def __init__(self, questions_file: str = "questions.json"):
        self.questions_file = questions_file
        self.questions_data = self._load_questions()
        self.active_sessions = {}  # Store active test sessions

    def _load_questions(self) -> Dict[str, Any]:
        """Load questions data from JSON file."""
        if os.path.exists(self.questions_file):
            try:
                with open(self.questions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_default_questions()
        return self._create_default_questions()

    def _create_default_questions(self) -> Dict[str, Any]:
        """Create default questions structure if file doesn't exist."""
        default_data = {
            "subjects": {
                "math": "Matematika",
                "physics": "Fizika",
                "chemistry": "Kimyo",
                "biology": "Biologiya"
            },
            "questions": {
                "math": [
                    {
                        "question": "2 + 2 = ?",
                        "options": ["3", "4", "5", "6"],
                        "correct": 1
                    },
                    {
                        "question": "5 × 3 = ?",
                        "options": ["12", "15", "18", "20"],
                        "correct": 1
                    },
                    {
                        "question": "10 ÷ 2 = ?",
                        "options": ["3", "4", "5", "6"],
                        "correct": 2
                    },
                    {
                        "question": "7 + 8 = ?",
                        "options": ["14", "15", "16", "17"],
                        "correct": 1
                    },
                    {
                        "question": "9 × 4 = ?",
                        "options": ["32", "34", "36", "38"],
                        "correct": 2
                    },
                    {
                        "question": "20 - 7 = ?",
                        "options": ["11", "12", "13", "14"],
                        "correct": 2
                    },
                    {
                        "question": "6² = ?",
                        "options": ["32", "34", "36", "38"],
                        "correct": 2
                    },
                    {
                        "question": "√16 = ?",
                        "options": ["2", "3", "4", "5"],
                        "correct": 2
                    },
                    {
                        "question": "15 ÷ 3 = ?",
                        "options": ["4", "5", "6", "7"],
                        "correct": 1
                    },
                    {
                        "question": "3 × 7 = ?",
                        "options": ["19", "20", "21", "22"],
                        "correct": 2
                    }
                ],
                "physics": [
                    {
                        "question": "Yerning tortishish kuchi qancha m/s²?",
                        "options": ["9.8", "10.8", "8.9", "9.9"],
                        "correct": 0
                    },
                    {
                        "question": "Yorug'lik tezligi qancha km/s?",
                        "options": ["300000", "299792458", "280000", "320000"],
                        "correct": 0
                    },
                    {
                        "question": "Newton qonunlarining nechta?",
                        "options": ["2", "3", "4", "5"],
                        "correct": 1
                    },
                    {
                        "question": "Ohm qonuni formulasi qanday?",
                        "options": ["V = I×R", "P = V×I", "F = m×a", "E = m×c²"],
                        "correct": 0
                    },
                    {
                        "question": "Kuchlanish birligi nima?",
                        "options": ["Volt", "Amper", "Om", "Vatt"],
                        "correct": 0
                    },
                    {
                        "question": "Issiqlik uzatishning necha xil turi bor?",
                        "options": ["2", "3", "4", "5"],
                        "correct": 1
                    },
                    {
                        "question": "Elastiklik moduli kim tomonidan aniqlangan?",
                        "options": ["Guk", "Young", "Newton", "Ohm"],
                        "correct": 1
                    },
                    {
                        "question": "Elektr toki qanday o'lchanadi?",
                        "options": ["Volt", "Amper", "Om", "Joule"],
                        "correct": 1
                    },
                    {
                        "question": "Magnit maydon birligi nima?",
                        "options": ["Tesla", "Gauss", "Weber", "Henry"],
                        "correct": 0
                    },
                    {
                        "question": "Radioaktivlik hodisasini kim kashf etgan?",
                        "options": ["Curie", "Becquerel", "Rutherford", "Einstein"],
                        "correct": 1
                    }
                ],
                "chemistry": [
                    {
                        "question": "Suvning kimyoviy formulasi qanday?",
                        "options": ["H2O", "H2O2", "HO", "H3O"],
                        "correct": 0
                    },
                    {
                        "question": "Kislorodning atom massasi qancha?",
                        "options": ["16", "15", "17", "18"],
                        "correct": 0
                    },
                    {
                        "question": "Davriy sistemada nechta element bor?",
                        "options": ["116", "117", "118", "119"],
                        "correct": 2
                    },
                    {
                        "question": "Tuzning kimyoviy formulasi?",
                        "options": ["NaCl", "KCl", "CaCl2", "MgCl2"],
                        "correct": 0
                    },
                    {
                        "question": "pH shkalasi nechanchi oraliqda?",
                        "options": ["0-12", "0-14", "1-13", "1-14"],
                        "correct": 1
                    },
                    {
                        "question": "Kislotalarning asosiy xususiyati nima?",
                        "options": ["H+ ionini beradi", "OH- ionini beradi", "Neytral", "Tuz hosil qiladi"],
                        "correct": 0
                    },
                    {
                        "question": "Organik kimyoning asosiy elementi?",
                        "options": ["Vodorod", "Kislorod", "Uglerod", "Azot"],
                        "correct": 2
                    },
                    {
                        "question": "Gazlarning molyar hajmi (n.sh.) qancha?",
                        "options": ["22.4 L", "24.4 L", "20.4 L", "26.4 L"],
                        "correct": 0
                    },
                    {
                        "question": "Avogadro soni qancha?",
                        "options": ["6.02×10²³", "6.22×10²³", "5.02×10²³", "7.02×10²³"],
                        "correct": 0
                    },
                    {
                        "question": "Metanning kimyoviy formulasi?",
                        "options": ["CH4", "C2H4", "C2H6", "C3H8"],
                        "correct": 0
                    }
                ],
                "biology": [
                    {
                        "question": "Hujayra yadrosi qayerda joylashgan?",
                        "options": ["Sitoplazma", "Membrana", "Mitoxondriya", "Ribosoma"],
                        "correct": 0
                    },
                    {
                        "question": "DNK tarkibida qanday asoslar bor?",
                        "options": ["A,T,G,C", "A,U,G,C", "A,T,G,U", "T,U,G,C"],
                        "correct": 0
                    },
                    {
                        "question": "Fotosintez jarayonida nima hosil bo'ladi?",
                        "options": ["Kislorod", "Karbonat angidrid", "Suv", "Metan"],
                        "correct": 0
                    },
                    {
                        "question": "Odamda nechta xromosoma bor?",
                        "options": ["44", "45", "46", "47"],
                        "correct": 2
                    },
                    {
                        "question": "Yurak necha bo'linmadan iborat?",
                        "options": ["2", "3", "4", "5"],
                        "correct": 2
                    },
                    {
                        "question": "Respiratsiya jarayonida nima ishlab chiqariladi?",
                        "options": ["ATP", "ADP", "DNA", "RNA"],
                        "correct": 0
                    },
                    {
                        "question": "Gemoglobin qaysi organda ishlab chiqariladi?",
                        "options": ["Jigar", "Suyak iligi", "O'pka", "Buyrak"],
                        "correct": 1
                    },
                    {
                        "question": "Ovqat hazm qilish tizimi qaysi organ bilan boshlanadi?",
                        "options": ["Og'iz", "Oshqozon", "O'n ikki barmoq ichak", "Jigar"],
                        "correct": 0
                    },
                    {
                        "question": "Nervlar tizimining asosiy birligi?",
                        "options": ["Neyron", "Akson", "Dendrit", "Sinaps"],
                        "correct": 0
                    },
                    {
                        "question": "Qonning tarkibida qancha foiz suv bor?",
                        "options": ["80%", "85%", "90%", "95%"],
                        "correct": 2
                    }
                ]
            }
        }

        # Save default questions to file
        try:
            with open(self.questions_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving default questions: {e}")

        return default_data

    def get_subjects(self) -> Dict[str, str]:
        """Get all available subjects."""
        return self.questions_data.get("subjects", {})

    def get_question(self, subject_id: str, question_index: int) -> Optional[Dict[str, Any]]:
        """Get a specific question for a subject."""
        questions = self.questions_data.get("questions", {}).get(subject_id, [])

        if 0 <= question_index < len(questions):
            return questions[question_index]
        return None

    def start_test(self, user_id: int, subject_id: str) -> None:
        """Start a new test session for a user."""
        session_key = f"{user_id}_{subject_id}"
        self.active_sessions[session_key] = {
            "user_id": user_id,
            "subject_id": subject_id,
            "current_question": 0,
            "answers": [],
            "start_time": None
        }

    def record_answer(self, user_id: int, subject_id: str, question_index: int, selected_option: int) -> None:
        """Record user's answer for a question."""
        session_key = f"{user_id}_{subject_id}"

        if session_key not in self.active_sessions:
            self.start_test(user_id, subject_id)

        session = self.active_sessions[session_key]

        # Ensure answers list is long enough
        while len(session["answers"]) <= question_index:
            session["answers"].append(-1)

        session["answers"][question_index] = selected_option

    def calculate_results(self, user_id: int, subject_id: str) -> Dict[str, Any]:
        """Calculate test results for a user."""
        session_key = f"{user_id}_{subject_id}"

        if session_key not in self.active_sessions:
            return {"correct": 0, "total": 0, "percentage": 0}

        session = self.active_sessions[session_key]
        answers = session["answers"]
        questions = self.questions_data.get("questions", {}).get(subject_id, [])

        correct_count = 0
        total_questions = min(len(answers), len(questions), 10)

        for i in range(total_questions):
            if i < len(questions) and i < len(answers):
                if questions[i]["correct"] == answers[i]:
                    correct_count += 1

        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0

        # Clean up session
        if session_key in self.active_sessions:
            del self.active_sessions[session_key]

        return {
            "correct": correct_count,
            "total": total_questions,
            "percentage": percentage,
            "answers": answers[:total_questions]
        }

    def get_correct_answer(self, subject_id: str, question_index: int) -> int:
        """Get the correct answer index for a question."""
        question = self.get_question(subject_id, question_index)
        return question["correct"] if question else -1
