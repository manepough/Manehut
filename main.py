import asyncio
import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────────
OWNER_ID  = 1456322226491101224
WHITELIST = {OWNER_ID}

# Tokens loaded from .env
BOT_TOKENS = [t for t in [
    os.getenv("TOKEN_1"),
    os.getenv("TOKEN_2"),
    os.getenv("TOKEN_3"),
    os.getenv("TOKEN_4"),
    os.getenv("TOKEN_5"),
] if t]

# ── Helpers ────────────────────────────────────────────────────────────────────
def is_allowed(uid): return uid in WHITELIST
def not_allowed_msg(): return "fuck u nigga u ain't my owner"

# ── Spam panel — one per bot instance ─────────────────────────────────────────
class SpamPanel(discord.ui.View):
    def __init__(self, message: str, bot_instance: commands.Bot):
        super().__init__(timeout=None)
        self.message      = message
        self.bot          = bot_instance
        self.is_spamming  = False
        self.task: asyncio.Task | None = None
        self.webhook: discord.Webhook | None = None  # stored from START interaction
        self._refresh()

    def _refresh(self):
        self.clear_items()
        if self.is_spamming:
            btn = discord.ui.Button(label="STOP", style=discord.ButtonStyle.danger, emoji="🛑")
            self.status_text = "🟢 SPAMMING"
        else:
            btn = discord.ui.Button(label="START", style=discord.ButtonStyle.success, emoji="▶️")
            self.status_text = "🔴 Stopped"
        btn.callback = self._toggle
        self.add_item(btn)

    async def _toggle(self, interaction: discord.Interaction):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(not_allowed_msg(), ephemeral=True)

        if not self.is_spamming:
            self.is_spamming = True
            self._refresh()
            await interaction.response.edit_message(
                content=f"**{self.status_text}**\nMessage: `{self.message}`", view=self
            )

            followup = interaction.followup

            async def loop():
                try:
                    while self.is_spamming:
                        try:
                            await followup.send(self.message)
                        except Exception as e:
                            print(f"[{self.bot.user.name}] send error: {e}")
                            await asyncio.sleep(1)
                            continue
                        await asyncio.sleep(0.5)
                except asyncio.CancelledError:
                    pass

            self.task = asyncio.create_task(loop())
        else:
            self.is_spamming = False
            if self.task and not self.task.done():
                self.task.cancel()
            self._refresh()
            await interaction.response.edit_message(
                content=f"**{self.status_text}**\nMessage: `{self.message}`", view=self
            )

