#########################
## Developed By jjeong ##
#########################

def read_and_parse_file():
    questions = []
    answers = []
    remove_tags = ['<summary>','<p>','<li>']
    return_tags = ['</p>','<ul>','</ul>','</li>', '</br>']

    def get_removed_text(text):
        for target in remove_tags:
            text = text.replace(target, '')
        return text

    def get_returned_text(text):
        for target in return_tags:
            text = text.replace(target, '\n')
        return text

    with open('./qna.txt', 'r', encoding='utf-8') as file:
        # print(file.read())
        parts = file.read().split('###')
        for qna_data in parts:
            qna_list = qna_data.split('<details>')
            title = qna_list[0].strip()
            for tags in qna_list[1:]:
                tag_list = tags.split('</summary>')
                question = tag_list[0].split('<summary>')[-1]
                answer = get_removed_text(tag_list[1].split('</details>')[0])
                answer = get_returned_text(answer)
                questions.append(title + '\n\n' + \
                    '\033[91m>>> \033[0m' + question)
                answers.append('\033[92m>>> \033[0m' + answer.strip())

    if len(questions) != len(answers):
        print('읽어온 질문과 답변이 1:1 매핑 되지않았습니다.')
        exit()
    return (questions, answers)

import random

def main():
    list1,list2 = read_and_parse_file()
    size = len(list1)
    visited = set()
    trace = []

    while True:
        current_index = random.randint(0, size - 1)
        if current_index in visited:
            continue
        trace.append(current_index)
        visited.add(current_index)
        curr_trace_size = len(trace)
        if curr_trace_size == size:
            for old_trace_index in trace[:(curr_trace_size // 2)]:
                visited.remove(old_trace_index)
            trace = trace[(curr_trace_size // 2):]
        index_pointer = 0
        while True:
            print("\n" + ('=' * 70))
            print("\033[91m질문\033[0m:\n", list1[trace[-1 + index_pointer]])
            input("\n엔터 키를 누르면 예상 답변이 출력됩니다.")
            print("\n" + ('-' * 70) + "\n\033[92m예상 답변\033[0m:\n\n", list2[trace[-1 + index_pointer]])
            choice = str(input("\n\
                엔터 키를 누르면 랜덤 문제, '1'입력하면 이전, '2' 최근으로 이동: "))
            if choice == '1':
                index_pointer -= 1
            elif choice == '2':
                index_pointer += 1
            else:
                break
            index_pointer %= curr_trace_size
                

if __name__ == "__main__":
    main()