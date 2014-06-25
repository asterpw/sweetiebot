#!/usr/bin/python
import random
catfacts = ["It has been scientifically proven that owning cats is good for our health and can decrease the occurrence of high blood pressure and other illnesses.",
"Stroking a cat can help to relieve stress, and the feel of a purring cat on your lap conveys a strong sense of security and comfort.",
"The ancient Egyptians were the first civilisation to realise the cat's potential as a vermin hunter and tamed cats to protect the corn supplies on which their lives depended.",
"Sir Isaac Newton is not only credited with the laws of gravity but is also credited with inventing the cat flap.",
"A cat has more bones than a human being; humans have 206 and the cat has 230 bones.",
"A cat's hearing is much more sensitive than humans and dogs.",
"The cat's tail is used to maintain balance. ",
"Cats see six times better in the dark and at night than humans.",
"Cats eat grass to aid their digestion and to help them get rid of any fur in their stomachs.",
"A healthy cat has a temperature between 38 and 39 degrees Celcius.",
"Cats have the largest eyes of any mammal.",
"The female cat reaches sexual maturity at around 6 to 10 months and the male cat between 9 and 12 months.",
"A female cat will be pregnant for approximately 9 weeks or between 62 and 65 days from conception to delivery. ",
"The average litter of kittens is between 2 - 6 kittens.",
"Ailurophile is the word cat lovers are officially called.",
"Purring does not always indicate that a cat is happy. Cats will also purr loudly when they are distressed or in pain.",
"All cats need taurine in their diet to avoid blindness. Cats must also have fat in their diet as they are unable to produce it on their own.",
"In households in the UK and USA, there are more cats kept as pets than dogs. At least 35% of households with cats have 2 or more cats.",
"When a cats rubs up against you, the cat is marking you with it's scent claiming ownership.",
"About 37% of American homes today have at least 1 cat.",
"Milk can give some cats diarrhea.",
"The average lifespan of an outdoor-only cat is about 3 to 5 years while an indoor-only cat can live 16 years or much longer.",
"On average, a cat will sleep for 16 hours a day.",
"A domestic cat can run at speeds of 30 mph.",
"The life expectancy of cats has nearly doubled over the last fifty years.",
"Blue-eyed, white cats are often prone to deafness.",
"The cat's front paw has 5 toes and the back paws have 4. Cats born with 6 or 7 front toes and extra back toes are called polydactl.",
"An adult cat has 30 teeth, 16 on the top and 14 on the bottom.",
"There are approximately 60,000 hairs per square inch on the back of a cat and about 120,000 per square inch on its underside.",
"Cats and kittens should be acquired in pairs whenever possible as cat families interact best in pairs.",
"In multi-cat households, cats of the opposite sex usually get along better.",
"The first official cat show in the UK was organised at Crystal Palace in 1871.",
"There are more than 500 million domestic cats in the world, with 33 different breeds.",
"Cats 'paw' or 'knead' (repeatedly treading on a spot - sometimes its owner) to mark their territory. Cats sweat through the bottom of their paws and rub off the sweat as a marking mechanism.",
"Cat urine glows in the dark when a black light shines on it. If you think your cat or kitten has had an accident in your home, use a black light to find the mishap.",
"The print on a cat's nose has a unique ridged pattern, like a human fingerprint.",
"25% of cat owners admit to blow drying their cat's hair after a bath.",
"If your cat is near you, and her tail is quivering, this is the greatest expression of love your cat can give you.",
"If your cat is thrashing its tail, she is in a bad mood - time for you to keep your distance!",
"Only domestic cats hold their tails straight up while walking. Wild cats hold their tails horizontally or tucked between their legs while walking.",
"During her productive life, one female cat could have more than 100 kittens. A single pair of cats and their kittens can produce as many as 420,000 kittens in just 7 years.",
"Sir Isaac Newton, discoverer of the principles of gravity, also invented the cat door.",
"The more you talk to your cat, the more it will speak to you.",
"Kittens begin dreaming when they are over one week old.",
"A group of kittens is called a 'kindle.' A group of grown cats is called a 'clowder.' A male cat is called a 'tom,' a female cat is called a 'molly' or 'queen', and young cats are called 'kittens.'",
"Cats spend 30% of their waking hours grooming themselves.",
"Each year Americans spend four billion dollars on cat food. That's one billion dollars more than they spend on baby food!",
"Cats can make over 100 vocal sounds, while dogs can only make 10.",
"The majority of cats do not have any eyelashes.",
"Cats have been used to deliver mail: In Belgium in 1879, 37 cats were used to deliver mail to villages. However they found that the cats were not disciplined enough to keep it up.",
"In a lifetime, the average house cat spends approximately 10,950 hours purring.",
"A cat's jaws cannot move sideways.",
"Cats rarely meow at other cats.",
"When cats are happy, they may squeeze their eyes shut.",
"Cats don't use their voice's natural frequency range to verbally communicate feelings such as affection, anger, hunger, boredom, happiness and fear - this would be inaudible to humans as this frequency is much lower than humans can hear. Some researchers believe cats may have learned we can't hear them in their natural range and have adapted so they can relate to us on our terms.",
"The reason for the lack of mouse-flavored cat food is due to the fact that the test subjects (cats, naturally!) did not like it.",
"Cats see so well in the dark because their eyes actually reflect light. Light goes in their eyes, and is reflected back out. This means that their eyes actually work almost like built-in flashlights."
]

def getCatMessage():
	message = "I see that you are asking about cats.\n\n"
	catfact = random.choice(catfacts)
	catfact = catfact[:1].lower() + catfact[1:]
	message += "[size=4][color=pink][b]Did you know that " + catfact.replace('.', '?', 1)
	message += "[/b][/color][/size]"
	return message

if __name__ == "__main__":
	for i in range( 50):
		print getCatMessage()