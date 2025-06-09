import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_TELEGRAM_BOT_TOKEN_HERE' with your actual bot token from BotFather!
TELEGRAM_BOT_TOKEN = "7742944875:AAEGAJ0A-fuHBK_enhoN8znTrdHM8kQf3c0"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING) # Set higher logging level for httpx to avoid all GET/POST requests being logged

logger = logging.getLogger(__name__)

# --- Data for the Bot ---

# Romantic messages for Hiyori
LOVE_NOTES = [
    "Hiyori, every moment with you is a home run in my heart.",
    "Just thinking of you, Hiyori, and it brings a smile to my face. You're wonderful!",
    "You're more radiant than the brightest stadium lights, Hiyori.",
    "Hiyori, you've captured my heart, just like a perfect catch in center field.",
    "Even when we're far apart, you're always close to my heart, Hiyori.",
    "Wishing you a day as amazing as you are, Hiyori!",
    "You have a way of making every day feel like a grand slam, Hiyori.",
    "Hiyori, you're the most valuable player in my life.",
    "Your kindness and spirit shine brighter than any trophy, Hiyori.",
    "Sending you a virtual hug and a kiss, Hiyori. Thinking of you always.",
    "Your smile, Hiyori, is my favorite grand slam.",
    "Every day with you in my thoughts is a walk-off win, Hiyori.",
    "Hiyori, you're truly out of this world – a cosmic home run!",
    "My heart does a happy dance whenever I think of you, Hiyori.",
    "You're the melody in my favorite song, Hiyori."
]

THINKING_OF_YOU_MESSAGES = [
    "Hey Hiyori, just popped in to say I'm thinking of you!",
    "Did you know Hiyori is on my mind right now? Hope you're having a great day!",
    "Just a quick reminder that Hiyori is awesome, and I'm thinking about you!",
    "Sending some good vibes your way, Hiyori. You're always in my thoughts.",
    "Thinking of Hiyori and smiling. Hope your day is fantastic!",
    "Just a random thought: Hiyori is amazing! ✨",
    "Hope your day is as bright as your spirit, Hiyori! Thinking of you.",
    "Wishing Hiyori a day filled with joy and success!",
    "You're inspiring, Hiyori. Just wanted to let you know I'm thinking of you.",
    "A little message to say Hiyori crossed my mind and made me happy!"
]

# Dad Jokes
DAD_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "What do you call a pig that does karate? A pork chop!",
    "My wife asked me to stop singing 'Wonderwall' to her. I said maybe...",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "I used to be a baker, but I couldn't make enough dough.",
    "What do you call a boomerang that won’t come back? A stick!",
    "Why did the bicycle fall over? Because it was two tired!",
]

# Baseball Jokes
BASEBALL_JOKES = [
    "Why did the baseball get sent to jail? Because it was caught stealing!",
    "What's a baseball player's favorite part of a computer? The space bar!",
    "Why was the baseball game so hot? Because there were so many fans!",
    "What does a baseball player and a pancake have in common? They both need a good batter!",
    "Why did the ghost play baseball? He was a phantom of the ballpark!",
    "Why did the baseball player need a new uniform? He already used his old one!",
    "What do you call a baseball player who sings? A pitcher!",
    "What's a baseball player's favorite type of music? Hip-hop! (Because of the base beats!)",
    "Why did the baseball team lose the game? They kept striking out their ideas!",
    "What do you call a pitcher who wins every game? An Ace!"
]

# General Fun Facts
FUN_FACTS = [
    "A group of owls is called a parliament.",
    "Honey never spoils.",
    "It is impossible for most people to lick their own elbow.",
    "A crocodile cannot stick its tongue out.",
    "A shrimp's heart is in its head.",
    "It is physically impossible for pigs to look up into the sky.",
    "The 'sixth sick sheik's sixth sheep's sick' is believed to be the toughest tongue twister in the English language.",
    "The average person walks the equivalent of three times around the world in a lifetime.",
    "The longest recorded flight of a chicken is 13 seconds.",
    "The fear of long words is called hippopotomonstrosesquippedaliophobia."
]

