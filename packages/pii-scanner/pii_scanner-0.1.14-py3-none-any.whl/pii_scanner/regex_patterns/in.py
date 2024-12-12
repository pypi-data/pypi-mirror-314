from presidio_analyzer import Pattern

patterns = {

    'VOTERID': Pattern(name="VoterID", regex=r"^[A-Z]{3}[0-9]{7}$", score=0.9),
    'PASSPORT': Pattern(name="Passport", regex=r"^[A-PR-WY-Z][0-9]{7}$", score=0.9),
}
