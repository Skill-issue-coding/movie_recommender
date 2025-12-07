from summa.summarizer import summarize
from summa import keywords

movie_request_1 = "I am looking for a visually stunning fantasy drama set within the Infinite Athenaeum, a sentient library existing in the space between seconds, focusing on two rival archivists named Elara and Kaelen. Elara is a chaotic pyromancer who views magic as raw emotion, while Kaelen is a rigid chronomancer who treats it as a precise calculation. For decades, their relationship has consisted solely of stinging insults scribbled in the margins of ancient scrolls, but when a catastrophic Void Leak threatens to erase history, they are forced into a collapsing pocket dimension to fix it. I want the narrative to focus on a mature, slow-burn romance where their survival depends entirely on synchronizing their opposing powers. Visually, the film should depict her violet flames thawing his frozen time-loops to create a dazzling new golden energy, symbolizing how their contradictory natures actually complete one another. The story shouldn't rely on generic action battles but rather on the intimacy of two intellectual equals realizing they are the only ones capable of understanding the burden of such immense power. The film should culminate in a heartbreaking choice where they must decide whether to save the library and return to their solitary lives or let the world crumble just to remain together in the chaos, prioritizing atmosphere and chemistry above all else."

print("------------ Test Text -----------")
print("keywords: \n", keywords.keywords(movie_request_1), "\n")
print("Top 5 Keywords:\n",keywords.keywords(movie_request_1,words=5), "\n")