# Baseball Fun Facts
BASEBALL_FUN_FACTS = [
    "The longest professional baseball game ever played lasted 8 hours and 6 minutes over 2 days.",
    "The first World Series was played in 1903.",
    "Babe Ruth wore a cabbage leaf under his cap to keep cool and changed it every two innings.",
    "The fastest pitch ever recorded was 105.1 mph by Aroldis Chapman.",
    "The distance between home plate and the pitcher's mound is 60 feet, 6 inches.",
    "Baseball was once played using only one glove, shared by all players.",
    "The term 'rookie' comes from 'recruit', a military term.",
    "Jackie Robinson broke the color barrier in Major League Baseball in 1947.",
    "The youngest player ever to play in a Major League Baseball game was 15 years old.",
    "The 'Curveball' was invented by Candy Cummings in the 1860s."
]

# Daily Affirmations
DAILY_AFFIRMATIONS = [
    "You are capable of amazing things, Hiyori.",
    "Today is a new opportunity to shine, Hiyori.",
    "Your strength and resilience are admirable, Hiyori.",
    "Believe in yourself, Hiyori, you've got this!",
    "You are worthy of all the good things that come your way, Hiyori.",
    "Your positive energy is infectious, Hiyori.",
    "Embrace your unique self, Hiyori, you are beautiful inside and out.",
    "Every challenge is a chance to grow, Hiyori.",
    "You are surrounded by love and support, Hiyori.",
    "Radiate kindness and it will return to you, Hiyori."
]

# General Compliments
GENERAL_COMPLIMENTS = [
    "Hiyori, your creativity is truly inspiring!",
    "You have such a wonderful sense of humor, Hiyori.",
    "Hiyori, your dedication to what you love is impressive.",
    "You always light up the room with your presence, Hiyori.",
    "Hiyori, you have such a thoughtful and caring heart.",
    "Your positive attitude is contagious, Hiyori.",
    "Hiyori, you're incredibly smart and insightful.",
    "You have a knack for making everyone around you feel comfortable, Hiyori.",
    "Hiyori, your resilience in the face of challenges is amazing.",
    "You have excellent taste, Hiyori!"
]

# Baseball Trivia Questions (question, correct_answer, wrong_answers)
BASEBALL_TRIVIA_QUESTIONS = [
    ("Which team has won the most World Series titles?", "New York Yankees", ["Boston Red Sox", "Los Angeles Dodgers", "St. Louis Cardinals"]),
    ("How many strikes are in a strikeout?", "3", ["2", "4", "5"]),
    ("What position does a catcher play?", "Catcher", ["Pitcher", "Shortstop", "Outfielder"]),
    ("What is it called when a batter hits the ball out of the park?", "Home Run", ["Triple", "Double", "Single"]),
    ("How many bases are there in baseball?", "4", ["3", "5", "6"]),
    ("What is the name of the professional baseball league in the USA and Canada?", "Major League Baseball", ["National Baseball League", "American Baseball Federation", "World Baseball League"]),
    ("What piece of equipment does the catcher wear on their hand?", "Glove", ["Bat", "Helmet", "Cleats"]),
    ("What is the area called where the pitcher stands?", "Mound", ["Plate", "Dugout", "Bullpen"]),
    ("How many outs are in a full baseball game (for both teams combined)?", "54", ["27", "18", "9"]),
    ("What is the term for a situation where a player runs the bases after a walk, hit-by-pitch, or error, and scores on the same play?", "Inside-the-park home run", ["Grand Slam", "Sacrifice Fly", "Stolen Base"]),
    ("Who broke Babe Ruth's career home run record?", "Hank Aaron", ["Barry Bonds", "Willie Mays", "Alex Rodriguez"]),
    ("What is the minimum number of players on a baseball field for one team?", "9", ["7", "8", "10"]),
    ("What is a 'no-hitter'?", "A game in which a pitcher gives up no hits", ["A game with no runs", "A game with no errors", "A game that ends in a tie"])
]

