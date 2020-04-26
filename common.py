import re


def split_chapter(chapter):
    return re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', chapter.replace('\n', ' ').replace('  ', ' ').strip())

# 
def read_file(filename):
    with open(filename, encoding='utf-8', mode='r', errors='ignore') as file:
        return file.read().strip()


def get_one_chapter_strang(chapter_number, book, subsections=False):
    s_chapter_number = str(chapter_number)
    chapter_starts = re.search('Chapter\s' + s_chapter_number + '\s\n.*\s\n' + s_chapter_number + '\.1.*\n', book)
    chapter_ends = re.search('Chapter\s' + str(chapter_number + 1) + '\s\n.*\s\n' + str(chapter_number + 1) + '\.1',
                             book[chapter_starts.start():])
    chapter = book[chapter_starts.start():chapter_starts.start() + chapter_ends.start()]

    subs_start = re.search(s_chapter_number + '\.[0-9]+.+', chapter)
    i = 1
    to_return = ''
    while True:
        subs_end = re.search('\nProblem\sSet\s' + s_chapter_number + '\.' + str(i) + '+\s', chapter)
        if not subs_end:
            subs_end = re.search(s_chapter_number + '\.' + str(i + 1) +
                                 '\s[A-Z]+[^0-9\.\n?]+[0-9]{0,1}[^0-9\.\n?]+[0-9]{0,1}[^0-9\.\n?]+\s*(?![0-9]+)\n',
                                 chapter)
        subs_name = chapter[subs_start.start():subs_start.end() - 1]  # exclude \n
        subs = chapter[subs_start.end():subs_end.start()]
        if subsections:
            yield subs_name[subs_name.find(' ') + 1:], split_chapter(subs)
        else:
            to_return += subs + ' '
        chapter = chapter[subs_end.start():]
        subs_start = re.search(s_chapter_number + '\.' + str(i + 1) +
                               '\s[A-Z]+[^0-9\.\n?]+[0-9]{0,1}[^0-9\.\n?]+[0-9]{0,1}[^0-9\.\n?]+\s*(?![0-9]+)\n',
                               chapter)
        if not subs_start:
            break
        i += 1
    if not subsections:
        yield split_chapter(to_return)


def get_one_chapter(chapter_number, book):
    s_chapter_number = str(chapter_number)
    chapter_starts = re.search('Chapter\s' + s_chapter_number + '\s\n.*\s\n' + s_chapter_number + '\.1.*\n', book)
    chapter_ends = re.search('Chapter\s' + str(chapter_number + 1) + '\s\n.*\s\n' + str(chapter_number + 1) + '\.1',
                             book[chapter_starts.start():])
    chapter = book[chapter_starts.end():chapter_starts.start() + chapter_ends.start()]
    problem_set_start = re.search('Problem\sSet\s' + s_chapter_number + '\.[0-9]+\s', chapter)

    while problem_set_start:
        if chapter.count('Problem\sSet\s') == 1:  # very clever ifka, only sverhrazums top 5 understand
            chapter = chapter[:problem_set_start.start()]
            break
        problem_set_end = re.search(s_chapter_number + '\.[0-9]+\s.*\n', chapter[problem_set_start.end():])
        chapter = chapter[:problem_set_start.start()] + chapter[problem_set_start.end() + problem_set_end.start():]
        problem_set_start = re.search('Problem\sSet\s' + s_chapter_number + '\.[0-9]+\s', chapter)

    return re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', chapter.replace('\n', ' ').replace('  ', ' ').strip())
