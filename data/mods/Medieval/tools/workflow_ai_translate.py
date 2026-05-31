# -*- coding: utf-8 -*-
import os
import re

# =========================================================================
# AI DYNAMIC TRANSLATION ENGINE & PO POPULATOR WORKFLOW
# One-time pipeline execution to write full localized values to zh_CN.po.
# For testing purposes, all item names are prepended with "中世纪".
# =========================================================================

AI_FULL_LOCALIZATION = {
    # ------------------ 场景与基础角色属性 ------------------
    "Naked Wanderer": "赤裸流浪者",
    "You have nothing.  No skills, no tools, no weapons — not even the faintest memory of how you got here.  In this harsh medieval wilderness, your bare hands and wits are all you possess.": 
        "您一无所有。没有技能，没有工具，没有武器——甚至记不起自己是如何来到这里的。在这片荒凉残酷的中世纪荒野中，双手和智慧是您仅有的依靠。",
    "Medieval Awakening": "中世纪苏醒",
    "You awaken in an unfamiliar wilderness, with nothing but the clothes on your back.  The world around you is unfamiliar — medieval, untamed, and full of danger.  Every tool, every scrap of food, every weapon must be found or made by your own hands.": 
        "您在一片未知的荒野中醒来，身上只有破旧的衣物。周围的世界陌生野蛮，充满危机。在这片中世纪荒原上，每一件工具、每一口食物、每一把武器，都必须用您自己的双手去寻找或制作。",
    "Wilderness": "荒野",
    "Middle of Nowhere": "无人区",
    "Field": "旷野",
    "River": "河岸",
    "Medieval": "中世纪",
    "abandoned farmstead": "废弃农庄",
    "manor house": "庄园主屋",
    "mill": "磨坊",
    "parish church": "教区教堂",
    "village crossroad": "村庄十字路口",
    "village smithy": "村庄铁匠铺",
    "mundane_survival": "世俗生存",
    "<statue_plaque>": "<雕像底座牌匾>",
    
    # ------------------ 现代 Hobbies (Options) 汉化（保持中文，便于整体体验） ------------------
    "amateur_electronics": "业余电子学",
    "baseball": "棒球",
    "baseball_beginner": "棒球新手",
    "baseball_expert": "棒球大师",
    "baseball_pitcher": "棒球投手",
    "basketball": "篮球",
    "basketball_beginner": "篮球新手",
    "basketball_expert": "篮球大师",
    "boating_license": "游艇驾照",
    "car_fan": "车迷",
    "car_rebuilding": "改装车",
    "computer_literate": "计算机精通",
    "cyclist_beginner": "骑行新手",
    "cyclist_expert": "骑行大师",
    "cyclist_intermediate": "骑行爱好者",
    "diy_crafts": "手工艺制作",
    "diy_crafts_expert": "手工大师",
    "driving_license": "驾照",
    "football": "橄榄球",
    "football_beginner": "橄榄球新手",
    "football_expert": "橄榄球大师",
    "golfing": "高尔夫球",
    "gunsmithing": "枪械修造",
    "ham_radio_operator": "业余无线电操作员",
    "handloading": "子弹复装",
    "high_school_graduate": "高中毕业生",
    "hobby_heli_pilot": "直升机驾驶兴趣",
    "hockey": "冰球",
    "home_improvement": "房屋装潢",
    "paintball": "彩弹",
    "plinking": "休闲打靶",
    "racing": "赛车竞速",
    "rifle": "步枪",
    "roller_derby": "轮滑竞技",
    "shooter": "射手",
    "shooter_beginner": "射击新手",
    "skating": "滑冰",
    "skeet_shooting": "双向飞碟射击",
    "throw": "投掷",
    "trap_shooting": "单向飞碟射击",
    "vid_games": "电子游戏兴趣",
    
    # ------------------ 基础材质定义 ------------------
    "Cuir Bouilli": "煮沸硬革",
    "Linen": "亚麻布",
    "Oilcloth": "防雨油布",
    "Quilted Linen": "绗缝亚麻/棉衬",
    "Straw": "稻草麦秆",
    "Test Localization Material": "测试本地化材质",
    "abstract_brigandine_base": "布里根丁抽象基类",
    "abstract_coat_of_plates_base": "板甲衣抽象基类",
    "Abstract base class for brigandines.": "布里根丁甲的抽象基类。",
    "Abstract base class for coats of plates.": "板甲衣的抽象基类。",

    # ------------------ 物品名称汉化（统一强制以“中世纪”开头） ------------------
    "med_ Chalcis brigandine": "中世纪查尔基斯布里根丁板甲衣",
    "med_ Visby coat of plates": "中世纪维斯比板甲衣",
    "med_ ankle boots": "中世纪短皮靴",
    "med_ arbalest": "中世纪绞盘重钢弩",
    "med_ archer's brigandine": "中世纪散兵/弓手布里根丁甲",
    "med_ arming sword": "中世纪单手武装佩剑",
    "med_ bascinet": "中世纪轻型颊盔/轻盔",
    "med_ bascinet with hounskull visor": "中世纪“猪脸”面罩颊盔/轻盔",
    "med_ baselard": "中世纪贝斯拉德短剑",
    "med_ battle axe": "中世纪战斧",
    "med_ bearded axe": "中世纪胡须战斧",
    "med_ bec de corbin": "中世纪鸦喙长柄锤",
    "med_ bill": "中世纪步兵长柄勾镰",
    "med_ blacksmith hammer": "中世纪铁匠锻锤",
    "med_ bollock dagger": "中世纪肾形匕首/睾丸匕首",
    "med_ brigandine arms": "中世纪布里根丁板甲护臂",
    "med_ brigandine legs": "中世纪布里根丁板甲护腿",
    "med_ chaperon": "中世纪沙佩隆罩帽",
    "med_ club": "中世纪木棒",
    "med_ commoner's brigandine": "中世纪平民布里根丁板甲衣",
    "med_ composite bow": "中世纪反曲复合弓",
    "med_ corrazina": "中世纪科拉齐纳板甲衣",
    "med_ couter": "中世纪板甲护肘",
    "med_ cuir bouilli": "中世纪煮沸皮甲片",
    "med_ cuir-bouilli coat of plates": "中世纪煮沸硬革板甲衣",
    "med_ cuirass": "中世纪钢制胸甲",
    "med_ cuisse": "中世纪板甲大腿甲",
    "med_ dane axe": "中世纪丹麦长柄大斧",
    "med_ doublet": "中世纪紧身短袄",
    "med_ eating knife": "中世纪便携餐刀",
    "med_ estoc": "中世纪穿甲剑",
    "med_ falchion": "中世纪法尔基翁弯刀",
    "med_ fauchard": "中世纪长柄大镰刀/弗沙德镰",
    "med_ felt cap": "中世纪毛毡帽",
    "med_ flail": "中世纪战斗连枷",
    "med_ flanged mace": "中世纪多叶页锤",
    "med_ francisca": "中世纪弗兰西斯卡飞斧",
    "med_ fur cloak": "中世纪毛皮大披风",
    "med_ gambeson": "中世纪武装衣/棉甲衬",
    "med_ glaive": "中世纪长柄长刀",
    "med_ great helm": "中世纪骑士巨盔",
    "med_ greave": "中世纪板甲护胫/腿甲",
    "med_ guisarme": "中世纪长柄大刺镰/钩镰",
    "med_ halberd": "中世纪战戟",
    "med_ hand axe": "中世纪手斧/短柄斧",
    "med_ heavy coat of plates": "中世纪重型板甲衣",
    "med_ heavy crossbow": "中世纪重弩",
    "med_ heavy mail hauberk": "中世纪重型长袖锁子甲罩衫",
    "med_ hourglass gauntlets": "中世纪沙漏型板甲手套",
    "med_ jack of plates": "中世纪板甲夹克衣",
    "med_ javelin": "中世纪投掷标枪",
    "med_ joined hose": "中世纪连体紧身裤",
    "med_ kettle hat": "中世纪笠盔/铁帽",
    "med_ kirtle": "中世纪柯特尔裙袍",
    "med_ leather apron": "中世纪皮革围裙",
    "med_ leather armor": "中世纪皮质护甲衣",
    "med_ leather belt": "中世纪皮革腰带",
    "med_ leather boots": "中世纪长筒皮靴",
    "med_ leather coif": "中世纪皮质武装布帽",
    "med_ leather gloves": "中世纪皮手套",
    "med_ leather standard": "中世纪皮质护喉/护颈",
    "med_ leg wraps": "中世纪毛料绑腿",
    "med_ light crossbow": "中世纪轻型钢弩",
    "med_ linen braies": "中世纪布雷裤/大裤衩",
    "med_ linen chemise": "中世纪亚麻衬裙",
    "med_ linen coif": "中世纪亚麻武装布帽",
    "med_ linen footwraps": "中世纪亚麻裹脚布",
    "med_ linen hood": "中世纪亚麻防尘兜帽",
    "med_ linen shirt": "中世纪亚麻内衬衫",
    "med_ linen tunic": "中世纪亚麻束腰短衣",
    "med_ linen wristwraps": "中世纪亚麻裹腕",
    "med_ longbow": "中世纪大长弓",
    "med_ longsword": "中世纪骑士长剑",
    "med_ lucerne hammer": "中世纪卢塞恩长柄锤",
    "med_ mace": "中世纪钉头锤",
    "med_ mail aventail": "中世纪锁子甲颈帘",
    "med_ mail chausses": "中世纪锁子甲护腿裤",
    "med_ mail hauberk": "中世纪长袖锁子甲罩衫",
    "med_ mail mittens": "中世纪锁子甲连指手套",
    "med_ mail sabatons": "中世纪锁子甲护面鞋",
    "med_ mail shirt": "中世纪锁子甲套衫",
    "med_ maul": "中世纪重型大战锤",
    "med_ messer": "中世纪梅瑟刀",
    "med_ misericorde": "中世纪慈悲匕首",
    "med_ morning star": "中世纪晨星锤",
    "med_ oilcloth cloak": "中世纪油布防雨披风",
    "med_ partisan": "中世纪翼矛/阔头枪",
    "med_ pattens": "中世纪木底防泥鞋/木屐",
    "med_ pickaxe": "中世纪鹤嘴锄",
    "med_ pike": "中世纪超长矛",
    "med_ pitchfork": "中世纪干草叉",
    "med_ plate bevor": "中世纪板甲护面/钢护喉甲",
    "med_ plate gauntlets": "中世纪全指板甲钢手套",
    "med_ plate gorget": "中世纪板甲护颈/铁护面",
    "med_ plate sabatons": "中世纪板甲钢铁鞋",
    "med_ poleyn": "中世纪板甲护膝",
    "med_ pollaxe": "中世纪长柄斧锤/战斧",
    "med_ quarterstaff": "中世纪长棍",
    "med_ rerebrace": "中世纪板甲上臂甲",
    "med_ rock": "中世纪飞石/石头",
    "med_ rondel dagger": "中世纪圆盘匕首",
    "med_ rope belt": "中世纪麻绳腰带",
    "med_ rusty mail hauberk": "中世纪锈蚀锁子甲罩衫",
    "med_ sallet": "中世纪沙雷特轻盔",
    "med_ scythe": "中世纪大镰刀",
    "med_ seax": "中世纪撒克逊单刃短刀",
    "med_ shortbow": "中世纪反曲猎弓/短弓",
    "med_ shortsword": "中世纪短剑",
    "med_ sling": "中世纪投石索",
    "med_ spaulder": "中世纪板甲护肩",
    "med_ spear": "中世纪长枪/木柄矛",
    "med_ split hose": "中世纪分体紧身裤/开裆裤",
    "med_ stiletto": "中世纪细剑/三棱刺匕首",
    "med_ straw hat": "中世纪草帽",
    "med_ thick leather cap": "中世纪加厚皮帽",
    "med_ turnshoes": "中世纪翻缝皮鞋",
    "med_ velvet brigandine": "中世纪天鹅绒布里根丁板甲",
    "med_ voulge": "中世纪长柄长格刀/沃斯特长格",
    "med_ wood axe": "中世纪伐木斧",
    "med_ wool cloak": "中世纪羊毛披风",
    "med_ wool hood": "中世纪羊毛防护兜帽",
    "med_ wool hose": "中世纪羊毛紧身袜裤",
    "med_ wool mittens": "中世纪羊毛连指手套",
    "med_ wool shawl": "中世纪羊毛披肩",
    "med_ wool tunic": "中世纪羊毛束腰外衣",
    "med_ work apron": "中世纪粗麻工作围裙",
    "med_ vambrace": "中世纪板甲前臂护甲",
    "med_ war hammer": "中世纪战锤",
    "dirt road": "中世纪泥土路",
    "A pair of small overlapping steel plates that cover the shoulders.  Worn over a gambeson or mail hauberk, these are the most basic plate armor pieces for the arms.":
        "一对覆盖在肩膀上的重叠钢制小板甲。穿戴在武装衣（Gambeson）或锁子甲罩衫（Mail Hauberk）之上，这些是手臂防具中最基础的板甲部位。",

    # ------------------ 长篇背景介绍和 Lore 描述（保持原味专业学术汉化） ------------------
    "A French and Burgundian polearm — essentially an early halberd with a broad cleaver-like blade and a thrusting point.  Less refined than the Swiss halberd it evolved into, but still a devastating combination of cutting and stabbing on a long pole.": 
        "一把法国和勃艮第式的长柄武器——本质上是早期战戟，配有宽大的斩切刀刃和刺击尖头。虽然不如后来演变出的瑞士战戟精细，但在长柄上结合了毁灭性的劈砍与刺击动作。",
        
    "A Swiss polearm with a distinctive three-pronged hammer head and a long top spike.  The prongs concentrate force into narrow points for maximum armor penetration, while the spike can be driven into plate gaps.  A formidable weapon in disciplined hands.": 
        "一把具有独特三爪锤头和长顶刺的瑞士长柄武器。三爪可以将冲击力集中到狭窄的点上，以实现最大程度的破甲，而顶刺则可以刺入板甲缝隙。在训练有素的士兵手中是一件可怕的武器。",
        
    "A basic, rugged torso defense worn by city guards and seasoned mercenary foot soldiers.  Features rough budget steel scales riveted inside a heavy canvas or cowhide shell, leaving the rivet heads exposed on the exterior.  Provides durable protection without the expensive decorative finish of knightly harnesses.": 
        "一种由城市卫兵和资深佣兵步兵穿着的基础且坚固的躯干护具。其特点是在厚帆布或牛皮外壳内侧铆接粗糙的廉价钢片，铆钉头露在外侧。提供耐用的保护，而没有骑士全身甲那种昂贵的装饰性外观。",
        
    "A brutal one-handed weapon consisting of a spiked steel ball mounted on a wooden haft.  The spikes puncture mail and concentrate crushing force behind each blow.  A favorite of infantry and mercenaries who favor intimidation as much as effectiveness.": 
        "一种野蛮的单手武器，由安装在木柄上的带刺钢球组成。刺击可以刺穿锁子甲，并在每次打击中集中毁灭性的钝击力。深受注重威慑力和实效性的步兵和雇佣兵的喜爱。",
        
    "A classic medieval one-handed sword, balanced for both cutting and thrusting.  The double-edged blade tapers to a sharp point, capable of piercing mail when aimed precisely.": 
        "一把经典的中世纪单手剑，在劈砍和刺击之间取得了极佳的平衡。双刃剑身逐渐收缩成锋利的尖端，在精准瞄准时能够刺穿锁子甲。",
        
    "A cloak made from stout linen impregnated with boiled linseed oil until it takes on a dark, semi-glossy sheen.  Oilcloth is the secret weapon of the medieval traveler caught in foul weather — it sheds rain like a duck's back and blocks the wind, though it is stiff, heavy, and smells faintly of linseed.  Hunters, sailors, and anyone who must travel through the wet swear by it.": 
        "一件由结实的亚麻布制成的披风，浸透了煮沸的亚麻籽油，呈现出深色半光泽。防雨油布是中世纪旅行者应对恶劣天气的秘密武器——它能像鸭子羽毛一样防雨并阻挡风寒，虽然它又硬又重，而且有一股淡淡的亚麻籽油味。猎人、水手和任何必须在潮湿环境中穿行的人都对其赞不绝口。",
        
    "A close-fitting cap made from undyed linen, covering the top of the head and ears.  The most basic medieval head covering, worn by all classes to keep hair clean and provide a modest layer of warmth.": 
        "一顶由未染色亚麻布制成的贴身布帽，覆盖头顶和耳朵。这是最基本的中世纪头部覆面，所有阶层都戴着它以保持头发清洁并提供适度的保暖。",
        
    "A close-fitting, padded garment that covers the torso and upper arms, with a linen lining and a wool outer shell.  The doublet is worn by townsfolk and skilled craftsmen who can afford tailored clothing — it buttons down the front and has points on the lower edge to tie the hose to, keeping everything in place.": 
        "一件贴身加厚的衣物，覆盖躯干和上臂，配有亚麻衬里和羊毛外层。紧身短袄是能够负担得起定制服装的市民和熟练工匠穿着的——它在正面扣紧，下摆边缘有绳孔用于系紧紧身裤，使一切保持原位。",
        
    "A commoner's defense constructed by securing small, overlapping metal plates with cord or twine stitched directly through pre-drilled holes between layers of heavy linen canvas.  While bulky and somewhat rigid, the thick linen-and-steel sandwich absorbs blunt trauma remarkably well.": 
        "一种平民防护具，通过用细绳或麻线直接穿过厚重亚麻帆布层之间预先钻好的孔，固定小型重叠金属板而制成。虽然笨重且有些僵硬，但厚实的亚麻加钢板夹层能极好地吸收钝击伤害。",
        
    "A compact crossbow that can be spanned by hand without mechanical assistance.  Easy to aim and fire with minimal training — the great equalizer that lets a peasant drop a knight.  Moderate power, but the simplicity and accessibility of the crossbow transformed medieval warfare.": 
        "一种可以手动拉弦而不需要机械辅助的紧凑型手弩。易于瞄准和射击，只需极少训练——这是让农民也能击倒骑士的伟大平等武器。威力适中，但弩的简单与普及改变了中世纪的战争面貌。",
        
    "A compact hunting bow, short enough to use from horseback or in dense woodland.  Quick to draw and loose, but lacks the range and penetration of a proper war bow.  The standard weapon of hunters and light skirmishers.": 
        "一种紧凑的猎弓，足够短小，便于在马背上或茂密的森林中使用。绘制和释放速度快，但缺乏正规战弓的射程和穿透力。这是猎人和轻步兵的标配武器。",
        
    "A compact sidearm with a short, double-edged blade designed primarily for thrusting in close quarters.  Light enough to be worn comfortably by townsfolk and travelers, it serves better as a defensive weapon than an offensive one.": 
        "一种紧凑的副手武器，具有设计用于在近距离进行刺击的短双刃刃部。足够轻便，可以让市民和旅行者舒适地佩戴，它作为防守武器比作为进攻武器更合适。",
        
    "A crude but effective weapon — nothing more than a sturdy tree branch, perhaps with the thicker end as the striking head.  Simple enough to be found or made anywhere, and a solid blow will crack bones regardless of what armor the target wears.": 
        "一种粗糙但有效的武器——不过是一根结实的树枝，或许较粗的一端作为打击头。简单到可以在任何地方找到或制作，而且无论目标穿着什么防具，坚实的一击都能敲碎骨头。",
        
    "A crude, poorly maintained chainmail hauberk scavenged from a battlefield.  Many of its cheap carbon steel rings are rusted or coming loose, making it heavy, stiff, and prone to breaking.  Offers mediocre protection but is highly affordable for desperate outlaws.": 
        "一件从战场上搜刮来的粗糙、维护不良的锁子甲罩衫。它的许多廉价碳钢环都生锈或松动了，使其沉重、僵硬且容易断裂。提供平庸的保护，但对于走投无路的歹徒来说非常实惠。",
        
    "A curtain of riveted chainmail rings that hangs from the bottom edge of a bascinet, protecting the neck and upper shoulders.  Worn by knights and men-at-arms to defend the vulnerable gap between helmet and body armor.": 
        "挂在轻型颊盔底缘的铆接锁甲帘，保护颈部和上肩。由骑士和重装步兵佩戴，以防御头盔和身体护甲之间脆弱的缝隙。",
        
    "A dedicated anti-armor weapon with a hammer head on one side and a curved spike on the other, mounted on a long haft.  The hammer face delivers crushing concussion through plate, while the spike — essentially a short bec de corbin — can punch through helmet tops and shoulder plates.  The preferred sidearm of knights fighting on foot against other armored opponents.": 
        "一种专用的反装甲武器，一侧为锤头，另一侧为弯曲的尖刺，安装在长柄上。锤面能透过板甲传递毁灭性的震荡力，而尖刺——本质上是缩短的鸦喙锄——可以刺穿头盔顶部和肩甲板。是骑士步战对抗其他重装对手时的首选副手武器。",
        
    "A deep woolen hood that drapes over the head, neck, and shoulders, shielding the wearer from wind, cold, and rain.  The single most important cold-weather garment a medieval commoner owns — worn by peasants and soldiers alike beneath helmets or on its own.": 
        "一个深垂的羊毛兜帽，罩在头、颈和肩膀上，保护穿着者免受风寒和雨水侵袭。这是中世纪平民拥有的最重要的防寒衣物——农民和士兵都会在头盔内侧或单独佩戴它。",
        
    "A farming tool with a long wooden handle and two or three steel tines.  In battle, it provides excellent reach and spacing — the tines keep enemies at a distance while the wielder remains safely behind.  A classic weapon of peasant revolts.": 
        "一种带有长木柄和两到三个钢叉齿的农具。在战斗中，它提供了出色的射程和间距——叉齿将敌人挡在远处，而使用者则安全地留在后方。这是农民起义的经典武器。",
        
    "A fashionable woolen hood with an extended tail that can be draped over one shoulder or wrapped around the neck like a scarf.  Popular among townsfolk and the merchant class — warmer and more stylish than the common wool hood, though still thoroughly practical.": 
        "一种时尚的羊毛兜帽，带有一条拉长的尾部，可以挂在单肩上或像围巾一样缠绕在脖子上。在市民和商人阶层中很受欢迎——比普通羊毛兜帽更暖和、更有型，但也完全实用。",
        
    "A fearsome two-handed axe with a long haft and a large, thin, gracefully curved blade.  A weapon of elite warriors, it sacrifices some of the battle axe's concentrated impact for faster, wider, more devastating cuts.  Excels at cleaving through lightly armored foes and sweeping multiple enemies.": 
        "一把可怕的双手大斧，配有长柄和巨大的、薄的、弧度优美的弯曲刃部。这是精锐战士的武器，它牺牲了战斧的部分集中冲击力，以实现更快、更宽、更具毁灭性的劈砍。擅长劈开轻装敌人并横扫多个目标。",
        
    "A fist-sized stone from the ground.  The weapon of last resort — throw it, smash it, drop it and run.  Even a knight in full plate respects a well-aimed rock to the visor, if only for a moment.": 
        "地上一块拳头大小的石头。最后的防身武器——扔出去，砸下去，扔掉然后逃跑。即使是穿着全套板甲的骑士，也会对一颗砸向面罩的精准飞石心存忌惮，哪怕只是一瞬间。",
        
    "A fitted cap of thin, supple leather that covers the top of the head and ears.  Offers a modicum of protection against scratches and light blows — favored by hunters, scouts, and anyone who expects to push through thick brush.": 
        "一顶由轻薄柔软皮革制成的贴身皮帽，覆盖头顶和耳朵。提供适度的防擦伤和轻微撞击保护——深受猎人、侦察兵和任何预计要穿过茂密灌木丛的人的喜爱。",
        
    "A full-sized English-style war bow — six feet of yew demanding immense strength to draw.  In trained hands, it can send a bodkin arrow through mail and into flesh at two hundred yards.  The weapon that won Crecy and Agincourt, but archers train from childhood for the strength required.": 
        "一把足尺寸的英式战弓——六英尺长的紫杉木，需要巨大的力量才能拉开。在受过训练的手中，它可以在两百码外将破甲箭射穿锁甲扎进肉里。这是赢得了克雷西和阿金库尔战役的武器，但弓箭手们从小就必须训练以获得所需的力量。",
        
    "A heavy apron of thick leather that covers the front of the body from chest to knee, secured by sturdy leather straps crossed behind the neck and back.  The defining garment of the blacksmith and the butcher — thick enough to deflect sparks, glancing blows, and the occasional splash of molten metal or hot blood.": 
        "一件厚皮的重型围裙，从胸部覆盖到膝盖，由交叉在脖子和背后的结实皮革带固定。这是铁匠和屠夫的标志性围裙——厚实到足以偏转火花、擦伤性撞击以及偶尔飞溅的熔融金属或热血。",
        
    "A heavy cloak made from the pelt of a large animal, worn with the fur turned inward for maximum warmth.  Fur cloaks are the ultimate cold-weather gear for those who live on the northern fringes of the medieval world — a hunter alone in the winter woods or a lord traveling through snowbound passes.  Incredibly warm, but heavy and prone to shedding when wet.": 
        "一件由大型野兽毛皮制成的重型披风，穿着时毛皮朝内以获得最大程度的保暖。毛皮披风是生活在中世纪世界北部边缘的人们的终极御寒装备——无论是在冬季森林中独自打猎的猎人，还是穿行在白雪皑皑山口的领主。极其保暖，但又重且弄湿后容易掉毛。",
        
    "A heavy felling axe designed for chopping trees, not men — but it will do in a pinch.  Heavier and slower than a fighting hand axe, but the weight behind the swing is terrifying.  Peasants pressed into service often carry whatever tools they have.": 
        "一把专为伐木而非砍人设计的重型采伐斧——但在紧急情况下也能凑合用。比战斗手斧更重、更慢，但挥动时的重量却很可怕。被强征入伍的农民通常会携带他们拥有的任何工具。",
        
    "A heavy two-handed axe built for war.  The broad steel head delivers crushing blows that combine weight and edge, capable of staggering armored opponents even when the blade cannot penetrate.  Requires both hands and considerable strength to wield effectively.": 
        "一把专为战争打造的重型双手战斧。宽大的钢质斧头提供了结合重量和锋利度的毁灭性打击，即使在刃部无法穿透的情况下也能使重装对手摇晃。需要双手和相当大的力量才能有效挥舞。",
        
    "A heavy, classic 14th-century torso protection reconstructed from the Wisby battlefield mass graves.  Consists of large overlapping iron plates riveted vertically and horizontally inside a strong leather vest.  Imparts solid protection against cuts and arrows, but its rigid plates restrict movement significantly.": 
        "一种根据维斯比战场万人坑重建的重型经典14世纪躯干防护甲。由纵横铆接在坚固皮革背心内侧的大型重叠铁板组成。对劈砍和箭矢提供坚实的防护，但其僵硬的甲板会显著限制移动。",
        
    "A heavy, knee-length cloak made from thick felted wool, fastened at the throat with a simple brooch or toggle.  The universal outer garment for travel, work, and battle — a wool cloak traps body heat in winter, sheds light rain, and can double as a blanket when you bed down for the night.  Every medieval traveler owns one or freezes without it.": 
        "一件及膝的重型披风，由厚毡羊毛制成，在喉部用简易胸针或扣子固定。是旅行、工作 and 战斗的通用外衣——羊毛披风在冬天能锁住体温，防小雨，夜里露营还能充当毯子。每个中世纪旅行者都有一件，否则就会挨冻。",
        
    "A highly protective, Italian-style transitional armor popular in the late 14th century.  Employs a combination of small, flexible steel plates along the waist and flanks, and larger, thick breastplate plates over the torso.  Superb front thrust protection while retaining moderate waist flexibility.": 
        "一种在14世纪后期流行的、具有高度保护性的意大利式过渡期盔甲。结合了沿腰部和肋侧的小型灵活钢片，以及覆盖在躯干上的较大、较厚的胸甲板。提供极佳的正面刺击保护，同时保留了适度的腰部灵活性。",
        
    "A knee-length coat of riveted chainmail rings, reaching from the shoulders to the thighs with long sleeves and a split skirt for riding.  The quintessential armor of the professional medieval soldier — nearly impervious to slashing cuts.  However, a bodkin arrow or spear thrust can burst individual rings, and blunt force transmits through the links with ease.  Always worn over a gambeson.": 
        "一件及膝的铆接锁子甲罩衫，从肩膀延伸到大腿，配有长袖和用于骑马的开叉摆。这是专业中世纪士兵的经典护甲——几乎无法被劈砍割裂。然而，破甲箭或长枪刺击可以冲散单个铁环，且钝击力很容易透过链环传递。必须穿着在武装衣之上。",
        
    "A knee-length tunic made from thick, felted wool with long sleeves.  The universal outermost garment of the medieval commoner — worn over a linen undershirt by every peasant, craftsman, and soldier in Europe.  This is the garment you picture when you think 'medieval clothing'.": 
        "一件及膝的长袖厚毡羊毛束腰短衣。这是中世纪平民通用的最外层衣物——欧洲的每一个农民、工匠和士兵都会在亚麻内衬衣外穿着它。这就是你想起“中世纪服装”时脑海中浮现的衣服。",
        
    "A knee-length tunic made from undyed linen — the summer alternative to the wool tunic.  Worn by peasants working the fields under a blazing sun, where the wool tunic would be unbearable.  Lighter, cooler, and utterly useless against a cold night.": 
        "一件及膝的未染色亚麻束腰短衣——羊毛外衣的夏季替代品。由农民在烈日下的田间劳动时穿着，那时穿羊毛外衣会难以忍受。更轻、更凉快，但在寒冷的夜晚完全无用。",
        
    "A knightly polearm featuring a hammer head opposite a long, curved beak-like spike — the 'crow's beak' that gives it its name.  The beak is designed to punch clean through helmet tops and shoulder plates, while the hammer delivers crushing force.  A precision anti-armor instrument.": 
        "一种骑士用的长柄武器，一边是锤头，另一边是长而弯曲的喙状尖刺——赋予它名称的“乌鸦之喙”。喙部旨在干净利落地刺穿头盔顶部和肩甲板，而锤子则提供粉碎力。这是一种精密的反装甲武器。",
        
    "A lavish, high-status armor worn by wealthy knights.  Consists of hundreds of meticulously overlapping steel scales, tin-plated to resist rust, and riveted securely to the inside of a rich velvet outer shell.  The gilded rivet heads form beautiful patterns on the outside.  Combines stunning protection, high flexibility, and peerless prestige.": 
        "一件由富有骑士穿着的奢华、地位高贵的盔甲。由数百片精心重叠的镀锡防锈钢鳞片组成，牢固地铆接在华丽的天鹅绒外壳内侧。镀金的铆钉头在外面形成美丽的图案。结合了极佳的防护、高度的灵活性和无与伦比的威望。",
        
    "A light throwing spear with a narrow steel head, designed to be launched at short range before closing to melee.  The impact of a thrown javelin is concentrated into a single sharp point — it can pierce shields and mail with terrifying efficiency.  Carry several.": 
        "一种带有窄钢头的轻型投掷枪，设计用于在进入肉搏战之前在近距离发射。投掷标枪的冲击力集中在一个锋利的点上——它可以以可怕的效率刺穿盾牌和锁子甲。建议多带几根。",
        
    "A lightened torso defense designed for archers and skirmishers.  Features medium carbon steel scales protecting the vitals of the chest, while the shoulders and sides are left open or backed only by light leather straps.  This grants superior breathability and maximum range of motion for drawing a warbow.": 
        "一种专为弓箭手和散兵设计的轻量化躯干防护具。其特点是使用中碳钢鳞片保护胸部的致命部位，而肩部和侧翼则保持敞开或仅用轻质皮革带支撑。这提供了卓越的透气性和拉开战弓所需的最大活动范围。",
        
    "A long wooden haft topped with a single-edged curved blade resembling a large knife or sword.  Designed for wide sweeping cuts that can clear a space around the wielder.  Less versatile than a halberd but unmatched in cutting arcs.": 
        "一根长木柄，顶部装有单刃弯曲刀刃，类似于大刀或大剑。设计用于宽范围的横扫劈砍，可以在使用者周围扫清一片空间。虽然不如战戟多功能，但劈砍弧度无可匹敌。",
        
    "A long woolen garment that falls from the shoulders to the calves, fitted at the bodice and flaring into a full skirt.  The standard everyday dress for medieval women of all stations — a kirtle is worn over a linen chemise and can be laced up the front or sides.": 
        "一件及小腿的羊毛长袍，从肩膀垂下，在紧身胸衣处贴身并在下方散开成饱满的裙摆。这是中世纪各阶层女性的标准日常裙装——柯特尔裙穿在亚麻内衣外面，可以在正面或侧面系带。",
        
    "A long, loose-fitting linen undergarment that falls from the shoulders to the thighs — the standard first layer for medieval women and the longer counterpart to the linen shirt.  Worn against the skin to absorb sweat and prevent outer garments from chafing.": 
        "一件及大腿的宽松亚麻长内衣——中世纪女性的标准贴身第一层，也是亚麻衬衫的加长版。贴身穿着以吸收汗水并防止外衣摩擦皮肤。",
        
    "A long-handled farming scythe with a curved blade designed for cutting grain at ground level.  Usable as a weapon in its original form, but the blade angle is awkward for combat.  A scythe blade rotated 90 degrees — a 'war scythe' — is a different animal entirely.": 
        "一种长柄农用割草镰刀，具有设计用于在地表收割谷物的弯曲刀刃。在其原始形式下可以用作武器，但刀刃角度对于战斗来说很别扭。如果将镰刀刃旋转90度——即“战镰”——就完全是另一回事了。",
        
    "A massive cylindrical steel helmet that encloses the entire head, with narrow eye slits and breathing holes punched through the lower face.  Though its heyday has passed, some knights still wear this imposing helm over a smaller bascinet for maximum protection.": 
        "一个巨大的圆柱形钢制头盔，包裹着整个头部，在下脸部开有狭窄的眼缝和呼吸孔。虽然它的全盛时期已过，但一些骑士仍将这种威严的巨盔佩戴在较小的轻盔外面，以获得最大的保护。",
        
    "A massive two-handed sledgehammer of war — a heavy steel head on a thick wooden haft.  Slow and exhausting to swing, but when it connects, armor is irrelevant.  Plate crumples, bones shatter, and even the stoutest shield cannot absorb the full force.  The weapon of choice for breaking shield walls and armored lines.": 
        "一把巨大的双手重型战锤——厚木柄上安装着沉重的钢制锤头。挥舞起来缓慢且令人疲惫，但一旦命中，护甲便形同虚设。板甲会凹陷，骨骼会粉碎，即使是最坚固的盾牌也无法吸收其全部力量。这是打破盾墙和装甲防线的首选武器。",
        
    "A massive, exceptionally robust knee-length chainmail coat forged from tempered medium carbon steel links.  Features double-layered ring weaving (double mail) over the chest and underarms to maximize defense against bodkin arrows and thrusts.  Offers peerless protection but drains the wearer's stamina quickly.": 
        "一件由回火中碳钢链环锻造而成的及膝重型锁子甲。在胸部和腋下采用双层环编织（双重锁甲），以最大限度地防御破甲箭和刺击。提供无可匹敌的保护，但会迅速消耗穿着者的耐力。",
        
    "A medieval bludgeon with a wood handle and a heavy steel head, often fluted or knobbed.  Heavy and slow to swing, but its crushing force transmits through armor — it does not need to penetrate plate to shatter the bones beneath.": 
        "一种带有木柄和沉重钢制头部的中世纪钝器，锤头通常有凹槽或突起。虽然沉重且挥舞缓慢，但其粉碎性力量会透过盔甲传递——它不需要穿透板甲就能震碎下方的骨头。",
        
    "A mining tool with a pointed steel head on one side and a flat hammer face on the other, mounted on a sturdy wooden handle.  In desperate times, its concentrated piercing force makes it a poor man's bec de corbin — slow but devastating against armored targets.": 
        "一种一侧为尖钢头、另一侧为平整锤面的采矿工具，安装在结实的木柄上。在绝望的时期，它集中的穿透力使其成为穷人版的鸦喙长柄锤——虽然慢，但对装甲目标具有毁灭性打击。",
        
    "A pair of articulated steel foot plates worn over armored boots.  Overlapping lames cover the top of the foot from ankle to toe, while the heel is enclosed in a solid steel cup.  Part of a knight's full harness — you will not be kicking or flexing these, but nothing is getting through them either.": 
        "套在护甲靴外的一对关节连接的钢制脚部防护板。重叠的甲片从脚踝到脚趾覆盖了脚面，而脚后跟则被包裹在一个坚固的钢罩中。这是骑士全套马具/全身甲的一部分——你无法穿着它们踢击或弯曲脚掌，但同样也没有什么东西能穿透它们。",
        
    "A pair of articulated steel plates that protect the elbows.  The couter bridges the gap between the rerebrace and vambrace, allowing the arm to bend while keeping the joint covered.": 
        "一对保护肘部的关节连接钢板。护肘连接了上臂甲和前臂甲之间的空隙，允许手臂弯曲同时保持关节被覆盖。",
        
    "A pair of articulated steel plates that protect the knees.  The poleyn connects the cuisse above with the greave below, with a fan-shaped side wing that shields the back of the knee joint.": 
        "一对保护膝部的关节连接钢板。护膝将上方的大腿甲与下方的胫甲连接起来，并带有一个扇形的侧翼，保护膝关节的后部。",
        
    "A pair of chainmail foot coverings worn over boots, protecting the top of the foot from slashing cuts.  The mail drapes from ankle to toe, laced underneath to keep it in place.  Worn by knights and men-at-arms who want foot protection without the crushing weight of plate sabatons.": 
        "套在皮靴外的一对锁子甲脚部防护。锁甲从脚踝一直垂到脚趾，底部系紧固定。适合那些需要防割且不想承受板甲铁鞋沉重负担的重装步兵和骑士。",
        
    "A pair of flexible arm protectors consisting of small overlapping steel plates riveted to the inside of protective leather or velvet sleeves.  Offers excellent flexibility and good defense against cuts and bites, keeping your weapon arm active.": 
        "一对由铆接在防护性皮革或天鹅绒袖子内侧的重叠小钢片组成的灵活护臂。提供优异的灵活性和对劈砍与咬伤的良好防御，保持您的持械手臂活动自如。",
        
    "A pair of flexible leg protectors consisting of small steel plates riveted inside strong leather trousers.  Designed to defend both the thighs and shins while retaining the natural dexterity needed for running and climbing.": 
        "一对由铆接在结实皮裤内侧的小钢片组成的灵活腿部护具。旨在保护大腿和胫骨，同时保留奔跑和攀爬所需的自然灵活性。",
        
    "A pair of formed steel plates that protect the forearms from elbow to wrist.  Vambraces are among the earliest plate armor pieces adopted by medieval warriors, offering vital protection to the sword arm.": 
        "一对保护前臂从肘部到手腕的成型钢板。前臂护甲是中世纪战士最早采用的板甲护具之一，为持剑手臂提供至关重要的保护。",
        
    "A pair of full plate steel gauntlets with articulated lames covering every finger joint from knuckle to tip.  The cuff extends well past the wrist, and the palm is protected by a solid steel plate.  Worn only by the wealthiest knights and lords, these represent the pinnacle of hand armor for the late 14th to early 15th century.": 
        "一双全板甲钢制手套，关节甲片覆盖了从指关节到指尖的每一个手指关节。手套口延伸到手腕之外，手掌由坚固的钢板保护。只有最富有的骑士和领主佩戴，代表了14世纪末到15世纪初手部防护的巅峰。",
        
    "A pair of gauntlets with an hourglass-shaped cuff, the signature hand armor of the late 14th century.  Articulated steel plates cover the back of the hand and wrist, while the palm and fingers are protected by overlapping steel scales stitched to a leather glove.  They offer excellent protection without completely sacrificing dexterity.": 
        "一双带有沙漏形袖口的板甲手套，是14世纪末的标志性手部装甲。关节钢板覆盖手背和手腕，而手掌和手指则由缝合在皮革手套上的重叠钢鳞片保护。它们在提供极佳防护的同时不完全牺牲手指的灵活性。",
        
    "A pair of long linen strips wound tightly around the feet, worn inside turnshoes or even alone.  The desperate man's sock — footwraps cost almost nothing and can be washed and re-used, but offer little protection from the cold, the wet, or the sharp stone underfoot.  When you have nothing else, these are what you have.": 
        "缠在脚上的长亚麻布条，穿在翻缝鞋内或直接赤脚穿。这是穷途末路之人的袜子——裹脚布几乎不花钱，且可以清洗重复使用，但防寒防湿效果差，无法防御脚下的尖锐石块。当您一无所有时，它是最后的选择。",
        
    "A pair of loose-fitting linen undergarments that sit at the waist and reach to mid-thigh, secured with a simple drawstring.  The standard medieval undergarment worn by all classes.": 
        "一条贴身腰间、及至大腿中部的宽松亚麻内裤，用简单的拉绳固定。这是所有阶层穿着的标准中世纪内衣。",
        
    "A pair of mittens woven from riveted chainmail rings, lined with thin leather on the inside.  They protect the hands from slashing cuts while leaving enough flexibility to grip a weapon, though a well-aimed thrust will find the gaps between rings.": 
        "一双由铆接锁链环织成的连指手套，内侧衬有薄皮革。它们能保护手部免受劈砍，同时保留足够的灵活性以握持武器，不过瞄准好的刺击仍会刺中锁环间的缝隙。",
        
    "A pair of riveted chainmail leggings that cover both legs from thigh to ankle.  Worn by knights and heavy cavalry over padded chausses, mail chausses provide excellent protection against slashing cuts but are vulnerable to piercing weapons.": 
        "一对覆盖从大腿到脚踝双腿的铆接锁子甲护腿。由骑士和重骑兵在加厚防护裤外穿着，锁甲护腿提供针对劈砍伤害的出色防护，但容易被穿刺武器击穿。",
        
    "A pair of separate woolen stockings, each covering one leg from thigh to toe, individually laced to the braies above.  This is the earlier and simpler form of hose — the legs are not joined at the crotch, leaving the braies exposed between them.  Practical for a peasant, but lacking the modesty of the joined hose.": 
        "一对分体的羊毛长袜，每只覆盖一条从大腿到脚趾的腿，分别系在上面的内裤（布雷裤）上。这是紧身裤更早、更简单的形式——双腿在裆部不相连，使布雷裤暴露在中间。对农民来说很实用，但缺乏连体紧身裤的体面。",
        
    "A pair of shaped steel plates that protect the thighs.  Cuisses are the upper part of a full plate leg harness, strapped over mail chausses for layered protection.": 
        "一对保护大腿的成型钢板。大腿甲是全套板甲腿具的上半部分，系在锁甲护腿之上，以提供分层保护。",
        
    "A pair of shaped steel plates that protect the upper arms from shoulder to elbow.  Worn together with a couter and vambrace for full arm protection.": 
        "一对保护从肩部到肘部上臂的成型钢板。与护肘和前臂护甲一起佩戴，以提供完整的手臂保护。",
        
    "A pair of simple leather shoes made by stitching the upper to a thin leather sole, then turning the whole thing inside-out so the seams sit on the inside.  The standard footwear of medieval peasants — soft enough to feel the ground beneath your feet, which is both a blessing for stealth and a curse when you step on a sharp rock.": 
        "一双通过将鞋面缝合到薄皮底上，然后将整只鞋里外翻转使接缝留在内侧而制成的简易皮鞋。中世纪农民的标准鞋履——柔软到能清晰感觉到脚下的地面，这对于潜行来说是一种祝福，但当你踩到锋利的石头时，它就是个诅咒。",
        
    "A pair of simple stitched leather gloves.  Worn by peasants and soldiers alike to keep their hands warm and protected from minor scrapes.": 
        "一双简单的缝合皮手套。农民和士兵都会佩戴，以保持双手温暖并防止轻微擦伤。",
        
    "A pair of snug-fitting woolen stockings that cover both legs from the waist down to the toes, worn as a matched pair tied to the doublet or braies above.  These are the universal leg coverings of the medieval world — every peasant and lord alike wears hose, differing only in the quality of the wool and the cut.": 
        "一双贴身的羊毛长袜，从腰部一直覆盖到脚趾，作为成对穿着系在上面的短袄或布雷裤上。这是中世纪世界通用的腿部覆盖物——每个农民和领主都会穿紧身裤，区别仅在于羊毛的质量和裁剪。",
        
    "A pair of steel plates shaped to protect the lower legs from knee to ankle.  Greaves shield the shins—a common target in foot combat—and are among the most frequently worn pieces of plate armor on the battlefield.": 
        "一对旨在保护膝部到脚踝下肢的成型钢板。胫甲能保护胫骨——步战中常见的受击目标——是战场上最常佩戴的板甲部位之一。",
        
    "A pair of sturdy leather boots that rise above the ankle, with thick doubled soles and reinforced stitching.  The step up from turnshoes — ankle boots provide better support for long walks and some protection against the wet and the mud.  The go-to footwear of craftsmen, hunters, and any commoner who can afford better than the bare minimum.": 
        "一双高度超过脚踝的结实皮靴，配有厚实的双层鞋底和加固缝线。比翻缝鞋更进了一步——短皮靴为长途跋涉提供更好的支撑，并对潮湿和泥泞提供一定保护。是工匠、猎人以及任何能够负担得起比最低限度更好鞋履的平民的常用鞋履。",
        
    "A pair of thick, fuzzy mittens knitted from unrefined wool.  Mittens keep the fingers together so they can share warmth, making them far more effective against the cold than fingered gloves — though you will struggle to do anything requiring individual finger dexterity while wearing them.": 
        "一双由粗羊毛织成的厚实毛茸茸的连指手套。连指手套将手指聚在一起以分享体温，这使它们在防寒方面比分指手套有效得多——不过戴着它们时，你很难做任何需要单个手指灵巧度的事情。",
        
    "A pair of wooden overshoes worn over regular footwear, secured by leather straps across the instep.  Pattens lift your feet an inch above the mud, snow, and filth of medieval streets — the difference between wet feet and dry feet in foul weather.  They clack loudly on stone and make you walk with a slightly awkward gait, but that is a small price to pay.": 
        "一种套在普通鞋外穿着的木制外套鞋，通过跨过脚背的皮革带固定。木套鞋将你的脚抬高到中世纪街道的泥泞、冰雪和污秽之上一英寸——这是恶劣天气中湿脚与干脚的区别。它们在石头上会发出响亮的咔哒声，让你走路的姿势有些别扭，但这是一个很小的代价。",
        
    "A pair of woolen hose joined together at the waist, forming a single garment that covers both legs fully from waist to toe.  The mark of a man who can afford a tailor — the joined hose offers better coverage and a trimmer silhouette than the separate split hose, though it takes longer to put on and costs more.": 
        "一件在腰部连接在一起的羊毛紧身裤，形成一个从腰部到脚趾完全覆盖双腿的单件衣物。这是负担得起裁缝的人的标志——连体裤比分体开裆裤提供更好的覆盖和更整洁的轮廓，虽然穿戴时间更长且价格更高。",
        
    "A pointed steel bascinet fitted with a protruding 'pig-faced' visor that covers the entire face.  The snout-like shape deflects blows and allows breathing through small holes.  The iconic helmet of knights and men-at-arms in the late 14th century.": 
        "一个配有凸出“猪脸”面罩的钢制轻盔，覆盖整个脸部。像猪嘴一样的形状能偏转打击，并允许通过小孔呼吸。这是14世纪后期骑士和重装步兵的标志性头盔。",
        
    "A pointed steel helmet with a conical crown, offering good protection to the top and sides of the head while leaving the face open.  The quintessential soldier's helm of the late 14th century.": 
        "一个带有圆锥形盔顶的钢制轻头盔，为头部顶部和两侧提供良好的保护，同时露出脸部。这是14世纪后期经典士兵头盔的缩影。",
        
    "A powerful military crossbow requiring a belt-hook or lever to span.  Each bolt hits with the force of a charging lance, punching through mail and most armors at medium range.  Slow to reload — each shot must count, but each shot will hurt.  The standard weapon of mercenary crossbow companies.": 
        "一种需要腰挂钩或拉杆才能拉弦的强力军用十字重弩。每发弩箭都以如同冲锋长枪般的力道击中目标，在中距离穿透锁甲和大多数护甲。装弹缓慢——每一次射击都必须算数，但每一次射击都会带来重创。是雇佣弩兵公司的标配武器。",
        
    "A rectangular length of soft wool cloth draped over the shoulders — the portable warmth solution of people who cannot afford a full cloak.  Lighter and easier to wear while working than a cloak, though it leaves the arms and lower body exposed.": 
        "一件披在肩上的长方形软羊毛织物——买不起完整披风者的简易御寒方案。比大披风更轻便，便于劳动，但手部和下半身仍然会暴露在风寒中。",
        
    "A recurve bow crafted from laminated layers of wood, horn, and sinew — a technique perfected by eastern peoples.  Shorter than a longbow but storing more energy for its size, it can deliver powerful shots from horseback or on foot.  Requires skilled craftsmanship to make and skilled hands to use.": 
        "一种由木、角和兽腱的分层层压板制成形反曲复合弓——这是由东方民族完善的技术。虽然比长弓短，但按其尺寸可以储存更多能量，无论是骑马还是步行都能提供强大的射击。需要高超的工艺制作，也需要熟练的人手使用。",
        
    "A shaped steel plate that covers the chin, lower cheeks, and throat.  Worn together with a sallet helmet, this combination provides full head and face protection that rivals a great helm while offering far better vision and ventilation.  The defining knightly gear of the mid-15th century.": 
        "一片设计用于保护下巴、下脸颊和喉部的成型钢板。与沙雷特轻盔一同佩戴，这种组合提供了与骑士巨盔相抗衡的完整头部和面部保护，同时提供好得多的视野和透气性。是15世纪中期标志性的骑士装备。",
        
    "A shaped steel plate that wraps around the throat and rests on the collarbones, closing the vulnerable gap between helmet and breastplate.  A vital piece of a knight's full harness that protects the most exposed junction in the armor.": 
        "一片包裹颈部并压在锁骨上的成型钢板，封闭了头盔和胸甲之间脆弱的缝隙。这是骑士全身甲中至关重要的一部分，保护了盔甲中最暴露的交界处。",
        
    "A shaped torso armor made from hardened leather boiled in wax or oil, then molded to the body while still warm.  Significantly tougher than untreated leather — it can turn a sword cut and soften a blunt blow.  Worn by light cavalry and professional infantry as a lighter alternative to metal armor.": 
        "一种由在蜡或油中煮沸的硬革制成的成型躯干铠甲，在温热时塑造成型。明显比未经处理的皮革更强韧——它能偏转剑劈并缓冲钝击。由轻骑兵和专业步兵穿着，作为金属盔甲的轻量化替代品。",
        
    "A short sword or long dagger with a distinctive I-shaped or H-shaped hilt, popular among merchants, artisans, and townsfolk for self-defense.  Compact enough to wear daily, substantial enough to settle disputes.  The urban equivalent of a handgun.": 
        "一种具有独特的I形或H形刀柄的短剑或长匕首，深受商人工匠和市民喜爱以用作自卫。足够紧凑以便日常佩戴，也足够坚实来解决争端。这是相当于城镇中手枪般的防身武器。",
        
    "A short-handled axe with a steel head, useful as both a tool and a weapon.  Common among woodsmen and peasants pressed into militia service.  Chops well but lacks reach.": 
        "一把带有钢质斧头的短柄手斧，可用作工具和武器。在战木工和被强征入伍的农民民兵中很常见。砍伐性能良好，但缺乏触及范围。",
        
    "A short-handled hammer used at the forge — too small to be a proper war hammer, but a well-aimed blow to the head or hand will still ruin someone's day.  Better than bare fists.": 
        "一种在锻造中使用的短柄铁锤——对于一把正规战锤来说太小了，但对于头部或手部瞄准好的一击仍会彻底毁掉某人的一天。总比赤手空拳好。",
        
    "A short-sleeved, hip-length shirt of riveted chainmail rings.  Lighter and less cumbersome than a full hauberk, it protects the vital areas of the torso while allowing maximum mobility.  Highly favored by archers, light cavalry, and skirmishers.": 
        "一件短袖、及臀的铆接锁子甲衬衫。比完整的锁甲罩衫更轻便且不那么累赘，在允许最大机动性的同时保护躯干的致命区域。深受弓箭手、轻骑兵和散兵的青睐。",
        
    "A simple apron of coarse linen that covers the front of the body from chest to knee, tied at the waist with a pair of strings.  Worn by farmers, millers, and craftsmen to keep the worst of the daily grime off their clothing — it will not stop a blade, but it will stop the flour and mud.": 
        "一件由粗亚麻制成的简易围裙，从胸部覆盖到膝盖，在腰部用一对带子固定。由农民、磨坊工和工匠穿着，以防止日常劳动中最大的污垢弄脏衣物——它不能阻挡刀刃，但能挡住面粉和泥土。",
        
    "A simple but effective weapon — a steel spearhead mounted on a sturdy wooden shaft.  The reach keeps enemies at bay, and it can be thrown in desperation.  The most common weapon in history for good reason.": 
        "一种简单但有效的武器——安装在结实木轴上的钢制长枪头。它的攻击范围能将敌人拒之门外，在绝望时也可以投掷出去。这是历史上最常见的武器，理由非常充分。",
        
    "A simple cap made from thick, felted wool that covers the crown of the head.  Worn by common folk of all stations to ward off the chill — the humble wool cap is as medieval as the sword.": 
        "一顶由厚毡羊毛制成的简易帽，覆盖头顶。由各阶层的普通百姓戴着以防风御寒——这顶不起眼的羊毛帽和剑一样具有中世纪特色。",
        
    "A simple hood made from undyed linen, long enough to drape over the neck and shoulders.  The most basic head covering worn by peasants across medieval Europe.": 
        "一个由未染色亚麻布制成的简易兜帽，长度足以垂在颈部和肩膀上。这是中世纪欧洲农民戴的最基本的头部覆面。",
        
    "A simple iron helmet with a wide brim, resembling a metal hat.  Popular among infantry and archers for its cheap construction and decent protection from downward blows.": 
        "一种配有宽大边缘的简易铁制头盔，酷似一顶金属帽子。因其廉价的造价和对向下打击的良好防御而深受步兵和弓箭手喜爱。",
        
    "A simple leather pouch with two cords — one looped around the wrist, the other held and released to launch a stone at high speed.  Costs nothing to make, takes years to master.  In skilled hands, a sling stone can match an arrow in range and surpass it in bone-breaking impact.  The weapon of shepherds and ancient peoples.": 
        "一个带有两根绳子的简易皮袋——一根套在手腕上，另一根阻持并释放，以高速发射石头。制作不花一分钱，但需要数年才能掌握。在熟手手中，投石索投出的石头在射程上可以与箭矢媲美，在骨折杀伤力上甚至超过箭矢。这是牧羊人和古代人民的武器。",
        
    "A simple length of hempen rope tied around the waist — the belt of someone who cannot afford leather.  It holds your braies up and gives you something to tuck small items behind, though it is nowhere near as secure or comfortable as a proper leather belt.": 
        "一根绑在腰间的粗糙大麻绳——买不起皮革的人用的简易腰带。用来防止紧身裤（布雷裤）滑落，也能塞一些随身小物件，不过它的稳固和舒适度远比不上皮腰带。",
        
    "A simple long-sleeved shirt made from undyed linen, reaching to the hips.  Worn directly against the skin by all classes of medieval society — the universal first layer beneath any armor.": 
        "一件由未染色亚麻布制成的简易长袖衬衫，及臀。由中世纪社会所有阶层直接贴身穿着——这是任何盔甲下通用的第一层贴身衣物。",
        
    "A simple stout wooden staff, about six feet long.  Deceptively effective — fast enough to strike and parry simultaneously, long enough to keep enemies at distance, and solid enough to break bones.  A skilled staff fighter can hold off multiple armed opponents.": 
        "一根简单的坚实木棍，大约六英尺长。出奇地有效——速度快到可以同时进行打击和格挡，长度足以与敌人保持距离，而且坚固到可以打碎骨头。一个熟练的棍术格斗者可以阻挡多个武装对手。",
        
    "A simpler predecessor to the bill, featuring a sickle-like curved blade with a back spike on a long pole.  Though gradually falling out of fashion, its hook is deadly for dragging horsemen down and pulling shields out of position.": 
        "长柄勾镰的简单前身，特点是在长柄上配有镰刀状弯曲刀刃 and 背刺。虽然逐渐过时，但其挂钩对于将骑兵拖下马和拉开防守盾牌是非常致命的。",
        
    "A single-edged German-style 'knife-sword' with a curved blade and a simple crossguard.  Constructed like a large knife, the messer was legally classified as a knife rather than a sword, allowing commoners to carry it.  Effective at chopping, passable at thrusting.": 
        "一把带有弯曲刀刃和简易护手的单刃德意志式“刀剑”。其构造像一把大刀，在法律上被归类为刀而不是剑，允许平民携带。擅长劈砍，穿刺性能尚可。",
        
    "A single-edged thick-backed knife of Germanic origin, worn horizontally at the belt.  Serves as an everyday utility blade for commoners and hunters — cutting rope, skinning game, and defending oneself when needed.  The heavy spine gives it more chopping power than a typical knife.": 
        "一把起源于德意志的单刃厚脊刀，水平佩戴在腰带上。作为平民和猎人的日常实用刀具——割绳、剥皮以及在需要时自卫。厚重的刀脊使其比一般刀具具有更强的劈砍力。",
        
    "A single-edged, cleaver-like sword with a broad curved blade.  Cheap to produce and easy to use, it delivers devastating chopping blows against unarmored or lightly armored targets, but glances uselessly off plate.": 
        "一把具有宽大弯曲刀刃的单刃割肉刀式短刀。制造成本低且易于使用，它能对未穿甲或轻装目标提供毁灭性的劈砍打击，但对板甲则会无力地弹开。",
        
    "A single-handed axe with a distinctive elongated blade that extends downward into a hook-like 'beard'.  The beard can catch shield edges, weapon hafts, or limbs, making it a versatile tool for both cutting and controlling an opponent.": 
        "一把具有独特细长刃部的单手斧，刃部向下延伸成挂钩状的“胡须”。胡须可以勾住盾牌边缘、武器柄或肢体，使其成为劈砍和控制对手的多功能工具。",
        
    "A slender, needle-pointed dagger with no cutting edge — designed solely for penetrating mail armor rings and sliding between the links.  Quick, quiet, and deadly at close range.  Favored by assassins and as a backup weapon for knights who need to finish armored opponents.": 
        "一把没有劈砍刃的纤细针尖匕首——完全设计用于穿透锁甲环并滑入链环之间。近距离快速、安静且致命。深受刺客喜爱，也作为骑士需要终结重装对手时的备用武器。",
        
    "A small single-edged knife with a blunt tip, carried by virtually everyone in the medieval world.  Designed for cutting food at the table, not for fighting — but when there is nothing else, it will do.  Better than your fingernails.": 
        "一把带有钝尖的小型单刃小刀，中世纪世界几乎人人携带。专为在餐桌上切食物而设计，并非为了战斗——但当别无选择时，它也能派上用场。总比用指甲好。",
        
    "A small throwing axe with a distinctive curved head, a relic of the migration era still occasionally seen.  Designed to be thrown in a high arc that drops onto shields and helmeted heads, its weight and rotation make it surprisingly effective against armor.  Works as a hand axe in a pinch.": 
        "一把具有独特弯曲斧头的小型投掷飞斧，是偶尔仍能见到的民族大迁徙时代的遗物。设计用于高弧度投掷以砸在盾牌和戴头盔的头部上，其重量和旋转使其对防具具有惊人的有效性。在紧急情况下也可以作为手斧使用。",
        
    "A smooth steel helmet that covers the top and back of the head, extending downward to shield the neck.  Lighter and more streamlined than the older great helm, the sallet is gaining favor among knights as the 15th century approaches.": 
        "一个平滑的钢制头盔，覆盖头部顶部和后部，并向下延伸以保护颈部。比旧式的巨盔更轻、更流线型，随着15世纪的临近，沙雷特轻盔在骑士中越来越受欢迎。",
        
    "A solid steel breastplate paired with a matching backplate, forged to fit the wearer's body and secured with leather straps at the shoulders and sides.  The culmination of medieval torso protection — a direct hit from a lance or sword will glance off the smooth, curved surface.  Worn only by knights and lords who can afford the work of a skilled armorer, the cuirass represents the pinnacle of personal protection in the late 14th century.": 
        "一副实心钢制胸甲配以相匹配的背甲，锻造以贴合穿着者的身体，并在肩膀和两侧用皮革带固定。这是中世纪躯干防护的巅峰之作——骑枪或剑的直接撞击会从光滑的弯曲表面弹开。只有能雇得起熟练护甲匠的骑士和领主才能穿着，胸甲代表了14世纪后期个人防护的巅峰。",
        
    "A specialized anti-armor dagger with a long, stiff, triangular or diamond-section blade and a disc-shaped guard and pommel.  Designed to be driven with two hands through mail rings and into the gaps of plate armor — the armpit, the groin, the visor slit.  In armored combat, this is the finishing tool.": 
        "一种专用的反装甲匕首，配有长而坚硬的三角形或菱形刃部，以及圆盘状的护手和柄头。设计用于用双手穿过锁甲环并刺入板甲的缝隙中——腋下、腹股沟、面罩缝。在装甲战斗中，这是终结对手的工具。",
        
    "A specialized two-handed thrusting sword with a rigid, narrow blade designed purely to penetrate mail rings and slip through plate armor gaps.  Nearly useless for cutting, but devastating when half-sworded into an armored opponent's weak points.": 
        "一把专门的双手刺击剑，具有坚硬、狭窄的刃部，纯粹设计用于穿透锁甲环并滑过板甲缝隙。对于劈砍来说几乎毫无用处，但当通过半剑术刺入重装对手的弱点时，它是毁灭性的。",
        
    "A sturdy cap of hardened leather, covering the top of the head.  Worn by militia and light infantry who cannot afford metal helmets.": 
        "一顶由硬化皮革制成的坚固帽子，覆盖头顶。由负担不起金属头盔的民兵和轻步兵戴着。",
        
    "A sturdy leather belt with a simple iron buckle, worn at the waist.  The belt is the medieval commoner's load-bearing system — tools, pouches, knives, and anything else you carry all hang from it.  A belt in good condition is as essential as a good pair of boots.": 
        "一条系于腰间的坚固皮革腰带，配有简易铁搭扣。腰带是中世纪平民的负重系统——工具、便携袋、小刀等一切随身物品都挂在上面。一条处于良好状态的腰带和一双好靴子一样重要。",
        
    "A sturdy pair of knee-length leather boots with thick soles, worn by all classes of medieval society.  While not military-grade foot armor, they keep the mud out and offer decent protection against the rough ground.": 
        "一双扎实的及膝长皮靴，配有厚鞋底，流行于中世纪各阶层。虽非军用级脚部护甲，但防泥泞，并能对粗糙的地面提供良好的防护。",
        
    "A thick collar of hardened leather worn around the neck to protect against slashing cuts.  A cheap alternative to metal gorgets, popular among militia and common soldiers who cannot afford full plate harness.": 
        "套在脖子上以防止劈砍伤害的硬皮革厚领。金属护颈的廉价替代品，在买不起全套板甲的民兵和普通士兵中很受欢迎。",
        
    "A thick padded jacket made from over a dozen layers of quilted linen, stuffed with raw fiber and stitched in vertical channels.  The most fundamental independent armor of the medieval age — worn by everyone from peasant levies to knights as a foundation layer beneath mail.  The dense padding absorbs blunt impacts remarkably well, though a powerful arrow will punch through.": 
        "一件由十几层绗缝亚麻布制成的厚实加厚夹克，里面塞满粗纤维并缝成垂直通道。这是中世纪最基本、最独立的护甲——从被征召的农民到骑士，每个人都戴着它作为锁甲下的基础层。厚实的衬垫能极好地吸收钝击冲击，虽然强力的箭矢仍会穿透它。",
        
    "A total conversion mod transforming Cataclysm into a medieval fantasy world.  Strips away all modern technology, firearms, electronics, and urban infrastructure, replacing them with medieval-era equivalents.": 
        "一个将大灾变完全转换为中世纪奇幻世界的整体转换Mod。剥离了所有现代科技、火器、电子设备和城市基础设施，代之以中世纪时期的等效物。",
        
    "A transitional coat of plates utilizing large curved scales of hardened leather instead of metal, riveted inside a heavy leather jacket.  Affords decent protection against cuts and thrusts, though it offers poor defense against heavy impacts and is highly vulnerable to fire.": 
        "一种过渡期的板甲衣，使用硬皮革制成的弧形大鳞片代替金属，铆接在重皮夹克内侧。提供针对劈砍和刺击的良好保护，虽然它对重击的防御力较差，且极易受到火灾伤害。",
        
    "A versatile two-handed sword with a long double-edged blade optimized for both cutting and thrusting.  The extended grip allows powerful two-handed swings, and the sharp point can find gaps in plate armor through half-swording technique.": 
        "一把多功能双手剑，配有针对劈砍和刺击进行优化的长双刃刃部。延长的剑柄允许进行强力的双手挥舞，且锋利的尖端可以通过半剑术在板甲中寻找缝隙。",
        
    "A vest-like armor made from thick, oil-cured leather panels stitched together at the sides.  Offers decent protection against cuts and minor impacts.  Commonly worn by militia and light infantry who cannot afford metal armor.": 
        "一种由结实的、油鞣皮革板在侧面缝合而成的背心状铠甲。提供针对劈砍和轻微撞击的良好保护。通常由负担不起金属护甲的民兵和轻步兵穿着。",
        
    "A wide-brimmed hat woven from dried straw, offering shade from the sun and a little shelter from light rain.  The universal headwear of peasants working the fields during the summer months.": 
        "一顶由干稻草编织而成的宽檐帽，可在夏日提供遮阳和防小雨的避所。是夏日月份在田间劳作的农民通用的头部佩戴物。",
        
    "A widely popular medieval dagger with a distinctive guard formed by two oval lobes — giving it its earthy name.  Carried by all social classes, from peasants to knights, as an everyday sidearm.  Balanced for both cutting and thrusting, reliable and unpretentious.": 
        "一种广受欢迎的中世纪匕首，带有由两个椭圆形瓣片组成的独特护手——赋予了它那个世俗的名字。由从农民到骑士的所有社会阶层作为日常副手携带。在劈砍和刺击之间取得了平衡，可靠且质朴。",
        
    "Abstract base class for brigandines.": "布里根丁甲的抽象基类。",
    "Abstract base class for coats of plates.": "板甲衣的抽象基类。",
    
    "An English infantry polearm with a broad curved hook-blade and a top spike.  The bill's hook is legendary — it can drag a mounted knight out of the saddle, pull shields aside, and trip fleeing enemies.  Less elegant than a halberd, but brutally effective.": 
        "一种配有宽大弯曲钩刃和顶刺的英格兰步兵长柄武器。勾镰的挂钩是传奇性的——它可以将马背上的骑士拉下马鞍，拉开防守的盾牌，并绊倒逃跑的敌人。虽然不如战戟优雅，但野蛮且极其有效。",
        
    "An advanced hybrid torso protection based on archaeological finds from Chalcis.  Integrates a solid steel breastplate split into two large plates over the upper chest for rigid defense, while the waist, lower abdomen and flanks are shielded by flexible overlapping scales.  The peak of transitional torso safety.": 
        "一种基于查尔基斯考古发现的先进混合躯干防护甲。在胸部上方集成了一个分裂为两块大板的实心钢胸甲以提供刚性防御，而腰部、下腹部和肋侧则由灵活的重叠鳞片保护。这是过渡期躯干防护的巅峰之作。",
        
    "An advanced mace with raised blade-like flanges radiating from the steel head.  The flanges concentrate the impact force into narrow ridges that tear into armor rather than just denting it, making this one of the most effective one-handed anti-armor weapons of the period.": 
        "一种先进的钉头锤，其钢制头部放射出凸起的叶片状法兰凸缘。叶片将冲击力集中在狭窄的脊部，撕裂护甲而不仅仅是使其凹陷，使其成为该时期最有效的单手反装甲武器之一。",
        
    "An early form of polearm with a curved single-edged blade mounted on a long shaft.  The crescent-like blade delivers arcing cuts from a safe distance.  An older design being phased out in favor of more versatile halberds and bills, but still lethal in the right hands.": 
        "一种早期的长柄武器，在长轴上安装有弯曲的单刃刀片。新月状的刀刃可从安全距离进行弧形劈砍。这是一种正在被更具多功能性的战戟和勾镰淘汰的旧设计，但在合适的手中仍极具杀伤力。",
        
    "An elegant polearm with a broad central spear blade flanked by smaller wing-blades at its base.  The wings can catch and deflect enemy weapons while the spear point does the work.  A weapon of guards, officers, and ceremonial use as much as the battlefield.": 
        "一种优雅的长柄武器，其宽大的中央枪尖两侧有较小的翼片。翼片可以在长枪尖发挥作用的同时抓住并偏转敌人的武器。既是一把用于仪仗的卫兵、军官武器，也是战场上的致命利器。",
        
    "An exceptionally heavy defensive garment designed for knightly shock combat.  It houses thick, massive steel plates over the chest, including an integrated lance rest on the right side to steady a lance on horseback.  Offers peerless protection against front impacts, though it is incredibly fatiguing to wear.": 
        "一种专为骑士近战冲锋设计的极重型防护装具。它在胸部覆盖着厚实沉重的钢板，包括右侧集成的枪托以在马背上稳定长枪。对正面撞击提供无可匹敌的保护，尽管穿着起来极其令人疲惫。",
        
    "An extremely long thrusting spear designed for massed infantry formations.  Devastating against cavalry charges and at range, but nearly useless if an enemy gets inside its reach.  The defining weapon of late medieval infantry tactics.": 
        "一种专为密集步兵方阵设计的极长型刺击长枪。对骑兵冲锋和远程范围具有毁灭性打击，但如果敌人进入其触及范围之内则几乎毫无用处。这是晚期中世纪步兵战术的决定性武器。",
        
    "Cuir Bouilli": "煮沸硬革",
    "Linen": "亚麻布",
    "Medieval": "中世纪",
    "Medieval Awakening": "中世纪苏醒",
    "Naked Wanderer": "赤裸流浪者",
    "Oilcloth": "防雨油布",
    
    "Originally a grain-threshing tool — two stout wooden rods connected by a short chain or leather hinge.  When swung, the striking rod whips around with tremendous force and can wrap over the top of a shield to strike the defender behind it.  The signature weapon of peasant revolts across medieval Europe.": 
        "最初是一种打谷物的农具——通过短铁链或皮革铰链连接的两根结实木棒。挥动时，打击棒以巨大的力量挥出，并能绕过盾牌顶部击中后方的防御者。这是整个中世纪欧洲农民起义的标志性武器。",
        
    "Quilted Linen": "绗缝亚麻/棉衬",
    
    "Simple linen bands wound around the wrists, secured by tucking the loose end under the last wrap.  Worn by craftsmen to keep sweat from dripping onto their work, and by archers to protect the bow-arm wrist from the string snap.  Almost no protective value, but better than nothing when the forge is hot.": 
        "缠绕在手腕上的简易亚麻带，通过将松散端塞入最后一次缠绕下来固定。由工匠佩戴以防止汗水滴在工作上，以及由弓箭手佩戴以保护拉弓手臂的手腕免受弓弦反弹的抽打。几乎没有防御价值，但当熔炉炎热时聊胜于无。",
        
    "Straw": "稻草麦秆",
    
    "Strips of woolen cloth wound tightly around the lower legs from ankle to knee, held in place by their own tension and the occasional pin or strap.  Wearing leg wraps — or 'winingas' in the old tongue — adds welcome warmth and keeps brambles and brush from snagging the hose underneath.  A common sight on hunters and peasants working rough ground.": 
        "紧紧缠绕在脚踝到膝盖下肢的羊毛布条，由自身的拉力和偶尔的别针或带子固定。佩戴绑腿——或者古语中的“winingas”——增加了令人喜悦的温暖，并防止荆棘和灌木钩破里面的长袜。在粗糙地面上工作的猎人和农民身上很常见。",
        
    "The 'mercy blade' — a long, thin dagger carried by knights specifically to deliver the killing blow to a downed armored opponent.  Its narrow blade can be guided precisely through visor slits, armpit gaps, and other weak points in plate armor.  The grim final word in armored combat.": 
        "“仁慈之刃”——骑士专门携带的一把长而细的匕首，用于对倒地的装甲对手致命一击。其狭窄的刃部可以精确地引导穿过面罩缝隙、腋下缝隙以及板甲的其他弱点。装甲战斗中严酷的终结象征。",
        
    "The iconic Swiss polearm — an axe blade for cleaving, a top spike for thrusting, and a back hook for dragging cavalry off their mounts.  A single weapon with an answer for every situation.  The backbone of disciplined infantry across Europe.": 
        "经典的瑞士长柄武器——用于劈砍的斧刃，用于刺击的顶刺，以及用于将骑兵拉下战马的背钩。一把能应对各种战况的多功能武器。是整个欧洲纪律严明步兵的支柱。",
        
    "The knight's polearm of choice for foot combat — an axe head on one side, a hammer on the other, and a top spike.  Designed to defeat plate armor with brutal efficiency: hammer to concuss, spike to pierce, axe to hook and control.  The complete anti-armor package.": 
        "骑士步战的首选长柄武器——一侧为斧头，另一侧为锤子，顶部装有尖刺。旨在以野蛮的效率击败板甲：锤子进行钝击震荡，尖刺进行穿刺，斧头进行勾勒和控制。全套反装甲方案。",
        
    "The pinnacle of crossbow technology — a steel-limbed monster requiring a mechanical windlass to span.  Each shot delivers staggering penetrating power, capable of punching through plate armor at considerable range.  Fires perhaps twice a minute, but against this weapon, even the finest Milanese plate becomes a gamble.": 
        "弩技术的巅峰之作——一头需要机械绞盘拉弦的钢臂巨兽。每次射击都提供了令人震惊的穿透力，能够在相当远的射程内洞穿板甲。每分钟可能仅能发射两次，但面对这种武器，即使是最好的米兰板甲也变成了一场豪赌。",
        
    "You awaken in an unfamiliar wilderness, with nothing but the clothes on your back.  The world around you is unfamiliar — medieval, untamed, and full of danger.  Every tool, every scrap of food, every weapon must be found or made by your own hands.": 
        "您在一片未知的荒野中醒来，身上只有破旧的衣物。周围的世界陌生野蛮，充满危机。在这片中世纪荒原上，每一件工具、每一口食物、每一把武器，都必须用您自己的双手去寻找或制作。",
        
    "You have nothing.  No skills, no tools, no weapons — not even the faintest memory of how you got here.  In this harsh medieval wilderness, your bare hands and wits are all you possess.": 
        "您一无所有。没有技能，没有工具，没有武器——甚至记不起自己是如何来到这里的。在这片荒凉残酷的中世纪荒野中，双手和智慧是您仅有的依靠。"
}

