from app.domain.chunking import split_into_chunks


def words(n):
    return " ".join(f"w{i}" for i in range(n))


def test_short_note_is_a_single_chunk():
    assert split_into_chunks("Ate full lunch, in good spirits") == ["Ate full lunch, in good spirits"]


def test_short_note_is_trimmed():
    assert split_into_chunks("  Slept well  ") == ["Slept well"]


def test_note_exactly_at_limit_is_not_split():
    assert len(split_into_chunks(words(60))) == 1


def test_long_note_is_split_into_chunks_no_longer_than_max():
    chunks = split_into_chunks(words(150), max_words=60, overlap=10)
    assert len(chunks) > 1
    assert all(len(c.split()) <= 60 for c in chunks)


def test_consecutive_chunks_overlap():
    chunks = split_into_chunks(words(150), max_words=60, overlap=10)
    for first, second in zip(chunks, chunks[1:]):
        assert first.split()[-10:] == second.split()[:10]


def test_no_words_are_lost():
    text = words(137)
    chunks = split_into_chunks(text, max_words=60, overlap=10)
    covered = set()
    for c in chunks:
        covered.update(c.split())
    assert covered == set(text.split())
