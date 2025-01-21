import random
import tkinter as tk
from questions import *


class Question:
    def __init__(self, number, text, answers, correct_answers):
        self.number = number
        self.text = text
        self.answers = answers
        self.correct_answers = correct_answers
        # Store original indices before shuffling
        self.original_indices = list(range(len(answers)))


def load_questions():
    return questions_test_2


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chemistry Quiz")
        self.score = 0
        self.total_questions = 0
        self.questions = load_questions()
        self.current_question = None
        self.selected_answers = []
        self.question_answered = False
        self.current_answer_mapping = []  # Store the current shuffle mapping

        # Bind keyboard events
        self.root.bind('<Key>', self.handle_key)
        self.root.bind('<Return>', lambda e: self.check_and_next())

        self.question_label = tk.Label(root, text="Welcome to the Chemistry Quiz!", font=("Arial", 16), wraplength=500)
        self.question_label.pack(pady=20)

        # Create a frame for each answer to hold checkbox and label
        self.answer_frames = []
        self.check_vars = []
        self.check_buttons = []
        self.answer_labels = []

        for i in range(4):
            frame = tk.Frame(root)
            frame.pack(anchor='w', padx=20, fill='x')
            self.answer_frames.append(frame)

            var = tk.IntVar()
            check_button = tk.Checkbutton(frame, variable=var)
            check_button.pack(side='left')

            answer_label = tk.Label(frame, text=f"{chr(97 + i)}) [Press {i + 1}]", anchor='w')
            answer_label.pack(side='left', fill='x')

            self.check_vars.append(var)
            self.check_buttons.append(check_button)
            self.answer_labels.append(answer_label)

        self.next_button = tk.Button(root, text="Submit [Press Enter]", command=self.check_and_next, state=tk.NORMAL)
        self.next_button.pack(pady=10)

        self.score_label = tk.Label(root, text=f"Score: {self.score}/{self.total_questions}", font=("Arial", 12))
        self.score_label.pack()

        self.next_question()

    def shuffle_answers(self):
        # Create list of tuples with (answer, original_index)
        answers_with_indices = list(enumerate(self.current_question.answers))
        random.shuffle(answers_with_indices)

        # Unpack the shuffled answers and store the mapping
        self.current_answer_mapping = []
        shuffled_answers = []
        for new_idx, (original_idx, answer) in enumerate(answers_with_indices):
            shuffled_answers.append(answer)
            self.current_answer_mapping.append(original_idx)

        return shuffled_answers

    def handle_key(self, event):
        if not self.questions or self.next_button.cget('state') == 'disabled':
            return

        # Handle number keys 1-4
        if event.char in ['1', '2', '3', '4']:
            index = int(event.char) - 1
            if index < len(self.check_vars) and not self.question_answered:
                current_value = self.check_vars[index].get()
                self.check_vars[index].set(1 - current_value)

    def next_question(self):
        # Reset colors of answer labels
        for label in self.answer_labels:
            label.config(bg=self.root.cget('bg'), fg='black')

        self.question_answered = False

        r = random.SystemRandom()
        if self.questions:
            self.current_question = r.choice(self.questions)
            self.questions.remove(self.current_question)

            self.question_label.config(
                text=f"Question {self.current_question.number}: {self.current_question.text}")

            # Shuffle the answers
            shuffled_answers = self.shuffle_answers()

            for i, answer in enumerate(shuffled_answers):
                self.answer_labels[i].config(text=f" [{i + 1}] {answer}")
                self.check_buttons[i].config(state=tk.NORMAL)
                self.check_vars[i].set(0)

            self.next_button.config(text="Submit [↵]", state=tk.NORMAL)
        else:
            self.question_label.config(text=f"Quiz completed! Final score: {self.score}/{self.total_questions}")
            self.next_button.config(state=tk.NORMAL, text="Finish [↵]")

    def check_and_next(self):
        if self.next_button.cget('text') == "Finish":
            self.root.quit()
            return

        if self.question_answered:
            self.next_question()
            return

        # Get user's selected answers and map them back to original indices
        user_answers = set()
        for new_idx, var in enumerate(self.check_vars):
            if var.get() == 1:
                original_idx = self.current_answer_mapping[new_idx]
                user_answers.add(original_idx)

        correct_answers = set(self.current_question.correct_answers)
        self.total_questions += 1

        # Color the answers using the mapping
        for new_idx, original_idx in enumerate(self.current_answer_mapping):
            if original_idx in correct_answers:
                self.answer_labels[new_idx].config(bg='#90EE90', fg='black')  # Light green
            elif new_idx in [i for i, var in enumerate(self.check_vars) if
                             var.get() == 1] and original_idx not in correct_answers:
                self.answer_labels[new_idx].config(bg='#FFB6C1', fg='black')  # Light red

        if user_answers == correct_answers:
            self.score += 1

        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")

        for button in self.check_buttons:
            button.config(state=tk.DISABLED)

        self.next_button.config(text="Next [↵]")
        self.question_answered = True


def run_quiz():
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_quiz()
