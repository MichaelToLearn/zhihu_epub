# coding:utf-8
r"""
下载知乎答案到epub电子书
"""
from __future__ import print_function, unicode_literals
import os
import time

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import GetDataErrorException
from EpubWriter import EpubWriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#  --- 配置信息 ----
# 每个问题最多下载多少个答案
QUESTION_NUM = 500
# 保存的登录凭证文件名
TOKEN_FILE_NAME = 'token.pkl'

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
    # 登陆过期大的时候，不能获得标题
    title = question.title
    print(u'正在处理《%s》' % title)
    ew = EpubWriter(title, with_catalog=False)
    i = 0
    for answer in question.answers:
        try:
            ew.add_chapter(title, parse_answer_content(answer))
        except:
            continue
        i = i + 1
        print(u"正在处理第%d个回答" % i)
        if i >= QUESTION_NUM:
            break
    print(u"处理完成！正在输出...")
    ew.write()
    print(u"《%s》输出成功!" % title)


def zhihu_login():
    r"""
    知乎登陆
    :return:        登陆之后的客户端client
    """
    client = ZhihuClient()
    # 登录
    if os.path.isfile(TOKEN_FILE_NAME):
        client.load_token(TOKEN_FILE_NAME)
    else:
        client.login_in_terminal()
        client.save_token(TOKEN_FILE_NAME)
    return client


def read_questions():
    r"""
    从list.txt中读取所有需要处理的问题id
    :return:        问题id列表
    """
    text = open('list.txt', 'r').read()
    question_id_strs = text.split('\n')
    return [int(id_str) for id_str in question_id_strs]


def main():
    client = zhihu_login()
    question_ids = read_questions()
    try:
        for question_id in question_ids:
            download_question(client, question_id)
    except GetDataErrorException as e:
        print(str(e))
        if 'ERR_LOGIN_TICKET_EXPIRED' in str(e):
            print(u'登录过期，重新请求登录...')
            # 删除凭证，重新登陆
            os.remove(TOKEN_FILE_NAME)
            main()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()














