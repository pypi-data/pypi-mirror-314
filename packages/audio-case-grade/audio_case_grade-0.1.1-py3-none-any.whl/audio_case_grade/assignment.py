"""Top level display objects like grade and assignments for student"""

from .core import get_score
from .types import Assignment, Case, Score, Student, Transcript


def get_grade(score: Score) -> float:
    """Grade a score with a weighted grade on a scale of 100"""

    # Adjust this to your grading scale
    return score.lexical_density


def get_assignment(student: Student, transcript: Transcript, case: Case) -> Assignment:
    """Create an assignment"""

    student_score = get_score(transcript, case)
    student_grade = get_grade(student_score)

    return Assignment(
        student=student,
        transcript=transcript,
        case=case,
        score=student_score,
        grade=student_grade,
    )
