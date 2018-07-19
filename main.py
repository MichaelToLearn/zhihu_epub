# coding:utf-8
r"""
下载知乎答案到epub电子书
"""
from __future__ import print_function, unicode_literals
import os
import time

from zhihu_oauth import ZhihuClient
from EpubWriter import EpubWriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def parse_answer_content(answer):
    r"""
    生成可以直接写入电子书的内容。
    :param answer:  当前答案的对象
    :return:        字符串内容
    """
    part_one_template = """<h1>{{title}}</h1>
<p><b>{{username}}</b>  |  赞同：<b>{{up_num}}</b>  |   评论：<b>{{comment_num}}</b>  |  {{time}}</p>
<hr>{{content}}"""
    part_one = part_one_template.replace("{{title}}", answer.question.title)
    part_one = part_one.replace("{{username}}", answer.author.name)
    part_one = part_one.replace("{{up_num}}", str(answer.voteup_count))
    part_one = part_one.replace("{{comment_num}}", str(answer.comment_count))
    part_one = part_one.replace("{{time}}", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(answer.updated_time)))
    part_one = part_one.replace("{{content}}", answer.content)
    part_two = ""
    part_two_template = """<p><b>评论区</b></p><ul>{{comments}}</ul>"""
    if answer.comment_count > 0:
        i = 0
        comment_str = ''
        for comment in answer.comments:
            if i >= answer.comment_count:
                break
            if i >= 10:
                break
            comment_str = comment_str + "<li><b>%s</b>：%s</li>" % (comment.author.name, comment.content)
            i = i + 1
        part_two = part_two_template.replace("{{comments}}", comment_str)
    return part_one + part_two


def download_question(zhihu_client, current_question_id):
    r"""
    下载
    :param zhihu_client:              已经登陆的客户端
    :param current_question_id:         问题的id
    :return:                    无
    """
    # 电子书
    question = zhihu_client.question(current_question_id)
    title = question.title
    print(u'正在处理《%s》' % title)
    ew = EpubWriter(title, with_catalog=False)
    i = 0
    for answer in question.answers:
        ew.add_chapter(title, parse_answer_content(answer))
        i = i + 1
        print(u"正在处理第%d个回答" % i)
        if i >= 1000:
            break
    print(u"处理完成！正在输出...")
    ew.write()
    print(u"《%s》输出成功!" % title)


def zhihu_login():
    r"""
    知乎登陆
    :return:        登陆之后的客户端client
    """
    token_file = 'token.pkl'
    client = ZhihuClient()
    # 登录
    if os.path.isfile(token_file):
        client.load_token(token_file)
    else:
        client.login_in_terminal()
        client.save_token(token_file)
    return client


def read_questions():
    r"""
    从list.txt中读取所有需要处理的问题id
    :return:        问题id列表
    """
    text = open('list.txt', 'r').read()
    question_id_strs = text.split('\n')
    return [int(id_str) for id_str in question_id_strs]


if __name__ == '__main__':
    client = zhihu_login()
    question_ids = read_questions()
    for question_id in question_ids:
        download_question(client, question_id)















