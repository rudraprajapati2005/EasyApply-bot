
#KEYWORDS to determine whether the job is early-career

KEYWORDS = ["intern"  , "internship" , "entry-level" , "graduate" , "fresher" , "trainee" ,  "early career"]

def is_early_career(title: str = "" , description : str = "") -> bool:
    text = f"{title} {description}".lower()

    return any(k in text for k in KEYWORDS)

def compute_match_score(title: str = "", description: str = "") -> int:
    # Very simple scoring: +10 if early-career keyword present, +1 per keyword occurrence
    text = f"{title} {description}".lower()
    score = 0
    for k in KEYWORDS:
        if k in text:
            score += 10
            score += text.count(k)
    return score