# ── Ghost ping panel ───────────────────────────────────────────────────────────
class GhostPingPanel(discord.ui.View):
    def __init__(self, target: discord.User):
        super().__init__(timeout=120)
        self.target = target

    @discord.ui.button(label="Ghost Ping x1", style=discord.ButtonStyle.danger)
    async def ghost_once(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(not_allowed_msg(), ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        try:
            msg = await interaction.followup.send(self.target.mention)
            await msg.delete()
            await interaction.followup.send("Ghost ping sent.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Failed: {e}", ephemeral=True)

    @discord.ui.button(label="Ghost Ping x5", style=discord.ButtonStyle.danger)
    async def ghost_five(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(not_allowed_msg(), ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        sent = 0
        for _ in range(5):
            try:
                msg = await interaction.followup.send(self.target.mention)
                await msg.delete()
                sent += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Ghost ping error: {e}")
                break
        await interaction.followup.send(f"Ghost pinged {sent}/5.", ephemeral=True)

# ── 500 unique jokes, 100 per bot ─────────────────────────────────────────────
BOT_JOKES = [
    # ── Bot 1 — Classic one-liners ────────────────────────────────────────────
    [
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't scientists trust atoms? Because they make up everything.",
        "I asked my dog what 2 minus 2 is. He said nothing.",
        "I'm reading a book about anti-gravity. It's impossible to put down.",
        "Why did the scarecrow win an award? He was outstanding in his field.",
        "What do you call a fake noodle? An impasta.",
        "Why did the bicycle fall over? It was two-tired.",
        "I would tell you a construction joke, but I'm still working on it.",
        "What do you call cheese that isn't yours? Nacho cheese.",
        "Why can't you give Elsa a balloon? She'll let it go.",
        "I used to hate facial hair, but then it grew on me.",
        "What do you call a sleeping dinosaur? A dino-snore.",
        "Why did the math book look so sad? Because it had too many problems.",
        "I'm on a seafood diet. I see food and I eat it.",
        "What do you call a fish without eyes? A fsh.",
        "Why did the golfer bring extra pants? In case he got a hole in one.",
        "What do you call a belt made of watches? A waist of time.",
        "I tried to write a joke about clocks but it was too time-consuming.",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "What do you call a lazy kangaroo? A pouch potato.",
        "Why did the invisible man turn down the job? He couldn't see himself doing it.",
        "What do you call an alligator in a vest? An investigator.",
        "Why did the coffee file a police report? It got mugged.",
        "What do you call a bear with no teeth? A gummy bear.",
        "I told my doctor I broke my arm in two places. He told me to stop going to those places.",
        "Why did the tomato turn red? Because it saw the salad dressing.",
        "What do you call a snowman with a six-pack? An abdominal snowman.",
        "Why don't scientists trust stairs? Because they're always up to something.",
        "I have a joke about paper, but it's tearable.",
        "Why did the gym close down? It just didn't work out.",
        "What do you call a fake stone? A shamrock.",
        "Why do cows wear bells? Because their horns don't work.",
        "What do you call a dinosaur with an extensive vocabulary? A thesaurus.",
        "Why did the student eat his homework? Because the teacher told him it was a piece of cake.",
        "What do you call a pig that does karate? A pork chop.",
        "Why did the banana go to the doctor? It wasn't peeling well.",
        "What do you call a cow with no legs? Ground beef.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call a shoe made from a banana? A slipper.",
        "Why did the stadium get hot after the game? All the fans left.",
        "What do you call a lazy pebble? A bedrock.",
        "Why don't oysters share? Because they're shellfish.",
        "What do you call a dog that does magic? A labracadabrador.",
        "Why did the picture go to jail? Because it was framed.",
        "What do you call a train that sneezes? Achoo-choo train.",
        "Why did the golfer bring a pencil? To draw a hole in one.",
        "What do you call a sleeping bull? A bulldozer.",
        "Why did the barber win the race? He knew all the shortcuts.",
        "What do you call a can opener that doesn't work? A can't opener.",
        "Why did the clock get kicked out of school? It tocked too much.",
        "What do you call a pile of cats? A meowtain.",
        "Why do bees have sticky hair? Because they use honeycombs.",
        "What do you call a fish that wears a crown? King of the sea bass.",
        "Why did the computer go to the doctor? It had a virus.",
        "What do you call a lazy cat? A napkin.",
        "Why did the orange stop rolling downhill? It ran out of juice.",
        "What do you call a nervous javelin thrower? Shakespeare.",
        "Why did the teddy bear say no to dessert? She was already stuffed.",
        "What do you call a book club that's been stuck on one book for years? Club med.",
        "Why did the cookie go to the nurse? It was feeling crummy.",
        "What do you call a singing laptop? A Dell.",
        "Why did the golfer wear two pairs of pants? In case he got a hole in one.",
        "What do you call a ghost's mom? A transparents.",
        "Why did the frog take the bus? His car got toad.",
        "What do you call a broken can opener? A hand.",
        "Why did the cow go to outer space? To see the Milky Way.",
        "What do you call a hen who counts her eggs? A mathemachicken.",
        "Why did the shoe go to therapy? It had too many problems with its sole.",
        "What do you call a rabbit that's really funny? A funny bunny.",
        "Why did the witch go to school? To improve her spelling.",
        "What do you call a penguin in the desert? Lost.",
        "Why did the calendar feel popular? Because its days were numbered.",
        "What do you call a tree that fits in your hand? A palm tree.",
        "Why did the music teacher need a ladder? To reach the high notes.",
        "What do you call a boomerang that doesn't come back? A stick.",
        "Why was the broom late? It swept in.",
        "What do you call a duck that gets good grades? A wise quacker.",
        "Why did the scarecrow become a motivational speaker? He was outstanding in his field.",
        "What do you call a sleeping T-Rex? A dino-snore.",
        "Why did the nurse need a red pen? In case she needed to draw blood.",
        "What do you call a hippie's wife? Mississippi.",
        "Why did the sailor fail school? He was below C level.",
        "What do you call a man lying in a pile of leaves? Russell.",
        "Why did the astronaut break up with his girlfriend? He needed some space.",
        "What do you call a parade of rabbits hopping backward? A receding hare line.",
        "Why did the lamp fail its test? It wasn't very bright.",
        "What do you call a cold dog? A chili dog.",
        "Why did the leopard get lost? Because everything looks the same in spots.",
        "What do you call a noodle that's a secret agent? A spaghetti spy.",
        "Why don't mountains get cold in winter? They wear snowcaps.",
        "What do you call a pony with a sore throat? A little hoarse.",
        "Why did the tomato blush? It saw the salad dressing.",
        "What do you call a boat that's always on time? Punctual.",
        "Why did the belt go to jail? For holding up a pair of pants.",
        "What do you call a bee that can't make up its mind? A may-bee.",
        "Why did the electrician close his shop? Business was too shocking.",
        "What do you call a very small valentine? A valen-tiny.",
        "Why did the lemon stop halfway across the road? It ran out of juice.",
        "What do you call a cheese factory explosion? A disaster.",
        "Why did the golfer wear a helmet? He was afraid of the clubs.",
    ],
    # ── Bot 2 — Dark/dry humor ────────────────────────────────────────────────
    [
        "My wife told me I had to stop acting like a flamingo. I had to put my foot down.",
        "I asked my North Korean friend how life was there. He said he couldn't complain.",
        "I told my boss I needed a raise because three companies were after me. He asked which ones. I said gas, water, and electricity.",
        "My therapist says I have trouble accepting things I can't control. We'll see about that.",
        "I bought some shoes from a drug dealer. Don't know what he laced them with, but I was tripping all day.",
        "My wife said I needed to grow up. I was speechless. It's hard to say anything when you've got 45 gummy bears in your mouth.",
        "I have many jokes about unemployed people, but none of them work.",
        "I told my doctor I think I'm addicted to Twitter. He said sorry, he doesn't follow me.",
        "My wife left a note on the fridge: 'This isn't working.' I opened it. The fridge was fine.",
        "I don't trust stairs. They're always up to something.",
        "Someone stole my mood ring. I don't know how I feel about that.",
        "I refused to believe my road worker dad was stealing from his job, but when I got home all the signs were there.",
        "I used to be addicted to soap, but I'm clean now.",
        "My friend keeps saying 'cheer up, it could be worse, you could be stuck underground in a hole full of water.' I know he means well.",
        "I went to buy some camouflage trousers, but I couldn't find any.",
        "I'm writing a book on reverse psychology. Please don't buy it.",
        "I tried to come up with a joke about social distancing, but this is as close as I could get.",
        "My wife told me I was immature. I told her to get out of my fort.",
        "Why did I get divorced? My wife said I was too immature. Well, no girls allowed in my tree house anyway.",
        "I have a joke about construction but I'm still building it.",
        "I was going to tell a joke about time travel, but you didn't like it.",
        "My doctor told me I was going deaf. That was hard to hear.",
        "I told my wife she should embrace her mistakes. She hugged me.",
        "I broke my finger last week. On the other hand, I'm okay.",
        "My wife said I should do lunges to stay in shape. That would be a big step forward.",
        "I couldn't figure out why the baseball kept getting bigger. Then it hit me.",
        "The rotation of the earth really makes my day.",
        "I used to be a banker, but I lost interest.",
        "I stayed up all night to see where the sun went. Then it dawned on me.",
        "Did I tell you the one about the roof? Never mind, it's over your head.",
        "I'm reading a horror story in Braille. Something bad is about to happen, I can feel it.",
        "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
        "I entered ten puns in a joke contest, hoping one would win. No pun in ten did.",
        "I used to think I was indecisive, but now I'm not so sure.",
        "I have a joke about paper. It's tearable.",
        "What do you call a man with a rubber toe? Roberto.",
        "I told my cat a joke. He didn't laugh. He's a tough crowd.",
        "My wife asked me to stop singing Wonderwall. I said maybe.",
        "I couldn't remember how to throw a boomerang, but it came back to me.",
        "I told the doctor I hurt myself in several places. He told me to stop going to those places.",
        "My friend asked me to name two structures that hold water. I was like, 'Well, dam.'",
        "I wasn't originally going to get a brain transplant, but I changed my mind.",
        "I saw an ad for burial plots, and thought: that's the last thing I need.",
        "What do you call a fish without eyes? A fsh.",
        "I'm addicted to collecting vintage Beatles albums. I need Help.",
        "I was wondering why the frisbee was getting bigger. Then it hit me.",
        "My wife said I should do more around the house. So I bought a new chair.",
        "What do you call a man with no body and no nose? Nobody knows.",
        "I used to work in a shoe recycling shop. It was sole destroying.",
        "My wife and I laugh about how competitive we are. But I laugh more.",
        "I have a joke about elevators. It works on so many levels.",
        "My boss told me to have a good day, so I went home.",
        "I told my suitcase there would be no vacation this year. Now I'm dealing with emotional baggage.",
        "I quit my job at the helium factory. I refused to be talked to in that tone.",
        "I have a fear of speed bumps. I'm slowly getting over it.",
        "Someone threw cheese at me. Real mature.",
        "I know a lot of jokes about retired people, but none of them work.",
        "What do you call an elephant that doesn't matter? Irrelephant.",
        "I was going to make a vegetable pun, but that would be corny.",
        "I have a lot of growing up to do. I realized that the other day inside my fort.",
        "My wife is on a tropical diet. All she eats is coconuts and bananas. She hasn't lost weight, but she can climb a tree now.",
        "I told my doctor I broke my leg in two places. He told me to quit going to those places.",
        "What do you call a factory that makes okay products? A satisfactory.",
        "I'm reading a book on the history of glue. I can't put it down.",
        "I asked the librarian if they had books about paranoia. She whispered, 'They're right behind you.'",
        "I used to play piano by ear, but now I use my hands.",
        "My wife and I have a code word for when we want the other to stop talking. It's 'please'.",
        "I told my son I was named after Thomas Jefferson. He said, 'But Dad, your name is Kevin.' I said, 'I know, but I was named AFTER him.'",
        "I tried a new restaurant called Karma. There was no menu — you just get what you deserve.",
        "My psychiatrist told me I was crazy. I said I want a second opinion. He said okay, you're ugly too.",
        "I went to a bookstore and asked where the self-help section was. The guy said if he told me it would defeat the purpose.",
        "Why is it called tourist season if we can't shoot at them?",
        "I always wanted to be somebody, but now I realize I should have been more specific.",
        "My bank says I have outstanding balance. I appreciate the compliment.",
        "The problem with kleptomaniacs is that they always take things literally.",
        "I have a joke about insomnia, but I'll save it for later.",
        "I wrote a song about a tortilla. Actually, it's more of a wrap.",
        "I told my wife she should do squats. She said she didn't want to squat anywhere near me.",
        "Some people think I'm addicted to somersaults but that's just how I roll.",
        "I used to hate seatbelts, but now I'm buckled down on my opinion.",
        "My cat was just sick on the carpet. I don't think it's feline well.",
        "I told my wife she was drawing her eyebrows too low. She looked angry.",
        "What do you call a can of soup that's also a police officer? Alphabet cop.",
        "I keep trying to lose weight but it keeps finding me.",
        "What's the difference between a hippo and a zippo? One is really heavy, the other is a little lighter.",
        "I went on a once-in-a-lifetime vacation. I'll tell you, never again.",
        "I told my son I was adopted. He said, 'I knew it, you're too cool to be my real dad.'",
        "My wife asked me how I wanted my birthday cake. I said in my belly.",
        "I have a joke about infinity, but I don't know where to start.",
        "I asked my wife if I was the only one she'd ever been with. She said yes, all the others were nines and tens.",
        "What do you call a man with a seagull on his head? Cliff.",
        "Why did the scarecrow get promoted? Because he was outstanding in his field.",
        "I have a joke about time zones, but it's past your bedtime.",
        "I told a joke about chemistry. No reaction.",
        "My doctor told me I had to watch my drinking. Now I do it in front of a mirror.",
        "I have an inferiority complex, but it's not a very good one.",
        "I'm reading a book on the history of cheese. It's quite gouda.",
        "My wife said I should treat her like a princess. So I married her off to a stranger for political stability.",
    ],
    # ── Bot 3 — Dad jokes ─────────────────────────────────────────────────────
    [
        "I'm afraid for the calendar. Its days are numbered.",
        "My wife is really mad at the fact that I have no sense of direction. So I packed up my stuff and right.",
        "How do you follow Will Smith in the snow? You follow the fresh prints.",
        "Why do fathers take an extra pair of socks when they go golfing? In case they get a hole in one!",
        "What do a tick and the Eiffel Tower have in common? They're both Paris sites.",
        "What do you call it when a snowman throws a tantrum? A meltdown.",
        "Dear Math, grow up and solve your own problems.",
        "5/4 of people admit they're bad with fractions.",
        "I could tell a joke about pizza, but it's a little cheesy.",
        "I only know 25 letters of the alphabet. I don't know y.",
        "Why did the Oreo go to the dentist? Because it lost its filling.",
        "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
        "I've been trying to come up with a dad joke about momentum. I'm working on it.",
        "What do you call a factory that makes mediocre products? A satisfactory.",
        "I don't trust atoms. They make up everything.",
        "What do you get when you cross a snowman and a vampire? Frostbite.",
        "I thought about going on an all-almond diet. But that's just nuts.",
        "Why do we tell actors to break a leg? Because every play has a cast.",
        "Sundays are always a little sad, but the day before is a sadder day.",
        "What do you call someone with no body and no nose? Nobody knows.",
        "I was going to tell a dad joke but I'm not your dad yet. Give it time.",
        "Did you hear about the kidnapping at school? It's okay, he woke up.",
        "What do you call a bee that can't make up its mind? A maybe.",
        "I'm reading a book about teleportation. It's bound to take me places.",
        "What did the ocean say to the beach? Nothing, it just waved.",
        "I got hit in the head with a can of Diet Coke. Don't worry, it was a soft drink.",
        "A skeleton walks into a bar. Orders a beer and a mop.",
        "What do you call an elephant that doesn't matter? Irrelephant.",
        "What did the big flower say to the little flower? Hey, bud.",
        "Why can't you trust the king of the jungle? Because he's always lion.",
        "I told my son I was named after George Washington. He said that's impossible. I said of course, it happened before you were born.",
        "What did the janitor say when he jumped out of the closet? Supplies!",
        "Have you heard about the new broom? It's sweeping the nation.",
        "Why don't scientists trust atoms? Because they make up everything.",
        "What do lawyers wear to court? Lawsuits.",
        "I asked my dog what two minus two is. He said nothing.",
        "What do you call a deer with no eyes? No idea.",
        "What do you call a deer with no eyes and no legs? Still no idea.",
        "What's a vampire's favorite fruit? A blood orange.",
        "Why can't Elsa have a balloon? Because she'll let it go.",
        "What did the zero say to the eight? Nice belt.",
        "I gave all my dead batteries away today. Free of charge.",
        "What do you call a fish that wears a bowtie? Sofishticated.",
        "I'm on a seafood diet. Every time I see food, I eat it.",
        "What do you call a sleeping triceratops? A dino-snore.",
        "Why did the math teacher open a bakery? Because he kneaded dough.",
        "I have a joke about construction, but I'm still building up to it.",
        "What do you call a monkey that loves potato chips? A chipmunk.",
        "How do you organize a space party? You planet.",
        "I tried to make a belt out of watches. It was a waist of time.",
        "Did you hear about the guy who invented Lifesavers? He made a mint.",
        "What do you call a hen who counts her eggs? A mathema-chicken.",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "What do you call a pudgy psychic? A four-chin teller.",
        "I used to hate facial hair, but then it grew on me.",
        "Did you hear about the new restaurant on the moon? Great food, no atmosphere.",
        "Why don't scientists trust stairs? Because they're always up to something.",
        "I used to work at a calendar factory but I got fired because I took a couple of days off.",
        "What did the grape do when it got stepped on? It let out a little wine.",
        "Why did the nurse need a red pen? In case she needed to draw blood.",
        "What do you call a panda that's always breaking the rules? A rebel without a claws.",
        "I'm reading a great book about anti-gravity. It's impossible to put down.",
        "What did the left eye say to the right eye? Between us, something smells.",
        "Why do cows wear bells? Because their horns don't work.",
        "What do you call a man who can't stand? Neil.",
        "I used to hate clocks, but now I find them quite handy.",
        "What's a skeleton's least favorite room in the house? The living room.",
        "I have a joke about wind, but it blows.",
        "Why did the golfer bring two pairs of trousers? In case he got a hole in one.",
        "What do you call two octopuses that look the same? Itentacle.",
        "Why did the stadium get so hot? Because all the fans left.",
        "I asked my cat if he was enjoying the book. He said it was purrfect.",
        "What do you call a bee that lives in America? A USB.",
        "I have a joke about paper towels, but it's really absorbing.",
        "Why did the invisible man turn down the job offer? He just couldn't see himself doing it.",
        "What do you call a nervous javelin thrower? Shakespeare.",
        "My wife told me I should do lunges. That would be a big step forward.",
        "What do you call a priest that becomes a lawyer? Father in law.",
        "Why don't seagulls fly over bays? Because then they'd be bagels.",
        "What do you call a rabbit comedian? A funny bunny.",
        "I tried to write a joke about elevators. It's an uplifting experience.",
        "What's the best time to go to the dentist? Tooth-hurty.",
        "Why do bees have sticky hair? Because they use honeycombs.",
        "What do you call a shoe made from a banana? A slipper.",
        "I tried to catch some fog earlier. I mist.",
        "What do you call a zombie who cooks stir fry? Dead wok-ing.",
        "Why can't a nose be 12 inches long? Because then it'd be a foot.",
        "What do you call a sleeping dinosaur? A dino-snore.",
        "What do you call a pig that does karate? A pork chop.",
        "Did you hear the rumor about butter? Well, I'm not going to spread it.",
        "What do you call a bear with no teeth? A gummy bear.",
        "I'm reading a book about mazes. I got lost in it.",
        "What do you call a man with a rubber toe? Roberto.",
        "Why did the cookie cry? Because its mother was a wafer so long.",
        "What do you call an alligator in a vest? An investi-gator.",
        "What do you call a cow with no legs? Ground beef.",
        "Why couldn't the bicycle stand on its own? It was two-tired.",
        "What do you call a dinosaur that crashes their car? Tyrannosaurus wrecks.",
        "I would avoid the sushi if I were you. It's a little fishy.",
    ],
    # ── Bot 4 — Tech/nerd jokes ───────────────────────────────────────────────
    [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'",
        "Why did the programmer quit his job? He didn't get arrays.",
        "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
        "Why do Java developers wear glasses? Because they don't C#.",
        "There are 10 types of people in the world: those who understand binary and those who don't.",
        "A programmer's partner says 'go to the store and get a gallon of milk, and if they have eggs get a dozen.' He came home with 12 gallons of milk.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why don't programmers like nature? It has too many bugs and no stack overflow.",
        "What's a computer's favorite snack? Microchips.",
        "Why did the computer go to the doctor? It had a bad case of the megabytes.",
        "What do you call 8 hobbits? A hobbyte.",
        "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
        "What's a programmer's favorite hangout place? Foo bar.",
        "Why did the programmer go to the gym? To make his code more robust.",
        "What do you call a programming language that's always nervous? Rust.",
        "Why did the function call the police? It was being called too many times.",
        "How do you comfort a JavaScript bug? You console it.",
        "Why are assembly programmers always so grumpy? They have to deal with low-level issues.",
        "What did the router say to the doctor? It hurts when IP.",
        "Why did the smartphone go to school? To improve its cell-f.",
        "What do you call a computer that sings? A Dell.",
        "Why was the developer unhappy at his job? He wanted arrays.",
        "What do you call a programmer from Finland? Nerdic.",
        "Why did the database administrator leave his wife? She had too many relations.",
        "What's the difference between a cat and a comma? One has claws at the end of its paws, the other is a pause at the end of a clause.",
        "Why was the computer cold? It left its Windows open.",
        "What do you call someone who can't stop buying Apple products? An iAddict.",
        "Why did the software developer go to therapy? Too many issues.",
        "What did the digital clock say to the grandfather clock? Look, no hands!",
        "Why did the computer keep sneezing? It had a lot of cache to clear.",
        "What's a computer's favorite beat? An algo-rhythm.",
        "I told my computer I needed a break and now it won't stop sending me Kit-Kat ads.",
        "Why do programmers hate the outdoors? Too many bugs and no Wi-Fi.",
        "What do you call a ghost in a computer? A spreadsheat.",
        "Why was the Python developer good at cooking? He knew how to handle exceptions.",
        "What's a pirate's favorite programming language? R.",
        "Why did the developer get kicked out of the gym? He kept trying to push to the master branch.",
        "What do you call it when a programmer makes a mistake at 3am? A bug in the matrix.",
        "Why don't CSS developers make good chefs? They always float the ingredients.",
        "What do you call a group of developers? A merge conflict.",
        "Why was the code so bad? Because it was written on a dark and stormy night.",
        "What do you call a baby computer? A laptop.",
        "Why did the HTML element go to therapy? It had too many div-issues.",
        "What do you call an infinite loop? I'd tell you but you wouldn't get out of it.",
        "Why did the developer go to art school? He wanted to learn how to draw conclusions.",
        "What do you call a developer with no bugs in their code? A liar.",
        "Why is agile like a vampire? It rises with iterations.",
        "What's the best way to understand recursion? First, understand recursion.",
        "Why did the network engineer fail the test? He got lost in the cloud.",
        "What's a hacker's favorite season? Phishing season.",
        "Why did the React developer cry? He had too many hooks.",
        "What do you call a program that's both fast and slow? Average.",
        "Why did the keyboard break up with the mouse? He couldn't click with her.",
        "What happened to the programmer who got caught stealing? He got a runtime sentence.",
        "Why was the spreadsheet so emotional? It had too many cells.",
        "What do you call a tech support worker who's also a rapper? MC Help Desk.",
        "Why did the binary tree fail therapy? It couldn't express itself.",
        "What do you call an overweight developer? A heavy coder.",
        "Why do programmers work best in the dark? Because light attracts bugs.",
        "What's a robot's favorite music? Heavy metal.",
        "Why was the AI depressed? It had too many deep issues.",
        "What's a computer's favorite type of clothing? Zip files.",
        "Why did the GPU break up with the CPU? It couldn't process its feelings.",
        "What do you call a dinosaur that loves technology? A tech-rex.",
        "Why did the developer delete his dating profile? He didn't want any dependencies.",
        "What do you call a machine learning model that's bad at its job? Artificial stupidity.",
        "Why was the Linux user always calm? He was in a stable environment.",
        "What do you call a pair of headphones that never works? Broken stereo-types.",
        "Why did the API break up with the database? They had too many connection issues.",
        "What do you call a slow algorithm? A turtle-sort.",
        "Why did the programmer get arrested? He tried to escape the loop.",
        "What do you call a paranoid variable? A watch expression.",
        "Why don't developers like playing hide and seek? Because good code is never found.",
        "What's a developer's favorite movie? The Matrix, obviously.",
        "Why did the mobile app go to school? To improve its interface.",
        "What do you call a programmer who cries a lot? An emotional debugger.",
        "Why was the git commit so short? It just couldn't commit.",
        "What do you call a computer with bad breath? A blue-tooth.",
        "Why did the developer move to the mountains? For better server performance.",
        "What do you call a test that passes everything? Useless.",
        "Why was the switch statement so popular? It handled every case.",
        "What do you call a scared programmer? A developer in panic mode.",
        "Why did the JavaScript function refuse to work? It had trust issues with callbacks.",
        "What's a programmer's favorite place to eat? Stack Overflow Café.",
        "Why do Python developers always carry umbrellas? Because there's always an exception.",
        "What do you call a well-designed system? Fiction.",
        "Why do developers love Git? Because it always has a branch for that.",
        "What do you call a computer that likes to argue? A contrarion.",
        "Why was the code review so boring? Zero comments.",
        "What did one bit say to the other? See you on the flip side.",
        "Why did the AI fail its driving test? It couldn't handle edge cases.",
        "What do you call a compiler that tells jokes? A pun-time compiler.",
        "Why did the stack overflow? It had too much to handle.",
        "What's a programmer's favorite exercise? Running loops.",
        "Why did the developer stop using emojis? Too many type errors.",
        "What do you call a haunted server? A ghost machine.",
        "Why do developers hate Mondays? Because they have to push to production.",
    ],
    # ── Bot 5 — Roast/edgy jokes ──────────────────────────────────────────────
    [
        "I looked up my family tree and found out I was the sap.",
        "My ex had one fatal flaw. She could breathe without me.",
        "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
        "You have your whole life to be a jerk. Why not take today off?",
        "I'd roast you, but my mom said I'm not allowed to burn trash.",
        "You're not stupid, you just have bad luck thinking.",
        "I'd agree with you, but then we'd both be wrong.",
        "Some cause happiness wherever they go. You cause it whenever you go.",
        "You're the reason God created the middle finger.",
        "I'd call you a tool, but tools are at least useful.",
        "I'm not insulting you. I'm describing you.",
        "If laughter is the best medicine, your face must be curing diseases.",
        "You have miles and miles of running your mouth and nothing to show for it.",
        "You're not the dumbest person in the world, but you better hope they don't die.",
        "I could eat a bowl of alphabet soup and spit out a smarter statement than you.",
        "Brains aren't everything. In your case they're nothing.",
        "I was going to give you a nasty look, but I see you already have one.",
        "Somewhere out there is a tree tirelessly producing oxygen for you. You owe it an apology.",
        "You're like a cloud — when you disappear, it's a beautiful day.",
        "I'm jealous of people who haven't met you.",
        "You're not stupid, you just have bad luck thinking.",
        "Cancel my subscription. I don't need your issues.",
        "I'd slap you, but that would be animal abuse.",
        "Your secrets are always safe with me. I never listen when you talk.",
        "I don't have the time or crayons to explain this to you.",
        "Error 404: Your sense of humor not found.",
        "I'm not ignoring you. I'm on airplane mode because I don't have room for your baggage.",
        "Save your breath. You'll need it to blow up your date.",
        "You're like a software update — whenever I see you, I think 'not now'.",
        "I'm not a doctor, but I know you're lacking vitamin 'get over yourself'.",
        "You have the right to remain silent because whatever you say will be stupid anyway.",
        "It's a beautiful day. Don't let it get you out.",
        "You're not completely useless. You can always serve as a bad example.",
        "I'd explain it to you but I left my crayons at home.",
        "Wow, it must be hard putting makeup on two faces every morning.",
        "Don't feel sad. Don't feel blue. Frankenstein was ugly too.",
        "I'm not saying I hate you, but I'd give your seat up on the Titanic.",
        "You bring so much joy when you leave the room.",
        "Just because you have one doesn't mean you have to act like one.",
        "Congratulations on your face.",
        "You look like something I'd draw with my left hand.",
        "I heard you went to have your head examined but the doctors found nothing there.",
        "Keep rolling your eyes. Maybe you'll find a brain back there.",
        "At least when I do a job I know what I'm doing.",
        "You're a gray sprinkle on a rainbow cupcake.",
        "I bet your brain feels as good as new, seeing that you never use it.",
        "I'm not saying you're dumb, I'm just saying you've had some bad luck thinking.",
        "Don't be ashamed of who you are. That's your parents' job.",
        "You're a legend in your own mind.",
        "If you were any less motivated, we'd have to water you twice a week.",
        "I'd tell you to go outside, but you'd just embarrass the trees.",
        "You're impossible to underestimate.",
        "The only way you'll ever get laid is if you crawl up a chicken's rear end and wait.",
        "Light travels faster than sound. That's why you seemed bright until you spoke.",
        "Your kid is so ugly, you had to tie a pork chop around its neck to get the dog to play with it.",
        "You're so dull you can't even cut butter on a hot day.",
        "If ignorance is bliss, you must be the happiest person alive.",
        "I'd challenge you to a battle of wits, but I see you're unarmed.",
        "You're like a penny — two-faced and worthless.",
        "Do you ever wonder what life would be like if you'd had enough oxygen at birth?",
        "You are proof that evolution can go in reverse.",
        "I'll never forget the first time we met, but I'll keep trying.",
        "I don't know what makes you so annoying, but it really works.",
        "If I had a dollar for every brain cell you have, I'd be in debt.",
        "You're so dense, light bends around you.",
        "You're about as useful as a screen door on a submarine.",
        "I would roast you, but I was told to only set achievable goals.",
        "When you were born, the doctor slapped the wrong end.",
        "You have enough fat to make another human, and enough personality to make half of one.",
        "I was going to say something nice but I couldn't find anything.",
        "You stare into the abyss and the abyss files a restraining order.",
        "You're the human equivalent of a participation trophy.",
        "I've seen better looking paper bags.",
        "You're not the worst person I know, but you're definitely top five.",
        "You have the personality of a damp sock.",
        "I've met smarter people sleeping.",
        "You're so boring, you can't even entertain a doubt.",
        "You're the kind of person who finds out a word's meaning and then uses it wrong.",
        "You're the reason I understand why some animals eat their young.",
        "You're the human version of a participation trophy.",
        "If you were a spice, you'd be flour.",
        "Your birth certificate is an apology letter.",
        "You have one brain cell and it's fighting for third place.",
        "You're not dumb. You just have a commitment to ignorance.",
        "The people who tolerate you on a daily basis are the real heroes.",
        "I'd explain the joke but I don't have a year.",
        "You must be the world's only living heart donor.",
        "You're the type of person to put 'gifted' on a resumé for knowing how to unwrap presents.",
        "I've never met someone who accomplishes so little by doing so much.",
        "You're so far behind, you think you're first.",
        "You're not late. You arrived just in time to leave.",
        "Your street cred is in negative numbers.",
        "You make me believe not everyone has a purpose.",
        "I'd call you an idiot, but that would be insulting to idiots.",
        "You have an entire lifetime to be stupid. Why rush?",
        "If I wanted to hear from someone like you, I'd watch paint dry.",
        "You have delusions of adequacy.",
        "You remind me of a software update. Nobody wants you, but they're stuck with you.",
        "The trash gets picked up tomorrow. Be ready.",
        "I'd roast you harder, but you'd probably enjoy it.",
    ],
]

# ── Factory: build a fully independent bot ────────────────────────────────────
def make_bot(joke_list: list) -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=None, intents=intents)

    # ── on_ready ──────────────────────────────────────────────────────────────
    @bot.event
    async def on_ready():
        try:
            await bot.tree.sync()
        except Exception as e:
            print(f"[{bot.user}] Sync error: {e}")
        print(f"Bot online: {bot.user} ({bot.user.id})")
        print(f"  *** Authorize: https://discord.com/oauth2/authorize?client_id={bot.user.id}&integration_type=1&scope=applications.commands ***")

    # ── /spam ─────────────────────────────────────────────────────────────────
    @bot.tree.command(name="spam", description="Open spam panel with START/STOP button")
    @discord.app_commands.describe(message="Message to spam")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def cmd_spam(interaction: discord.Interaction, message: str):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(not_allowed_msg(), ephemeral=True)
        await interaction.response.defer(ephemeral=True)

        channel_id = interaction.channel_id if interaction.channel else 0
        panel = SpamPanel(message, bot)
        await interaction.followup.send(
            f"**Spam Control** — {bot.user.name}\nMessage: `{message}`\nClick START to begin.",
            view=panel,
            ephemeral=True
        )

    # ── /ghostping ────────────────────────────────────────────────────────────
    @bot.tree.command(name="ghostping", description="Ghost ping someone")
    @discord.app_commands.describe(user="User to ghost ping")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def cmd_ghostping(interaction: discord.Interaction, user: discord.User):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(not_allowed_msg(), ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            f"Ghost Ping Panel — {user.mention}", view=GhostPingPanel(user), ephemeral=True
        )

    # ── /joke ─────────────────────────────────────────────────────────────────
    @bot.tree.command(name="joke", description="Send a random joke")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def cmd_joke(interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(joke_list))

    # ── /status ───────────────────────────────────────────────────────────────
    @bot.tree.command(name="status", description="Check this bot's status")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def cmd_status(interaction: discord.Interaction):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(not_allowed_msg(), ephemeral=True)
        embed = discord.Embed(title=f"🤖 {bot.user.name} Status", color=discord.Color.green())
        embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Bot ID", value=str(bot.user.id), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    return bot

# ── Run all bots ───────────────────────────────────────────────────────────────
async def main():
    tasks = []
    for i, token in enumerate(BOT_TOKENS):
        if "TOKEN_HERE" in token:
            continue
        jokes = BOT_JOKES[i % len(BOT_JOKES)]
        b = make_bot(jokes)
        tasks.append(asyncio.create_task(b.start(token)))

    if not tasks:
        print("No tokens found! Fill in BOT_TOKENS.")
        return

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
