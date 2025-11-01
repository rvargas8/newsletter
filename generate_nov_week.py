#!/usr/bin/env python3
# Script to generate 10 cold reads for November 3-7, 2025

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
        body { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #FFF8E7 0%, #FFE4E1 100%); padding: 2rem 1rem; padding-top: 5rem; line-height: 1.6; color: var(--navy); }
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
        .back-button { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: var(--teal); color: white; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 0.95rem; transition: all 0.3s; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3); margin-bottom: 2rem; }
        .back-button:hover { background: var(--coral); transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <a href="cold-reads-nov-archive.html" class="back-button">← Back to Cold Reads Archive</a>
        <div class="header">
            <h1>Cold Reads Practice</h1>
            <div class="subtitle">''' + date + '''</div>
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

# Story data for November 3-7, 2025 week
nov_stories = {
    "date": "November 3-7, 2025",
    "stories": {
        "nov-week-passage1": ("The Amazing Octopus", "Informational", [
            ("Octopuses are some of the smartest animals in the ocean. They have eight long arms covered with hundreds of suckers that help them grab things and taste their food. An octopus can change its color and texture in less than one second to hide from danger or to sneak up on prey.", 18),
            ("These incredible creatures have three hearts and blue blood! Two hearts pump blood to their gills so they can breathe underwater, while the third heart sends blood to the rest of their body. When an octopus swims, the heart that pumps blood to the body actually stops beating.", 41),
            ("Octopuses are also famous escape artists. They can squeeze through tiny spaces because they don't have any bones in their soft bodies. The only hard part is their beak, which looks like a parrot's beak. Scientists have watched octopuses open childproof jars, solve mazes and puzzles, and even recognize different human faces.", 75),
            ("Some octopuses have been seen using coconut shells as portable hiding places. They pick up two halves of a shell, carry them along the ocean floor, and put them together to hide inside when danger appears.", 98)
        ], [
            ("How many hearts does an octopus have, and what does each one do?", [("One heart for breathing and one for blood flow", "A"), ("Three hearts: two for gills and one for the body", "B"), ("Two hearts that both pump to the body", "C"), ("Four hearts like humans", "D")], "B"),
            ("Why can an octopus squeeze through tiny spaces?", [("They are very small animals", "A"), ("They have no bones in their soft bodies", "B"), ("They can make themselves flat", "C"), ("Their tentacles can shrink", "D")], "B"),
            ("Based on the passage, what evidence shows that octopuses are intelligent animals?", [("They have three hearts", "A"), ("They can open jars, solve puzzles, and recognize faces", "B"), ("They have suckers on their arms", "C"), ("They live in the ocean", "D")], "B"),
            ("What does the word 'portable' mean in the last sentence?", [("Something that is heavy", "A"), ("Something that can be carried or moved", "B"), ("Something that is permanent", "C"), ("Something that is broken", "D")], "B")
        ]),
        "nov-week-passage2": ("How Honeybees Make Honey", "Informational", [
            ("Honeybees work together in amazing ways to make the sweet honey we enjoy on our toast and in our tea. First, worker bees fly from flower to flower collecting nectar, which is a sugary liquid found deep inside flowers. They use their long tongues to suck up the nectar and store it in a special stomach called a honey stomach. A single bee might visit up to 100 flowers on just one trip!", 19),
            ("Back at the hive, the bees pass the nectar to other bees who chew it for about 30 minutes. While chewing, they add special chemicals called enzymes from their bodies that begin to change the nectar into honey. Then they spread the nectar into six-sided cells in the honeycomb.", 43),
            ("The bees fan their wings really fast to help water evaporate from the nectar, making it thicker and thicker. It can take the nectar from two million flowers to make just one pound of honey! When the honey is thick enough and ready, the bees cover the cell with a wax cap to seal it and store it as food for the winter months when flowers aren't blooming.", 80)
        ], [
            ("What is nectar, and where do bees find it?", [("A sugary liquid inside flowers", "A"), ("Pollen from leaves", "B"), ("Honey from other hives", "C"), ("Water from rivers", "D")], "A"),
            ("How do bees make the nectar thicker and turn it into honey?", [("By adding sugar", "A"), ("By fanning wings to evaporate water and adding enzymes", "B"), ("By putting it in the sun", "C"), ("By shaking it", "D")], "B"),
            ("Why do you think bees need to store honey for the winter?", [("To feed the queen", "A"), ("Flowers don't bloom in winter", "B"), ("They like to save food", "C"), ("It makes them strong", "D")], "B"),
            ("What does 'evaporate' mean in this passage?", [("To freeze solid", "A"), ("To turn from liquid into gas", "B"), ("To get thicker", "C"), ("To get bigger", "D")], "B")
        ]),
        "nov-week-passage3": ("The Life of a Butterfly", "Informational", [
            ("Butterflies go through an amazing transformation called metamorphosis, which means their bodies completely change form. This incredible journey has four distinct stages. It starts when an adult female butterfly carefully lays tiny eggs on a leaf, usually choosing a plant that caterpillars like to eat. After a few days or weeks, a small caterpillar hatches from the egg and immediately begins its job: eating! The caterpillar munches on leaves constantly, growing bigger and bigger.", 24),
            ("As it grows, it sheds its tight skin several times. When the caterpillar is fully grown, it finds a safe spot and forms a hard shell called a chrysalis around itself. It hangs upside down and stays very still. Inside the chrysalis, something magical happens. The caterpillar's body actually breaks down into a soupy liquid, and then rebuilds itself into a completely different form.", 57),
            ("After one to four weeks, depending on the type of butterfly, a beautiful adult butterfly breaks out of the chrysalis with wet, crumpled wings. The butterfly hangs on its old chrysalis and pumps special fluid from its body into its wings to make them expand and become strong. Once its wings dry and harden in the sun, the butterfly can fly away to find flowers, drink nectar, and eventually start the cycle all over again by laying eggs of its own.", 100)
        ], [
            ("What is the hard shell that forms around a caterpillar called?", [("A cocoon", "A"), ("A chrysalis", "B"), ("An egg", "C"), ("A pod", "D")], "B"),
            ("List the four stages of a butterfly's life cycle in order.", [("Egg, chrysalis, caterpillar, adult", "A"), ("Egg, caterpillar, chrysalis, adult", "B"), ("Adult, egg, caterpillar, chrysalis", "C"), ("Caterpillar, egg, adult, chrysalis", "D")], "B"),
            ("Why can't a butterfly fly immediately after coming out of the chrysalis?", [("Its wings are wet and need to dry", "A"), ("It needs to eat first", "B"), ("It's too tired", "C"), ("It needs to practice", "D")], "A"),
            ("What does 'metamorphosis' mean?", [("A complete change of form", "A"), ("Growing bigger", "B"), ("Eating leaves", "C"), ("Laying eggs", "D")], "A")
        ]),
        "nov-week-passage4": ("Volcanoes: Mountains of Fire", "Informational", [
            ("A volcano is an opening in Earth's surface where hot melted rock can escape from deep underground. This melted rock is called magma when it's still underground and lava when it flows out onto the surface. Volcanoes form in places where Earth's rocky outer shell, called the crust, is weak or cracked.", 18),
            ("Deep beneath the surface, temperatures are so hot that rock melts into a thick, glowing liquid. When pressure builds up beneath the Earth's crust, it pushes the magma upward through cracks and weak spots until it erupts out of the volcano. When a volcano erupts, it can shoot out lava, clouds of ash, chunks of rock, poisonous gases, and even lightning!", 44),
            ("Some volcanic eruptions are quiet and gentle, with lava slowly oozing down the sides of the mountain like thick syrup. Other eruptions are explosive and very dangerous, sending ash miles into the sky and destroying everything nearby. Not all volcanoes erupt all the time. Scientists put volcanoes into three groups. Active volcanoes erupt regularly or have erupted recently and could erupt again soon. Dormant volcanoes haven't erupted in a long time but still could erupt again someday. Extinct volcanoes will probably never erupt again because they no longer have magma beneath them.", 93),
            ("Despite their dangers, volcanoes also create benefits. Volcanic soil is very rich and good for growing crops, which is why people sometimes live near volcanoes.", 112)
        ], [
            ("What is the difference between magma and lava?", [("Magma is gas, lava is liquid", "A"), ("Magma is underground, lava is above ground", "B"), ("They are the same thing", "C"), ("Lava is colder than magma", "D")], "B"),
            ("Name and describe the three types of volcanoes mentioned in the passage.", [("Hot, warm, and cold", "A"), ("Active, dormant, and extinct", "B"), ("Big, medium, and small", "C"), ("New, old, and ancient", "D")], "B"),
            ("Why would an explosive eruption be more dangerous than a quiet eruption?", [("It shoots ash miles high and destroys things", "A"), ("It happens more often", "B"), ("It lasts longer", "C"), ("It's louder", "D")], "A"),
            ("What does 'dormant' mean in this passage?", [("Never erupting", "A"), ("Sleeping but could wake up", "B"), ("Always erupting", "C"), ("Extremely active", "D")], "B")
        ]),
        "nov-week-passage5": ("The Water Cycle", "Informational", [
            ("Water on Earth is always moving and changing in an endless process called the water cycle. This cycle has been happening for billions of years and is the reason we have fresh water to drink. It starts when the sun heats up water in oceans, lakes, rivers, and even puddles. The heat causes the water to turn into an invisible gas called water vapor that rises into the air. This process is called evaporation.", 24),
            ("Water also evaporates from plants through tiny holes in their leaves. As the water vapor rises higher and higher into the atmosphere, it gets colder because the air is cooler up high. When water vapor gets cold enough, it changes back into tiny liquid water droplets. This process is called condensation. Millions and millions of these tiny droplets come together to form clouds that you can see floating in the sky.", 58),
            ("The droplets in the clouds bump into each other and stick together, growing bigger and bigger. When the droplets become too heavy to float in the air anymore, they fall back down to Earth. This falling water is called precipitation, and it can happen as rain, snow, sleet, or hail depending on how cold the air is. When precipitation reaches the ground, some of it soaks into the soil where plant roots can use it. The rest flows into streams and rivers, eventually returning to the ocean where the whole amazing cycle begins again.", 102)
        ], [
            ("What are the three main stages of the water cycle?", [("Ice, liquid, gas", "A"), ("Evaporation, condensation, precipitation", "B"), ("Clouds, rain, ocean", "C"), ("Sun, sky, ground", "D")], "B"),
            ("What happens to water during the evaporation stage?", [("It freezes solid", "A"), ("It turns into vapor and rises", "B"), ("It falls as rain", "C"), ("It becomes salt water", "D")], "B"),
            ("Why do you think water vapor turns back into liquid droplets when it rises higher in the sky?", [("The air gets colder up high", "A"), ("The air gets warmer up high", "B"), ("There is no wind up high", "C"), ("The clouds push it down", "D")], "A"),
            ("What does 'precipitation' mean?", [("Water rising up", "A"), ("Water falling down from clouds", "B"), ("Water in oceans", "C"), ("Water in plants", "D")], "B")
        ]),
        "nov-week-passage6": ("How Your Heart Works", "Informational", [
            ("Your heart is an amazing, powerful muscle about the size of your fist that never stops working your entire life. It beats about 100,000 times every single day, which adds up to more than 35 million times each year! Your heart's job is to pump blood through your body. Blood is important because it carries oxygen and nutrients that every cell in your body needs to stay alive and healthy.", 25),
            ("Your heart is divided into four separate sections called chambers, almost like four connected rooms. The two chambers on top are called atria, and the two chambers on the bottom are called ventricles. The right side of your heart receives dark red blood from your body that has already delivered its oxygen. It pumps this blood to your lungs, where the blood picks up fresh oxygen and gets rid of carbon dioxide when you breathe.", 58),
            ("The blood turns bright red when it has lots of oxygen. Then the left side of your heart receives this oxygen-rich blood from your lungs and pumps it out forcefully through tubes called arteries to every part of your body. Your heart never gets to rest, even when you're sleeping peacefully at night. When you exercise or play hard, your heart beats faster to deliver more oxygen to your working muscles. Regular exercise actually makes your heart muscle stronger and more efficient, just like it makes your other muscles stronger when you use them.", 101)
        ], [
            ("How many times does your heart beat in one day?", [("1,000 times", "A"), ("10,000 times", "B"), ("100,000 times", "C"), ("1,000,000 times", "D")], "C"),
            ("What important things does blood carry through your body?", [("Food and water", "A"), ("Oxygen and nutrients", "B"), ("Bones and muscles", "C"), ("Clothes and toys", "D")], "B"),
            ("Why does the heart need to pump blood to the lungs before sending it to the rest of the body?", [("To make it flow faster", "A"), ("To pick up oxygen and remove carbon dioxide", "B"), ("To make it warmer", "C"), ("To clean it", "D")], "B"),
            ("What does 'chambers' mean in this passage?", [("Small rooms in the heart", "A"), ("Heart beats", "B"), ("Blood vessels", "C"), ("Muscle cells", "D")], "A")
        ]),
        "nov-week-passage7": ("Ancient Egyptian Pyramids", "Informational", [
            ("The ancient Egyptians built enormous pyramids as tombs for their pharaohs, who were the kings and queens of Egypt. The Great Pyramid of Giza is the largest pyramid ever built and was constructed around 4,500 years ago for a pharaoh named Khufu. This massive structure took approximately 20 years and an estimated 100,000 workers to complete.", 22),
            ("The pyramid is made of over two million stone blocks, with each block weighing as much as a small car or even more! Workers cut these heavy stones from rock quarries using copper tools and wooden wedges. Then they moved the enormous blocks using wooden sleds, log rollers, and dirt ramps. Scientists are still amazed by how the ancient Egyptians accomplished this incredible feat without modern machinery.", 56),
            ("Inside the pyramids, Egyptians placed golden treasures, fancy furniture, food, clothing, and many other objects they believed the pharaoh would need in the afterlife. The pyramids were built with secret passages and hidden rooms to protect these valuable items from robbers. Ancient Egyptians believed that when pharaohs died, they became gods and needed their belongings in the next world.", 87),
            ("The pyramids were designed and built to last forever as monuments to the pharaohs' power and greatness. Many pyramids still stand today in the Egyptian desert as reminders of one of history's most advanced ancient civilizations and their amazing engineering and building skills.", 114)
        ], [
            ("Why did ancient Egyptians build pyramids?", [("As schools for children", "A"), ("As tombs for their pharaohs", "B"), ("As houses", "C"), ("As stores", "D")], "B"),
            ("How long did it take to build the Great Pyramid of Giza, and how many workers did it require?", [("5 years and 50,000 workers", "A"), ("20 years and 100,000 workers", "B"), ("50 years and 200,000 workers", "C"), ("100 years and 500,000 workers", "D")], "B"),
            ("Based on the passage, what can we learn about ancient Egyptian beliefs about death and the afterlife?", [("They believed pharaohs became gods after death", "A"), ("They didn't believe in afterlife", "B"), ("They buried pharaohs with nothing", "C"), ("They believed pharaohs stayed ordinary people", "D")], "A"),
            ("What does 'quarries' mean in this passage?", [("Ancient tools", "A"), ("Places where stone is cut from rock", "B"), ("Type of pyramid", "C"), ("Egyptian workers", "D")], "B")
        ]),
        "nov-week-passage8": ("Earthquakes and How They Happen", "Informational", [
            ("An earthquake is a sudden shaking or trembling of the ground caused by movement deep inside the Earth. To understand earthquakes, you need to know that Earth's outer layer, called the crust, is not one solid piece. Instead, it's broken into huge pieces called tectonic plates that fit together like a giant jigsaw puzzle.", 20),
            ("These enormous plates are always slowly moving, but they usually move so slowly you can't feel it. They might move just a few inches each year, about as fast as your fingernails grow. Sometimes these plates get stuck as they try to slide past each other, rub against each other, or push into each other. Pressure and energy build up at the edges where they're stuck, kind of like when you bend a stick until it snaps.", 56),
            ("After many years, the pressure becomes too great and the plates suddenly slip or break free. When they finally move, they release all that stored energy at once. This energy travels through the ground in waves, making the Earth shake and causing an earthquake. The place underground where the earthquake starts is called the focus, and the place on the surface directly above it is called the epicenter.", 91),
            ("Scientists use special instruments called seismographs to detect and measure earthquakes, even small ones that people can't feel. The strength of an earthquake is measured using numbers on a special scale. Small earthquakes happen somewhere in the world almost every day, but people rarely notice them. Large earthquakes are much more rare but can be very destructive, knocking down buildings, cracking roads, and changing the landscape.", 131)
        ], [
            ("What are tectonic plates?", [("Small pieces of rock", "A"), ("Huge pieces of Earth's crust that move", "B"), ("Types of earthquakes", "C"), ("Underground caverns", "D")], "B"),
            ("Explain in your own words what causes the ground to shake during an earthquake.", [("Volcanoes erupt", "A"), ("Plates get stuck, pressure builds, then plates suddenly slip and release energy", "B"), ("The Earth spins too fast", "C"), ("Meteors hit the Earth", "D")], "B"),
            ("Why do you think scientists want to measure and detect earthquakes?", [("To prevent all earthquakes", "A"), ("To help people prepare and stay safe", "B"), ("To cause more earthquakes", "C"), ("To study the weather", "D")], "B"),
            ("What does 'destructive' mean in the last sentence?", [("Helpful", "A"), ("Causing great damage", "B"), ("Beautiful", "C"), ("Quiet", "D")], "B")
        ]),
        "nov-week-passage9": ("The Rainforest Layers", "Informational", [
            ("Tropical rainforests are thick, green forests that receive a huge amount of rain and stay warm throughout the entire year. These forests are home to more than half of all the plant and animal species on Earth! Rainforests are structured in four different layers, almost like floors in a tall apartment building, and each layer has its own special community of plants and animals.", 27),
            ("The emergent layer is at the very top, where the tallest trees in the forest poke their crowns high above everything else, sometimes reaching 200 feet tall. These giant trees get the most sunshine and must be strong enough to handle wind and storms. Eagles, hawks, butterflies, bats, and monkeys live way up here in the bright sunshine.", 53),
            ("Below that is the canopy layer, which forms a thick, dense roof of overlapping branches and leaves about 60 to 90 feet above the ground. This is where most rainforest animals live, including colorful parrots, tree frogs, sloths, and many types of monkeys that swing from branch to branch. The understory layer sits below the canopy in much darker conditions because the thick canopy blocks most of the sunlight from reaching down this far.", 93),
            ("Small trees, bushes, and large-leafed plants grow here, along with insects, snakes, lizards, and jaguars that hunt in the shadows. The forest floor is the bottom layer where hardly any sunlight reaches at all. It's dark, damp, and covered with a carpet of decomposing leaves, fallen branches, and rotting fruit. Surprisingly, few plants grow here because of the lack of light. However, the forest floor is home to many insects like ants and termites, plus larger animals like tapirs, anteaters, and armadillos that search through the dead leaves for food.", 141)
        ], [
            ("How many layers does a rainforest have, and what are they called?", [("Two layers: top and bottom", "A"), ("Three layers: high, middle, low", "B"), ("Four layers: emergent, canopy, understory, forest floor", "C"), ("Five layers: extra top, high, middle, low, bottom", "D")], "C"),
            ("Which layer gets the most sunlight, and which gets the least?", [("Forest floor gets most, emergent gets least", "A"), ("Emergent gets most, forest floor gets least", "B"), ("Canopy gets most and least equally", "C"), ("Understory gets most, canopy gets least", "D")], "B"),
            ("Why do you think few plants grow on the dark forest floor?", [("It's too wet", "A"), ("Lack of sunlight", "B"), ("Too many animals", "C"), ("The soil is bad", "D")], "B"),
            ("What does 'decomposing' mean in this passage?", [("Growing", "A"), ("Breaking down or rotting", "B"), ("Falling", "C"), ("Floating", "D")], "B")
        ]),
        "nov-week-passage10": ("How Bats Use Echolocation", "Informational", [
            ("Most bats are nocturnal animals, which means they sleep during the day and hunt for food at night when it's completely dark. You might wonder how they can fly through forests and catch tiny insects when they can't see anything. Bats use an amazing skill called echolocation to find their way and locate food in total darkness.", 22),
            ("Here's how this incredible natural sonar system works: the bat opens its mouth or nose and makes very high-pitched sounds, sometimes as many as 200 calls per second. These sounds are usually too high for human ears to detect. The sound waves travel through the air like invisible ripples until they hit an object, such as a flying moth, a tree branch, or the wall of a cave.", 53),
            ("When the sound waves hit something, they bounce back toward the bat like an echo. The bat's large, specially-shaped ears catch these returning sound waves. Then the bat's brain quickly processes information about the echo, including how long it took for the sound to travel back and how the sound changed.", 82),
            ("From this information, the bat's brain creates a detailed sound picture that tells the bat exactly where the object is located, how big it is, what shape it has, and even which direction it's moving and how fast. This amazing ability lets bats catch tiny flying insects in complete darkness with incredible accuracy! Some bats are so skilled at echolocation that they can detect a human hair in total darkness. Scientists have studied bat echolocation to help create technology for ships, submarines, and even tools to help people who are blind navigate their surroundings.", 125)
        ], [
            ("What does it mean when the passage says bats are 'nocturnal animals'?", [("They sleep at night and hunt during day", "A"), ("They sleep during day and hunt at night", "B"), ("They never sleep", "C"), ("They only hunt at dawn", "D")], "B"),
            ("Describe the process of how echolocation works, from start to finish.", [("Bats use eyes to see, find food, and eat", "A"), ("Bats make sounds, sound bounces back, ears catch echoes, brain creates a sound picture", "B"), ("Bats smell food and fly to it", "C"), ("Bats feel vibrations in the air", "D")], "B"),
            ("What physical feature helps bats use echolocation successfully?", [("Their wings", "A"), ("Their large, specially-shaped ears", "B"), ("Their sharp teeth", "C"), ("Their tails", "D")], "B"),
            ("What does 'high-pitched' mean in this passage?", [("Very loud", "A"), ("Very quiet", "B"), ("Very low frequency", "C"), ("Very high frequency sounds", "D")], "D")
        ])
    }
}

# Generate all November stories
print("Generating November 3-7, 2025 cold reads...")
for story_key, (title, subtitle, paragraphs, questions) in nov_stories["stories"].items():
    filename = f"cold-reads-{story_key}.html"
    create_story_html(title, subtitle, nov_stories["date"], paragraphs, questions, filename)
    print(f"Created: cold-reads-{story_key}.html")

print("\nNovember week completed!")
print(f"Total files created: {len(nov_stories['stories'])}")

