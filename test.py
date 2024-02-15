#!/usr/bin/env python3

#########################
## Developed By jjeong ##
#########################

import random,os,platform,shutil

def clear_terminal():
    system_platform = platform.system()
    if system_platform == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def get_color_form(num, text):
    return '\033[' + str(num) + 'm' + text + '\033[0m'

def get_red_text(text):
    return get_color_form(91, text)

def get_green_text(text):
    return get_color_form(92, text)

def read_and_parse_file():
    questions = []
    answers = []
    remove_tags = ['<summary>','<p>','<li>','<b>','</b>']
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
                    get_red_text('>>> ') + question)
                answers.append(get_green_text('>>> ') + answer.strip())

    if len(questions) != len(answers):
        print('읽어온 질문과 답변이 1:1 매핑 되지않았습니다.')
        exit()
    return (questions, answers)



def main():
    list1,list2 = read_and_parse_file()
    size = len(list1)
    visited = set()
    trace = []

    def get_index_str(quest_num):
        return str(trace.index(quest_num) + 1)

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
            clear_terminal()
            terminal_size = shutil.get_terminal_size().columns
            print(('=' * terminal_size) + '\n')
            print(get_red_text('질문 ' + get_index_str(trace[-1 + index_pointer])) + ":\n", list1[trace[-1 + index_pointer]])
            input("\n엔터 키를 누르면 예상 답변이 출력됩니다.")
            print("\n" + ('-' * terminal_size) + "\n" + get_green_text("예상 답변")\
                + ":\n\n", list2[trace[-1 + index_pointer]])
            choice = str(input("\n\
                Enter를 누르면 랜덤 문제, '" + get_green_text("1") \
                + "'입력하면 이전, '" + get_green_text("2") + "'입력하면 앞으로" + get_red_text(" : ") + "\n\
                " + get_red_text("q") +"입력하면 종료"+ get_red_text(" : ")))
            if choice == '1':
                index_pointer -= 1
            elif choice == '2':
                index_pointer += 1
            elif choice == 'q':
                exit()
            else:
                break
            index_pointer %= curr_trace_size


if __name__ == "__main__":
    main()