# Music suggestions
MOOD_MUSIC_SUGGESTIONS = {
    "happy": [
        "https://www.youtube.com/watch?v=y6Sxv-sUYtM (Pharrell Williams - Happy)",
        "https://www.youtube.com/watch?v=kfVsfFXzQ2o (Katrina & The Waves - Walking On Sunshine)",
        "https://www.youtube.com/watch?v=mCFAZcM5L_w (Bruno Mars - Uptown Funk)"
    ],
    "relaxed": [
        "https://www.youtube.com/watch?v=Dx5qF--Z94Q (Lofi Hip Hop Radio - 24/7)",
        "https://www.youtube.com/watch?v=F_S6pX2Wz00 (Weightless - Marconi Union)",
        "https://www.youtube.com/watch?v=DWFz4qgK1-c (Enya - Orinoco Flow)"
    ],
    "pumped": [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ (Rick Astley - Never Gonna Give You Up) - Just kidding!",
        "https://www.youtube.com/watch?v=btPJPFnesV4 (Queen - Don't Stop Me Now)",
        "https://www.youtube.com/watch?v=ZXN6tgFV_4g (AC/DC - Thunderstruck)",
        "https://www.youtube.com/watch?v=e_wK7LqF7pU (Eye of the Tiger - Survivor)"
    ],
    "romantic": [
        "https://www.youtube.com/watch?v=KEXQkrllGw4 (Ed Sheeran - Thinking Out Loud)",
        "https://www.youtube.com/watch?v=JGwWOKlW_Qo (John Legend - All of Me)",
        "https://www.youtube.com/watch?v=lp-EO5I60CE (Elvis Presley - Can't Help Falling in Love)"
    ]
}

# Would You Rather Questions (question, option1, option2)
WOULD_YOU_RATHER_QUESTIONS = [
    ("Would you rather bat a grand slam or pitch a perfect game?", "Bat a grand slam", "Pitch a perfect game"),
    ("Would you rather travel to the past or the future?", "Travel to the Past", "Travel to the Future"),
    ("Would you rather be able to fly or be invisible?", "Be Able to Fly", "Be Invisible"),
    ("Would you rather talk to animals or speak all human languages?", "Talk to Animals", "Speak All Human Languages"),
    ("Would you rather have unlimited money or unlimited wishes?", "Unlimited Money", "Unlimited Wishes"),
    ("Would you rather live in a house made of candy or a house made of trampolines?", "House of Candy", "House of Trampolines"),
    ("Would you rather always be 10 minutes early or always be 10 minutes late?", "Always 10 Mins Early", "Always 10 Mins Late"),
    ("Would you rather fight one horse-sized duck or 100 duck-sized horses?", "One Horse-Sized Duck", "100 Duck-Sized Horses")
]

# Quick Quiz Questions (question, correct_answer, wrong_answers)
QUICK_QUIZ_QUESTIONS = [
    ("The capital of France is Berlin. (True/False)", "False", ["True"]),
    ("The largest ocean on Earth is the Pacific Ocean. (True/False)", "True", ["False"]),
    ("Humans breathe in carbon dioxide and breathe out oxygen. (True/False)", "False", ["True"]),
    ("The sun is a planet. (True/False)", "False", ["True"]),
    ("A triangle has 3 sides. (True/False)", "True", ["False"]),
    ("Water boils at 100 degrees Celsius at sea level. (True/False)", "True", ["False"]),
    ("The Great Wall of China is visible from space with the naked eye. (True/False)", "False", ["True"]),
    ("Sharks are mammals. (True/False)", "False", ["True"]),
    ("The currency of Japan is the Yen. (True/False)", "True", ["False"]),
    ("Bats are blind. (True/False)", "False", ["True"])
]

# --- Global state for games (in-memory for simplicity) ---
# Stores {chat_id: {'question_text': str, 'correct_answer': str, 'options': list}}
baseball_trivia_games = {}
would_you_rather_games = {}
quick_quiz_games = {} # New game state

# --- Helper Function for Main Menu Keyboard ---