def apply_ai_translations():
    po_file = r"e:\Cataclysm-Medieval\data\mods\Medieval\lang\po\zh_CN.po"
    if not os.path.exists(po_file):
        print("PO file does not exist")
        return
        
    with open(po_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Standard header block pattern
    header_match = re.match(r'^(msgid ""\nmsgstr ""\n(?:".*"\n)+)\n', content)
    header = ""
    if header_match:
        header = header_match.group(1) + "\n"
        
    # Split entries
    entries = content.split("\n\n")
    updated_entries = []
    
    for entry in entries:
        if not entry.strip():
            continue
            
        # Parse msgid
        lines = entry.strip().split("\n")
        
        # Check if it's the header block
        if len(lines) > 0 and lines[0] == 'msgid ""' and lines[1] == 'msgstr ""':
            continue
            
        msgid_lines = []
        msgstr_lines = []
        in_msgid = False
        in_msgstr = False
        
        for line in lines:
            if line.startswith("msgid "):
                msgid_lines.append(line[6:].strip().strip('"'))
                in_msgid = True
                in_msgstr = False
            elif line.startswith("msgstr "):
                msgstr_lines.append(line[7:].strip().strip('"'))
                in_msgid = False
                in_msgstr = True
            elif line.startswith('"') and line.endswith('"'):
                val = line.strip().strip('"')
                if in_msgid:
                    msgid_lines.append(val)
                elif in_msgstr:
                    msgstr_lines.append(val)
                    
        msgid = "".join(msgid_lines).replace('\\\\', '\\').replace('\\"', '"')
        
        if msgid == "":
            continue
            
        # Run AI translation translation pass!
        if msgid in AI_FULL_LOCALIZATION:
            msgstr = AI_FULL_LOCALIZATION[msgid]
        else:
            msgstr = ""
            
        msgid_esc = msgid.replace('\\', '\\\\').replace('"', '\\"')
        msgstr_esc = msgstr.replace('\\', '\\\\').replace('"', '\\"')
        
        updated_entries.append(f'msgid "{msgid_esc}"\nmsgstr "{msgstr_esc}"')
        
    # Reassemble PO file
    with open(po_file, "w", encoding="utf-8") as f:
        if header:
            f.write(header)
        else:
            f.write('msgid ""\nmsgstr ""\n')
            f.write('"Project-Id-Version: Medieval Mod 1.0\\n"\n')
            f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
            f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
            f.write('"Language: zh_CN\\n"\n')
            f.write('"Language-Team: Cataclysm-Medieval team\\n"\n')
            f.write('"Plural-Forms: nplurals=1; plural=0;\\n"\n\n')
            
        for entry_str in sorted(updated_entries):
            f.write(entry_str + "\n\n")
            
    print(f"Successfully processed AI dynamically translated PO. Written {len(updated_entries)} translated entries directly to zh_CN.po.")

if __name__ == "__main__":
    apply_ai_translations()
