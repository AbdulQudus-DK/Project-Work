#NAME INPUT
name = input("Type your name:" )
print("Hello", name, "Welcome to the test.")
Are_You_Ready = input("Are you ready to start?")
Ready = Are_You_Ready == "yes" or "YES"
if Ready:
    print("Answer the 5 questions correctly.")

#INPUT OF QUESTIONS

    questions = [
        {
            "question": "1. What football club is currently the best in the world?",
            "options": ["A. Arsenal", "B. Atletico Madrid", "C. Manchester City", "D. Real Madrid"],
            "answer": "D"
        },
        {
            "question": "2. Who is the President of Russia",
            "options": ["A. Vladmir Putin", "B. Hilary Clinton", "C. Jusrin Razarov", "D. Donald Trump"],
            "answer": "A"
        },
        {
            "question": "3. What is 15 + 15?",
            "options": ["A. 225", "B. 25", "C. 50", "D. 30"],
            "answer": "D"
        },
        {
            "question": "4. Which of the options is a hardware?",
            "options": ["A. Mouse", "B. Chrome", "C. Pycharm", "D. Microsoft Word"],
            "answer": "A"
        },
        {
            "question": "5. What is 100/4?",
            "options": ["A. 20", "B. 35", "C. 40", "D. 25"],
            "answer": "D"
        }
    ]

    score = 0

    for q in questions:
        print(q["question"])
        for opt in q["options"]:
            print(opt)
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        if user_answer == q["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! The correct answer was {q['answer']}.\n")

    print(f"Test complete. Your score: {score}/5")