def _get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Returns the InlineKeyboardMarkup for the main category menu."""
    keyboard = [
        [
            InlineKeyboardButton("💖 Love & Connection", callback_data="menu_love_connection"),
            InlineKeyboardButton("😂 Fun & Laughter", callback_data="menu_fun_laughter")
        ],
        [
            InlineKeyboardButton("🎮 Games & Challenges", callback_data="menu_games_challenges"),
            InlineKeyboardButton("🎵 Music & Moods", callback_data="menu_music_moods")
        ],
        [
            InlineKeyboardButton("✨ Daily Positivity", callback_data="menu_daily_positivity"),
            InlineKeyboardButton("🎁 Surprise Me!", callback_data="cmd_surprise_me")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def _get_back_to_main_menu_button() -> InlineKeyboardMarkup:
    """Returns a single button to go back to the main menu."""
    keyboard = [[InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")]]
    return InlineKeyboardMarkup(keyboard)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcoming message and main category menu with buttons."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hello, Hiyori! 👋 It's your special bot, sent just for you by {user.mention_html()}!\n\n"
        "I'm here to bring you smiles, fun, and maybe a little bit of magic. ✨\n\n"
        "What would you like to do?",
        reply_markup=_get_main_menu_keyboard()
    )

# --- Sub-Menu Handlers ---

async def show_love_connection_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the 'Love & Connection' sub-menu."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("💖 Love Note", callback_data="cmd_lovenote"),
            InlineKeyboardButton("🤔 Thinking of You", callback_data="cmd_thinkingofyou")
        ],
        [
            InlineKeyboardButton("🎶 Our Special Song", callback_data="cmd_oursong")
        ],
        [
            InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Love & Connection options for you, Hiyori:", reply_markup=reply_markup)

async def show_fun_laughter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the 'Fun & Laughter' sub-menu."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("😂 Dad Joke", callback_data="cmd_dadjoke"),
            InlineKeyboardButton("🤣 Baseball Joke", callback_data="cmd_baseballjoke")
        ],
        [
            InlineKeyboardButton("💡 Fun Fact (General)", callback_data="cmd_fun_fact_general"),
            InlineKeyboardButton("⚾ Fun Fact (Baseball)", callback_data="cmd_fun_fact_baseball")
        ],
        [
            InlineKeyboardButton("😇 Random Compliment", callback_data="cmd_random_compliment")
        ],
        [
            InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Ready for some fun and laughs, Hiyori?", reply_markup=reply_markup)

async def show_games_challenges_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the 'Games & Challenges' sub-menu."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("⚾ Baseball Trivia", callback_data="cmd_baseball_trivia")
        ],
        [
            InlineKeyboardButton("❓ Would You Rather", callback_data="cmd_would_you_rather")
        ],
        [
            InlineKeyboardButton("🧠 Quick Quiz", callback_data="cmd_quick_quiz")
        ],
        [
            InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Let's play some games, Hiyori! What's your challenge?", reply_markup=reply_markup)

async def show_music_moods_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the 'Music & Moods' sub-menu."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("🎧 Mood Music", callback_data="cmd_mood_music_select_mood") # This will lead to mood selection
        ],
        [
            InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Find your perfect tune, Hiyori!", reply_markup=reply_markup)

async def show_daily_positivity_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the 'Daily Positivity' sub-menu."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("🌟 Daily Affirmation", callback_data="cmd_daily_affirmation")
        ],
        [
            InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("A little boost for your day, Hiyori!", reply_markup=reply_markup)


# --- Core Feature Handlers (now always provide a 'Back to Main Menu' option) ---

async def lovenote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random romantic message."""
    query = update.callback_query # Assuming this is always triggered by a button now
    await query.answer()
    await query.edit_message_text(random.choice(LOVE_NOTES), reply_markup=_get_back_to_main_menu_button())

