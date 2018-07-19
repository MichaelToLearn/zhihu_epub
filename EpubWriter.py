# coding:utf-8
r"""
写电子书
"""
from __future__ import unicode_literals

import re

from ebooklib import epub
import uuid
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib


class EpubWriter:

    book = None
    title = None
    chapters = []
    with_catalog = True

    def __init__(self, title, with_catalog=True):
        self.book = epub.EpubBook()
        self.title = title
        self.with_catalog = with_catalog

    def set_info(self):
        r"""
        设置电子书的各种信息
        :return:    无
        """
        self.book.set_identifier(str(uuid.uuid1()))
        self.book.set_title(self.title)
        self.book.set_language('en')
        self.book.add_author('Zhi hu')

    def add_chapter(self, title, content):
        r"""
        添加章节
        :param title:       标题
        :param content:     内容
        :return:
        """
        # 处理图片
        img_urls = re.findall(r'<img\ssrc="(\S+)"', content)
        for img_url in img_urls:
            pic_path = "images/%s.jpg" % str(uuid.uuid1())
            # 下载图片
            content = content.replace(img_url, pic_path)
            img_data = urllib.urlopen(img_url).read()
            image_item = epub.EpubImage()
            image_item.set_content(img_data)
            image_item.file_name = pic_path
            self.book.add_item(image_item)
        chapter = epub.EpubHtml(title=title, file_name='%s.xhtml' % str(uuid.uuid1()), lang='hr')
        chapter.content = content
        self.chapters.append(chapter)
        self.book.add_item(chapter)

    def add_style(self, style):
        r"""
        添加样式
        :param style:       样式
        :return:
        """
        nav_css = epub.EpubItem(uid=str(uuid.uuid1()), file_name="style/%s.css" % str(uuid.uuid1()), media_type="text/css", content=style)
        # add CSS file
        self.book.add_item(nav_css)

    def write(self):
        r"""
        输出电子书
        :return:    无
        """
        if self.with_catalog:
            self.book.toc = self.chapters

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        if self.with_catalog:
            self.book.spine = ["nav"] + self.chapters
        else:
            self.book.spine = self.chapters
        remove_strs = r'\/:*?"<>|'
        write_title = self.title
        for s in list(remove_strs):
            write_title = write_title.replace(s, "#")
        epub.write_epub('./output/%s.epub' % write_title, self.book, {})


