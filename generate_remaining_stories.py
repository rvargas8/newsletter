#!/usr/bin/env python3
# Script to generate all remaining cold reads stories (Weeks 4-10)

import os

# HTML template function
def create_story_html(title, subtitle, date, story_paragraphs, questions, filename):
    # Build story content
    story_html = ""
    for para, line_num in story_paragraphs:
        story_html += f'''            <div class="line-numbers">
                <div class="line-number"></div>
                <p>{para}</p>
                <div class="line-number">{line_num}</div>
            </div>\n\n'''
    
    # Build questions
    questions_html = ""
    correct_answers_list = []
    for i, (q_text, choices, correct) in enumerate(questions, 1):
        choices_html = ""
        for choice_text, letter in choices:
            choices_html += f'                    <div class="choice" data-answer="{letter}"><span class="choice-letter">{letter}</span>{choice_text}</div>\n'
        
        questions_html += f'''            <div class="question" data-question="{i}">
                <div class="question-text">
                    <span class="question-number">{i}</span>
                    {q_text}
                </div>
                <div class="choices">
{choices_html}                </div>
            </div>\n\n'''
        correct_answers_list.append(f"{i}: '{correct}'")
    
    correct_answers = ", ".join(correct_answers_list)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + title + ''' - 3rd Grade Cold Reads</title>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --primary-yellow: #FFD93D; --coral: #FF6B6B; --teal: #4ECDC4; --navy: #2C3E50; --warm-white: #FFFEF7; }
        body { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #FFF8E7 0%, #FFE4E1 100%); padding: 2rem 1rem; line-height: 1.6; color: var(--navy); }
        .container { max-width: 52rem; margin: 0 auto; background: var(--warm-white); padding: clamp(2rem, 5vw, 3rem); border-radius: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.05), 0 8px 16px rgba(0,0,0,0.05); }
        .header { text-align: center; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 3px solid var(--primary-yellow); }
        .header h1 { font-family: 'Fraunces', serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 900; color: var(--coral); text-transform: uppercase; }
        .header .subtitle { font-size: 1.125rem; color: var(--navy); font-weight: 600; }
        .directions { background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); padding: 1.5rem; border-radius: 16px; margin-bottom: 2rem; border-left: 6px solid #2196F3; }
        .directions p { font-weight: 600; font-size: 1.05rem; }
        .progress-bar { width: 100%; height: 8px; background: #E0E0E0; border-radius: 10px; margin-bottom: 2rem; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, var(--teal), var(--primary-yellow)); width: 0%; transition: width 0.3s ease; }
        .story-title { text-align: center; margin-bottom: 1.5rem; }
        .story-title h2 { font-family: 'Fraunces', serif; font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 900; color: var(--navy); }
        .story-title .subtitle { font-style: italic; color: #666; font-size: 1.125rem; }
        .story-content { background: white; padding: 2rem; border-radius: 16px; border: 2px solid #E0E0E0; margin-bottom: 2rem; line-height: 1.8; }
        .story-content p { margin-bottom: 1.25rem; text-align: justify; }
        .line-numbers { display: grid; grid-template-columns: auto 1fr auto; gap: 1rem; }
        .line-number { color: #999; font-size: 0.85rem; text-align: right; min-width: 30px; }
        .questions-section { margin-top: 3rem; }
        .question { background: white; padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem; border: 2px solid #E0E0E0; transition: all 0.2s ease; }
        .question:hover { border-color: var(--teal); box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2); }
        .question-text { font-weight: 600; font-size: 1.05rem; margin-bottom: 1rem; }
        .question-number { display: inline-block; background: var(--teal); color: white; width: 28px; height: 28px; border-radius: 50%; text-align: center; line-height: 28px; font-weight: 700; margin-right: 0.5rem; }
        .choices { margin-left: 2.5rem; }
        .choice { margin-bottom: 0.75rem; padding: 0.75rem; border-radius: 8px; cursor: pointer; border: 2px solid transparent; transition: all 0.2s; }
        .choice:hover { background: #F5F5F5; border-color: var(--teal); }
        .choice.selected { background: var(--teal); color: white; }
        .choice.correct { background: #4CAF50; color: white; }
        .choice.incorrect { background: #F44336; color: white; }
        .choice.disabled { cursor: not-allowed; opacity: 0.7; }
        .choice-letter { font-weight: 700; color: var(--coral); margin-right: 0.5rem; }
        .choice.selected .choice-letter, .choice.correct .choice-letter, .choice.incorrect .choice-letter { color: white; }
        .footer-note { text-align: center; margin-top: 2rem; padding: 1.5rem; background: var(--primary-yellow); border-radius: 16px; font-weight: 600; }
        .score-section { background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%); padding: 2rem; border-radius: 16px; margin-top: 2rem; text-align: center; border: 3px solid #4CAF50; display: none; }
        .score-section.show { display: block; animation: slideIn 0.5s ease; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .score-title { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 900; color: #2E7D32; margin-bottom: 1rem; }
        .score-display { font-size: 3rem; font-weight: 900; color: #1B5E20; margin: 1rem 0; }
        .score-message { font-size: 1.25rem; font-weight: 600; }
        .restart-btn { background: var(--coral); color: white; border: none; padding: 1rem 2rem; border-radius: 25px; font-size: 1.1rem; font-weight: 600; cursor: pointer; margin-top: 1rem; }
        .restart-btn:hover { background: #ff5252; transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Cold Reads Practice</h1>
            <div class="subtitle">Week of ''' + date + '''</div>
        </div>
        <div class="directions">
            <p>📖 Directions: Read the selection carefully and answer the questions that follow. Click on your answer choice for each question.</p>
        </div>
        <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
        <div class="story-title">
            <h2>''' + title + '''</h2>
            <div class="subtitle">''' + subtitle + '''</div>
        </div>
        <div class="story-content">
''' + story_html + '''        </div>
        <div class="questions-section">
''' + questions_html + '''        </div>
        <div class="score-section" id="scoreSection">
            <div class="score-title">🎉 Great Job!</div>
            <div class="score-display" id="scoreDisplay">0/4</div>
            <div class="score-message" id="scoreMessage"></div>
            <button class="restart-btn" onclick="restartQuiz()">🔄 Try Again</button>
        </div>
        <div class="footer-note">⭐ Remember to read carefully and look back at the story to find your answers!</div>
    </div>
    <script>
        const correctAnswers = { ''' + correct_answers + ''' };
        let userAnswers = {}, answeredCount = 0;
        const totalQuestions = 4;
        document.querySelectorAll('.choice').forEach(choice => {
            choice.addEventListener('click', function() {
                if (this.classList.contains('disabled')) return;
                const question = this.closest('.question'), questionNum = question.dataset.question;
                const choices = question.querySelectorAll('.choice'), selectedAnswer = this.dataset.answer;
                choices.forEach(c => { c.classList.remove('selected'); c.classList.add('disabled'); });
                this.classList.add('selected');
                if (userAnswers[questionNum] === undefined) answeredCount++;
                userAnswers[questionNum] = selectedAnswer;
                setTimeout(() => {
                    if (selectedAnswer === correctAnswers[questionNum]) {
                        this.classList.remove('selected'); this.classList.add('correct');
                    } else {
                        this.classList.remove('selected'); this.classList.add('incorrect');
                        choices.forEach(c => { if (c.dataset.answer === correctAnswers[questionNum]) c.classList.add('correct'); });
                    }
                    document.getElementById('progressFill').style.width = (answeredCount / totalQuestions) * 100 + '%';
                    if (answeredCount === totalQuestions) setTimeout(showScore, 500);
                }, 300);
            });
        });
        function showScore() {
            let score = 0;
            for (let q in correctAnswers) if (userAnswers[q] === correctAnswers[q]) score++;
            document.getElementById('scoreDisplay').textContent = score + '/4';
            let message = score === 4 ? '🌟 Perfect! You got them all right!' : score >= 3 ? '👏 Excellent work! Keep it up!' : score >= 2 ? '👍 Good job! Try reading more carefully next time.' : '💪 Keep practicing! You\\'ll do better next time!';
            document.getElementById('scoreMessage').textContent = message;
            document.getElementById('scoreSection').classList.add('show');
        }
        function restartQuiz() {
            userAnswers = {}; answeredCount = 0;
            document.querySelectorAll('.choice').forEach(c => c.classList.remove('selected', 'correct', 'incorrect', 'disabled'));
            document.getElementById('progressFill').style.width = '0%';
            document.getElementById('scoreSection').classList.remove('show');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>'''
    
    with open(filename, 'w') as f:
        f.write(html_content)

