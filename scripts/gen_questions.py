#!/usr/bin/env python3
"""Build assets/bible.qus: keep existing rows, add unique trivia up to TARGET."""

from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

TARGET = 834

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "bible.qus"
OUT = SRC

# canon, kind, ref, question, correct, w1, w2, w3
Fact = tuple[int, int, str, str, str, str, str, str]


def norm(s: str) -> str:
    return " ".join(s.lower().split())


def facts() -> list[Fact]:
    f: list[Fact] = []

    def add(canon: int, kind: int, ref: str, q: str, correct: str, w1: str, w2: str, w3: str) -> None:
        f.append((canon, kind, ref, q, correct, w1, w2, w3))

    # --- Creation and Genesis ---
    days = [
        (1, "Light", "Gen. 1:3-5"),
        (2, "The firmament (sky)", "Gen. 1:6-8"),
        (3, "Dry land and plants", "Gen. 1:9-13"),
        (4, "The sun, moon, and stars", "Gen. 1:14-19"),
        (5, "Fish and birds", "Gen. 1:20-23"),
        (6, "Land animals and mankind", "Gen. 1:24-31"),
    ]
    others = [d[1] for d in days]
    for n, thing, ref in days:
        wr = [x for x in others if x != thing][:3]
        add(1, 1 if n <= 4 else 2, ref, f"What did God make on the {n}{'st' if n==1 else 'nd' if n==2 else 'rd' if n==3 else 'th'} day?", thing, wr[0], wr[1], wr[2])
    add(1, 1, "Gen. 1:1", "What did God create in the beginning?", "The heaven and the earth", "Only the angels", "The church", "The sun alone")
    add(1, 1, "Gen. 1:27", "In whose image did God create man?", "God's image", "The angels' image", "The animals' image", "His own imagination")
    add(1, 1, "Gen. 2:7", "From what did God form man?", "The dust of the ground", "Water", "Clay from a river", "A rib")
    add(1, 1, "Gen. 2:21-22", "From what did God make Eve?", "Adam's rib", "Dust", "Clay", "Light")
    add(1, 1, "Gen. 2:8", "Where did God put Adam?", "The garden of Eden", "Mount Sinai", "Canaan", "Ur")
    add(1, 1, "Gen. 3:1", "What animal tempted Eve?", "A serpent", "A lion", "A raven", "A fox")
    add(1, 1, "Gen. 3:6", "What did Eve eat that God had forbidden?", "Fruit of the tree of knowledge", "Manna", "Unleavened bread", "A golden apple")
    add(1, 2, "Gen. 3:20", "What does the name Eve mean, according to Genesis?", "Mother of all living", "Princess", "Life of God", "First woman")
    add(1, 2, "Gen. 3:24", "What guarded the way to the tree of life after the fall?", "Cherubim and a flaming sword", "A wall of fire", "An angel with a scroll", "A great flood")
    add(1, 1, "Gen. 4:8", "Who killed Abel?", "Cain", "Seth", "Ham", "Esau")
    add(1, 2, "Gen. 4:2", "What was Abel's occupation?", "A keeper of sheep", "A tiller of the ground", "A hunter", "A carpenter")
    add(1, 2, "Gen. 4:17", "Who built a city named Enoch?", "Cain", "Noah", "Nimrod", "Seth")
    add(1, 1, "Gen. 5:24", "Who walked with God and was not, for God took him?", "Enoch", "Elijah", "Moses", "Noah")
    add(1, 1, "Gen. 6:19", "How many of each kind of animal did Noah take on the ark (the general command)?", "Two", "Seven", "Twelve", "Forty")
    add(1, 2, "Gen. 7:13", "How many people boarded Noah's ark?", "8", "2", "12", "40")
    add(1, 1, "Gen. 7:12", "How many days and nights did rain fall in the flood?", "40", "7", "12", "120")
    add(1, 2, "Gen. 8:8-11", "What bird brought Noah an olive leaf?", "A dove", "A raven", "A sparrow", "An eagle")
    add(1, 1, "Gen. 9:13", "What token of the covenant did God set in the cloud?", "A rainbow", "A star", "A pillar of fire", "A dove")
    add(1, 2, "Gen. 11:4", "What were the people building at Babel?", "A tower", "A temple", "An ark", "A wall")
    add(1, 1, "Gen. 11:9", "Why was the place called Babel?", "The LORD confounded their language", "A king named Babel died there", "It means house of God", "They found gold")
    add(1, 1, "Gen. 12:1", "Who was called to leave his country for a land God would show him?", "Abram", "Noah", "Moses", "Jacob")
    add(1, 2, "Gen. 11:31", "From what city did Abram leave?", "Ur of the Chaldees", "Nineveh", "Damascus", "Jericho")
    add(1, 1, "Gen. 17:5", "What new name did God give Abram?", "Abraham", "Israel", "Paul", "Joshua")
    add(1, 2, "Gen. 17:15", "What new name did God give Sarai?", "Sarah", "Hannah", "Rachel", "Rebekah")
    add(1, 1, "Gen. 21:3", "Who was Abraham and Sarah's promised son?", "Isaac", "Ishmael", "Jacob", "Esau")
    add(1, 2, "Gen. 16:15", "Who was the son of Abraham and Hagar?", "Ishmael", "Isaac", "Lot", "Esau")
    add(1, 1, "Gen. 19:26", "What happened to Lot's wife when she looked back?", "She became a pillar of salt", "She was turned to stone", "She fell into the fire", "She went blind")
    add(1, 1, "Gen. 19:24", "Which cities did the LORD destroy with brimstone and fire?", "Sodom and Gomorrah", "Tyre and Sidon", "Nineveh and Babylon", "Jericho and Ai")
    add(1, 1, "Gen. 22:2", "Where did God tell Abraham to offer Isaac?", "The land of Moriah", "Mount Sinai", "Mount Carmel", "Bethel")
    add(1, 2, "Gen. 22:13", "What did Abraham offer instead of Isaac?", "A ram", "A lamb", "A dove", "A bullock")
    add(1, 1, "Gen. 24:67", "Who became Isaac's wife?", "Rebekah", "Rachel", "Leah", "Sarah")
    add(1, 1, "Gen. 25:26", "Who was Isaac's younger twin?", "Jacob", "Esau", "Joseph", "Benjamin")
    add(1, 1, "Gen. 25:34", "For what did Esau sell his birthright?", "A mess of pottage", "Silver", "A coat", "A field")
    add(1, 2, "Gen. 27:16", "How did Jacob disguise himself to get Isaac's blessing?", "Goat skins on his hands", "Esau's armor", "A painted face", "A borrowed beard")
    add(1, 1, "Gen. 28:12", "What did Jacob see in a dream at Bethel?", "A ladder to heaven", "A burning bush", "Four beasts", "A great fish")
    add(1, 2, "Gen. 32:28", "What new name was Jacob given after wrestling?", "Israel", "Abraham", "Judah", "Ephraim")
    add(1, 3, "Gen. 32:30", "What did Jacob call the place where he wrestled?", "Peniel", "Bethel", "Beersheba", "Mahanaim")
    add(1, 1, "Gen. 29:28", "Which sister did Jacob marry first?", "Leah", "Rachel", "Rebekah", "Bilhah")
    add(1, 1, "Gen. 37:3", "What did Jacob give Joseph that made his brothers jealous?", "A coat of many colours", "A gold ring", "A sword", "A flock of sheep")
    add(1, 2, "Gen. 37:28", "To whom did Joseph's brothers sell him?", "Ishmeelites", "Philistines", "Egyptians", "Amalekites")
    add(1, 1, "Gen. 39:20", "Where was Joseph put after Potiphar's wife accused him?", "Prison", "The army", "A pit in Canaan", "The tower of Babel")
    add(1, 1, "Gen. 41:29-30", "What did Joseph say Pharaoh's dreams meant?", "Seven years of plenty then seven of famine", "A coming flood", "War with Canaan", "The death of Pharaoh")
    add(1, 3, "Gen. 41:46", "How old was Joseph when he stood before Pharaoh?", "30", "17", "40", "110")
    add(1, 2, "Gen. 41:45", "What Egyptian name was Joseph given?", "Zaphnath-paaneah", "Potiphar", "On", "Rameses")
    add(1, 1, "Gen. 49:10", "Which son's line was promised the sceptre?", "Judah", "Reuben", "Joseph", "Levi")
    add(1, 3, "Gen. 50:26", "How old was Joseph when he died?", "110", "120", "147", "175")
    add(1, 2, "Gen. 50:25", "What did Joseph make the Israelites swear about his bones?", "To carry them out of Egypt", "To bury them in the Nile", "To build a pyramid", "To burn them")

    tribes = [
        "Reuben", "Simeon", "Levi", "Judah", "Dan", "Naphtali",
        "Gad", "Asher", "Issachar", "Zebulun", "Joseph", "Benjamin",
    ]
    not_tribes = ["Caleb", "Enoch", "Noah", "Job", "Boaz", "Gideon"]
    for i, t in enumerate(tribes):
        wr = [x for x in not_tribes]
        add(1, 2 if i > 5 else 1, "Gen. 49", f"Which of these was a son of Jacob?", t, wr[i % 3], wr[(i + 1) % 3], wr[(i + 2) % 3])
    add(1, 3, "Gen. 35:18", "What did Rachel name her younger son before she died (before Jacob renamed him Benjamin)?", "Ben-oni", "Ben-ammi", "Ichabod", "Gershom")

    # --- Exodus–Deuteronomy ---
    add(2, 1, "Ex. 1:8", "What changed for Israel in Egypt after Joseph died?", "A new king who knew not Joseph", "The Nile dried up", "They returned to Canaan", "They became priests")
    add(2, 1, "Ex. 2:3", "In what did Moses' mother hide him?", "An ark of bulrushes", "A cave", "A basket of gold", "A manger")
    add(2, 2, "Ex. 6:20", "Who was Moses' mother?", "Jochebed", "Miriam", "Hannah", "Zipporah")
    add(2, 1, "Ex. 2:21", "Who became Moses' wife in Midian?", "Zipporah", "Miriam", "Rachel", "Asenath")
    add(2, 1, "Ex. 3:2", "How did God appear to Moses at Horeb?", "A burning bush", "A still small voice", "A pillar of cloud", "A dream of a ladder")
    add(2, 2, "Ex. 3:14", "What name did God give Moses at the bush?", "I AM THAT I AM", "Jehovah-jireh", "El Shaddai", "The Ancient of Days")
    add(2, 1, "Ex. 4:14", "Who was Moses' spokesman?", "Aaron", "Joshua", "Hur", "Caleb")
    add(2, 2, "Ex. 7:1", "What role did Aaron serve for Moses before Pharaoh?", "His prophet / spokesman", "His general", "His scribe", "His judge")
    plagues = [
        (1, "Water turned to blood", "Ex. 7:20"),
        (2, "Frogs", "Ex. 8:6"),
        (3, "Lice", "Ex. 8:17"),
        (4, "Flies", "Ex. 8:24"),
        (5, "Disease of livestock", "Ex. 9:6"),
        (6, "Boils", "Ex. 9:10"),
        (7, "Hail", "Ex. 9:23"),
        (8, "Locusts", "Ex. 10:13"),
        (9, "Darkness", "Ex. 10:22"),
        (10, "Death of the firstborn", "Ex. 12:29"),
    ]
    pnames = [p[1] for p in plagues]
    for n, name, ref in plagues:
        wr = [x for x in pnames if x != name][:3]
        add(2, 1 if n in (1, 9, 10) else 2, ref, f"What was plague number {n} in Egypt?", name, wr[0], wr[1], wr[2])
    add(2, 1, "Ex. 12:7", "What did Israel put on the doorposts at Passover?", "The blood of a lamb", "Oil", "Hyssop only", "A mark of ink")
    add(2, 1, "Ex. 14:21", "What sea did the LORD divide for Israel?", "The Red Sea", "The Dead Sea", "The Sea of Galilee", "The Mediterranean")
    add(2, 1, "Ex. 16:15", "What food did God send in the wilderness?", "Manna", "Olives", "Fish", "Unleavened cakes only")
    add(2, 2, "Ex. 16:13", "What birds did God send for meat?", "Quails", "Ravens", "Doves", "Eagles")
    add(2, 1, "Ex. 20:3", "What is the first of the ten commandments?", "Thou shalt have no other gods before me", "Remember the sabbath", "Honour thy father and mother", "Thou shalt not steal")
    add(2, 1, "Ex. 20:13", "Which commandment says, 'Thou shalt not kill'?", "The sixth", "The first", "The tenth", "The third")
    add(2, 2, "Ex. 20:15", "Which commandment forbids stealing?", "The eighth", "The fifth", "The ninth", "The second")
    add(2, 2, "Ex. 20:14", "Which commandment forbids adultery?", "The seventh", "The sixth", "The fourth", "The tenth")
    add(2, 2, "Ex. 20:17", "Which commandment forbids coveting?", "The tenth", "The first", "The eighth", "The third")
    add(2, 1, "Ex. 20:8", "Which day did God command Israel to keep holy?", "The sabbath", "The first day", "The new moon", "Passover only")
    add(2, 1, "Ex. 32:4", "What did Aaron make while Moses was on the mount?", "A golden calf", "A bronze serpent", "An altar of twelve stones", "The ark")
    add(2, 2, "Ex. 31:18", "On what were the ten commandments written?", "Two tables of stone", "A scroll of papyrus", "Gold plates", "A clay tablet")
    add(2, 3, "Ex. 25:10", "Of what wood was the ark of the covenant made?", "Shittim (acacia) wood", "Gopher wood", "Cedar", "Oak")
    add(2, 3, "Ex. 28:1", "Who was the first high priest of Israel?", "Aaron", "Moses", "Levi", "Eleazar")
    add(2, 2, "Ex. 15:20", "Who led the women in song after the Red Sea?", "Miriam", "Deborah", "Hannah", "Zipporah")
    add(2, 4, "Ex. 17:12", "Who held up Moses' hands in the fight with Amalek (with Aaron)?", "Hur", "Joshua", "Caleb", "Nadab")
    add(3, 2, "Lev. 16:8", "On the day of atonement, one goat was for the LORD. What was the other called?", "The scapegoat", "The passover goat", "The Nazarite goat", "The peace goat")
    add(3, 1, "Lev. 11:7", "Which animal is listed as unclean because it divides the hoof but does not chew the cud?", "The swine", "The ox", "The sheep", "The goat")
    add(3, 3, "Lev. 17:11", "What does Leviticus say makes atonement for the soul?", "The blood", "Fine flour", "Incense", "Water")
    add(3, 2, "Lev. 23:5", "On what day of the first month is the LORD's passover?", "The fourteenth", "The first", "The seventh", "The tenth")
    add(3, 3, "Lev. 25:10", "How often was the jubile to be proclaimed?", "Every 50th year", "Every 7th year", "Every 12th year", "Every 40th year")
    add(3, 4, "Lev. 10:1-2", "Which sons of Aaron died for offering strange fire?", "Nadab and Abihu", "Eleazar and Ithamar", "Hophni and Phinehas", "Gershom and Eliezer")
    add(4, 1, "Num. 13:30", "Which spy said, 'Let us go up at once, and possess it'?", "Caleb", "Joshua only", "Korah", "Balaam")
    add(4, 1, "Num. 14:6", "Which two spies brought a good report?", "Joshua and Caleb", "Aaron and Hur", "Nadab and Abihu", "Eldad and Medad")
    add(4, 1, "Num. 14:34", "How many years did Israel wander for the ten spies' evil report?", "40", "12", "7", "70")
    add(4, 2, "Num. 16:32", "What happened to Korah's company?", "The earth swallowed them", "Fire from heaven only", "They were stoned", "They fled to Egypt")
    add(4, 2, "Num. 20:11", "How did Moses bring water from the rock at Meribah (the second time)?", "He smote the rock twice", "He spoke to it only", "He stretched his rod over the sea", "He dug a well")
    add(4, 3, "Num. 21:8-9", "What did Moses make for the people bitten by serpents?", "A serpent of brass", "A golden calf", "An ephod", "A pot of manna")
    add(4, 2, "Num. 22:28", "What animal spoke to Balaam?", "An ass", "A serpent", "A ram", "A dove")
    add(4, 3, "Num. 6:2-5", "What vow included not cutting one's hair?", "The vow of a Nazarite", "The vow of a priest", "The vow of a judge", "The vow of a king")
    add(4, 4, "Num. 25:7-8", "Who stopped the plague at Peor by slaying Zimri and Cozbi?", "Phinehas", "Joshua", "Caleb", "Eleazar")
    add(4, 3, "Num. 27:18", "Whom did God choose to succeed Moses?", "Joshua", "Caleb", "Aaron", "Eleazar")
    add(5, 1, "Deut. 6:4", "What is the first word of the Shema: 'Hear, O Israel: The LORD our God is one LORD'?", "Hear", "Love", "Fear", "Remember")
    add(5, 1, "Deut. 6:5", "How are we to love the LORD according to Deuteronomy 6?", "With all thine heart, soul, and might", "With tithes only", "With burnt offerings", "With silence")
    add(5, 2, "Deut. 34:5-6", "Where did Moses die?", "In the land of Moab", "On Mount Sinai", "In Canaan", "In Egypt")
    add(5, 2, "Deut. 34:7", "How old was Moses when he died?", "120", "110", "137", "80")
    add(5, 3, "Deut. 34:1", "From what mountain did Moses view the promised land?", "Nebo (Pisgah)", "Sinai", "Carmel", "Zion")
    add(5, 3, "Deut. 18:15", "Whom did Moses say the LORD would raise up like unto him?", "A Prophet", "A king", "A priest only", "A judge")
    add(5, 1, "Deut. 5:16", "Which commandment has a promise of long life in the land?", "Honour thy father and thy mother", "Keep the sabbath", "Do not steal", "Do not covet")
    add(5, 4, "Deut. 25:4", "What does Deuteronomy say you shall not muzzle?", "The ox when he treadeth out the corn", "The ass", "The horse of a king", "The camel")

    # --- Joshua–Esther ---
    add(6, 1, "Josh. 3:17", "What river did Israel cross on dry ground into Canaan?", "Jordan", "Nile", "Euphrates", "Kishon")
    add(6, 1, "Josh. 6:20", "How did the walls of Jericho fall?", "The people shouted after circling the city", "They tunneled under", "Lightning struck them", "An earthquake only")
    add(6, 2, "Josh. 2:1", "Which woman hid the spies in Jericho?", "Rahab", "Ruth", "Deborah", "Jael")
    add(6, 2, "Josh. 2:18", "What color was the line Rahab was to bind in the window?", "Scarlet", "Blue", "Purple", "White")
    add(6, 2, "Josh. 7:1", "Who took of the accursed thing at Jericho?", "Achan", "Caleb", "Ahiman", "Phinehas")
    add(6, 3, "Josh. 10:13", "What stood still at Joshua's word?", "The sun", "The Jordan", "The moon only", "The wind")
    add(6, 3, "Josh. 14:13", "What city did Joshua give Caleb?", "Hebron", "Jericho", "Ai", "Gibeon")
    add(6, 4, "Josh. 24:15", "Finish: 'as for me and my house, we will ___'", "serve the LORD", "keep the law", "build a temple", "return to Egypt")
    add(7, 1, "Judg. 4:4", "Who was the prophetess who judged Israel?", "Deborah", "Miriam", "Huldah", "Anna")
    add(7, 2, "Judg. 4:21", "Who killed Sisera with a tent peg?", "Jael", "Deborah", "Ruth", "Delilah")
    add(7, 1, "Judg. 6:37", "What sign did Gideon ask with a fleece?", "Dew on the fleece only", "Fire from heaven", "A rainbow", "A talking donkey")
    add(7, 1, "Judg. 7:7", "With how many men did Gideon defeat Midian?", "300", "3000", "32,000", "700")
    add(7, 2, "Judg. 7:16", "What did Gideon's men carry besides trumpets?", "Lamps in pitchers", "Spears", "Slings", "Bows")
    add(7, 1, "Judg. 16:19", "Who cut Samson's hair?", "Delilah", "a Philistine soldier", "his mother", "a priest")
    add(7, 2, "Judg. 13:5", "What vow was Samson under from the womb?", "A Nazarite", "A priest", "A judge's oath", "A Nazirite of 7 days")
    add(7, 3, "Judg. 15:4", "How many foxes did Samson catch?", "300", "30", "3", "3000")
    add(7, 3, "Judg. 16:3", "What did Samson carry to the top of a hill before Hebron?", "The doors of Gaza's gate", "The ark", "Goliath's sword", "A millstone")
    add(7, 2, "Judg. 16:30", "Where did Samson die?", "The temple of Dagon", "A cave at Etam", "Jerusalem", "Hebron")
    add(7, 4, "Judg. 11:31", "What rash vow is Jephthah remembered for?", "To offer whatever came out of his house", "To shave his head", "To never drink wine", "To spare no Canaanite")
    add(7, 3, "Judg. 3:15", "Which left-handed judge killed Eglon?", "Ehud", "Shamgar", "Othniel", "Tola")
    add(7, 4, "Judg. 3:31", "Who slew 600 Philistines with an ox goad?", "Shamgar", "Samson", "Gideon", "Ehud")
    add(8, 1, "Ruth 1:16", "Who said, 'whither thou goest, I will go'?", "Ruth", "Naomi", "Orpah", "Hannah")
    add(8, 1, "Ruth 1:4", "From what country was Ruth?", "Moab", "Edom", "Egypt", "Philistia")
    add(8, 2, "Ruth 2:1", "Who was the kinsman who married Ruth?", "Boaz", "Elimelech", "Mahlon", "Chilion")
    add(8, 2, "Ruth 1:20", "What name did Naomi ask to be called?", "Mara", "Hannah", "Sarah", "Keturah")
    add(8, 3, "Ruth 4:17", "Who was Ruth's son, the grandfather of David?", "Obed", "Jesse", "Salmon", "Perez")
    add(8, 3, "Ruth 1:2", "What was Naomi's husband named?", "Elimelech", "Boaz", "Jesse", "Othniel")
    add(9, 1, "1 Sam. 1:20", "Who was Samuel's mother?", "Hannah", "Peninnah", "Naomi", "Deborah")
    add(9, 1, "1 Sam. 3:10", "Who called Samuel in the night?", "The LORD", "Eli", "An angel named Gabriel", "His mother")
    add(9, 2, "1 Sam. 4:21", "What name means 'the glory is departed'?", "Ichabod", "Nabal", "Ichabod's brother", "Jabez")
    add(9, 1, "1 Sam. 9:2", "Who was Israel's first king?", "Saul", "David", "Solomon", "Samuel")
    add(9, 2, "1 Sam. 9:3", "What was Saul looking for when he met Samuel?", "His father's asses", "A lost sheep", "A wife", "The ark")
    add(9, 1, "1 Sam. 16:13", "Whom did Samuel anoint in Jesse's house?", "David", "Eliab", "Saul", "Jonathan")
    add(9, 1, "1 Sam. 17:49", "With what did David kill Goliath?", "A sling and a stone", "A spear", "Saul's sword", "A jawbone")
    add(9, 2, "1 Sam. 17:4", "Of what city was Goliath?", "Gath", "Gaza", "Ashkelon", "Ekron")
    add(9, 3, "1 Sam. 17:4", "How tall was Goliath?", "Six cubits and a span", "Nine cubits", "Four cubits", "Ten cubits")
    add(9, 2, "1 Sam. 17:40", "How many smooth stones did David choose?", "5", "3", "7", "12")
    add(9, 1, "1 Sam. 18:1", "Who loved David as his own soul?", "Jonathan", "Saul", "Abner", "Joab")
    add(9, 3, "1 Sam. 25:3", "Who was the foolish man whose wife was Abigail?", "Nabal", "Ner", "Kish", "Doeg")
    add(9, 4, "1 Sam. 28:7", "Where did Saul seek a woman with a familiar spirit?", "Endor", "Bethel", "Shiloh", "Ramah")
    add(10, 1, "2 Sam. 5:3", "Where was David anointed king over all Israel?", "Hebron", "Bethlehem", "Jerusalem", "Gibeah")
    add(10, 1, "2 Sam. 6:6-7", "Who died for touching the ark?", "Uzzah", "Ahio", "Obed-edom", "Asahel")
    add(10, 2, "2 Sam. 11:3", "Whom did David take, the wife of Uriah?", "Bathsheba", "Abigail", "Michal", "Ahinoam")
    add(10, 2, "2 Sam. 12:7", "Who said to David, 'Thou art the man'?", "Nathan", "Samuel", "Gad", "Ahithophel")
    add(10, 3, "2 Sam. 18:9", "How did Absalom die?", "His head caught in an oak, then Joab slew him", "He fell on his own sword", "He was stoned", "He drowned in Jordan")
    add(10, 3, "2 Sam. 21:17", "What did men call David after he waxed faint in battle?", "The light of Israel", "The lion of Judah", "The sweet psalmist only", "The giant-killer")
    add(10, 4, "2 Sam. 23:8", "What were David's elite warriors called?", "The mighty men", "The Cherethites only", "The 300", "The sons of thunder")
    add(11, 1, "1 Ki. 3:9", "What did Solomon ask of God?", "An understanding heart", "Long life", "Riches", "The death of his enemies")
    add(11, 1, "1 Ki. 6:1", "What did Solomon build in Jerusalem?", "The temple", "The tower of David", "A pyramid", "The second wall")
    add(11, 2, "1 Ki. 6:38", "How many years was the temple in building?", "7", "3", "12", "40")
    add(11, 2, "1 Ki. 11:3", "How many wives did Solomon have?", "700", "70", "300", "12")
    add(11, 1, "1 Ki. 18:38", "What happened at Elijah's altar on Carmel?", "Fire of the LORD fell", "Rain immediately", "An earthquake", "The sea split")
    add(11, 2, "1 Ki. 17:6", "What fed Elijah by the brook Cherith?", "Ravens", "Doves", "Angels with bread", "A widow daily")
    add(11, 2, "1 Ki. 17:9", "To which city was Elijah sent to a widow?", "Zarephath", "Jericho", "Shunem", "Nineveh")
    add(11, 3, "1 Ki. 18:19", "How many prophets of Baal did Elijah face on Carmel?", "450", "400", "70", "12")
    add(11, 3, "1 Ki. 19:12", "After the fire, what did Elijah hear?", "A still small voice", "Thunder", "A trumpet", "Nothing")
    add(11, 1, "1 Ki. 21:1-16", "Whose vineyard did Ahab covet?", "Naboth's", "Naboth's neighbor's", "Elijah's", "Jezebel's")
    add(11, 2, "1 Ki. 16:31", "Who was Ahab's wife?", "Jezebel", "Athaliah", "Maacah", "Michal")
    add(11, 4, "1 Ki. 10:1", "Which queen came to prove Solomon with hard questions?", "The queen of Sheba", "The queen of Egypt", "Jezebel", "Candace")
    add(12, 1, "2 Ki. 2:11", "How was Elijah taken up?", "A chariot of fire and horses of fire", "He walked with God and was not", "He died on Nebo", "He was translated in his bed")
    add(12, 2, "2 Ki. 2:13", "What of Elijah's fell to Elisha?", "His mantle", "His staff", "His cruse of oil", "His sandals")
    add(12, 1, "2 Ki. 5:14", "How many times did Naaman dip in Jordan?", "7", "3", "12", "40")
    add(12, 2, "2 Ki. 5:1", "What was Naaman's disease?", "Leprosy", "Blindness", "Palsy", "Boils")
    add(12, 3, "2 Ki. 6:5-6", "What miracle did Elisha do for a borrowed axe?", "He made the iron swim", "He multiplied oil", "He raised a child", "He called fire")
    add(12, 3, "2 Ki. 4:1-7", "What did Elisha multiply for a widow?", "Oil", "Meal", "Wine", "Bread")
    add(12, 2, "2 Ki. 20:6", "How many years were added to Hezekiah's life?", "15", "10", "7", "40")
    add(12, 3, "2 Ki. 20:11", "What sign was given Hezekiah?", "The shadow returned ten degrees", "A rainbow", "A wet fleece", "Fire on the altar")
    add(12, 2, "2 Ki. 22:8", "What did Hilkiah find in the house of the LORD?", "The book of the law", "The ark", "Goliath's sword", "Manna")
    add(12, 1, "2 Ki. 22:1", "Which boy-king repaired the temple and found the law?", "Josiah", "Joash", "Manasseh", "Ahaz")
    add(12, 4, "2 Ki. 2:23-24", "What came out of the wood and tare the children who mocked Elisha?", "Two she bears", "Lions", "Wolves", "Serpents")
    add(13, 2, "1 Chr. 16:4", "Who appointed Levites to thank and praise the LORD?", "David", "Solomon", "Samuel", "Moses")
    add(13, 3, "1 Chr. 21:1", "Who provoked David to number Israel, according to Chronicles?", "Satan", "Joab", "Nathan", "A prophet of Baal")
    add(13, 2, "1 Chr. 29:28", "How is David's death described?", "He died in a good old age, full of days, riches, and honour", "He fell in battle", "He was murdered", "He was taken in a chariot")
    add(14, 2, "2 Chr. 7:14", "If my people, which are called by my name, shall humble themselves, and pray... what will God do?", "Hear, forgive, and heal their land", "Send a king", "End the world", "Give them manna")
    add(14, 3, "2 Chr. 20:21", "What did Jehoshaphat put in the front of the army?", "Singers", "Chariots", "Archers", "Priests with trumpets only")
    add(14, 4, "2 Chr. 26:16-21", "What happened when Uzziah burned incense?", "He was smitten with leprosy", "Fire consumed him", "The earth swallowed him", "He became mute")
    add(15, 2, "Ezra 1:1", "Which king let the Jews return to build the house of the LORD?", "Cyrus", "Nebuchadnezzar", "Darius the Mede only", "Ahasuerus")
    add(15, 2, "Ezra 7:6", "What was Ezra?", "A ready scribe in the law of Moses", "A cupbearer", "A shepherd", "A soldier")
    add(15, 3, "Ezra 3:12", "Why did many old men weep when the foundation of the temple was laid?", "They had seen the first house", "They feared Persia", "They had no music", "Rain fell")
    add(16, 1, "Neh. 1:11", "What office did Nehemiah hold in Persia?", "The king's cupbearer", "Scribe", "Governor of Egypt", "Captain of the guard")
    add(16, 2, "Neh. 2:17", "What did Nehemiah rebuild?", "The wall of Jerusalem", "The temple", "Solomon's palace", "Jericho")
    add(16, 3, "Neh. 6:15", "In how many days was the wall finished?", "52", "7", "40", "70")
    add(16, 3, "Neh. 8:4", "Who stood with Ezra when he read the law?", "Other Levites / leaders", "Nehemiah only", "The king", "No one")
    add(17, 1, "Est. 2:17", "Who became queen instead of Vashti?", "Esther", "Ruth", "Bathsheba", "Jezebel")
    add(17, 2, "Est. 2:7", "What was Esther's Hebrew name?", "Hadassah", "Miriam", "Hannah", "Abigail")
    add(17, 1, "Est. 3:1", "Who plotted to destroy the Jews?", "Haman", "Mordecai", "Ahasuerus", "Sanballat")
    add(17, 2, "Est. 2:5", "Who raised Esther?", "Mordecai", "Haman", "Hegai", "Daniel")
    add(17, 3, "Est. 7:10", "On what was Haman hanged?", "The gallows he built for Mordecai", "A tree in Shushan", "A cross", "The city wall")
    add(17, 2, "Est. 9:26", "What feast remembers this deliverance?", "Purim", "Passover", "Hanukkah", "Tabernacles")
    add(17, 4, "Est. 8:9", "Which verse is often called the longest in the Bible?", "Esther 8:9", "Psalm 119:1", "John 11:35", "Genesis 1:1")

    # --- Wisdom and major prophets ---
    add(18, 1, "Job 1:1", "Where did Job live?", "The land of Uz", "Uz of the Chaldees", "Nineveh", "Teman only")
    add(18, 1, "Job 1:8", "How did the LORD describe Job?", "A perfect and an upright man", "A mighty hunter", "A king", "A priest")
    add(18, 2, "Job 1:2", "How many children did Job have at first?", "Seven sons and three daughters", "Twelve sons", "Three sons and seven daughters", "Ten sons")
    add(18, 2, "Job 2:7", "With what did Satan smite Job?", "Boils", "Blindness", "Leprosy as snow", "Palsy")
    add(18, 2, "Job 2:9", "What did Job's wife tell him to do?", "Curse God, and die", "Flee to Uz", "Offer a ram", "Call his friends")
    add(18, 3, "Job 42:16", "How many years did Job live after his trial?", "140", "120", "70", "40")
    add(18, 3, "Job 38:1", "From what did the LORD answer Job?", "The whirlwind", "A still small voice", "A burning bush", "A dream")
    add(18, 1, "Job 19:25", "What did Job say he knew?", "That his redeemer liveth", "That he would die at dawn", "That God had forgotten him", "That his friends were right")
    add(19, 1, "Ps. 23:1", "Who is the shepherd in Psalm 23?", "The LORD", "David", "Moses", "An angel")
    add(19, 1, "Ps. 23:4", "Through what valley does the psalmist walk?", "The valley of the shadow of death", "The valley of dry bones", "The Kidron", "The valley of Achor")
    add(19, 1, "Ps. 51:1", "After what sin did David write Psalm 51 (the title)?", "His sin with Bathsheba / Nathan's rebuke", "Numbering Israel", "Killing Goliath", "Fleeing Saul")
    add(19, 2, "Ps. 119", "What is the longest chapter in the Bible?", "Psalm 119", "Psalm 23", "Isaiah 53", "Matthew 1")
    add(19, 2, "Ps. 117", "What is the shortest chapter in the Bible?", "Psalm 117", "Psalm 1", "Obadiah 1", "John 11")
    add(19, 2, "Ps. 150:6", "How does the last psalm end its call?", "Let every thing that hath breath praise the LORD", "Selah", "Amen and amen", "The LORD is my shepherd")
    add(19, 3, "Ps. 90 (title)", "Which psalm is a prayer of Moses?", "Psalm 90", "Psalm 23", "Psalm 51", "Psalm 1")
    add(19, 1, "Ps. 1:1", "What is the first word of the book of Psalms?", "Blessed", "Praise", "Hear", "The")
    add(19, 3, "Ps. 22:1", "Which psalm begins, 'My God, my God, why hast thou forsaken me'?", "Psalm 22", "Psalm 23", "Psalm 51", "Psalm 2")
    add(19, 4, "Ps. 90:10", "What span of years does Psalm 90 give as the days of our years?", "Threescore years and ten", "Forty years", "A hundred and twenty", "Three score and sixteen")
    add(20, 1, "Prov. 1:7", "What is the beginning of knowledge?", "The fear of the LORD", "Much study", "Gold", "The law of Moses only")
    add(20, 1, "Prov. 3:5", "Trust in the LORD with all thine heart; and lean not unto thine own ___", "understanding", "strength", "riches", "friends")
    add(20, 2, "Prov. 15:1", "What turns away wrath?", "A soft answer", "A gift", "Silence always", "A sword")
    add(20, 2, "Prov. 22:6", "Train up a child in the way he should go: and when he is old, he will not ___", "depart from it", "forget his father", "need the law", "fear God")
    add(20, 3, "Prov. 31:10", "Who is described as more precious than rubies?", "A virtuous woman", "A king", "A wise son", "A faithful friend")
    add(20, 1, "Prov. 9:10", "The fear of the LORD is the beginning of ___", "wisdom", "knowledge only", "wealth", "power")
    add(21, 1, "Eccl. 1:2", "What word does Ecclesiastes repeat about earthly things?", "Vanity", "Glory", "Hope", "Peace")
    add(21, 2, "Eccl. 3:1", "To every thing there is a season, and a time to every ___", "purpose under the heaven", "man", "king", "nation")
    add(21, 3, "Eccl. 12:13", "What is the conclusion of the whole matter?", "Fear God, and keep his commandments", "Eat, drink, and be merry", "Get wisdom", "Remember thy youth")
    add(22, 2, "Song 2:1", "What flower does the beloved compare herself to?", "The rose of Sharon / lily of the valleys", "The cedar of Lebanon", "The olive", "The hyssop")
    add(22, 3, "Song 1:1", "Whose song is the Song of Songs called?", "Solomon's", "David's", "Moses'", "Asaph's")
    add(23, 1, "Is. 7:14", "What name would a virgin's son be called, according to Isaiah?", "Immanuel", "Jesus", "Maher-shalal-hash-baz only", "Wonderful only")
    add(23, 1, "Is. 9:6", "For unto us a child is born, unto us a son is given: and the government shall be upon his ___", "shoulder", "head", "throne", "right hand")
    add(23, 1, "Is. 53:5", "With whose stripes are we healed, in Isaiah 53?", "His (the servant's)", "Isaiah's", "Israel's", "David's")
    add(23, 2, "Is. 6:1", "In what year did Isaiah see the LORD high and lifted up?", "The year king Uzziah died", "The year of jubile", "Hezekiah's 15th year", "The exile")
    add(23, 2, "Is. 6:3", "What did the seraphim cry?", "Holy, holy, holy, is the LORD of hosts", "Worthy is the Lamb", "Glory to God in the highest", "Hear, O Israel")
    add(23, 3, "Is. 40:31", "They that wait upon the LORD shall renew their strength; they shall mount up with wings as ___", "eagles", "doves", "cherubim", "ravens")
    add(23, 3, "Is. 11:6", "What shall dwell with the lamb in Isaiah's peaceable kingdom?", "The wolf", "The lion only", "The serpent", "The bear only")
    add(23, 4, "Is. 14:12", "What fallen one is addressed as Lucifer, son of the morning?", "The king of Babylon (in the taunt)", "Pharaoh", "Goliath", "Cain")
    add(24, 1, "Jer. 1:5", "When did God say he knew Jeremiah?", "Before he formed him in the belly", "At his circumcision", "When he was 30", "At the temple")
    add(24, 2, "Jer. 38:6", "Where was Jeremiah cast?", "A dungeon / cistern", "A lion's den", "A furnace", "The sea")
    add(24, 2, "Jer. 29:11", "I know the thoughts that I think toward you, saith the LORD, thoughts of peace, and not of ___", "evil", "judgment only", "exile", "wrath only")
    add(24, 3, "Jer. 36:23", "What did king Jehoiakim do to Jeremiah's scroll?", "He cut it and burned it", "He hid it", "He read it and rent his clothes", "He sent it to Babylon")
    add(24, 3, "Jer. 32:7-15", "What did Jeremiah buy as a sign of hope?", "A field", "A donkey", "Gold from Egypt", "The temple vessels")
    add(25, 2, "Lam. 3:22-23", "How often are God's mercies said to be new?", "Every morning", "Every sabbath", "Every year", "Every jubile")
    add(25, 3, "Lam. 1:1", "What city does Lamentations weep over?", "Jerusalem", "Babylon", "Nineveh", "Samaria")
    add(26, 2, "Ez. 37:1-10", "What did Ezekiel see in the valley?", "Dry bones that lived", "Four beasts", "A ladder", "A great image")
    add(26, 3, "Ez. 1:5-10", "What four faces did the living creatures have?", "Man, lion, ox, eagle", "Man, ox, camel, dove", "Lion, bear, leopard, beast", "Cherub, seraph, man, ox")
    add(26, 2, "Ez. 3:17", "What did God make Ezekiel to the house of Israel?", "A watchman", "A king", "A priest in the temple", "A shepherd in Judah")
    add(26, 4, "Ez. 4:4-6", "How long did Ezekiel lie on his left side for Israel?", "390 days", "40 days", "70 days", "7 days")
    add(27, 1, "Dan. 1:7", "What Babylonian name was given to Daniel?", "Belteshazzar", "Shadrach", "Abednego", "Zerubbabel")
    add(27, 1, "Dan. 3:26", "Who walked in the fiery furnace with the three Hebrews?", "One like the Son of God", "An angel named Michael only", "Daniel", "Nebuchadnezzar")
    add(27, 1, "Dan. 6:22", "Who shut the lions' mouths?", "God / his angel", "Daniel's friends", "Darius", "Cyrus")
    add(27, 2, "Dan. 1:8", "What did Daniel purpose not to do?", "Defile himself with the king's meat", "Pray toward Jerusalem", "Serve in the court", "Learn the tongue of Chaldea")
    add(27, 2, "Dan. 2:32-33", "What were the metals of the great image, from the head down?", "Gold, silver, brass, iron (and clay)", "Gold only", "Iron, brass, silver, gold", "Silver, gold, clay, iron")
    add(27, 2, "Dan. 5:5", "What appeared at Belshazzar's feast?", "A hand writing on the wall", "A fiery furnace", "Four beasts", "A ram and a goat")
    add(27, 3, "Dan. 5:25", "What words were written on the wall?", "MENE, MENE, TEKEL, UPHARSIN", "ICHABOD", "HOLY, HOLY, HOLY", "JESUS OF NAZARETH")
    add(27, 3, "Dan. 3:12", "What Hebrew names did Shadrach, Meshach, and Abednego have?", "Hananiah, Mishael, and Azariah", "Joel, Amos, and Obadiah", "Peter, James, and John", "Hophni, Phinehas, and Ichabod")
    add(27, 4, "Dan. 9:24", "How many weeks are determined upon Daniel's people in the seventy-weeks prophecy?", "Seventy weeks", "Seven weeks", "Seventy years", "Four hundred ninety days only")

    # --- Minor prophets ---
    add(28, 2, "Hos. 1:2", "Whom was Hosea told to take as a wife?", "A wife of whoredoms (Gomer)", "A Moabitess", "A prophetess named Deborah", "A widow of Zarephath")
    add(28, 3, "Hos. 6:6", "I desired mercy, and not ___", "sacrifice", "prayer", "tithes", "fasting")
    add(29, 2, "Joel 2:28", "I will pour out my spirit upon all flesh: and your sons and your daughters shall ___", "prophesy", "sing", "go to war", "keep silence")
    add(29, 3, "Joel 1:4", "What disaster does Joel describe with palmerworm and locust?", "A locust plague", "A flood", "An exile", "A drought of three years only")
    add(30, 2, "Amos 1:1", "What was Amos besides a prophet?", "A herdsman of Tekoa", "A priest", "A scribe", "A king")
    add(30, 3, "Amos 7:14", "Amos said he was no prophet, neither a prophet's son, but a herdsman and a ___", "gatherer of sycomore fruit", "smith", "fisherman", "tentmaker")
    add(31, 3, "Obad. 1:1", "Against what nation is Obadiah's vision?", "Edom", "Moab", "Assyria", "Egypt")
    add(32, 1, "Jon. 1:17", "How long was Jonah in the fish?", "Three days and three nights", "Seven days", "Forty days", "One night")
    add(32, 1, "Jon. 1:3", "Where did Jonah try to flee?", "Tarshish", "Nineveh", "Egypt", "Cyprus")
    add(32, 1, "Jon. 3:3", "To what city was Jonah sent?", "Nineveh", "Babylon", "Tarshish", "Damascus")
    add(32, 2, "Jon. 4:6", "What did God prepare to shade Jonah?", "A gourd", "A cedar", "A cloud", "A cave")
    add(32, 3, "Jon. 3:4", "How many days until Nineveh would be overthrown, in Jonah's preaching?", "40", "3", "7", "70")
    add(33, 1, "Mic. 5:2", "Which town did Micah name as the ruler's coming forth?", "Bethlehem Ephratah", "Nazareth", "Jerusalem", "Hebron")
    add(33, 3, "Mic. 6:8", "What three things does the LORD require, according to Micah?", "Do justly, love mercy, walk humbly", "Tithe, fast, and pray", "Sacrifice, incense, and song", "Build, plant, and marry")
    add(34, 3, "Nah. 1:1", "Against what city is the burden of Nahum?", "Nineveh", "Babylon", "Tyre", "Samaria")
    add(35, 2, "Hab. 2:4", "The just shall live by his ___", "faith", "works", "law", "wisdom")
    add(35, 4, "Hab. 3:17-18", "Though the fig tree shall not blossom... yet I will ___", "rejoice in the LORD", "return to Egypt", "keep silence", "curse the day")
    add(36, 3, "Zeph. 1:1", "In whose days did Zephaniah prophesy?", "Josiah", "Hezekiah", "Uzziah", "Zedekiah")
    add(37, 3, "Hag. 1:8", "What did Haggai urge the people to rebuild?", "The house of the LORD", "The wall", "The palace", "Jericho")
    add(38, 2, "Zech. 9:9", "Thy King cometh unto thee... lowly, and riding upon an ___", "ass", "horse", "camel", "chariot")
    add(38, 3, "Zech. 11:12", "How many pieces of silver are named in Zechariah's shepherd wage?", "30", "20", "40", "100")
    add(38, 4, "Zech. 4:6", "Not by might, nor by power, but by my ___, saith the LORD of hosts", "spirit", "sword", "name only", "angel")
    add(39, 2, "Mal. 3:8", "Will a man rob God? Wherein have we robbed thee? In ___", "tithes and offerings", "prayer", "the sabbath", "the temple tax")
    add(39, 2, "Mal. 4:5", "Whom will God send before the coming of the great day?", "Elijah the prophet", "Moses", "David", "John only, by name")
    add(39, 1, "Mal. 4:6", "What is the last book of the Old Testament?", "Malachi", "Zechariah", "Haggai", "Micah")

    # --- Gospels ---
    add(40, 1, "Matt. 1:21", "What does the name Jesus mean in Matthew's angelic word: he shall ___ his people from their sins?", "save", "judge", "rule", "teach")
    add(40, 1, "Matt. 2:1", "Where was Jesus born?", "Bethlehem of Judaea", "Nazareth", "Jerusalem", "Capernaum")
    add(40, 1, "Matt. 2:13", "Where did Joseph take the child Jesus to escape Herod?", "Egypt", "Syria", "Galilee first", "Rome")
    add(40, 1, "Matt. 3:13", "Who baptized Jesus?", "John the Baptist", "Peter", "Ananias", "James")
    add(40, 1, "Matt. 4:18-19", "Whom did Jesus call first by the sea, with Andrew?", "Peter (Simon)", "Matthew", "Philip", "Thomas")
    add(40, 1, "Matt. 5:3", "Blessed are the poor in spirit: for theirs is the ___", "kingdom of heaven", "earth", "comfort", "sight of God")
    add(40, 2, "Matt. 5:5", "Blessed are the meek: for they shall inherit the ___", "earth", "kingdom of heaven", "nations", "temple")
    add(40, 2, "Matt. 5:9", "Blessed are the peacemakers: for they shall be called the ___", "children of God", "sons of thunder", "salt of the earth", "light of the world")
    add(40, 1, "Matt. 6:9", "How does the Lord's prayer begin?", "Our Father which art in heaven", "Hail, Mary", "Hear, O Israel", "The LORD is my shepherd")
    add(40, 1, "Matt. 6:11", "Give us this day our daily ___", "bread", "water", "word", "peace")
    add(40, 2, "Matt. 6:24", "Ye cannot serve God and ___", "mammon", "Caesar", "self", "the law")
    add(40, 1, "Matt. 7:12", "What is often called the Golden Rule in Matthew 7?", "Do unto others as you would have them do unto you", "Love your enemies only", "Give a tithe", "Keep the sabbath")
    add(40, 2, "Matt. 14:19-21", "How many men besides women and children did Jesus feed with five loaves?", "About 5000", "4000", "120", "70")
    add(40, 2, "Matt. 15:38", "How many men were fed in the second feeding miracle in Matthew?", "4000", "5000", "3000", "120")
    add(40, 1, "Matt. 14:29", "Who walked on the water to Jesus, then feared?", "Peter", "John", "Andrew", "Thomas")
    add(40, 2, "Matt. 17:1-2", "Which three disciples saw the transfiguration?", "Peter, James, and John", "Peter, Andrew, and John", "Matthew, Mark, and Luke", "Thomas, Philip, and John")
    add(40, 3, "Matt. 17:3", "Who appeared with Jesus at the transfiguration?", "Moses and Elias", "Abraham and David", "Gabriel and Michael", "Enoch and Elijah only")
    add(40, 1, "Matt. 21:9", "What did the crowds cry as Jesus entered Jerusalem?", "Hosanna to the son of David", "Crucify him", "Hail, king of the Jews only", "Glory to God in the highest only")
    add(40, 1, "Matt. 26:26", "What did Jesus say of the bread at the last supper?", "This is my body", "This is the passover lamb", "This is manna", "This is the new law")
    add(40, 1, "Matt. 27:35", "How was Jesus put to death?", "He was crucified", "He was stoned", "He was beheaded", "He was hanged on a tree by Saul")
    add(40, 1, "Matt. 28:6", "What did the angel say at the tomb?", "He is not here: for he is risen", "He sleepeth", "Come see the gardener", "He has gone to Galilee only")
    add(40, 2, "Matt. 28:19", "Into what name are disciples to be baptized, according to Matthew?", "The Father, the Son, and the Holy Ghost", "Jesus only, in these words", "The God of Abraham", "The church")
    add(40, 3, "Matt. 10:2-4", "How many apostles did Jesus name in Matthew 10?", "12", "7", "70", "3")
    add(40, 2, "Matt. 10:4", "Which apostle is called the traitor in the list?", "Judas Iscariot", "Thomas", "Simon the Canaanite", "Thaddaeus")
    add(40, 2, "Matt. 9:9", "What was Matthew's occupation?", "A publican (tax collector)", "A fisherman", "A zealot", "A priest")
    add(40, 3, "Matt. 13:31", "To what seed did Jesus liken the kingdom in one parable?", "A grain of mustard seed", "Wheat only", "Tares", "A fig")
    add(40, 3, "Matt. 25:1-13", "How many virgins were wise in the parable?", "5", "10", "3", "7")
    add(40, 4, "Matt. 27:16", "What prisoner was released instead of Jesus?", "Barabbas", "Barnabas", "Barrabas the priest", "Simon of Cyrene")
    add(40, 4, "Matt. 27:32", "Who was compelled to bear Jesus' cross?", "Simon of Cyrene", "Joseph of Arimathaea", "Nicodemus", "John")

    apostles = [
        "Peter", "Andrew", "James", "John", "Philip", "Bartholomew",
        "Thomas", "Matthew", "James the son of Alphaeus", "Thaddaeus",
        "Simon the Canaanite", "Judas Iscariot",
    ]
    not_ap = ["Luke", "Mark", "Barnabas", "Timothy", "Titus", "Silas", "Apollos", "Lazarus"]
    for i, name in enumerate(apostles):
        wr = [not_ap[i % len(not_ap)], not_ap[(i + 1) % len(not_ap)], not_ap[(i + 2) % len(not_ap)]]
        add(40, 1 if i < 4 else 2, "Matt. 10:2-4", f"Which of these was one of the twelve apostles?", name, wr[0], wr[1], wr[2])

    add(41, 1, "Mark 1:17", "What did Jesus say he would make Simon and Andrew?", "Fishers of men", "Kings of Israel", "Priests", "Scribes")
    add(41, 2, "Mark 2:14", "What other name did Matthew the publican have in Mark?", "Levi", "Justus", "Barsabas", "Alphaeus")
    add(41, 2, "Mark 5:9", "What was the name of the legion of unclean spirits?", "Legion", "Beelzebub", "Abaddon", "Python")
    add(41, 3, "Mark 5:41", "What Aramaic words did Jesus speak to Jairus' daughter?", "Talitha cumi", "Ephphatha", "Eloi, Eloi", "Maranatha")
    add(41, 3, "Mark 7:34", "What did Jesus say when he healed a deaf man?", "Ephphatha", "Talitha cumi", "Amen", "Peace, be still")
    add(41, 1, "Mark 4:39", "What did Jesus say to the storm?", "Peace, be still", "Come forth", "It is I; be not afraid", "Get thee behind me")
    add(41, 2, "Mark 10:46", "What blind man at Jericho did Jesus heal in Mark?", "Bartimaeus", "Malchus", "Zacchaeus", "Lazarus")
    add(41, 3, "Mark 12:42", "How much did the poor widow cast into the treasury?", "Two mites", "A penny", "Two farthings of gold", "A shekel")
    add(41, 4, "Mark 14:51-52", "What unique detail does Mark record at Jesus' arrest?", "A young man who fled naked", "Malchus' ear", "Pilate's wife", "The cock crowing twice only")
    add(41, 2, "Mark 16:1", "Who brought spices to the tomb in Mark?", "Mary Magdalene, Mary the mother of James, and Salome", "The eleven", "Joseph only", "The soldiers")
    add(42, 1, "Luke 1:27", "To whom was the angel Gabriel sent in Nazareth?", "Mary", "Elizabeth", "Anna", "Martha")
    add(42, 1, "Luke 1:13", "Who was John the Baptist's father?", "Zacharias", "Zadok", "Zebedee", "Aaron")
    add(42, 2, "Luke 1:5", "Of what course was Zacharias?", "Abia", "Levi", "Aaron only", "Melchisedec")
    add(42, 1, "Luke 2:7", "Where was the baby Jesus laid?", "In a manger", "In a crib of gold", "In the temple", "In a house of stone")
    add(42, 1, "Luke 2:8-11", "To whom did angels announce Jesus' birth?", "Shepherds", "Wise men", "Priests", "King Herod")
    add(42, 2, "Luke 2:25", "Who was waiting to see the Lord's Christ before he died?", "Simeon", "Anna only", "Nicodemus", "Joseph of Arimathaea")
    add(42, 3, "Luke 2:36", "What prophetess served in the temple at Jesus' presentation?", "Anna", "Deborah", "Huldah", "Miriam")
    add(42, 2, "Luke 10:33", "Who helped the wounded man in Jesus' parable?", "A Samaritan", "A priest", "A Levite", "A Pharisee")
    add(42, 1, "Luke 15:11-32", "What parable tells of a son who wasted his living?", "The prodigal son", "The sower", "The talents", "The ten virgins")
    add(42, 2, "Luke 19:2", "Who climbed a sycamore tree to see Jesus?", "Zacchaeus", "Bartimaeus", "Nicodemus", "Lazarus")
    add(42, 2, "Luke 10:38-42", "Who sat at Jesus' feet while her sister served?", "Mary", "Martha", "Mary Magdalene", "Joanna")
    add(42, 3, "Luke 17:12", "How many lepers did Jesus heal of whom one returned?", "10", "12", "7", "1")
    add(42, 3, "Luke 24:13", "To what village were two disciples going when the risen Jesus joined them?", "Emmaus", "Bethany", "Jericho", "Capernaum")
    add(42, 4, "Luke 3:23", "About how old was Jesus when he began his ministry, according to Luke?", "About thirty", "About twelve", "About forty", "About thirty-three")
    add(42, 2, "Luke 23:43", "What did Jesus promise the repentant thief?", "To-day shalt thou be with me in paradise", "He would not die", "A place at his right hand", "To be unbound")
    add(42, 1, "Luke 24:6", "He is not here, but is ___", "risen", "sleeping", "taken away by gardeners", "in Galilee only")
    add(43, 1, "John 1:1", "In the beginning was the Word, and the Word was with God, and the Word was ___", "God", "a god", "created", "an angel")
    add(43, 1, "John 1:14", "The Word was made flesh, and dwelt among us", "True — John's gospel", "That is Luke 2", "That is Genesis 1", "That is Matthew 1")
    add(43, 1, "John 3:16", "For God so loved the world, that he gave his only begotten ___", "Son", "Word", "Spirit", "Law")
    add(43, 1, "John 3:3", "Except a man be born again, he cannot see the ___", "kingdom of God", "temple", "resurrection only", "promised land")
    add(43, 2, "John 3:1", "Which Pharisee came to Jesus by night?", "Nicodemus", "Gamaliel", "Saul", "Joseph of Arimathaea")
    add(43, 1, "John 11:35", "What is the shortest verse in the KJV?", "Jesus wept.", "God is love.", "Rejoice evermore.", "Pray without ceasing.")
    add(43, 1, "John 11:43", "What did Jesus cry at Lazarus' tomb?", "Lazarus, come forth", "Peace, be still", "Talitha cumi", "It is finished")
    add(43, 1, "John 2:9", "What was Jesus' first miracle in John?", "Water turned to wine", "Healing a blind man", "Feeding 5000", "Walking on water")
    add(43, 2, "John 2:1", "Where was the wedding of the first miracle?", "Cana of Galilee", "Capernaum", "Nazareth", "Jerusalem")
    add(43, 2, "John 4:7", "To whom did Jesus speak at Jacob's well?", "A woman of Samaria", "The Syrophenician woman", "Martha", "Mary Magdalene")
    add(43, 2, "John 6:35", "Jesus said, I am the bread of ___", "life", "heaven only", "the temple", "the passover")
    add(43, 2, "John 8:12", "Jesus said, I am the light of the ___", "world", "temple", "Jews only", "gentiles only")
    add(43, 2, "John 10:11", "Jesus said, I am the good ___", "shepherd", "priest", "king only", "vine only")
    add(43, 2, "John 11:25", "Jesus said, I am the resurrection, and the ___", "life", "way", "truth", "door")
    add(43, 2, "John 14:6", "I am the way, the truth, and the life: no man cometh unto the Father, but by ___", "me", "the law", "Peter", "the church")
    add(43, 3, "John 15:1", "Jesus said, I am the true ___", "vine", "olive tree", "fig tree", "mustard seed")
    add(43, 3, "John 10:9", "Jesus said, I am the ___: by me if any man enter in, he shall be saved", "door", "gate of the temple", "shepherd only", "light")
    add(43, 1, "John 19:30", "What were Jesus' last words in John at the cross?", "It is finished", "Father, forgive them", "My God, my God", "Into thy hands")
    add(43, 3, "John 19:26-27", "To whom did Jesus commit his mother?", "The disciple whom he loved", "Peter", "James", "Joseph of Arimathaea")
    add(43, 3, "John 20:24-28", "Which disciple wanted to see the print of the nails?", "Thomas", "Peter", "Philip", "Andrew")
    add(43, 4, "John 21:11", "How many great fishes did the disciples catch after the resurrection?", "153", "1530", "12", "70")
    add(43, 4, "John 1:40-41", "Who first found his brother Simon and said, We have found the Messias?", "Andrew", "Philip", "John", "James")
    add(43, 3, "John 12:3", "Who anointed Jesus' feet with costly ointment in John 12?", "Mary (of Bethany)", "Mary Magdalene", "Martha", "a sinner of the city in this verse")

    # --- Acts ---
    add(44, 1, "Acts 1:8", "Ye shall receive power, after that the Holy Ghost is come upon you: and ye shall be ___ unto me", "witnesses", "kings", "priests", "scribes")
    add(44, 1, "Acts 1:9", "How did Jesus leave the disciples in Acts 1?", "He was taken up, and a cloud received him", "He vanished at Emmaus only", "He walked into the wilderness", "He entered the temple")
    add(44, 2, "Acts 1:26", "Who was chosen to take Judas' place?", "Matthias", "Barnabas", "Paul", "Stephen")
    add(44, 1, "Acts 2:1-4", "On what feast did the Holy Ghost fall at Pentecost?", "Pentecost (the day of Pentecost)", "Passover", "Tabernacles", "Dedication")
    add(44, 2, "Acts 2:41", "About how many were added the day of Pentecost?", "3000", "120", "5000", "70")
    add(44, 2, "Acts 1:15", "About how many were in the upper room before Pentecost?", "120", "12", "70", "500")
    add(44, 1, "Acts 3:6", "What did Peter say to the lame man at the Beautiful gate?", "In the name of Jesus Christ of Nazareth rise up and walk", "Silver and gold have I plenty", "Go wash in Siloam", "Thy faith hath made thee whole only")
    add(44, 2, "Acts 5:1-10", "Who lied about the price of land and died?", "Ananias and Sapphira", "Annas and Caiaphas", "Hymenaeus and Alexander", "Jannes and Jambres")
    add(44, 1, "Acts 7:59", "Who was the first Christian martyr in Acts?", "Stephen", "James", "Peter", "Paul")
    add(44, 2, "Acts 8:27", "Whom did Philip meet on the Gaza road?", "An Ethiopian eunuch", "Cornelius", "Saul", "Simon the sorcerer")
    add(44, 2, "Acts 8:9", "What sorcerer in Samaria believed and was baptized?", "Simon", "Elymas", "Bar-jesus", "Demetrius")
    add(44, 1, "Acts 9:3-4", "Where was Saul when a light from heaven shone?", "The road to Damascus", "The road to Emmaus", "The temple", "Tarsus")
    add(44, 2, "Acts 9:11", "On what street was Saul staying in Damascus?", "Straight", "Beautiful", "Damascus Gate", "Via Dolorosa")
    add(44, 2, "Acts 9:17", "Who laid hands on Saul that he might receive his sight?", "Ananias", "Peter", "Barnabas", "James")
    add(44, 3, "Acts 9:36", "What woman did Peter raise at Joppa?", "Dorcas (Tabitha)", "Lydia", "Priscilla", "Phoebe")
    add(44, 2, "Acts 10:1", "What centurion was the first recorded Gentile household to receive the Spirit in this way?", "Cornelius", "Julius", "Pilate", "Cornelius Agrippa")
    add(44, 3, "Acts 12:2", "Which apostle did Herod kill with the sword?", "James the brother of John", "John", "Peter", "Andrew")
    add(44, 2, "Acts 12:7", "Who delivered Peter from prison in Acts 12?", "An angel of the Lord", "Barnabas", "the jailer", "Rhoda")
    add(44, 2, "Acts 13:2", "Whom did the Holy Ghost separate for the work, with Saul?", "Barnabas", "Silas", "Timothy", "Luke")
    add(44, 3, "Acts 13:6-11", "What sorcerer did Paul blind on Cyprus?", "Elymas (Bar-jesus)", "Simon of Samaria", "Demetrius", "Sceva")
    add(44, 2, "Acts 16:14", "Who was the seller of purple at Philippi?", "Lydia", "Phoebe", "Priscilla", "Dorcas")
    add(44, 2, "Acts 16:25-26", "What happened while Paul and Silas sang in prison?", "An earthquake opened the doors", "The jailer fled", "Fire fell", "An angel led them out silently")
    add(44, 3, "Acts 16:27-31", "What did Paul tell the Philippian jailer?", "Believe on the Lord Jesus Christ, and thou shalt be saved", "Keep the law of Moses", "Be baptized first, then believe", "Flee the city")
    add(44, 3, "Acts 17:22", "In what city did Paul preach about the unknown God?", "Athens", "Corinth", "Ephesus", "Rome")
    add(44, 3, "Acts 18:3", "What trade did Paul share with Aquila and Priscilla?", "Tentmakers", "Fishermen", "Silversmiths", "Scribes")
    add(44, 3, "Acts 19:24", "What silversmith stirred a riot in Ephesus?", "Demetrius", "Alexander", "Sceva", "Elymas")
    add(44, 4, "Acts 19:14", "How many sons of Sceva tried to exorcise in Jesus' name?", "7", "12", "3", "2")
    add(44, 3, "Acts 20:9", "Who fell from a window while Paul preached?", "Eutychus", "Trophimus", "Tychicus", "Epaphroditus")
    add(44, 2, "Acts 21:39", "Of what city was Paul a citizen by birth, besides Rome?", "Tarsus", "Jerusalem", "Damascus", "Antioch")
    add(44, 4, "Acts 27:37", "How many souls were in the ship that wrecked?", "276", "153", "120", "70")
    add(44, 3, "Acts 28:1", "On what island was Paul shipwrecked?", "Melita (Malta)", "Cyprus", "Crete", "Patmos")
    add(44, 4, "Acts 28:3-5", "What fastened on Paul's hand at Melita?", "A viper", "A scorpion", "A dog", "A leech")

    # --- Epistles ---
    add(45, 1, "Rom. 3:23", "For all have sinned, and come short of the ___ of God", "glory", "law", "mercy", "kingdom")
    add(45, 1, "Rom. 6:23", "The wages of sin is death; but the gift of God is eternal life through ___", "Jesus Christ our Lord", "the law", "works", "Israel")
    add(45, 1, "Rom. 8:28", "All things work together for good to them that ___ God", "love", "fear only", "serve in the temple", "keep every feast")
    add(45, 2, "Rom. 12:1", "Present your bodies a living ___", "sacrifice", "temple of stone", "tithe", "witness in court")
    add(45, 2, "Rom. 1:16", "I am not ashamed of the gospel of Christ: for it is the power of God unto ___", "salvation", "the Jews only", "Rome", "the law")
    add(45, 3, "Rom. 9:3", "For whom did Paul wish himself accursed, if it could save them?", "His kinsmen according to the flesh (Israel)", "The Romans", "The Gentiles only", "False teachers")
    add(45, 3, "Rom. 16:1", "Who is commended as a servant of the church at Cenchrea?", "Phoebe", "Priscilla", "Lydia", "Lois")
    add(46, 1, "1 Cor. 13:4", "Charity suffereth long, and is ___", "kind", "proud", "jealous", "weak")
    add(46, 1, "1 Cor. 13:13", "The greatest of faith, hope, and charity is ___", "charity (love)", "faith", "hope", "none is greater")
    add(46, 2, "1 Cor. 15:3-4", "What did Paul say was of first importance: Christ died, was buried, and ___", "rose again the third day", "ascended immediately", "will come in secret", "gave the law")
    add(46, 2, "1 Cor. 6:19", "Your body is the temple of the ___", "Holy Ghost", "law", "soul only", "church building")
    add(46, 3, "1 Cor. 9:24", "They which run in a race run all, but one receiveth the ___", "prize", "law", "crown of thorns", "tithe")
    add(46, 3, "1 Cor. 11:23-26", "What ordinance does Paul recount from the Lord in 1 Corinthians 11?", "The Lord's supper", "Baptism only", "Foot washing only", "Anointing the sick")
    add(46, 2, "1 Cor. 12:4", "Now there are diversities of gifts, but the same ___", "Spirit", "Lord only", "baptism", "office")
    fruit = [
        "love", "joy", "peace", "longsuffering", "gentleness",
        "goodness", "faith", "meekness", "temperance",
    ]
    not_fruit = ["wealth", "anger", "envy", "pride", "fear of man"]
    for i, fr in enumerate(fruit):
        wr = [not_fruit[i % 5], not_fruit[(i + 1) % 5], not_fruit[(i + 2) % 5]]
        add(48, 1 if i < 3 else 2, "Gal. 5:22-23", "Which of these is listed as fruit of the Spirit?", fr, wr[0], wr[1], wr[2])
    add(48, 1, "Gal. 5:22-23", "How many items are listed as the fruit of the Spirit in the KJV?", "9", "7", "12", "3")
    add(48, 2, "Gal. 6:7", "Whatsoever a man soweth, that shall he also ___", "reap", "forget", "sell", "burn")
    add(48, 2, "Gal. 2:20", "I am crucified with Christ: nevertheless I live; yet not I, but ___ liveth in me", "Christ", "the law", "Adam", "an angel")
    add(48, 3, "Gal. 1:17", "Where did Paul go after his conversion, according to Galatians (not Jerusalem at first)?", "Arabia", "Rome", "Spain", "Ephesus")
    add(49, 1, "Eph. 2:8", "By grace are ye saved through ___", "faith", "works", "baptism only", "the law")
    add(49, 2, "Eph. 2:8-9", "Not of works, lest any man should ___", "boast", "fall", "tithe", "pray")
    add(49, 1, "Eph. 6:11", "Put on the whole ___ of God", "armour", "robe", "ephod", "crown")
    add(49, 2, "Eph. 6:17", "The sword of the Spirit is ___", "the word of God", "prayer", "faith", "hope")
    add(49, 2, "Eph. 6:16", "The shield of faith can quench the fiery darts of the ___", "wicked", "law", "flesh only", "world only")
    add(49, 3, "Eph. 6:14", "Having your loins girt about with ___", "truth", "gold", "the law of Moses", "pride")
    add(49, 3, "Eph. 6:14", "The breastplate is ___", "righteousness", "faith", "salvation", "the gospel")
    add(49, 3, "Eph. 6:17", "The helmet is ___", "salvation", "hope", "glory", "wisdom")
    add(49, 2, "Eph. 5:25", "Husbands, love your wives, even as Christ also loved the ___", "church", "law", "world only", "angels")
    add(49, 4, "Eph. 4:11", "Which office is not listed in Ephesians 4:11?", "Kings", "Apostles", "Prophets", "Pastors and teachers")
    add(50, 1, "Phil. 4:13", "I can do all things through Christ which ___ me", "strengtheneth", "judgeth", "tempteth", "leaveth")
    add(50, 2, "Phil. 4:4", "Rejoice in the Lord ___", "alway", "on the sabbath", "in the temple", "when you feel it")
    add(50, 2, "Phil. 2:5-8", "Christ made himself of no reputation and took upon him the form of a ___", "servant", "king", "priest", "scribe")
    add(50, 3, "Phil. 4:7", "The peace of God, which passeth all ___, shall keep your hearts", "understanding", "sorrow", "wealth", "time")
    add(50, 3, "Phil. 1:21", "For to me to live is Christ, and to die is ___", "gain", "loss", "sleep only", "the end")
    add(51, 2, "Col. 3:2", "Set your affection on things ___, not on things on the earth", "above", "new", "legal", "Roman")
    add(51, 3, "Col. 4:14", "Who is the beloved physician?", "Luke", "Matthew", "John", "Paul")
    add(51, 2, "Col. 1:16", "By Christ were all things created, that are in heaven, and that are in ___", "earth", "the temple", "Israel only", "the church only")
    add(52, 2, "1 Thes. 4:16", "The dead in Christ shall rise ___", "first", "last", "never", "after the living")
    add(52, 3, "1 Thes. 5:17", "Pray without ___", "ceasing", "words", "faith", "the temple")
    add(52, 2, "1 Thes. 4:17", "Then we which are alive and remain shall be caught up together with them in the ___", "clouds", "temple", "sea", "wilderness")
    add(53, 3, "2 Thes. 3:10", "If any would not work, neither should he ___", "eat", "pray", "tithe", "sing")
    add(53, 4, "2 Thes. 2:3", "That day shall not come, except there come a falling away first, and that man of ___ be revealed", "sin", "peace", "law", "Rome")
    add(54, 1, "1 Tim. 6:10", "The love of money is the root of all ___", "evil", "happiness", "wisdom", "power")
    add(54, 2, "1 Tim. 4:12", "Let no man despise thy ___", "youth", "bonds", "poverty", "nation")
    add(54, 3, "1 Tim. 3:1", "If a man desire the office of a bishop, he desireth a good ___", "work", "crown", "salary", "name only")
    add(54, 2, "1 Tim. 2:5", "There is one God, and one mediator between God and men, the man ___", "Christ Jesus", "Moses", "Peter", "an angel")
    add(55, 2, "2 Tim. 3:16", "All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for ___", "instruction in righteousness", "history only", "poetry", "the Jews only")
    add(55, 2, "2 Tim. 4:7", "I have fought a good fight, I have finished my course, I have kept the ___", "faith", "law", "sabbath", "temple")
    add(55, 3, "2 Tim. 1:5", "Who was Timothy's mother?", "Eunice", "Lois", "Priscilla", "Lydia")
    add(55, 3, "2 Tim. 1:5", "Who was Timothy's grandmother?", "Lois", "Eunice", "Hannah", "Elisabeth")
    add(55, 4, "2 Tim. 4:13", "What did Paul ask Timothy to bring from Troas?", "The cloke, books, and parchments", "Gold", "A physician", "Barnabas")
    add(56, 3, "Titus 1:5", "Where did Paul leave Titus?", "Crete", "Cyprus", "Rome", "Antioch")
    add(56, 3, "Titus 2:13", "Looking for that blessed hope, and the glorious appearing of the great God and our Saviour ___", "Jesus Christ", "the law", "an angel", "Elijah")
    add(57, 2, "Philem. 10", "Who was the runaway slave Paul sent back?", "Onesimus", "Epaphras", "Tychicus", "Archippus")
    add(57, 3, "Philem. 1", "To whom is the letter about Onesimus written?", "Philemon", "Timothy", "Titus", "Gaius")
    add(58, 1, "Heb. 11:1", "Faith is the substance of things hoped for, the evidence of things not ___", "seen", "heard", "written", "felt")
    add(58, 2, "Heb. 12:2", "Looking unto Jesus the author and finisher of our ___", "faith", "law", "race only", "hope only")
    add(58, 2, "Heb. 4:12", "The word of God is quick, and powerful, and sharper than any twoedged ___", "sword", "thorn", "nail", "spear")
    add(58, 3, "Heb. 11:7", "By faith ___ prepared an ark", "Noah", "Moses", "Abraham", "Enoch")
    add(58, 3, "Heb. 11:8", "By faith ___ obeyed when he was called to go out", "Abraham", "Noah", "Jacob", "Joseph")
    add(58, 2, "Heb. 13:8", "Jesus Christ the same yesterday, and to day, and for ___", "ever", "a season", "Israel only", "the church age only")
    add(58, 4, "Heb. 7:1-3", "Who is described as king of Salem and priest of the most high God, without father or mother in the record?", "Melchisedec", "Aaron", "Moses", "David")
    add(59, 1, "James 1:5", "If any of you lack wisdom, let him ask of ___", "God", "the priest", "the king", "an angel")
    add(59, 2, "James 1:19", "Let every man be swift to hear, slow to speak, slow to ___", "wrath", "pray", "give", "work")
    add(59, 2, "James 2:17", "Faith, if it hath not works, is ___", "dead", "enough", "hidden", "perfect already")
    add(59, 3, "James 5:16", "The effectual fervent prayer of a righteous man availeth ___", "much", "little", "nothing without a priest", "only in the temple")
    add(59, 3, "James 3:5-6", "What small member does James say is a fire?", "The tongue", "The eye", "The hand", "The foot")
    add(60, 2, "1 Pet. 5:7", "Casting all your care upon him; for he careth for ___", "you", "the angels", "Israel only", "kings")
    add(60, 2, "1 Pet. 2:9", "Ye are a chosen generation, a royal ___, an holy nation", "priesthood", "army", "city", "family of Levi")
    add(60, 3, "1 Pet. 3:15", "Be ready always to give an answer to every man that asketh you a reason of the hope that is in you with ___", "meekness and fear", "anger", "silence", "gold")
    add(61, 2, "2 Pet. 3:8", "One day is with the Lord as a thousand years, and a thousand years as ___", "one day", "an hour", "a watch in the night only", "seventy years")
    add(61, 3, "2 Pet. 1:21", "Holy men of God spake as they were moved by the ___", "Holy Ghost", "law of Moses", "kings of Judah", "traditions")
    add(61, 4, "2 Pet. 2:15", "Which prophet loved the wages of unrighteousness, in Peter's warning?", "Balaam", "Jonah", "Caiaphas", "Ahithophel")
    add(62, 1, "1 John 1:9", "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all ___", "unrighteousness", "memory", "law", "weakness only")
    add(62, 1, "1 John 4:8", "God is ___", "love", "an idea", "force", "unknown")
    add(62, 2, "1 John 4:19", "We love him, because he first ___ us", "loved", "judged", "called as a nation", "baptized")
    add(62, 3, "1 John 5:7", "In the KJV, the Father, the Word, and the Holy Ghost are said to be ___", "one", "three gods", "angels", "prophets")
    add(63, 3, "2 John 1:1", "To whom is 2 John addressed?", "The elect lady and her children", "Gaius", "Timothy", "Philemon")
    add(64, 3, "3 John 1:1", "To whom is 3 John written?", "Gaius", "the elect lady", "Diotrephes", "Demetrius only")
    add(64, 4, "3 John 1:9", "Who loved to have the preeminence in 3 John?", "Diotrephes", "Gaius", "Demetrius", "Demas")
    add(65, 3, "Jude 1:9", "Who contended with the devil about the body of Moses?", "Michael the archangel", "Gabriel", "Raphael", "Peter")
    add(65, 4, "Jude 1:14", "Which patriarch is quoted as prophesying in Jude?", "Enoch", "Noah", "Abraham", "Adam")

    # --- Revelation ---
    add(66, 1, "Rev. 1:9", "On what island was John when he received the Revelation?", "Patmos", "Cyprus", "Melita", "Crete")
    add(66, 1, "Rev. 1:8", "I am Alpha and Omega, the beginning and the ending, saith the ___", "Lord", "angel", "apostle", "elder")
    add(66, 2, "Rev. 1:11", "How many churches in Asia received the letters?", "7", "12", "3", "10")
    churches = [
        "Ephesus", "Smyrna", "Pergamos", "Thyatira", "Sardis", "Philadelphia", "Laodicea",
    ]
    not_ch = ["Rome", "Corinth", "Antioch", "Jerusalem", "Athens", "Philippi", "Colosse"]
    for i, c in enumerate(churches):
        add(66, 2 if i > 1 else 1, "Rev. 2-3", "Which of these is one of the seven churches of Asia in Revelation?", c, not_ch[i], not_ch[(i + 1) % 7], not_ch[(i + 2) % 7])
    add(66, 3, "Rev. 3:16", "What did the Lord say he would do with the lukewarm church?", "Spue thee out of my mouth", "Crown them", "Ignore them", "Give them gold")
    add(66, 2, "Rev. 3:20", "Behold, I stand at the door, and ___", "knock", "enter by force", "wait in silence", "leave")
    add(66, 2, "Rev. 4:8", "What do the four beasts cry?", "Holy, holy, holy, Lord God Almighty", "Worthy is the Lamb only", "Amen", "Hosanna")
    add(66, 2, "Rev. 5:6", "Who was worthy to open the book?", "The Lamb", "A mighty angel", "John", "One of the elders")
    add(66, 3, "Rev. 6:1-8", "How many horsemen appear as the first seals are opened?", "4", "7", "12", "3")
    add(66, 3, "Rev. 7:4", "How many were sealed of the tribes of Israel in the vision?", "144000", "12000", "7000", "1000")
    add(66, 2, "Rev. 12:7", "Who fought against the dragon?", "Michael and his angels", "Gabriel", "Peter", "The Lamb only in that verse")
    add(66, 3, "Rev. 13:18", "What number is the number of the beast?", "666", "616 only in KJV", "777", "144")
    add(66, 2, "Rev. 20:2-3", "For how many years is the dragon bound?", "1000", "7", "40", "70")
    add(66, 2, "Rev. 21:1", "What did John see after the first heaven and earth passed?", "A new heaven and a new earth", "The garden of Eden restored only", "A second flood", "The temple of Solomon")
    add(66, 3, "Rev. 21:2", "What city came down from God out of heaven?", "New Jerusalem", "Babylon the great", "Nineveh", "Zion of David only")
    add(66, 3, "Rev. 21:12", "How many gates did the city have?", "12", "7", "4", "3")
    add(66, 4, "Rev. 21:16", "The city lieth foursquare: the length is as large as the ___", "breadth", "height only", "wall only", "river")
    add(66, 2, "Rev. 22:18-19", "What warning closes Revelation about the words of the book?", "Do not add or take away", "Do not translate it", "Do not read it aloud", "Do not copy it")
    add(66, 1, "Rev. 22:20", "He which testifieth these things saith, Surely I come quickly. Amen. Even so, come, ___", "Lord Jesus", "Holy Ghost", "Michael", "Elijah")
    add(66, 4, "Rev. 2:17", "What hidden food is promised to the overcomer in Pergamos?", "Hidden manna", "The tree of life only", "Living water only", "A crown of gold")

    # --- Who wrote / which book ---
    writers = [
        (1, 2, "Gen. 1", "Which book begins, 'In the beginning God created'?", "Genesis", "John", "Psalms", "Matthew"),
        (40, 2, "Matt. 1:1", "Which gospel begins with a genealogy of Jesus, son of David, son of Abraham?", "Matthew", "Mark", "Luke", "John"),
        (41, 3, "Mark 1:1", "Which gospel begins, 'The beginning of the gospel of Jesus Christ, the Son of God'?", "Mark", "Matthew", "Luke", "John"),
        (42, 2, "Luke 1:3", "Which gospel is addressed to Theophilus?", "Luke", "John", "Acts", "Mark"),
        (44, 2, "Acts 1:1", "Which book is the sequel to Luke, also to Theophilus?", "Acts", "Hebrews", "John", "Romans"),
        (19, 1, "Ps. 23", "In which book is 'The LORD is my shepherd'?", "Psalms", "Proverbs", "Isaiah", "John"),
        (20, 2, "Prov. 1:1", "Which book is largely the proverbs of Solomon?", "Proverbs", "Ecclesiastes", "Psalms", "Song of Solomon"),
        (32, 1, "Jon. 1", "Which book tells of a prophet swallowed by a great fish?", "Jonah", "Joel", "Amos", "Nahum"),
        (17, 2, "Est. 4:14", "Which book has no explicit name of God in the Hebrew/KJV text, yet shows his providence?", "Esther", "Song of Solomon", "Obadiah", "Philemon"),
        (8, 2, "Ruth 1", "Which book tells of a Moabitess who became David's ancestor?", "Ruth", "Esther", "Judges", "Ezra"),
        (66, 1, "Rev. 1:1", "Which is the last book of the New Testament?", "Revelation", "Jude", "3 John", "Acts"),
        (39, 1, "Mal. 1:1", "Which is the last book of the Old Testament?", "Malachi", "Zechariah", "Micah", "Haggai"),
        (31, 4, "Obad. 1", "Which is the shortest Old Testament book?", "Obadiah", "Haggai", "Nahum", "Joel"),
        (63, 4, "2 John 1", "Which New Testament book has only one chapter and is written to the elect lady?", "2 John", "3 John", "Philemon", "Jude"),
        (45, 2, "Rom. 1:1", "Which epistle is Paul's great letter to the saints at Rome?", "Romans", "Hebrews", "Ephesians", "Galatians"),
        (58, 3, "Heb. 1:1", "Which book begins, 'God, who at sundry times and in divers manners spake'?", "Hebrews", "Romans", "James", "1 Peter"),
        (59, 2, "James 1:1", "Which general epistle is written by James, a servant of God?", "James", "Jude", "1 Peter", "Hebrews"),
        (18, 2, "Job 1:1", "Which book tells of a man from Uz who suffered and was restored?", "Job", "Ecclesiastes", "Lamentations", "Jonah"),
        (25, 3, "Lam. 1:1", "Which book is a series of acrostic dirges over Jerusalem?", "Lamentations", "Jeremiah", "Ezekiel", "Joel"),
        (26, 3, "Ez. 1:1", "Which book opens with a vision of a whirlwind and four living creatures by the Chebar?", "Ezekiel", "Daniel", "Isaiah", "Zechariah"),
    ]
    for w in writers:
        add(*w)

    pauline = [
        (45, "Romans", "Rome"),
        (46, "1 Corinthians", "Corinth"),
        (47, "2 Corinthians", "Corinth"),
        (48, "Galatians", "the churches of Galatia"),
        (49, "Ephesians", "Ephesus"),
        (50, "Philippians", "Philippi"),
        (51, "Colossians", "Colosse"),
        (52, "1 Thessalonians", "Thessalonica"),
        (53, "2 Thessalonians", "Thessalonica"),
        (54, "1 Timothy", "Timothy"),
        (55, "2 Timothy", "Timothy"),
        (56, "Titus", "Titus"),
        (57, "Philemon", "Philemon"),
    ]
    names = [p[1] for p in pauline]
    for i, (c, book, dest) in enumerate(pauline):
        wr = [n for n in names if n != book][i : i + 3]
        while len(wr) < 3:
            wr.append(["Hebrews", "James", "1 Peter"][len(wr) % 3])
        add(c, 2, book[:12], f"Which of these is a letter of Paul?", book, wr[0], wr[1], wr[2])
        add(c, 3, book[:12], f"To whom (or to which place) is {book} addressed?", dest, "Rome only" if dest != "Rome" else "Corinth", "Jerusalem", "Antioch")

    add(58, 3, "Heb. 13:23", "The human author of Hebrews is ___ in the text itself", "not named", "Paul, named in 1:1", "Barnabas, named in 1:1", "Luke, named in 1:1")
    add(19, 1, "Ps. 150", "How many psalms are in the book of Psalms?", "150", "100", "66", "119")
    add(5, 1, "Deut. / OT count", "How many books are in the Protestant Old Testament?", "39", "27", "66", "22")
    add(66, 1, "NT count", "How many books are in the New Testament?", "27", "39", "66", "12")
    add(40, 1, "whole Bible", "How many books are in the Protestant Bible?", "66", "73", "39", "27")
    add(40, 2, "Gospels", "How many Gospels are there?", "4", "3", "5", "12")
    add(4, 2, "Num. 13", "How many spies did Moses send into Canaan?", "12", "10", "2", "40")
    add(40, 2, "Matt. 10:1", "How many apostles did Jesus send out in Matthew 10?", "12", "70", "7", "3")
    add(42, 3, "Luke 10:1", "How many others did the Lord appoint in Luke 10?", "70", "12", "120", "7")
    add(2, 1, "Ex. 20", "How many commandments did God give on the tables of stone, commonly counted?", "10", "12", "7", "2")
    add(2, 1, "Ex. 7-12", "How many plagues fell on Egypt?", "10", "7", "12", "3")
    add(1, 2, "Gen. 5-9", "How many of each clean animal did Noah take, besides the pairs (KJV)?", "By sevens", "Two only of all", "Twelve", "Forty")
    add(44, 2, "Acts 6:3", "How many men were chosen to serve tables (the first deacons)?", "7", "12", "3", "70")
    add(66, 2, "Rev. 1:4", "How many spirits are before the throne in John's greeting?", "7", "3", "12", "4")
    add(66, 3, "Rev. 8:2", "How many angels stood before God with trumpets?", "7", "12", "4", "3")
    add(27, 2, "Dan. 3", "How many Hebrews were cast into the furnace (besides the fourth figure)?", "3", "4", "7", "2")
    add(42, 1, "Luke 2:21", "On what day was Jesus circumcised and named?", "The eighth day", "The first day", "The fortieth day", "The twelfth day")
    add(40, 2, "Matt. 4:2", "How many days did Jesus fast in the wilderness?", "40", "7", "3", "12")
    add(44, 2, "Acts 1:3", "How many days did Jesus show himself after his passion?", "40", "3", "7", "50")
    add(43, 2, "John 2:19", "In how many days did Jesus say he would raise the temple of his body?", "3", "7", "40", "1")
    add(40, 1, "Matt. 12:40", "As Jonas was three days and three nights in the whale's belly, so shall the Son of man be three days and three nights in the heart of the ___", "earth", "sea", "temple", "heaven")

    # More people / places
    add(1, 2, "Gen. 10:8-9", "Who was a mighty hunter before the LORD?", "Nimrod", "Esau", "Ishmael", "Goliath")
    add(1, 3, "Gen. 14:18", "Who was king of Salem and priest of the most high God in Genesis?", "Melchizedek", "Abimelech", "Pharaoh", "Lot")
    add(1, 2, "Gen. 18:1-8", "How many men did Abraham entertain before the destruction of Sodom?", "3", "2", "12", "7")
    add(1, 3, "Gen. 19:1", "How many angels came to Sodom in the evening?", "2", "3", "7", "1")
    add(1, 3, "Gen. 41:48", "What did Joseph store up in the seven plentiful years?", "Food in the cities", "Gold", "Soldiers", "Horses")
    add(2, 3, "Ex. 18:13-24", "Who advised Moses to appoint rulers of thousands and hundreds?", "Jethro", "Aaron", "Joshua", "Hur")
    add(2, 2, "Ex. 18:1", "Who was Moses' father in law?", "Jethro (Reuel)", "Laban", "Potiphar", "Hobab only in this verse")
    add(4, 4, "Num. 12:1-10", "Who was struck with leprosy for speaking against Moses?", "Miriam", "Aaron", "Korah", "Zipporah")
    add(6, 3, "Josh. 9:4", "Who pretended to be ambassadors from a far country with old sacks and wine bottles?", "The Gibeonites", "The men of Ai", "The Philistines", "The Moabites")
    add(9, 3, "1 Sam. 16:11", "Which son of Jesse was keeping the sheep when Samuel came?", "David, the youngest", "Eliab, the eldest", "Abinadab", "Shammah")
    add(9, 4, "1 Sam. 21:6", "What holy bread did David eat at Nob?", "Shewbread", "Manna", "Unleavened bread of passover", "Firstfruits")
    add(11, 3, "1 Ki. 12:8", "Whose counsel did Rehoboam reject?", "The old men", "The young men", "Jeroboam", "Ahijah")
    add(11, 4, "1 Ki. 12:28", "What did Jeroboam set up at Bethel and Dan?", "Golden calves", "Asherah poles only", "A temple of Baal", "High places to Molech only")
    add(12, 4, "2 Ki. 4:32-35", "Whose son did Elisha raise at Shunem?", "The Shunammite's", "The widow of Zarephath's", "Jairus'", "Naaman's")
    add(23, 4, "Is. 38:8", "What went backward ten degrees for Hezekiah in Isaiah's account?", "The shadow of the sundial of Ahaz", "The sun in the sky over Gibeon", "The moon", "A star")
    add(27, 4, "Dan. 4:33", "What happened to Nebuchadnezzar in his pride?", "He ate grass as oxen", "He was slain that night", "He became a leper", "He went mad for 7 hours only")
    add(40, 3, "Matt. 2:23", "In what town was Jesus brought up?", "Nazareth", "Bethlehem", "Capernaum", "Bethany")
    add(40, 2, "Matt. 4:13", "What town became Jesus' base in Galilee?", "Capernaum", "Nazareth", "Cana", "Tiberias")
    add(40, 3, "Matt. 26:36", "Where did Jesus pray before his arrest?", "Gethsemane", "Golgotha", "Bethany", "the temple")
    add(40, 2, "Matt. 27:33", "What was Golgotha also called?", "A place of a skull", "The mount of olives", "The beautiful gate", "Aceldama")
    add(44, 4, "Acts 1:19", "What was the field bought with Judas' money called?", "Aceldama, the field of blood", "Golgotha", "Potter's gate", "Gehenna")
    add(42, 3, "Luke 8:2", "Out of whom had seven devils gone?", "Mary called Magdalene", "Martha", "the Syrophenician woman", "Joanna")
    add(41, 3, "Mark 15:21", "Of whom was Simon of Cyrene the father, according to Mark?", "Alexander and Rufus", "James and John", "Castor and Pollux", "James and Joses")
    add(40, 4, "Matt. 1:5", "Which Gentile women appear in Matthew's genealogy of Jesus?", "Thamar, Rachab, Ruth (and her of Urias)", "Deborah, Jael, and Hannah", "Sarah, Rebekah, and Rachel", "Miriam, Abigail, and Esther")
    add(43, 3, "John 5:2", "At what pool did Jesus heal a man who had been infirm 38 years?", "Bethesda", "Siloam", "Jacob's well", "the Jordan")
    add(43, 3, "John 9:7", "Where did the blind man wash to receive sight?", "The pool of Siloam", "Bethesda", "Jordan", "Galilee")
    add(40, 3, "Matt. 8:5-13", "Whose servant did Jesus heal at a distance in Capernaum?", "A centurion's", "Jairus'", "Peter's mother-in-law", "the nobleman's in John 4 is another account")
    add(40, 2, "Matt. 8:14-15", "Whom did Jesus heal in Peter's house?", "Peter's wife's mother", "Peter's brother", "a leper", "a centurion")
    add(41, 2, "Mark 5:22", "Who was the ruler of the synagogue whose daughter Jesus raised?", "Jairus", "Zacchaeus", "Nicodemus", "Crispus")
    add(42, 4, "Luke 7:37-38", "What did a woman do at Jesus' feet in a Pharisee's house?", "Washed them with tears and wiped them with her hair", "Poured oil on his head only", "Asked for crumbs", "Sat and learned")
    add(40, 2, "Matt. 14:3-4", "Why did Herod imprison John?", "John said Herodias was not lawful for him", "John claimed to be king", "John refused to baptize him", "John stirred Galilee to revolt")
    add(40, 3, "Matt. 14:8", "What did Herodias' daughter ask for?", "John the Baptist's head in a charger", "Half the kingdom in gold", "To dance again", "The Baptist's raiment")
    add(43, 4, "John 18:13", "Who was Caiaphas' father in law?", "Annas", "Pilate", "Herod", "Gamaliel")
    add(40, 3, "Matt. 27:24", "What did Pilate wash before the multitude?", "His hands", "The Lord's feet", "the judgment seat", "a cup")
    add(43, 2, "John 19:19", "What title did Pilate write?", "JESUS OF NAZARETH THE KING OF THE JEWS", "King of Israel only", "Son of God", "The prophet of Galilee")
    add(42, 3, "Luke 23:12", "Who were made friends that day, over Jesus' trial?", "Pilate and Herod", "Pilate and Caiaphas", "Herod and Caiaphas", "Pilate and Barabbas")
    add(40, 2, "Matt. 27:57-60", "Who buried Jesus in his own new tomb?", "Joseph of Arimathaea", "Nicodemus only", "Peter", "Simon of Cyrene")
    add(43, 3, "John 19:39", "Who brought a mixture of myrrh and aloes?", "Nicodemus", "Joseph only", "Mary Magdalene", "the soldiers")
    add(40, 2, "Matt. 28:1", "Who first came to the sepulchre in Matthew?", "Mary Magdalene and the other Mary", "Peter and John", "the eleven", "the soldiers")
    add(43, 2, "John 20:15", "Whom did Mary Magdalene suppose Jesus to be at first?", "The gardener", "an angel", "Peter", "a soldier")
    add(42, 2, "Luke 24:39", "What did the risen Jesus invite the disciples to handle?", "His hands and his feet", "His robe", "bread only", "the scriptures only")
    add(43, 3, "John 21:15", "What did Jesus ask Peter three times?", "Lovest thou me?", "Wilt thou die for me?", "Knowest thou me?", "Feedest thou the poor?")
    add(44, 2, "Acts 2:38", "What did Peter tell the Pentecost crowd to do?", "Repent, and be baptized", "Keep the law of Moses", "Follow him to Galilee", "Buy a field")

    # Famous KJV fill-ins
    add(19, 1, "Ps. 119:105", "Thy word is a lamp unto my feet, and a light unto my ___", "path", "eyes", "house", "mind")
    add(19, 1, "Ps. 46:1", "God is our refuge and strength, a very present help in ___", "trouble", "battle", "the temple", "Zion only")
    add(19, 2, "Ps. 19:1", "The heavens declare the glory of God; and the firmament sheweth his ___", "handywork", "throne", "anger", "sabbath")
    add(19, 2, "Ps. 100:4", "Enter into his gates with thanksgiving, and into his courts with ___", "praise", "fear", "silence", "gold")
    add(19, 1, "Ps. 122:1", "I was glad when they said unto me, Let us go into the house of the ___", "LORD", "king", "prophet", "mighty")
    add(23, 1, "Is. 40:8", "The grass withereth, the flower fadeth: but the word of our God shall stand for ___", "ever", "a generation", "Israel", "a thousand years")
    add(24, 2, "Jer. 17:9", "The heart is deceitful above all things, and desperately ___", "wicked", "weak", "wise", "willing")
    add(33, 2, "Mic. 6:8", "What doth the LORD require of thee, but to do justly, and to love mercy, and to walk ___ with thy God?", "humbly", "boldly", "silently", "quickly")
    add(40, 1, "Matt. 11:28", "Come unto me, all ye that labour and are heavy laden, and I will give you ___", "rest", "gold", "the law", "a crown")
    add(40, 2, "Matt. 5:14", "Ye are the light of the ___", "world", "temple", "Jews", "church only")
    add(40, 2, "Matt. 5:13", "Ye are the salt of the ___", "earth", "covenant only", "sea", "altar")
    add(40, 1, "Matt. 7:7", "Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be ___ unto you", "opened", "shut", "measured", "written")
    add(42, 1, "Luke 2:14", "Glory to God in the highest, and on earth peace, good will toward ___", "men", "Israel only", "angels", "kings")
    add(43, 1, "John 14:27", "Peace I leave with you, my peace I give unto you: not as the world ___", "giveth", "taketh", "knoweth", "seeth")
    add(43, 2, "John 16:33", "In the world ye shall have tribulation: but be of good cheer; I have overcome the ___", "world", "grave only", "law", "devil only")
    add(45, 1, "Rom. 5:8", "While we were yet sinners, Christ died for ___", "us", "the righteous only", "angels", "Israel only")
    add(45, 2, "Rom. 10:9", "If thou shalt confess with thy mouth the Lord Jesus, and shalt believe in thine heart that God hath raised him from the dead, thou shalt be ___", "saved", "baptized", "a Jew", "perfect")
    add(45, 2, "Rom. 10:13", "Whosoever shall call upon the name of the Lord shall be ___", "saved", "healed only", "rich", "a prophet")
    add(46, 2, "1 Cor. 10:13", "God is faithful, who will not suffer you to be tempted above that ye are ___", "able", "willing", "holy", "old")
    add(46, 3, "1 Cor. 15:55", "O death, where is thy sting? O grave, where is thy ___", "victory", "power", "king", "fear")
    add(47, 2, "2 Cor. 5:17", "If any man be in Christ, he is a new ___", "creature", "priest", "nation", "temple of stone")
    add(47, 3, "2 Cor. 12:9", "My grace is sufficient for thee: for my strength is made perfect in ___", "weakness", "wisdom", "wealth", "the law")
    add(50, 2, "Phil. 4:6", "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto ___", "God", "the priest", "Caesar", "the church only")
    add(58, 2, "Heb. 11:6", "Without faith it is impossible to ___ him", "please", "see", "hear", "serve in the temple")
    add(62, 2, "1 John 1:7", "The blood of Jesus Christ his Son cleanseth us from all ___", "sin", "sorrow", "law", "memory")
    add(66, 1, "Rev. 3:20", "If any man hear my voice, and open the door, I will come in to him, and will sup with him", "True — Revelation 3:20", "That is John 3:16", "That is Luke 24", "That is Psalm 23")

    # Extra coverage for thin books
    add(3, 4, "Lev. 16:29", "On what day of the seventh month was the day of atonement?", "The tenth", "The first", "The fifteenth", "The seventh")
    add(21, 4, "Eccl. 11:1", "Cast thy bread upon the waters: for thou shalt find it after many ___", "days", "years", "hours", "sabbaths")
    add(22, 4, "Song 8:6-7", "Many waters cannot quench ___", "love", "wrath", "faith", "hope")
    add(25, 4, "Lam. 3:22", "It is of the LORD's mercies that we are not ___", "consumed", "exiled", "forgotten", "poor")
    add(29, 4, "Joel 2:32", "Whosoever shall call on the name of the LORD shall be ___", "delivered", "rich", "a priest", "a prophet")
    add(30, 4, "Amos 5:24", "Let judgment run down as waters, and righteousness as a mighty ___", "stream", "wall", "army", "fire")
    add(31, 4, "Obad. 1:15", "As thou hast done, it shall be done unto thee: thy reward shall return upon thine own ___", "head", "house", "nation only", "children")
    add(34, 4, "Nah. 1:7", "The LORD is good, a strong hold in the day of ___", "trouble", "battle only", "atonement", "jubile")
    add(36, 4, "Zeph. 3:17", "The LORD thy God in the midst of thee is mighty; he will save, he will rejoice over thee with ___", "joy", "fire", "silence always", "judgment only")
    add(37, 4, "Hag. 2:8", "The silver is mine, and the gold is mine, saith the LORD of ___", "hosts", "Israel only", "heaven only", "the temple")
    add(47, 2, "2 Cor. 9:6", "He which soweth sparingly shall reap also sparingly; and he which soweth bountifully shall reap also ___", "bountifully", "nothing", "judgment", "fame")
    add(53, 2, "2 Thes. 2:15", "Stand fast, and hold the traditions which ye have been ___", "taught", "inventing", "buying", "forbidding")
    add(56, 4, "Titus 3:5", "Not by works of righteousness which we have done, but according to his mercy he ___ us", "saved", "called as Jews", "crowned", "judged")
    add(61, 2, "2 Pet. 3:9", "The Lord is not slack concerning his promise... but is longsuffering to us-ward, not willing that any should ___", "perish", "wait", "pray", "work")
    add(65, 2, "Jude 1:3", "Earnestly contend for the faith which was once delivered unto the ___", "saints", "angels", "priests", "kings")

    # --- more unique items to reach 834 ---
    add(1, 2, "Gen. 4:22", "Who was an instructer of every artificer in brass and iron?", "Tubal-cain", "Jabal", "Jubal", "Naamah")
    add(1, 3, "Gen. 4:21", "Who was the father of all such as handle the harp and organ?", "Jubal", "Jabal", "Tubal-cain", "Enoch")
    add(1, 3, "Gen. 4:20", "Who was the father of such as dwell in tents, and of such as have cattle?", "Jabal", "Jubal", "Tubal-cain", "Lamech")
    add(1, 2, "Gen. 5:32", "How old was Noah when he begat Shem, Ham, and Japheth?", "500", "100", "120", "950")
    add(1, 3, "Gen. 7:2", "Of every clean beast Noah was to take by ___", "sevens", "twos only", "tens", "twelves")
    add(1, 4, "Gen. 10:25", "In whose days was the earth divided?", "Peleg", "Nimrod", "Eber", "Salah")
    add(1, 3, "Gen. 13:11", "Which way did Lot choose?", "The plain of Jordan", "The hills of Hebron", "Egypt", "Haran")
    add(1, 2, "Gen. 14:14", "How many trained servants did Abraham arm to rescue Lot?", "318", "300", "120", "12")
    add(1, 3, "Gen. 15:6", "Abraham believed in the LORD; and he counted it to him for ___", "righteousness", "wisdom", "a son immediately", "land that day")
    add(1, 2, "Gen. 17:10", "What token of the covenant was given to Abraham?", "Circumcision", "A rainbow", "The sabbath", "A lamb")
    add(1, 3, "Gen. 21:8-10", "Who mocked Isaac at his weaning?", "Ishmael", "Esau", "Lot", "Abimelech")
    add(1, 2, "Gen. 24:15", "Who came to the well as Abraham's servant waited?", "Rebekah", "Rachel", "Leah", "Sarah")
    add(1, 3, "Gen. 29:18", "How many years did Jacob serve for Rachel the first time?", "7", "14", "20", "40")
    add(1, 3, "Gen. 31:19", "What did Rachel steal from her father?", "His images (teraphim)", "His gold", "His flocks", "His ring")
    add(1, 4, "Gen. 36:1", "Esau is also called ___", "Edom", "Seir only", "Amalek", "Moab")
    add(1, 3, "Gen. 37:2", "How old was Joseph when he was feeding the flock?", "17", "12", "30", "40")
    add(1, 4, "Gen. 38:29", "Who was Perez's twin, born of Tamar?", "Zarah", "Onan", "Shelah", "Er")
    add(1, 2, "Gen. 48:14", "Which of Joseph's sons received the right-hand blessing?", "Ephraim, the younger", "Manasseh, the elder", "Benjamin", "Reuben")
    add(2, 3, "Ex. 2:10", "Who named the child Moses?", "Pharaoh's daughter", "Jochebed", "Miriam", "Aaron")
    add(2, 3, "Ex. 4:2-4", "What did Moses' rod become?", "A serpent", "A tree", "A sword", "A staff of gold")
    add(2, 2, "Ex. 12:37", "About how many men besides children left Rameses?", "600000", "70000", "12000", "3000")
    add(2, 3, "Ex. 13:21", "How did the LORD go before Israel by day?", "In a pillar of a cloud", "In a pillar of fire", "As an angel only", "As a star")
    add(2, 2, "Ex. 17:6", "From what did water come at Horeb the first time?", "A rock that Moses smote", "A well Abraham dug", "The Nile", "A cloud")
    add(2, 4, "Ex. 24:18", "How many days was Moses in the mount?", "40", "7", "12", "3")
    add(2, 3, "Ex. 34:29", "What shone when Moses came down with the tables?", "The skin of his face", "His rod", "The tables themselves", "His garments")
    add(3, 3, "Lev. 19:18", "Thou shalt love thy neighbour as ___", "thyself", "the LORD", "a stranger", "a brother only")
    add(3, 2, "Lev. 23:34", "The feast of tabernacles is in the ___ month", "seventh", "first", "third", "twelfth")
    add(4, 2, "Num. 11:16", "How many elders helped Moses bear the burden?", "70", "12", "40", "7")
    add(4, 3, "Num. 13:23", "What fruit did the spies bring from Eshcol?", "A cluster of grapes", "Pomegranates only", "Figs only", "Olives")
    add(4, 4, "Num. 17:8", "Whose rod budded, bloomed, and yielded almonds?", "Aaron's", "Moses'", "Korah's", "Joshua's")
    add(5, 2, "Deut. 8:3", "Man doth not live by bread only, but by every word that proceedeth out of the mouth of the ___", "LORD", "priest", "king", "prophet")
    add(5, 3, "Deut. 31:9", "Who wrote this law and delivered it unto the priests?", "Moses", "Joshua", "Eleazar", "Samuel")
    add(6, 2, "Josh. 4:20", "How many stones were set up in Gilgal from Jordan?", "12", "7", "10", "40")
    add(6, 3, "Josh. 5:12", "What ceased the day after they ate of the old corn of the land?", "Manna", "The pillar of cloud", "The Jordan's flood", "Quails")
    add(6, 4, "Josh. 20:2", "What cities were appointed for the manslayer?", "Cities of refuge", "Levitical barns", "Royal cities", "Store cities")
    add(7, 2, "Judg. 6:15", "Of what family did Gideon say he was the least?", "Manasseh / Abiezer", "Judah", "Ephraim", "Benjamin")
    add(7, 3, "Judg. 8:27", "What did Gideon make that became a snare?", "An ephod", "A golden calf", "A high place", "A fleece idol")
    add(9, 2, "1 Sam. 7:12", "What did Samuel name the stone of help?", "Ebenezer", "Bethel", "Mizpeh", "Gilgal")
    add(9, 3, "1 Sam. 16:23", "What did David play to refresh Saul?", "A harp", "A trumpet", "A psaltery only", "Cymbals")
    add(10, 2, "2 Sam. 9:7", "Whom did David show kindness for Jonathan's sake?", "Mephibosheth", "Ishbosheth", "Ziba", "Absalom")
    add(10, 3, "2 Sam. 15:12", "Who was David's counsellor that joined Absalom?", "Ahithophel", "Hushai", "Joab", "Abiathar")
    add(11, 2, "1 Ki. 4:32", "How many proverbs did Solomon speak?", "3000", "1005", "150", "700")
    add(11, 3, "1 Ki. 4:32", "How many songs did Solomon write?", "1005", "3000", "150", "22")
    add(11, 4, "1 Ki. 7:23", "What sea did Solomon make for the temple court?", "A molten sea", "The brazen laver of Moses only", "A pool of Siloam", "The great deep")
    add(12, 2, "2 Ki. 4:34", "How did Elisha raise the Shunammite's son?", "He stretched himself upon the child", "He called from outside", "He used a staff only", "He washed him in Jordan")
    add(12, 3, "2 Ki. 13:21", "What happened when a dead man touched Elisha's bones?", "He revived, and stood up", "The bones burned", "Nothing", "A dove appeared")
    add(15, 3, "Ezra 8:22", "Why was Ezra ashamed to ask the king for a band of soldiers?", "He had told the king the hand of God was upon them", "He had no gold", "The king forbade it", "The Levites refused")
    add(16, 2, "Neh. 4:17", "They which builded on the wall... with one of his hands wrought in the work, and with the other hand held a ___", "weapon", "trowel only", "scroll", "trumpet")
    add(17, 3, "Est. 4:16", "How many days did Esther ask the Jews to fast?", "3", "7", "40", "12")
    add(18, 3, "Job 1:3", "How many sheep did Job have at the first?", "7000", "3000", "1000", "500")
    add(18, 4, "Job 42:12", "How many sheep did Job have at the last?", "14000", "7000", "6000", "1000")
    add(19, 2, "Ps. 8:4", "What is man, that thou art mindful of him? and the son of man, that thou ___ him?", "visitest", "judgest", "forgettest", "crownedst with gold only")
    add(19, 3, "Ps. 42:1", "As the hart panteth after the water brooks, so panteth my soul after ___", "thee, O God", "Zion", "the temple courts", "rain")
    add(19, 2, "Ps. 51:10", "Create in me a clean heart, O God; and renew a right spirit within ___", "me", "Israel", "the king", "thy house")
    add(19, 3, "Ps. 84:10", "A day in thy courts is better than a ___", "thousand", "sabbath", "year in palaces", "lifetime")
    add(19, 2, "Ps. 103:12", "As far as the east is from the west, so far hath he removed our ___ from us", "transgressions", "tears", "enemies", "fears")
    add(19, 3, "Ps. 119:11", "Thy word have I hid in mine heart, that I might not sin against ___", "thee", "man", "the king", "my neighbour")
    add(19, 1, "Ps. 139:14", "I will praise thee; for I am fearfully and wonderfully ___", "made", "saved", "crowned", "taught")
    add(20, 2, "Prov. 16:18", "Pride goeth before destruction, and an haughty spirit before a ___", "fall", "crown", "storm", "famine")
    add(20, 3, "Prov. 18:10", "The name of the LORD is a strong ___", "tower", "wall", "sword", "shield only")
    add(20, 2, "Prov. 27:1", "Boast not thyself of to morrow; for thou knowest not what a day may bring ___", "forth", "thee", "of rain", "of gold")
    add(23, 2, "Is. 1:18", "Though your sins be as scarlet, they shall be as white as ___", "snow", "wool only in this half", "light", "linen")
    add(23, 3, "Is. 26:3", "Thou wilt keep him in perfect peace, whose mind is stayed on ___", "thee", "the law", "Zion", "the temple")
    add(23, 2, "Is. 41:10", "Fear thou not; for I am with thee: be not dismayed; for I am thy ___", "God", "king", "priest", "shepherd only")
    add(23, 3, "Is. 55:8", "My thoughts are not your thoughts, neither are your ways my ___", "ways", "laws", "sabbaths", "feasts")
    add(24, 3, "Jer. 20:9", "His word was in mine heart as a burning ___ shut up in my bones", "fire", "coal", "lamp", "scroll")
    add(26, 3, "Ez. 36:26", "A new heart also will I give you, and a new spirit will I put within you: and I will take away the stony heart... and I will give you an heart of ___", "flesh", "gold", "faith", "stone still")
    add(27, 2, "Dan. 2:44", "In the days of these kings shall the God of heaven set up a kingdom, which shall never be ___", "destroyed", "divided", "translated", "numbered")
    add(32, 2, "Jon. 1:7", "How did the mariners find Jonah was the cause?", "They cast lots", "A dove landed on him", "He confessed first", "The fish spoke")
    add(40, 2, "Matt. 5:16", "Let your light so shine before men, that they may see your good works, and glorify your Father which is in ___", "heaven", "the temple", "Israel", "secret")
    add(40, 3, "Matt. 6:33", "Seek ye first the kingdom of God, and his righteousness; and all these things shall be ___ unto you", "added", "taken", "hidden", "sold")
    add(40, 2, "Matt. 16:16", "Whom did Peter confess Jesus to be?", "The Christ, the Son of the living God", "Elias", "Jeremiah", "John the Baptist")
    add(40, 3, "Matt. 16:18", "Upon this rock I will build my ___; and the gates of hell shall not prevail against it", "church", "temple", "nation", "throne")
    add(40, 2, "Matt. 18:20", "Where two or three are gathered together in my name, there am I in the midst of ___", "them", "the temple", "the angels", "the world")
    add(40, 3, "Matt. 22:37-39", "Which is the second great commandment in Matthew 22?", "Thou shalt love thy neighbour as thyself", "Remember the sabbath", "Pay tithe", "Honor the king")
    add(40, 2, "Matt. 24:35", "Heaven and earth shall pass away, but my words shall not pass ___", "away", "the temple", "Israel", "this generation only")
    add(40, 3, "Matt. 28:18", "All power is given unto me in heaven and in ___", "earth", "the church only", "Israel", "the grave only")
    add(41, 2, "Mark 8:29", "Whom do men say that I am? Peter answered, Thou art the ___", "Christ", "Baptist", "Elias", "one of the prophets")
    add(41, 3, "Mark 9:23", "If thou canst believe, all things are possible to him that ___", "believeth", "fasteth", "giveth", "seeth")
    add(42, 2, "Luke 4:8", "Thou shalt worship the Lord thy God, and him only shalt thou ___", "serve", "fear in secret", "name", "see")
    add(42, 3, "Luke 6:31", "As ye would that men should do to you, do ye also to them ___", "likewise", "first", "in the temple", "if they pay")
    add(42, 2, "Luke 9:23", "If any man will come after me, let him deny himself, and take up his cross ___", "daily", "once", "on the sabbath", "in Jerusalem only")
    add(42, 3, "Luke 12:34", "Where your treasure is, there will your heart be ___", "also", "safe", "hidden", "judged")
    add(43, 2, "John 1:29", "Behold the Lamb of God, which taketh away the sin of the ___", "world", "Jews only", "temple", "priests")
    add(43, 3, "John 4:24", "God is a Spirit: and they that worship him must worship him in spirit and in ___", "truth", "Jerusalem", "this mountain", "the law")
    add(43, 2, "John 8:32", "Ye shall know the truth, and the truth shall make you ___", "free", "wise", "rich", "priests")
    add(43, 3, "John 13:34", "A new commandment I give unto you, That ye love one ___", "another", "the law", "your enemies only", "the temple")
    add(43, 2, "John 15:13", "Greater love hath no man than this, that a man lay down his life for his ___", "friends", "king", "nation only", "family only")
    add(44, 3, "Acts 4:12", "Neither is there salvation in any other: for there is none other name under heaven given among men, whereby we must be ___", "saved", "healed", "named", "numbered")
    add(44, 2, "Acts 16:31", "Believe on the Lord Jesus Christ, and thou shalt be saved, and thy ___", "house", "nation", "city", "goods")
    add(45, 3, "Rom. 8:1", "There is therefore now no condemnation to them which are in Christ Jesus, who walk not after the flesh, but after the ___", "Spirit", "law", "temple", "elders")
    add(45, 2, "Rom. 12:21", "Be not overcome of evil, but overcome evil with ___", "good", "force", "the law", "silence")
    add(46, 2, "1 Cor. 15:57", "Thanks be to God, which giveth us the victory through our Lord ___", "Jesus Christ", "the law", "Moses", "the apostles")
    add(47, 3, "2 Cor. 4:18", "We look not at the things which are seen, but at the things which are not seen: for the things which are seen are temporal; but the things which are not seen are ___", "eternal", "hidden", "legal", "Israel's")
    add(48, 3, "Gal. 3:28", "There is neither Jew nor Greek, there is neither bond nor free, there is neither male nor female: for ye are all one in ___", "Christ Jesus", "the law", "Abraham only", "Rome")
    add(49, 3, "Eph. 4:32", "Be ye kind one to another, tenderhearted, forgiving one another, even as God for Christ's sake hath forgiven ___", "you", "Israel", "the angels", "Adam")
    add(50, 3, "Phil. 2:10-11", "Every knee should bow... and every tongue should confess that Jesus Christ is Lord, to the glory of God the ___", "Father", "Spirit only", "church", "law")
    add(51, 3, "Col. 3:23", "Whatsoever ye do, do it heartily, as to the Lord, and not unto ___", "men", "angels", "Caesar", "the flesh")
    add(54, 3, "1 Tim. 6:12", "Fight the good fight of ___", "faith", "Rome", "the Jews", "words")
    add(58, 3, "Heb. 10:25", "Not forsaking the assembling of ourselves together, as the manner of some is; but exhorting one another: and so much the more, as ye see the day ___", "approaching", "ending", "hidden", "of atonement")
    add(59, 2, "James 4:7", "Submit yourselves therefore to God. Resist the devil, and he will ___ from you", "flee", "laugh", "fight", "hide")
    add(60, 3, "1 Pet. 1:16", "Be ye holy; for I am ___", "holy", "your king", "jealous", "the LORD of hosts only")
    add(62, 3, "1 John 5:11", "This is the record, that God hath given to us eternal life, and this life is in his ___", "Son", "law", "temple", "name only")
    add(66, 3, "Rev. 21:4", "God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more ___", "pain", "sea only", "night only", "temple")
    add(66, 2, "Rev. 22:17", "The Spirit and the bride say, ___", "Come", "Wait", "Fear", "Hide")

    return f


