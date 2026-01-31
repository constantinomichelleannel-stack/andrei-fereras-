BASIC_TEMPLATES = [
    ('Motion practice', 'File motion focusing on strongest dispositive issues; attach controlling jurisprudence.'),
    ('Settlement posture', 'Pursue early settlement if risk exceeds threshold; propose mediation timetable.'),
    ('Evidence development', 'Identify gaps; request documents; consider subpoena/FOI where appropriate.'),
    ('Client communication', 'Prepare client memo with risks, options, and likely timelines.'),
]

def recommend(objective: str, case_facts: str):
    o = objective.lower()
    out = []
    for label, rationale in BASIC_TEMPLATES:
        if 'win' in o and label == 'Motion practice':
            out.append({'label': label, 'rationale': rationale, 'references': []})
        elif 'settle' in o and label == 'Settlement posture':
            out.append({'label': label, 'rationale': rationale, 'references': []})
        else:
            out.append({'label': label, 'rationale': rationale, 'references': []})
    return out
