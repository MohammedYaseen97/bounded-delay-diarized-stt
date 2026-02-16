from scripts._bootstrap import add_src_to_path


def test_imports_smoke():
    add_src_to_path()
    import audio.chunking  # noqa: F401
    import audio.io  # noqa: F401
    import asr.interfaces  # noqa: F401
    import diarization.interfaces  # noqa: F401
    import embeddings.interfaces  # noqa: F401
    import fusion.attribution  # noqa: F401
    import schemas.types  # noqa: F401
    import stabilization.interfaces  # noqa: F401
    import vad.interfaces  # noqa: F401

