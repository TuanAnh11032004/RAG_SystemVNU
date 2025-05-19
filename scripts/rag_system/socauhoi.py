with open("data/test/questions.txt", 'r', encoding='utf-8') as f:
    questions = [line.strip() for line in f if line.strip()]
print(f"Số câu hỏi đọc được: {len(questions)}")
print("Một vài câu hỏi:", questions[:3])