def shuffle_answers(correct: str, wrongs: list[str], key: str) -> tuple[str, list[str]]:
    opts = [correct] + list(wrongs)
    seed = int(hashlib.md5(key.encode()).hexdigest(), 16)
    # stable shuffle
    for i in range(len(opts) - 1, 0, -1):
        j = seed % (i + 1)
        seed = seed // (i + 1) ^ (seed << 3)
        opts[i], opts[j] = opts[j], opts[i]
    letter = "ABCD"[opts.index(correct)]
    return letter, opts


def load_original() -> list[list[str]]:
    with SRC.open(newline="") as f:
        return [row for row in csv.reader(f) if row]


def main() -> int:
    original = load_original()
    seen = {norm(r[4]) for r in original if len(r) >= 5}
    extra: list[list[str]] = []
    skipped_dup = 0
    for canon, kind, ref, q, correct, w1, w2, w3 in facts():
        if norm(q) in seen:
            skipped_dup += 1
            continue
        if any(not x.strip() for x in (q, correct, w1, w2, w3, ref)):
            continue
        if '"' in q or any('"' in x for x in (correct, w1, w2, w3)):
            q = q.replace('"', "'")
            correct = correct.replace('"', "'")
            w1, w2, w3 = (x.replace('"', "'") for x in (w1, w2, w3))
        letter, opts = shuffle_answers(correct, [w1, w2, w3], q)
        row = [
            f"C{canon:02d}",
            str(kind),
            letter,
            ref,
            q,
            *opts,
        ]
        extra.append(row)
        seen.add(norm(q))

    chosen: list[list[str]] = []
    for r in extra:
        if len(original) + len(chosen) >= TARGET:
            break
        chosen.append(r)

    out_rows = original + chosen
    if len(out_rows) > TARGET:
        out_rows = out_rows[:TARGET]
    if len(out_rows) < TARGET:
        print(f"only generated {len(out_rows)} (existing {len(original)}, extra unique {len(extra)}, skipped dups {skipped_dup})", file=sys.stderr)

    with OUT.open("w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        for r in out_rows:
            w.writerow(r)

    kinds = {1: 0, 2: 0, 3: 0, 4: 0}
    ot = nt = 0
    for r in out_rows:
        kinds[int(r[1])] += 1
        n = int(r[0][1:])
        if n <= 39:
            ot += 1
        else:
            nt += 1
    print(f"wrote {len(out_rows)} questions to {OUT}")
    print(f"  kinds 1-4: {kinds[1]}/{kinds[2]}/{kinds[3]}/{kinds[4]}")
    print(f"  OT {ot}  NT {nt}")
    print(f"  unique extra generated {len(extra)}, skipped dups {skipped_dup}")
    if len(out_rows) != TARGET:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