# All story data for weeks 4-10
all_weeks = {
    "Week 4": {
        "date": "October 27–31, 2025",
        "stories": {
            "week4-monday": ("The Spooky Forest", "A Mysterious Tale", [
                ("Deep in the forest stood an old oak tree that locals called 'The Whispering Oak.' People said if you listened carefully on a windy night, you could hear it talking. Ten-year-old Ben decided to investigate this mystery.", 14),
                ("One breezy evening, Ben walked to the tree with his notebook. As the wind blew through the branches, he heard soft whooshing sounds. 'It does sound like whispers!' he thought. But Ben knew there had to be a scientific explanation.", 38),
                ("Ben learned that wind passing through leaves and branches creates vibrations that sound like whispers. He also discovered that the oak tree had a hollow section that acted like a musical instrument, amplifying the sound.", 60),
                ("Ben shared his discovery with his class. His teacher was so impressed that she organized a field trip to the Whispering Oak. Everyone learned that mysteries often have logical explanations waiting to be discovered.", 80)
            ], [
                ("What was special about the old oak tree?", [("It glowed at night", "A"), ("People said it whispered", "B"), ("It was the tallest tree", "C"), ("Animals lived in it", "D")], "B"),
                ("The word 'investigate' means to —", [("ignore something", "A"), ("carefully examine something", "B"), ("run away from something", "C"), ("destroy something", "D")], "B"),
                ("What caused the whispering sounds?", [("Ghosts in the tree", "A"), ("People hiding nearby", "B"), ("Wind through leaves and hollow sections", "C"), ("Birds singing", "D")], "C"),
                ("What lesson did Ben teach his classmates?", [("Trees can talk", "A"), ("Forests are scary", "B"), ("Mysteries have logical explanations", "C"), ("Never go into the forest", "D")], "C")
            ]),
            "week4-tuesday": ("The Black Cat", "A Superstition Story", [
                ("Midnight was a sleek black cat who lived in Mrs. Chen's bookstore. Some customers refused to enter when they saw Midnight, believing black cats brought bad luck. This made Mrs. Chen sad because Midnight was the friendliest cat she'd ever known.", 14),
                ("One day, a little girl named Amy came into the store looking for a book about science. Midnight rubbed against her leg, purring loudly. 'What a sweet cat!' Amy exclaimed, petting Midnight's soft fur.", 36),
                ("Mrs. Chen told Amy about the superstition. Amy, who loved learning facts, researched black cats. She discovered that in many countries, black cats are considered lucky! She created a poster with fun facts about black cats and hung it in the bookstore window.", 64),
                ("Soon, more people came to meet Midnight and learn the truth about black cats. They realized that judging something based on old superstitions wasn't fair. Midnight became the most popular greeter in the bookstore!", 82)
            ], [
                ("Why did some customers avoid the bookstore?", [("It was too expensive", "A"), ("They believed black cats brought bad luck", "B"), ("It was always closed", "C"), ("There were too many books", "D")], "B"),
                ("How did Amy feel about Midnight?", [("Scared", "A"), ("Angry", "B"), ("Happy and friendly", "C"), ("Bored", "D")], "C"),
                ("What did Amy do to help Midnight?", [("Took him home", "A"), ("Created an educational poster", "B"), ("Hid him in the back", "C"), ("Gave him away", "D")], "B"),
                ("What is the main message of the story?", [("All cats are mean", "A"), ("Superstitions are always true", "B"), ("Don't judge based on old superstitions", "C"), ("Bookstores don't need pets", "D")], "C")
            ]),
            "week4-wednesday": ("Trick or Treat Safety", "An Informational Text", [
                ("Halloween is one of the most exciting nights of the year for kids. Dressing up in costumes and collecting candy door-to-door is a beloved tradition. However, staying safe while trick-or-treating is very important.", 14),
                ("First, always go trick-or-treating with an adult or in a group with friends. Wear bright or reflective clothing so drivers can see you in the dark. Carry a flashlight to light your path and help you see where you're stepping.", 36),
                ("Only visit houses with porch lights on—this signals that they're welcoming trick-or-treaters. Never enter someone's home, and always say 'thank you' politely. Stay on sidewalks and cross streets at crosswalks, looking both ways carefully.", 62),
                ("When you get home, have an adult check your candy before eating any. Remove anything that's unwrapped or looks tampered with. Following these safety rules means you can enjoy Halloween fun while staying safe!", 82)
            ], [
                ("What is the main purpose of this text?", [("To scare children", "A"), ("To teach Halloween safety", "B"), ("To explain Halloween history", "C"), ("To describe costumes", "D")], "B"),
                ("Why should trick-or-treaters wear bright clothing?", [("It looks better", "A"), ("It's warmer", "B"), ("So drivers can see them", "C"), ("It's required by law", "D")], "C"),
                ("What does a porch light being on mean?", [("Nobody is home", "A"), ("The house is haunted", "B"), ("They welcome trick-or-treaters", "C"), ("They ran out of candy", "D")], "C"),
                ("Who should check your candy before you eat it?", [("Your friends", "A"), ("Nobody needs to check it", "B"), ("An adult", "C"), ("Your neighbors", "D")], "C")
            ]),
            "week4-thursday": ("The Night Owl", "A Nature Story", [
                ("Olivia loved staying up late reading under her covers with a flashlight. Her mom always called her 'my little night owl.' Curious about the nickname, Olivia decided to learn about real night owls.", 14),
                ("She discovered that owls are nocturnal, meaning they're active at night and sleep during the day. Their special eyes can see in very dim light, and their feathers are designed for silent flight so they can sneak up on prey.", 38),
                ("Olivia learned that different owl species make different sounds—from the Great Horned Owl's deep 'hoo-hoo' to the Barn Owl's eerie screech. She even found out that owls can turn their heads 270 degrees because their eyes can't move in their sockets!", 64),
                ("For her school project, Olivia created a presentation about owls. She shared fascinating facts and explained why being called a 'night owl' was actually a compliment—it meant she was wise, observant, and comfortable in the quiet of night.", 86)
            ], [
                ("What does 'nocturnal' mean?", [("Sleeping all the time", "A"), ("Active at night", "B"), ("Very loud", "C"), ("Living in trees", "D")], "B"),
                ("Why can owls fly silently?", [("They don't have wings", "A"), ("They fly very slowly", "B"), ("Their feathers are specially designed", "C"), ("They never fly", "D")], "C"),
                ("How many degrees can owls turn their heads?", [("90 degrees", "A"), ("180 degrees", "B"), ("270 degrees", "C"), ("360 degrees", "D")], "C"),
                ("Why did Olivia's mom call her a 'night owl'?", [("She was scared of the dark", "A"), ("She liked staying up late", "B"), ("She had big eyes", "C"), ("She hooted like an owl", "D")], "B")
            ]),
            "week4-friday": ("The Harvest Moon", "A Seasonal Story", [
                ("October's full moon is called the Harvest Moon. Grandpa Joe took his grandson Daniel outside to see it rise over the corn fields. The moon looked enormous and glowed bright orange against the darkening sky.", 14),
                ("'Why is it so big and orange?' Daniel asked. Grandpa explained that when the moon is near the horizon, it appears larger due to an optical illusion. The orange color comes from looking at it through more of Earth's atmosphere, which scatters blue light.", 42),
                ("'Farmers used to rely on the Harvest Moon's bright light to work late into the evening, gathering crops before winter,' Grandpa said. 'That's why it's called the Harvest Moon—it helped with the harvest.'", 62),
                ("Daniel was amazed. 'So the moon isn't actually bigger or changing color?' 'That's right,' Grandpa smiled. 'It's the same moon we always see, just appearing different because of where we're viewing it from. Science and nature together create beautiful experiences.'", 86)
            ], [
                ("Why is it called the Harvest Moon?", [("It's shaped like a farm", "A"), ("It helped farmers harvest crops", "B"), ("It only appears at harvest time", "C"), ("Farmers named it", "D")], "B"),
                ("What makes the moon appear orange?", [("It's actually burning", "A"), ("Paint from space", "B"), ("Earth's atmosphere scattering blue light", "C"), ("The sun is setting", "D")], "C"),
                ("The word 'enormous' means —", [("very small", "A"), ("very bright", "B"), ("very large", "C"), ("very dark", "D")], "C"),
                ("What did Daniel learn from Grandpa?", [("The moon changes size", "A"), ("Science explains natural wonders", "B"), ("Farmers control the moon", "C"), ("The moon is made of cheese", "D")], "B")
            ])
        }
    }
}

# Generate Week 4
print("Generating Week 4 stories...")
week_data = all_weeks["Week 4"]
for story_key, (title, subtitle, paragraphs, questions) in week_data["stories"].items():
    filename = f"/Users/admin/Desktop/newsletter/cold-reads-{story_key}.html"
    create_story_html(title, subtitle, week_data["date"], paragraphs, questions, filename)
    print(f"Created: cold-reads-{story_key}.html")

print("\nWeek 4 completed!")
print("Total files created: 5")

