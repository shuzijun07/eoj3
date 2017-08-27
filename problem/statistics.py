from random import uniform
from math import log10

from django.core.cache import cache

from submission.models import SubmissionStatus, Submission

PROBLEM_AC_USER_COUNT = 'p{problem}_c{contest}_ac_user_count'
PROBLEM_ALL_USER_COUNT = 'p{problem}_c{contest}_all_user_count'
PROBLEM_AC_USER_RATIO = 'p{problem}_c{contest}_ac_ratio_user'
PROBLEM_AC_COUNT = 'p{problem}_c{contest}_ac_count'
PROBLEM_ALL_COUNT = 'p{problem}_c{contest}_all_count'
PROBLEM_AC_RATIO = 'p{problem}_c{contest}_ac_ratio'
PROBLEM_DIFFICULTY = 'p{problem}_difficulty'


def _get_or_invalidate(problem_id, contest_id, cache_name):
    t = cache.get(cache_name)
    if t is None:
        invalidate_problems([problem_id], contest_id)
        return cache.get(cache_name)
    else:
        return t


def _get_many_or_invalidate(problem_ids, contest_id, cache_template):
    cache_res = cache.get_many(list(map(lambda x: cache_template.format(problem=x, contest=contest_id),
                                        problem_ids)))
    ans = dict()
    second_attempt = []
    for problem_id in problem_ids:
        cache_name = cache_template.format(problem=problem_id, contest=contest_id)
        if cache_name not in cache_res:
            second_attempt.append(problem_id)
        else:
            ans[problem_id] = cache_res[cache_name]
    invalidate_problems(second_attempt, contest_id)
    if second_attempt:
        res2 = cache.get_many(list(map(lambda x: cache_template.format(problem=x, contest=contest_id),
                                       second_attempt)))
        for problem_id in problem_ids:
            cache_name = cache_template.format(problem=problem_id, contest=contest_id)
            if cache_name in res2:
                ans[problem_id] = res2[cache_name]
    assert len(ans) == len(problem_ids)
    return ans


def get_problem_accept_user_count(problem_id, contest_id=0):
    """
    get problem accept count (user), with cache

    :type problem_id: int
    :return:
    """
    return get_many_problem_accept_count([problem_id], contest_id)[problem_id]


def get_problem_all_user_count(problem_id, contest_id=0):
    cache_name = PROBLEM_ALL_USER_COUNT.format(problem=problem_id, contest=contest_id)
    return _get_or_invalidate(problem_id, contest_id, cache_name)


def get_problem_accept_user_ratio(problem_id, contest_id=0):
    cache_name = PROBLEM_AC_USER_RATIO.format(problem=problem_id, contest=contest_id)
    return _get_or_invalidate(problem_id, contest_id, cache_name)


def get_problem_accept_count(problem_id, contest_id=0):
    cache_name = PROBLEM_AC_COUNT.format(problem=problem_id, contest=contest_id)
    return _get_or_invalidate(problem_id, contest_id, cache_name)


def get_problem_all_count(problem_id, contest_id=0):
    cache_name = PROBLEM_ALL_COUNT.format(problem=problem_id, contest=contest_id)
    return _get_or_invalidate(problem_id, contest_id, cache_name)


def get_problem_accept_ratio(problem_id, contest_id=0):
    cache_name = PROBLEM_AC_RATIO.format(problem=problem_id, contest=contest_id)
    return _get_or_invalidate(problem_id, contest_id, cache_name)


def get_problem_difficulty(problem_id, contest_id=0):
    cache_name = PROBLEM_DIFFICULTY.format(problem=problem_id, contest=contest_id)
    return _get_or_invalidate(problem_id, contest_id, cache_name)


def get_many_problem_accept_count(problem_ids, contest_id=0):
    return _get_many_or_invalidate(problem_ids, contest_id, PROBLEM_AC_USER_COUNT)


def get_many_problem_difficulty(problem_ids, contest_id=0):
    return _get_many_or_invalidate(problem_ids, contest_id, PROBLEM_DIFFICULTY)


def invalidate_problems(problem_ids, contest_id=0):
    if contest_id > 0:
        cache_time = 60 * uniform(0.6, 1)
        problem_filter = Submission.objects.filter(problem_id__in=problem_ids, contest_id=contest_id).\
            only('problem_id', 'contest_id', 'author_id', 'status')
    else:
        cache_time = 300 * uniform(0.6, 1)
        problem_filter = Submission.objects.filter(problem_id__in=problem_ids). \
            only('problem_id', 'author_id', 'status')

    all_count = {problem_id: 0 for problem_id in problem_ids}
    accept_count = {problem_id: 0 for problem_id in problem_ids}
    all_user = {problem_id: set() for problem_id in problem_ids}
    accept_user = {problem_id: set() for problem_id in problem_ids}
    cache_res = {}
    for submission in problem_filter:
        pid = submission.problem_id
        if submission.status == SubmissionStatus.ACCEPTED:
            accept_count[pid] += 1
            accept_user[pid].add(submission.author_id)
        all_count[pid] += 1
        all_user[pid].add(submission.author_id)
    for problem_id in problem_ids:
        accept_user_count = len(accept_user[problem_id])
        all_user_count = len(all_user[problem_id])
        if all_user_count > 0:
            accept_ratio = int(accept_count[problem_id] / all_count[problem_id] * 100)
            accept_user_ratio = int(accept_user_count / all_user_count * 100)
        else:
            accept_ratio = accept_user_ratio = 0
        difficulty = max(min(.02 * (100 - accept_ratio) + .03 * (100 - accept_user_ratio) + max(
            6 - 2 * log10(accept_user_count + 1), 0), 9.9), 0.1)
        cache_res.update({
            PROBLEM_ALL_COUNT.format(problem=problem_id, contest=contest_id): all_count[problem_id],
            PROBLEM_AC_COUNT.format(problem=problem_id, contest=contest_id): accept_count[problem_id],
            PROBLEM_ALL_USER_COUNT.format(problem=problem_id, contest=contest_id): all_user_count,
            PROBLEM_AC_USER_COUNT.format(problem=problem_id, contest=contest_id): accept_user_count,
            PROBLEM_AC_RATIO.format(problem=problem_id, contest=contest_id): accept_ratio,
            PROBLEM_AC_USER_RATIO.format(problem=problem_id, contest=contest_id): accept_user_ratio,
            PROBLEM_DIFFICULTY.format(problem=problem_id, contest=contest_id): difficulty
        })

    cache.set_many(cache_res, cache_time)