if __name__ == "__main__":
    ew = EpubWriter('zhihu')
    ew.add_chapter('name', 'value')
    ew.write()
    # book = epub.EpubBook()
    #
    # # set metadata
    # book.set_identifier('id123456')
    # book.set_title('Sample book')
    # book.set_language('en')
    #
    # book.add_author('Author Authorowski')
    # book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')
    #
    # # create chapter
    # c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
    # c1.content = u'<h1>Intro heading</h1><p>盛迪的第一本电子书</p>'
    #
    # c2 = epub.EpubHtml(title='Intro', file_name='chap_02.xhtml', lang='hr')
    # c2.content = u'<p>经典女神李嘉欣到了中年却瘦的不像富人家的太太，不过前一段时间她终于胖了一下下…</p><p>但人家只是胖着玩的，没几天就瘦回去了，还在电梯里玩起了自拍。</p><figure><img src="https://pic2.zhimg.com/v2-a36cc5d89417a64c1280e911a9c1c2e9_b.jpg" data-caption="" data-size="normal" data-rawwidth="547" data-rawheight="367" class="origin_image zh-lightbox-thumb" width="547" data-original="https://pic2.zhimg.com/v2-a36cc5d89417a64c1280e911a9c1c2e9_r.jpg"></figure><p>以前的电梯照加上现在的都能召唤出神龙了，所以网友们都叫她称“电梯时尚穿搭博主”。</p><figure><img src="https://pic4.zhimg.com/v2-d88fe5c624ef2aa7380d37abbfe1545b_b.jpg" data-caption="" data-size="normal" data-rawwidth="389" data-rawheight="490" class="content_image" width="389"></figure><p>不过所长注意的重点可不是她两条纤细的腿和保养好的脸，而是电梯本梯，只有人家的私人电梯才能肆无忌惮的拍拍拍吧。换成小区公用电梯这么拍拍拍，怕是一开门瞬间就尴尬了。</p><figure><img src="https://pic4.zhimg.com/v2-36cf80fc4647b825324e700cee8b9e47_b.jpg" data-caption="" data-size="normal" data-rawwidth="448" data-rawheight="238" class="origin_image zh-lightbox-thumb" width="448" data-original="https://pic4.zhimg.com/v2-36cf80fc4647b825324e700cee8b9e47_r.jpg"></figure><p>从电梯的细节上看李嘉欣住的是7层独栋别墅，真的豪气冲天！</p><figure><img src="https://pic4.zhimg.com/v2-97d610a4ae01844ff0e99d9816734e97_b.jpg" data-caption="" data-size="normal" data-rawwidth="360" data-rawheight="418" class="content_image" width="360"></figure><p>自从嫁给了许晋亨以后，李嘉欣息影过起了阔太太的生活，而她的阔太生活看似低调，实则豪气冲天，到底有多豪？所长带你们看看。</p><figure><img src="https://pic4.zhimg.com/v2-1c16f7f47cdcef84301fe593f856e807_b.jpg" data-caption="" data-size="normal" data-rawwidth="255" data-rawheight="256" class="content_image" width="255"></figure><p>先从李嘉欣的婚礼说起吧，所长见过最壕的婚礼莫过于黄教主夫妇的了，花2亿举办童话婚礼，引来妹子们一片羡慕。</p><figure><img src="https://pic1.zhimg.com/v2-fb87d08c329f1f57d5ed96e80bb4b068_b.jpg" data-caption="" data-size="normal" data-rawwidth="651" data-rawheight="429" class="origin_image zh-lightbox-thumb" width="651" data-original="https://pic1.zhimg.com/v2-fb87d08c329f1f57d5ed96e80bb4b068_r.jpg"></figure><p>而李嘉欣结婚是在2008年，婚礼开支在1亿港币（9000万人民币）。</p><figure><img src="https://pic3.zhimg.com/v2-787c4a7924438a69c00b1a93a406ec5a_b.jpg" data-caption="" data-size="normal" data-rawwidth="527" data-rawheight="386" class="origin_image zh-lightbox-thumb" width="527" data-original="https://pic3.zhimg.com/v2-787c4a7924438a69c00b1a93a406ec5a_r.jpg"></figure><p>按当时北京一万多的房价算，emmm，人家结婚的钱够买一个9000平的大豪宅，贫穷限制了所长的想象力！</p><figure><img src="https://pic3.zhimg.com/v2-1b27a8080954a3eb8cd7dfe095fb2952_b.jpg" data-caption="" data-size="normal" data-rawwidth="240" data-rawheight="179" class="content_image" width="240"></figure><p>这个婚礼应该算得上是世纪婚礼了，李嘉欣的婚纱和晚礼服一个个都价值不菲，一套普通婚纱30万，另一套定制的意大利婚纱要100万，还有5件加起来价值500万的晚礼服。</p><figure><img src="https://pic2.zhimg.com/v2-98accfc1487ad0fb4d7b08b71adb7d5d_b.jpg" data-caption="" data-size="normal" data-rawwidth="731" data-rawheight="485" class="origin_image zh-lightbox-thumb" width="731" data-original="https://pic2.zhimg.com/v2-98accfc1487ad0fb4d7b08b71adb7d5d_r.jpg"></figure><p>1000万的求婚钻戒，1800万的钻石项链，还有550万的劳斯莱斯花车。</p><figure><img src="https://pic4.zhimg.com/v2-ebb9a3816c1b2ec6648b8bc352313bd7_b.jpg" data-caption="" data-size="normal" data-rawwidth="350" data-rawheight="507" class="content_image" width="350"></figure><p>所长写不下去了，心脏受不了…</p><figure><img src="https://pic4.zhimg.com/v2-22a40f3705831c52d58a6330427d081b_b.jpg" data-caption="" data-size="normal" data-rawwidth="239" data-rawheight="237" class="content_image" width="239"></figure><p>所以网传许晋亨砸了4.3亿才娶到李嘉欣。</p><figure><img src="https://pic2.zhimg.com/v2-a6d5f1ffd83d9135fcef424f6e0f8c59_b.jpg" data-caption="" data-size="normal" data-rawwidth="593" data-rawheight="400" class="origin_image zh-lightbox-thumb" width="593" data-original="https://pic2.zhimg.com/v2-a6d5f1ffd83d9135fcef424f6e0f8c59_r.jpg"></figure><p>婚后的李嘉欣更是幸福豪门阔太的典范，她住着有香港第一豪宅之称的许家别墅，估值7亿，总面积87150平方尺，老公和儿子能在家里的草坪上放风筝踢球。</p><figure><img src="https://pic1.zhimg.com/v2-55232d7346ea9816eca60757bfd17c30_b.jpg" data-caption="" data-size="normal" data-rawwidth="466" data-rawheight="586" class="origin_image zh-lightbox-thumb" width="466" data-original="https://pic1.zhimg.com/v2-55232d7346ea9816eca60757bfd17c30_r.jpg"></figure><p>而且一个豪宅就占了一个山头儿，每天巡山都需要花几个小时吧？所长替她累。</p><figure><img src="https://pic3.zhimg.com/v2-5749d48191b6425455c6495483c29992_b.jpg" data-caption="" data-size="normal" data-rawwidth="445" data-rawheight="372" class="origin_image zh-lightbox-thumb" width="445" data-original="https://pic3.zhimg.com/v2-5749d48191b6425455c6495483c29992_r.jpg"></figure><p>豪宅大到一些旅游的人以为这是公园景点…</p><figure><img src="https://pic2.zhimg.com/v2-41b666a70ed789741981d8eae7fceff9_b.jpg" data-caption="" data-size="normal" data-rawwidth="265" data-rawheight="244" class="content_image" width="265"></figure><p>李嘉欣结婚时，許世勛也就是许晋亨的爸爸送她2亿豪宅，生孩子直接被奖励1亿现金，相比于林青霞嫁的豪门，李嘉欣这种简直壕无人性！</p><figure><img src="https://pic1.zhimg.com/v2-94a0b15cab00d9cbf7ee6dd14922f8fc_b.jpg" data-caption="" data-size="normal" data-rawwidth="593" data-rawheight="418" class="origin_image zh-lightbox-thumb" width="593" data-original="https://pic1.zhimg.com/v2-94a0b15cab00d9cbf7ee6dd14922f8fc_r.jpg"></figure><p>和李嘉欣一样非常成功嫁入豪门，从模特翻身到阔太的就是<b>徐子淇</b>了，老公李家诚在她15岁时就对她一见钟情，等到她22岁才结婚，这简直就是一部现实的“豪门媳妇养成”小说啊。</p><figure><img src="https://pic1.zhimg.com/v2-46c572a7a543281857ec665033def504_b.jpg" data-caption="" data-size="normal" data-rawwidth="303" data-rawheight="331" class="content_image" width="303"></figure><p>本着对徐子淇的喜欢，她们的婚礼更壕出天际，光婚礼就花了7亿。</p><figure><img src="https://pic1.zhimg.com/v2-86f9fdce81b4eb32f36d45239b5edd30_b.jpg" data-caption="" data-size="normal" data-rawwidth="450" data-rawheight="250" class="origin_image zh-lightbox-thumb" width="450" data-original="https://pic1.zhimg.com/v2-86f9fdce81b4eb32f36d45239b5edd30_r.jpg"></figure><p>结婚礼物更是价值3.74亿的私人飞机，再想想所长自己，也就键盘是私人，哦不，私人键盘都没有…</p><figure><img src="https://pic3.zhimg.com/v2-1917ce8f7e86e10fa1742bc3a750a41a_b.jpg" data-caption="" data-size="normal" data-rawwidth="700" data-rawheight="700" class="origin_image zh-lightbox-thumb" width="700" data-original="https://pic3.zhimg.com/v2-1917ce8f7e86e10fa1742bc3a750a41a_r.jpg"></figure><p>徐子淇嫁入豪门后8年连生4个娃，每生一胎都能获得相应的奖励。</p><figure><img src="https://pic1.zhimg.com/v2-9a3852c2beffb8ac874b1a6dcfc757d4_b.jpg" data-caption="" data-size="normal" data-rawwidth="546" data-rawheight="322" class="origin_image zh-lightbox-thumb" width="546" data-original="https://pic1.zhimg.com/v2-9a3852c2beffb8ac874b1a6dcfc757d4_r.jpg"></figure><p><b>来你们感受一下：</b></p><blockquote>2007年第一胎女儿奖励500万法拉利，公公送400多平豪宅。<br>2008年8月怀二胎，并生二女儿，送400平豪宅，还有百万钻石以及保养品。<br>第三胎儿子，网传有10亿奖金，她老公送了1.35亿游艇半亿的钻戒。爷爷为孙子成立了逾亿的成长基金。<br>第四胎儿子，据说李家诚在洛杉矶购置亿元豪宅送她。</blockquote><p>虽然网上都说徐子淇成为了豪门生育的机器，但要说生一个给一个亿，老公还那么宠，所长这老爷们都想去给他生娃了！</p><figure><img src="https://pic1.zhimg.com/v2-911607fdc0eeefe12b40de6a64f9de48_b.jpg" data-caption="" data-size="normal" data-rawwidth="133" data-rawheight="153" class="content_image" width="133"></figure><p>而且徐子淇在采访时更说，豪门并不深似海，她形容自己的豪门生活很普通，除了家里的姥爷出名，房子舒服外，没有其他不同，而且没有任何豪门规矩。</p><figure><img src="https://pic1.zhimg.com/v2-af9a6a13d71e8c1cc0b2702d1c73f374_b.jpg" data-caption="" data-size="normal" data-rawwidth="595" data-rawheight="412" class="origin_image zh-lightbox-thumb" width="595" data-original="https://pic1.zhimg.com/v2-af9a6a13d71e8c1cc0b2702d1c73f374_r.jpg"></figure><p>所以李嘉欣、徐子淇成功嫁入豪门后，仿佛成了女星和模特界的典范，所以那几年后很多人都挤破了头的想做豪门阔太，然而才知道可能就李家诚家的豪门海不深，其他家都深不可测！</p><figure><img src="https://pic4.zhimg.com/v2-d809b7d3a136cbfb19b37b32d7a550f3_b.jpg" data-caption="" data-size="normal" data-rawwidth="249" data-rawheight="247" class="content_image" width="249"></figure><p>这些自以为嫁了豪门就能飞山枝头变凤凰的女星，<b>实则不是成了笼中雀就是连豪门枝都碰不到的~</b></p><p><b>吴佩慈</b>算是一心想嫁入豪门的代表女星了，为纪晓波5年生3个孩子，比徐子淇还拼。</p><figure><img src="https://pic3.zhimg.com/v2-dd719fc50c0f6ec6228eee7555a28cd2_b.jpg" data-caption="" data-size="normal" data-rawwidth="385" data-rawheight="550" class="content_image" width="385"></figure><p>但又有什么用呢？还不是两只脚在豪门的边缘试探…</p><figure><img src="https://pic4.zhimg.com/v2-963c7682909461adfd897feabb9d95a7_b.jpg" data-caption="" data-size="normal" data-rawwidth="210" data-rawheight="197" class="content_image" width="210"></figure><p>吴佩慈想要绑住富豪除了生孩子好像没有别的方式了，所以她就一个一个不停的生，但当生第一个女孩时，据说吴佩慈自己出院的，纪晓波没有露面。</p><figure><img src="https://pic2.zhimg.com/v2-9ca8b47f7614dca7e7a8e738d193d3e9_b.jpg" data-caption="" data-size="normal" data-rawwidth="531" data-rawheight="455" class="origin_image zh-lightbox-thumb" width="531" data-original="https://pic2.zhimg.com/v2-9ca8b47f7614dca7e7a8e738d193d3e9_r.jpg"></figure><p>对比老公来接还细心照料的郭晶晶，心疼吴佩慈1分钟。</p><figure><img src="https://pic3.zhimg.com/v2-97bb810805ac3d8ecc5d2f47c01d20e6_b.jpg" data-caption="" data-size="normal" data-rawwidth="568" data-rawheight="401" class="origin_image zh-lightbox-thumb" width="568" data-original="https://pic3.zhimg.com/v2-97bb810805ac3d8ecc5d2f47c01d20e6_r.jpg"></figure><p>网传第一胎因为是女儿所以纪晓波对她比较冷淡，所以2015年吴佩慈的肚皮很争气，顺利剖腹产一个儿子，终于有了和老公与孩子的幸福合影。</p><figure><img src="https://pic4.zhimg.com/v2-16c494a4391033c203ad82260399547b_b.jpg" data-caption="" data-size="normal" data-rawwidth="504" data-rawheight="422" class="origin_image zh-lightbox-thumb" width="504" data-original="https://pic4.zhimg.com/v2-16c494a4391033c203ad82260399547b_r.jpg"></figure><p>媒体都猜测：吴佩慈嫁入豪门的机会大增~</p><figure><img src="https://pic1.zhimg.com/v2-9fce181cfca34ca95bba1d6f10abce34_b.jpg" data-caption="" data-size="normal" data-rawwidth="609" data-rawheight="127" class="origin_image zh-lightbox-thumb" width="609" data-original="https://pic1.zhimg.com/v2-9fce181cfca34ca95bba1d6f10abce34_r.jpg"></figure><p>然而外界的猜测和祝福并没有实现，纪晓波就在香港中环被贴海报讨债，吴佩慈离豪宅仿佛又远了一步。</p><figure><img src="https://pic3.zhimg.com/v2-16cdf7298130538c8b5afa1d9ac1359a_b.jpg" data-caption="" data-size="normal" data-rawwidth="378" data-rawheight="428" class="content_image" width="378"></figure><p>生完二胎后的吴佩慈没有顺利嫁入豪门，就开始生了第三胎，相比于之前每个月10万块的生活费和常年只能住四季酒店，这次她终于得到了更多的经济补偿，钻戒豪宅都有了，身价上升到51亿。</p><figure><img src="https://pic3.zhimg.com/v2-c4354cffb28fef647795c56c6cb82972_b.jpg" data-caption="" data-size="normal" data-rawwidth="673" data-rawheight="104" class="origin_image zh-lightbox-thumb" width="673" data-original="https://pic3.zhimg.com/v2-c4354cffb28fef647795c56c6cb82972_r.jpg"></figure><p>但就差老公了，老公却说：孩子可以生，但结婚不可能的~</p><figure><img src="https://pic1.zhimg.com/v2-b84423ce98b9c26c2759296cff741068_b.jpg" data-caption="" data-size="normal" data-rawwidth="769" data-rawheight="191" class="origin_image zh-lightbox-thumb" width="769" data-original="https://pic1.zhimg.com/v2-b84423ce98b9c26c2759296cff741068_r.jpg"></figure><figure><img src="https://pic4.zhimg.com/v2-fe0100513b75f8a4b1d0479188f0c92b_b.jpg" data-caption="" data-size="normal" data-rawwidth="196" data-rawheight="198" class="content_image" width="196"></figure><p>吴佩慈拼命生孩子就是为了巩固地位，但没想到老公就是花心大少，经常拈花惹草，之前还和颖儿亲密合影。据知情人士说跑男在塞班岛拍摄时还和纪晓波同桌吃饭，最后只剩下baby和纪晓波在一个房间里，emmmmmm…</p><figure><img src="https://pic2.zhimg.com/v2-846f7f59d68ef9c9ce2d510010bc5c65_b.jpg" data-caption="" data-size="normal" data-rawwidth="300" data-rawheight="304" class="content_image" width="300"></figure><p>吴佩慈为了嫁入豪门才是真正的成了生娃机器吧，她还说要养好肚皮备战第4胎，可没有领证，她就准备没有名分的生下去吗？可怜又可怕。</p><figure><img src="https://pic4.zhimg.com/v2-8c161d3ca070694252ef72a013d15da7_b.jpg" data-caption="" data-size="normal" data-rawwidth="581" data-rawheight="586" class="origin_image zh-lightbox-thumb" width="581" data-original="https://pic4.zhimg.com/v2-8c161d3ca070694252ef72a013d15da7_r.jpg"></figure><p>在大家眼里已经成功进入豪门却过的不太好的就是晴格格<b>王艳</b>了，虽然老公是著名地产大亨，家住毗邻紫禁城，生活看似奢华幸福。</p><figure><img src="https://pic2.zhimg.com/v2-0e58468c0f7c49e98a23ea5d7cbeb7f5_b.jpg" data-caption="" data-size="normal" data-rawwidth="494" data-rawheight="274" class="origin_image zh-lightbox-thumb" width="494" data-original="https://pic2.zhimg.com/v2-0e58468c0f7c49e98a23ea5d7cbeb7f5_r.jpg"></figure><p>但她婆婆是皇族后裔，因为年纪大就延续着老佛爷般的生活，据说他们的关系像还珠格格里晴格格对老佛爷一样，王艳对她毕恭毕敬，呵护伺候备至。</p><figure><img src="https://pic1.zhimg.com/v2-c3ab67180de3ea8c95857635dc9e544c_b.jpg" data-caption="" data-size="normal" data-rawwidth="736" data-rawheight="474" class="origin_image zh-lightbox-thumb" width="736" data-original="https://pic1.zhimg.com/v2-c3ab67180de3ea8c95857635dc9e544c_r.jpg"></figure><p>所以我们看到电视剧里晴格格对老佛爷照顾的细节，也都和王艳家差不多。江湖传言说王艳会跪下给婆婆洗脚，让婆婆享受老佛爷般的待遇，家里虽然有保姆还要自己刷马桶。</p><figure><img src="https://pic3.zhimg.com/v2-9e82c154b5422d97887d6a9526117aca_b.jpg" data-caption="" data-size="normal" data-rawwidth="762" data-rawheight="532" class="origin_image zh-lightbox-thumb" width="762" data-original="https://pic3.zhimg.com/v2-9e82c154b5422d97887d6a9526117aca_r.jpg"></figure><figure><img src="https://pic3.zhimg.com/v2-91ae1345148539c567f7904b6c85f002_b.jpg" data-caption="" data-size="normal" data-rawwidth="788" data-rawheight="459" class="origin_image zh-lightbox-thumb" width="788" data-original="https://pic3.zhimg.com/v2-91ae1345148539c567f7904b6c85f002_r.jpg"></figure><p>而老公对王艳也不是特别满意，可能因为王艳本身就没啥太大理想，她老公动用自己的一切关系帮她牵线，她都不太愿意演戏，只想着相夫教子，网传她老公能和她在一起，就因为她婆婆比较喜欢她。</p><figure><img src="https://pic1.zhimg.com/v2-da0e78f0db89df388cc9989fa7b96060_b.jpg" data-caption="" data-size="normal" data-rawwidth="575" data-rawheight="390" class="origin_image zh-lightbox-thumb" width="575" data-original="https://pic1.zhimg.com/v2-da0e78f0db89df388cc9989fa7b96060_r.jpg"></figure><figure><img src="https://pic1.zhimg.com/v2-20aa296744151eb60eca0ba8e172611c_b.jpg" data-caption="" data-size="normal" data-rawwidth="577" data-rawheight="49" class="origin_image zh-lightbox-thumb" width="577" data-original="https://pic1.zhimg.com/v2-20aa296744151eb60eca0ba8e172611c_r.jpg"></figure><p>从各个细节可以看出来，在她家里婆婆是老佛爷，老公是皇帝，而儿子自己也说了<b>自己就是小皇帝，</b>还骂过王艳是猪，她在家里顶多算是丫鬟？</p><figure><img src="https://pic2.zhimg.com/v2-25543334a5636e9b4ec4f90c2bb83a35_b.jpg" data-caption="" data-size="normal" data-rawwidth="1080" data-rawheight="517" class="origin_image zh-lightbox-thumb" width="1080" data-original="https://pic2.zhimg.com/v2-25543334a5636e9b4ec4f90c2bb83a35_r.jpg"></figure><figure><img src="https://pic3.zhimg.com/v2-cab02876d443fa5b3472d9d981646f52_b.jpg" data-caption="" data-size="normal" data-rawwidth="1080" data-rawheight="79" class="origin_image zh-lightbox-thumb" width="1080" data-original="https://pic3.zhimg.com/v2-cab02876d443fa5b3472d9d981646f52_r.jpg"></figure><p>但在采访里王艳也说婆婆其实对她不错，自己不会做饭也从不逼迫，富豪生活是她的，冷暖自知。</p><figure><img src="https://pic2.zhimg.com/v2-e96a5c59da3dc2f30e1a64b9a7e59b7d_b.jpg" data-caption="" data-size="normal" data-rawwidth="738" data-rawheight="533" class="origin_image zh-lightbox-thumb" width="738" data-original="https://pic2.zhimg.com/v2-e96a5c59da3dc2f30e1a64b9a7e59b7d_r.jpg"></figure><p>如果说王艳过的不好都是网传，那<b>贾静雯</b>之前离婚案就是给想嫁入豪门的妹子当头一棒了。</p><figure><img src="https://pic2.zhimg.com/v2-543a0562f2dd20a1a9a890f7696da80d_b.jpg" data-caption="" data-size="normal" data-rawwidth="343" data-rawheight="433" class="content_image" width="343"></figure><p>她意外怀孕进豪门还要验DNA，产前老公偷腥气的她早产，还传被家暴，最后离婚也闹的满城皆知，孩子想看都看不到，和卸磨杀驴没啥区别。</p><figure><img src="https://pic4.zhimg.com/v2-fab7dded6c2fae78a0289d05cdbbc74b_b.jpg" data-caption="" data-size="normal" data-rawwidth="564" data-rawheight="337" class="origin_image zh-lightbox-thumb" width="564" data-original="https://pic4.zhimg.com/v2-fab7dded6c2fae78a0289d05cdbbc74b_r.jpg"></figure><p>而刘涛和曾是京城四少之一的王珂相识20天就闪婚，2008年刚结完婚，王珂的事业就赶上了全球金融危机导致破产，所长不知道该说是刘涛当时被爱情冲昏头脑还是王珂时运不好，还是这俩人命里相克了。</p><figure><img src="https://pic1.zhimg.com/v2-5f471465727a373e278f92c51837f578_b.jpg" data-caption="" data-size="normal" data-rawwidth="577" data-rawheight="415" class="origin_image zh-lightbox-thumb" width="577" data-original="https://pic1.zhimg.com/v2-5f471465727a373e278f92c51837f578_r.jpg"></figure><figure><img src="https://pic2.zhimg.com/v2-c8584f3d0ae67de6f82944e6650d4e8d_b.jpg" data-caption="" data-size="normal" data-rawwidth="584" data-rawheight="49" class="origin_image zh-lightbox-thumb" width="584" data-original="https://pic2.zhimg.com/v2-c8584f3d0ae67de6f82944e6650d4e8d_r.jpg"></figure><p>刘涛豪门的炕头还没有坐热，就要复出拍戏赚钱为老公还4亿债务，所以想进豪门时一定要看清家底再嫁啊。</p><figure><img src="https://pic2.zhimg.com/v2-b747230bbf351f63457b4f8b9cde9be1_b.jpg" data-caption="" data-size="normal" data-rawwidth="613" data-rawheight="392" class="origin_image zh-lightbox-thumb" width="613" data-original="https://pic2.zhimg.com/v2-b747230bbf351f63457b4f8b9cde9be1_r.jpg"></figure><p>都知道豪门大院内过着富丽堂皇的生活，所以富豪们也把娱乐圈看做选秀场，而女星们更抓破头的想钓到豪门，但谁能想到豪门里有像许晋亨、李家诚这样的好男人，也有像孙志浩这样的渣男，还有像王珂这样前一秒富豪后一秒土贫的，所以不管你想不想嫁豪门，一定要看对人~！</p><p>那些嫁错豪门深似海的，幸福感可能还不如我们~</p><p><b>给所长点赞的都能嫁对人</b></p><p></p>'
    #
    #
    # # add chapter
    # book.add_item(c1)
    # book.add_item(c2)
    #
    # # define Table Of Contents
    # book.toc = (c1, c2)
    #
    # # add default NCX and Nav file
    # book.add_item(epub.EpubNcx())
    # book.add_item(epub.EpubNav())
    #
    # # define CSS style
    # style = 'BODY {color: white;}'
    # nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    #
    # # add CSS file
    # book.add_item(nav_css)
    #
    # # basic spine
    # book.spine = ['nav', c1, c2]
    #
    # # write to the file
    # epub.write_epub('test.epub', book, {})