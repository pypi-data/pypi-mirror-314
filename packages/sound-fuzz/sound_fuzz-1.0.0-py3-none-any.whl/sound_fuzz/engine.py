from sound_fuzz.string import *


class MatchingRuleEngine:
    MATCHING_THRESHOLD = 0.8

    @staticmethod
    def get_name_matching_score(string_1, string_2, force_version=2):
        if force_version == 2:
            return (
                MatchingRuleEngineV2().get_name_matching_score(string_1, string_2)
            ) * 100
        return (
            MatchingRuleEngineV1().get_name_matching_score(string_1, string_2)
        ) * 100


class MatchingRuleEngineV1:
    MATCHING_THRESHOLD = 0.8

    @staticmethod
    def get_name_matching_score(string_1, string_2):
        if not all([string_1, string_2]):
            print("Sent blank / null strings for name matching score.")
            return None, None

        if string_1.lower() == string_2.lower():
            return True, 1.0

        is_matched, match_score = dg_cv_check_is_matched_for_names(
            dg_cv_filter_employer_name(string_1.lower()),
            dg_cv_filter_employer_name(string_2.lower()),
        )
        return is_matched, round(match_score, 1)


def default_name_matching(name1, name2):
    return MatchingRuleEngineV1().get_name_matching_score(name1, name2)


class MatchingRuleEngineV2:
    MATCHING_THRESHOLD = 0.8

    @staticmethod
    def get_name_matching_score(string_1, string_2):

        rule_num = 0
        rule_score = 0
        name_prefix = ["master", "miss", "mr", "mrs", "ms", "w/o"]

        order_list = [
            ["SC012", "inc_common_names_missing", sc012_common_names],
            ["SC000", "inc_permute_join_matching", sc000_permute_matched],
            ["SC013", "inc_initials_check", sc013_initials_check],
            ["SC014", "inc_soundex_matched", sc014_soundex_matched],
            ["SC015", "3W_2W_one_word_missing", sc015_word_missing],
            ["DEFAULT", "default code", default_name_matching],
        ]

        reduction_list = [
            ["RE002", "dec_initials_check", re002_initials_check],
            ["RE001", "dec_soundex_unequal_names", re001_soundex_unequal_names],
            ["RE003", "dec_two_names_vs_one", re003_two_words_vs_one],
            ["RE005", "dec_soundex_single_name", re005_single_name_soundex],
            ["RE006", "dec_name_gender_check", re006_name_gender_check],
            ["RE010", "dec_is_not_exact_match", re010_is_exact_match],
        ]

        if not all([string_1, string_2]):
            print("Sent blank / null strings for name matching score.")
            return 0.0

        if string_1.lower() == string_2.lower():
            return 1.0

        string1_replaced = string_1.lower().replace(".", " ").split()
        string2_replaced = string_2.lower().replace(".", " ").split()

        string1_replaced = [
            name for name in string1_replaced if name not in name_prefix
        ]
        string2_replaced = [
            name for name in string2_replaced if name not in name_prefix
        ]

        string1_replaced = " ".join(string1_replaced)
        string2_replaced = " ".join(string2_replaced)

        if not all([string1_replaced, string2_replaced]):
            return None

        if string1_replaced.lower() == string2_replaced.lower():
            return 1.0

        for rule_num in range(0, len(order_list)):
            is_matched, rule_score = order_list[rule_num][2](
                string1_replaced, string2_replaced
            )
            if is_matched:
                break

        if rule_score >= 0.8 and rule_num == len(order_list) - 1:
            reduced_rule_score = rule_score
            for re_rule_num in range(0, len(reduction_list)):
                is_matched, reduced_rule_score = reduction_list[re_rule_num][2](
                    string1_replaced, string2_replaced, rule_score
                )
                if reduced_rule_score < rule_score:
                    break
        else:
            reduced_rule_score = rule_score

        return round(reduced_rule_score, 1)
