"""
Basic Language support checks
"""
from hyperglot.languages import Languages
from hyperglot.language import Language


def test_language_has_support():
    Langs = Languages()

    # A Language object with the 'fin' data
    fin = Language(Langs["fin"], "fin")

    # These "chars" represent a font with supposedly those codepoints in it
    fin_chars_missing_a = "bcdefghijklmnopqrstuvwxyzäöå"
    fin_chars_base = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÅabcdefghijklmnopqrstuvwxyzäöå ̈ ̊"  # noqa
    fin_chars_aux = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÅÆÕØÜŠŽabcdefghijklmnopqrstuvwxyzäöåæõøüšž ̈ ̊ ̃ ̌"  # noqa
    fin_chars_no_precomposed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ̈ ̊"  # noqa

    # This is what has_support should look like if it determines 'fin' is
    # supported
    fin_matched = {"Latin": ["fin"]}

    matches = fin.has_support(fin_chars_base, pruneOrthographies=False)
    assert matches == fin_matched

    no_matches = fin.has_support(fin_chars_base, level="aux",
                                 pruneOrthographies=False)
    assert no_matches == {}

    matches = fin.has_support(fin_chars_aux, level="aux",
                              pruneOrthographies=False)
    assert matches == fin_matched

    no_matches = fin.has_support(fin_chars_base, level="aux",
                                 pruneOrthographies=False)
    assert no_matches == {}

    no_matches = fin.has_support(fin_chars_missing_a, pruneOrthographies=False)
    assert no_matches == {}

    matches = fin.has_support(fin_chars_no_precomposed,
                              pruneOrthographies=False)
    assert matches == fin_matched


def test_language_inherit():
    Langs = Languages(inherit=True)

    # aae inherits aln orthography
    aae = Language(Langs["aae"], "aae")
    aln = Language(Langs["aln"], "aln")
    assert aae.get_orthography()["base"] == aln.get_orthography()["base"]

    # without inheritance aae's only orthography should not have any base chars
    Langs = Languages(inherit=False)
    aae = Language(Langs["aae"], "aae")
    assert "base" not in aae.get_orthography()


def test_language_preferred_name():
    Langs = Languages()
    bal = Language(Langs["bal"], "bal")
    #   name: Baluchi
    #   preferred_name: Balochi
    assert bal.get_name() == "Balochi"


def test_language_get_autonym():
    Langs = Languages()
    bal = Language(Langs["bal"], "bal")
    #   name: Baluchi
    #   - autonym: بلۏچی
    #     script: Arabic
    #   preferred_name: Balochi

    # For Arabic it should return the correct autonym, without script False
    assert bal.get_autonym(script="Arabic") == "بلۏچی"
    assert bal.get_autonym() is False


def test_language_all_orthographies():
    Langs = Languages()
    # smj Lule Sami with one primary and one deprecated orthography should
    # always return only the primary
    smj = Language(Langs["smj"], "smj")
    # All the chars from both orthographies
    smj_base = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z Á Ä Å Ñ Ö Ń a b c d e f g h i j k l m n o p q r s t u v w x y z á ä å ñ ö ń A B D E F G H I J K L M N O P R S T U V Á Ä Å Ŋ a b d e f g h i j k l m n o p r s t u v á ä å ŋ a n o ́ ̃ ̈ ̊"  # noqa

    # When checking primary orthographies only one should be included
    support = smj.has_support(smj_base)
    assert ("smj" in support["Latin"]) is True
    assert len(smj["orthographies"]) == 1

    # Even when checking all orthographies the 'deprecated' orthography should
    # not be included
    support = smj.has_support(smj_base, checkAllOrthographies=True)
    assert len(smj["orthographies"]) == 1

    # rmn Balkan Romani has Latin (primary) and Cyrillic orthographies
    # It should return only Latin by default, but both when listing all
    rmn = Language(Langs["rmn"], "rmn")

    # All the chars from both orthographies
    rmj_base = "A B C D E F H I J K L M N O P Q R S T U V W X Y Z a b c d e f h i j k l m n o p q r s t u v w x y z А Б В Г Д Е Ж З И К Л М Н О П Р С Т У Ф Х Ц Ч Ш Ы Ь Э Ю Я а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ы ь э ю я G g ́ ̂ ̆ ̇ ̈ ̌"  # noqa

    # When checking all orthographies, the Cyrillic non-primary should be
    # included
    support = rmn.has_support(rmj_base, checkAllOrthographies=True)
    assert ("rmn" in support["Latin"]) is True
    assert ("Cyrillic" in support.keys()) is True
    assert len(rmn["orthographies"]) == 2

    # When checking only primary only Latin should be included
    support = rmn.has_support(rmj_base, checkAllOrthographies=False)
    assert ("rmn" in support["Latin"]) is True
    assert ("Cyrillic" not in support.keys()) is True
    assert len(rmn["orthographies"]) == 1
