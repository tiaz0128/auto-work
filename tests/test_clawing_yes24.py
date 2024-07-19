from app.clawing.yes24 import ClawerYes24


def test_clawing_yes24():
    searching_book_name = "파이썬 자동화 스킬"

    clawer = ClawerYes24(searching_book_name)

    book_info = clawer.get_booK_info()

    with open(".temp/test_clawing_yes24.txt", "w") as f:
        f.write(",".join(book_info))

    assert book_info