async def thinking_of_you(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random thinking of you message."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(random.choice(THINKING_OF_YOU_MESSAGES), reply_markup=_get_back_to_main_menu_button())

async def dadjoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random dad joke."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(random.choice(DAD_JOKES), reply_markup=_get_back_to_main_menu_button())

async def baseballjoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random baseball-themed joke."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(random.choice(BASEBALL_JOKES), reply_markup=_get_back_to_main_menu_button())

async def fun_fact_general(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random general fun fact."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"💡 Fun Fact: {random.choice(FUN_FACTS)}", reply_markup=_get_back_to_main_menu_button())

async def fun_fact_baseball(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random baseball fun fact."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"⚾ Baseball Fun Fact: {random.choice(BASEBALL_FUN_FACTS)}", reply_markup=_get_back_to_main_menu_button())

async def daily_affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a daily affirmation."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"🌟 Daily Affirmation for Hiyori: {random.choice(DAILY_AFFIRMATIONS)}", reply_markup=_get_back_to_main_menu_button())

async def random_compliment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random general compliment."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"😇 Here's a compliment for you, Hiyori: {random.choice(GENERAL_COMPLIMENTS)}", reply_markup=_get_back_to_main_menu_button())

async def our_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a link to 'our song'."""
    # Replace with the actual link to your and Hiyori's special song!
    song_link = "https://www.youtube.com/watch?v=lp-EO5I60CE" # Example: Elvis Presley - Can't Help Falling in Love
    message_text = f"Hiyori, this song always reminds me of you! 💖\n\n{song_link}"
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(message_text, reply_markup=_get_back_to_main_menu_button())

async def mood_music_select_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends buttons for mood selection."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("😊 Happy", callback_data="mood_happy"),
            InlineKeyboardButton("😌 Relaxed", callback_data="mood_relaxed")
        ],
        [
            InlineKeyboardButton("🚀 Pumped", callback_data="mood_pumped"),
            InlineKeyboardButton("💖 Romantic", callback_data="mood_romantic")
        ],
        [
            InlineKeyboardButton("↩️ Back to Music Menu", callback_data="menu_music_moods") # Go back to music sub-menu
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "What mood are you in, Hiyori? Choose below:",
        reply_markup=reply_markup
    )

async def mood_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles callback queries for mood music buttons."""
    query = update.callback_query
    await query.answer()

    mood = query.data.replace("mood_", "")
    chat_id = query.message.chat_id

    if mood in MOOD_MUSIC_SUGGESTIONS:
        suggestions = MOOD_MUSIC_SUGGESTIONS[mood]
        await query.edit_message_text(
            f"Here's some music for your {mood} mood, Hiyori! 🎧\n" + random.choice(suggestions),
            reply_markup=_get_back_to_main_menu_button()
        )
    else:
        await query.edit_message_text(
            f"Hmm, I don't have suggestions for '{mood}' yet. Something went wrong.",
            reply_markup=_get_back_to_main_menu_button()
        )

# --- Baseball Trivia Game Logic ---

async def baseball_trivia_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts a new baseball trivia game and sends the first question with buttons."""
    chat_id = update.effective_chat.id if update.message else update.callback_query.message.chat_id
    
    if chat_id in baseball_trivia_games:
        if update.callback_query:
            await update.callback_query.answer("You're already in a trivia game, Hiyori! Answer the current question or go back to menu.")
            # We don't edit the message here, as the current question should still be visible.
        else:
            await update.message.reply_text("You're already in a trivia game, Hiyori! Answer the current question or send `/baseball_trivia_stop` to end it.", reply_markup=_get_back_to_main_menu_button())
        return

    await _send_baseball_trivia_question(update, context)


async def _send_baseball_trivia_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helper function to send a new trivia question with inline keyboard buttons."""
    chat_id = update.effective_chat.id if update.message else update.callback_query.message.chat_id
    question_data = random.choice(BASEBALL_TRIVIA_QUESTIONS)
    question_text, correct_answer, wrong_answers = question_data

    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    baseball_trivia_games[chat_id] = {
        'question_text': question_text,
        'correct_answer': correct_answer,
        'options': options
    }

    keyboard = []
    for i, option in enumerate(options):
        callback_data = f"trivia_{correct_answer.replace(' ', '_').lower()}|{option.replace(' ', '_').lower()}"
        keyboard.append([InlineKeyboardButton(option, callback_data=callback_data)])
    
    keyboard.append([InlineKeyboardButton("↩️ Back to Games Menu", callback_data="menu_games_challenges")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f"⚾ Baseball Trivia Time, Hiyori! ⚾\n\nQuestion: {question_text}\n\nChoose your answer below:"

    if update.callback_query: # If triggered from a start menu button or "Play Again"
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=reply_markup
        )
    else: # If triggered by /baseball_trivia command
        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup
        )

async def baseball_trivia_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles callback queries for baseball trivia answers."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id # Corrected line

    if chat_id not in baseball_trivia_games:
        await query.edit_message_text("This trivia game has ended or expired. Please start a new one with `/baseball_trivia`.", reply_markup=_get_back_to_main_menu_button())
        return

    try:
        _, data_payload = query.data.split('_', 1)
        correct_answer_slug, chosen_answer_slug = data_payload.split('|', 1)
        actual_correct_answer_for_comp = correct_answer_slug.replace('_', ' ')
        chosen_answer_for_comp = chosen_answer_slug.replace('_', ' ')
    except ValueError:
        await query.edit_message_text("Oops! There was an issue with your answer. Please try starting a new game with `/baseball_trivia`.", reply_markup=_get_back_to_main_menu_button())
        del baseball_trivia_games[chat_id]
        return

    game_state = baseball_trivia_games[chat_id]
    original_question_text = game_state['question_text']
    correct_answer_display = next((opt for opt in game_state['options'] if opt.lower() == actual_correct_answer_for_comp), "N/A")


    if chosen_answer_for_comp == actual_correct_answer_for_comp:
        response_text = (f"⚾ *Correct!* You got it right, Hiyori! 🎉\n"
                         f"Question: _{original_question_text}_\n"
                         f"Your Answer: _{chosen_answer_for_comp.title()}_\n"
                         f"The answer was: *{correct_answer_display}*")
        
    else:
        response_text = (f"😅 *Oops!* That's not quite right, Hiyori. \n"
                         f"Question: _{original_question_text}_\n"
                         f"Your Answer: _{chosen_answer_for_comp.title()}_\n"
                         f"The correct answer was: *{correct_answer_display}*")
    
    response_text += "\n\nWant another question? Tap below or return to menu."
    
    keyboard = [
        [InlineKeyboardButton("Play Again!", callback_data="cmd_baseball_trivia")],
        [InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')
    del baseball_trivia_games[chat_id] # End the current question


async def baseball_trivia_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stops the current baseball trivia game."""
    chat_id = update.effective_chat.id
    if chat_id in baseball_trivia_games:
        del baseball_trivia_games[chat_id]
        await update.message.reply_text("Okay, Hiyori! The baseball trivia game has ended. See you next time!", reply_markup=_get_back_to_main_menu_button())
    else:
        await update.message.reply_text("You're not currently in a baseball trivia game, Hiyori.", reply_markup=_get_back_to_main_menu_button())

# --- Would You Rather Game Logic ---

async def would_you_rather_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts a new 'Would You Rather' game."""
    chat_id = update.effective_chat.id if update.message else update.callback_query.message.chat_id
    if chat_id in would_you_rather_games:
        if update.callback_query:
            await update.callback_query.answer("You're already in a 'Would You Rather' game, Hiyori! Answer the current question or go back to menu.")
        else:
            await update.message.reply_text("You're already in a 'Would You Rather' game, Hiyori! Answer the current question or send `/would_you_rather_stop` to end it.", reply_markup=_get_back_to_main_menu_button())
        return

    await _send_would_you_rather_question(update, context)

async def _send_would_you_rather_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helper function to send a new 'Would You Rather' question with buttons."""
    chat_id = update.effective_chat.id if update.message else update.callback_query.message.chat_id
    question_data = random.choice(WOULD_YOU_RATHER_QUESTIONS)
    question_text, option1, option2 = question_data

    would_you_rather_games[chat_id] = {
        'question_text': question_text,
        'option1': option1,
        'option2': option2
    }

    keyboard = [
        [InlineKeyboardButton(option1, callback_data=f"wyr_{option1.replace(' ', '_').lower()}")],
        [InlineKeyboardButton(option2, callback_data=f"wyr_{option2.replace(' ', '_').lower()}")],
        [InlineKeyboardButton("↩️ Back to Games Menu", callback_data="menu_games_challenges")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f"❓ Would You Rather, Hiyori? ❓\n\n{question_text}\n\nChoose wisely:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message_text, reply_markup=reply_markup)

async def would_you_rather_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles callback queries for 'Would You Rather' answers."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id # Corrected line

    if chat_id not in would_you_rather_games:
        await query.edit_message_text("This 'Would You Rather' game has ended or expired. Please start a new one with `/would_you_rather`.", reply_markup=_get_back_to_main_menu_button())
        return

    chosen_option_slug = query.data.replace("wyr_", "")
    chosen_option_display = chosen_option_slug.replace('_', ' ').title()

    game_state = would_you_rather_games[chat_id]
    original_question_text = game_state['question_text']
    
    response_text = (f"You chose: *{chosen_option_display}*!\n\n"
                     f"Interesting choice, Hiyori! No right or wrong, just fun! 😉\n"
                     f"Question: _{original_question_text}_")
    
    response_text += "\n\nWant to play again? Tap below or return to menu."

    keyboard = [
        [InlineKeyboardButton("Play Again!", callback_data="cmd_would_you_rather")],
        [InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')
    del would_you_rather_games[chat_id]

async def would_you_rather_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stops the current 'Would You Rather' game."""
    chat_id = update.effective_chat.id
    if chat_id in would_you_rather_games:
        del would_you_rather_games[chat_id]
        await update.message.reply_text("Okay, Hiyori! The 'Would You Rather' game has ended. See you next time!", reply_markup=_get_back_to_main_menu_button())
    else:
        await update.message.reply_text("You're not currently in a 'Would You Rather' game, Hiyori.", reply_markup=_get_back_to_main_menu_button())

# --- Quick Quiz Game Logic ---

async def quick_quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts a new quick quiz game."""
    chat_id = update.effective_chat.id if update.message else update.callback_query.message.chat_id
    if chat_id in quick_quiz_games:
        if update.callback_query:
            await update.callback_query.answer("You're already in a quick quiz game, Hiyori! Answer the current question or go back to menu.")
        else:
            await update.message.reply_text("You're already in a quick quiz game, Hiyori! Answer the current question or send `/quick_quiz_stop` to end it.", reply_markup=_get_back_to_main_menu_button())
        return

    await _send_quick_quiz_question(update, context)

async def _send_quick_quiz_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helper function to send a new quick quiz question with buttons."""
    chat_id = update.effective_chat.id if update.message else update.callback_query.message.chat_id
    question_data = random.choice(QUICK_QUIZ_QUESTIONS)
    question_text, correct_answer, wrong_answers = question_data

    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    quick_quiz_games[chat_id] = {
        'question_text': question_text,
        'correct_answer': correct_answer,
        'options': options
    }

    keyboard = []
    for option in options:
        callback_data = f"quiz_{correct_answer.replace(' ', '_').lower()}|{option.replace(' ', '_').lower()}"
        keyboard.append([InlineKeyboardButton(option, callback_data=callback_data)])
    
    keyboard.append([InlineKeyboardButton("↩️ Back to Games Menu", callback_data="menu_games_challenges")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f"🧠 Quick Quiz Time, Hiyori! 🧠\n\nQuestion: {question_text}\n\nChoose your answer:"

    if update.callback_query:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup
        )

async def quick_quiz_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles callback queries for quick quiz answers."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id # Corrected line

    if chat_id not in quick_quiz_games:
        await query.edit_message_text("This quick quiz game has ended or expired. Please start a new one with `/quick_quiz`.", reply_markup=_get_back_to_main_menu_button())
        return

    try:
        _, data_payload = query.data.split('_', 1)
        correct_answer_slug, chosen_answer_slug = data_payload.split('|', 1)
        actual_correct_answer_for_comp = correct_answer_slug.replace('_', ' ')
        chosen_answer_for_comp = chosen_answer_slug.replace('_', ' ')
    except ValueError:
        await query.edit_message_text("Oops! There was an issue with your answer. Please try starting a new game with `/quick_quiz`.", reply_markup=_get_back_to_main_menu_button())
        del quick_quiz_games[chat_id]
        return

    game_state = quick_quiz_games[chat_id]
    original_question_text = game_state['question_text']
    correct_answer_display = next((opt for opt in game_state['options'] if opt.lower() == actual_correct_answer_for_comp), "N/A")

    if chosen_answer_for_comp == actual_correct_answer_for_comp:
        response_text = (f"🎉 *Correct!* You got it right, Hiyori!\n"
                         f"Question: _{original_question_text}_\n"
                         f"Your Answer: _{chosen_answer_for_comp.title()}_\n"
                         f"The answer was: *{correct_answer_display}*")
    else:
        response_text = (f"😞 *Not quite!* The correct answer was: *{correct_answer_display}*.\n"
                         f"Question: _{original_question_text}_\n"
                         f"Your Answer: _{chosen_answer_for_comp.title()}_")
    
    response_text += "\n\nWant another question? Tap below or return to menu."

    keyboard = [
        [InlineKeyboardButton("Play Again!", callback_data="cmd_quick_quiz")],
        [InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')
    del quick_quiz_games[chat_id]

async def quick_quiz_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stops the current quick quiz game."""
    chat_id = update.effective_chat.id
    if chat_id in quick_quiz_games:
        del quick_quiz_games[chat_id]
        await update.message.reply_text("Okay, Hiyori! The quick quiz has ended. See you next time!", reply_markup=_get_back_to_main_menu_button())
    else:
        await update.message.reply_text("You're not currently in a quick quiz game, Hiyori.", reply_markup=_get_back_to_main_menu_button())

# --- Surprise Me! Logic ---
async def surprise_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Randomly triggers one of the bot's features."""
    query = update.callback_query
    await query.answer()

    # List of callable functions for features
    # Exclude game starts that require specific state management as they need dedicated button for "Play Again"
    # and main menu. Instead, call the general-purpose, single-response handlers.
    features = [
        lovenote, thinking_of_you, dadjoke, baseballjoke, fun_fact_general,
        fun_fact_baseball, daily_affirmation, random_compliment, our_song
    ]
    
    # Mood music is special because it opens a sub-menu, so handling it separately
    # Games will also be called directly to start a new game with its specific flow and exit options.
    games_and_mood = [
        baseball_trivia_start, would_you_rather_start, quick_quiz_start, mood_music_select_mood
    ]

    # Randomly pick a feature. Adjust weights if some features should appear more often.
    if random.random() < 0.7: # 70% chance for a simple message feature
        chosen_feature = random.choice(features)
        await chosen_feature(update, context) # Call the handler
    else: # 30% chance for a game or mood music
        chosen_feature = random.choice(games_and_mood)
        await chosen_feature(update, context) # Call the handler

# --- Main Callback Query Handler for Menu Navigation ---

async def handle_button_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles callback queries that directly trigger commands or sub-menus."""
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    action = query.data # The full callback data

    # Main menu navigation
    if action == "menu_main":
        await query.edit_message_text(
            "What would you like to do, Hiyori?",
            reply_markup=_get_main_menu_keyboard()
        )
    elif action == "menu_love_connection":
        await show_love_connection_menu(update, context)
    elif action == "menu_fun_laughter":
        await show_fun_laughter_menu(update, context)
    elif action == "menu_games_challenges":
        await show_games_challenges_menu(update, context)
    elif action == "menu_music_moods":
        await show_music_moods_menu(update, context)
    elif action == "menu_daily_positivity":
        await show_daily_positivity_menu(update, context)

    # Direct command triggers from sub-menus or surprise me
    elif action == "cmd_lovenote":
        await lovenote(update, context)
    elif action == "cmd_thinkingofyou":
        await thinking_of_you(update, context)
    elif action == "cmd_dadjoke":
        await dadjoke(update, context)
    elif action == "cmd_baseballjoke":
        await baseballjoke(update, context)
    elif action == "cmd_fun_fact_general":
        await fun_fact_general(update, context)
    elif action == "cmd_fun_fact_baseball":
        await fun_fact_baseball(update, context)
    elif action == "cmd_daily_affirmation":
        await daily_affirmation(update, context)
    elif action == "cmd_random_compliment":
        await random_compliment(update, context)
    elif action == "cmd_oursong":
        await our_song(update, context)
    elif action == "cmd_mood_music_select_mood":
        await mood_music_select_mood(update, context)
    elif action == "cmd_baseball_trivia":
        await baseball_trivia_start(update, context)
    elif action == "cmd_would_you_rather":
        await would_you_rather_start(update, context)
    elif action == "cmd_quick_quiz":
        await quick_quiz_start(update, context)
    elif action == "cmd_surprise_me":
        await surprise_me(update, context)
    else:
        await query.edit_message_text("Sorry, I don't recognize that command from the button.", reply_markup=_get_back_to_main_menu_button())


# --- Main Function ---

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers (for direct /commands, though buttons will primarily drive interaction)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("baseball_trivia_stop", baseball_trivia_stop))
    application.add_handler(CommandHandler("would_you_rather_stop", would_you_rather_stop))
    application.add_handler(CommandHandler("quick_quiz_stop", quick_quiz_stop))

    # Callback Query Handlers for inline buttons
    # Handlers for specific game/mood answers (patterns are more specific)
    application.add_handler(CallbackQueryHandler(baseball_trivia_button_handler, pattern=r"^trivia_"))
    application.add_handler(CallbackQueryHandler(mood_button_handler, pattern=r"^mood_"))
    application.add_handler(CallbackQueryHandler(would_you_rather_button_handler, pattern=r"^wyr_"))
    application.add_handler(CallbackQueryHandler(quick_quiz_button_handler, pattern=r"^quiz_"))
    
    # Generic handler for all menu navigation and cmd_ actions
    application.add_handler(CallbackQueryHandler(handle_button_commands, pattern=r"^(menu_|cmd_)"))

    # Fallback for unhandled messages (can be removed if not desired)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_message))

    logger.info("Bot is starting... Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
