from src.recommendation_functions.recommendations_user import get_ratings

def get_recommendations_from_dicts(rec1, rec2, n=None, c=0.5):
    '''
    Given the reccomendations of two users, this function calculates the first n common
    recommendations of movies for both of them, to be seen together. To sort these

    Parameters
    ----------
    rec1 : dict
        Dictionary {id_1: r_1, id_2: r_2, ..., id_n1: r_n1}, where id_1, ..., id_n1 are
        the ids of the movies recommended for the first user, and r_1, ..., r_n1 are its
        corresponding ratings.
    
    rec2 : dict
        Dictionary {id_1: r_1, id_2: r_2, ..., id_n2: r_n2}, where id_1, ..., id_n2 are
        the ids of the movies recommended for the second user, and r_1, ..., r_n2 are its
        corresponding ratings.

    n : int
        Number of common recommendations returned. If n is None, all the movies that rec1
        and rec2 have in common are returned. n = None by default.

    c : float
        Parameter of the score. The score used to sort the recommendations is
        r1 + r2 - c * abs(r1 - r2), where r1 is the rating given by the first user and r2
        is the rating given by the second user. The term r1 + r2 aims to take into account
        that, of course the sum of the ratings has to be as big as possible. However, the
        term - c * abs(r1 - r2) aims to reduce the variance between both ratings, to
        priorize those combinations of r1 and r2 which have similar values instead of
        so different ones. So, depending on c, this will be considered more or less.
        c = 0.5 by default.

    Returns
    -------
    dict
        Dictionary {id_1: s_1, id_2: s_2, ..., id_n: s_n} of the n recommended films for
        both users sorted in descending order by score, where id_1, ..., id_n are the ids
        of the movies recommended for both users, and s_1, ..., s_n are its corresponding
        scores.

    '''

    # Select the common movies that both users have in common
    common_ids = set(rec1.keys()) & set(rec2.keys())

    # Create the common dictionary
    score = lambda x, y: x + y - c * abs(x - y)
    combined_recs = {m_id: score(rec1[m_id], rec2[m_id]) for m_id in common_ids}

    # Sort the dictionary by score
    combined_recs = dict(sorted(combined_recs.items(), key=lambda item: -item[1]))

    # Return the n first recommentations
    if n is not None:
        return dict(list(combined_recs.items())[:n])
    return combined_recs


def get_combined_recommendations(user1_id, user2_id, n=None, c=0.5, all=False):

    rec1, _ = get_ratings(folder='../spotlight',
                         in_model='../../models/movielens_1M_model.pkl',
                         in_dataset='../../data/datasets/movielens_1M.csv',
                         user=user1_id,
                         out_predictions='None',
                         top=0)

    rec2, _ = get_ratings(folder='../spotlight',
                        in_model='../../models/movielens_1M_model.pkl',
                        in_dataset='../../data/datasets/movielens_1M.csv',
                        user=user2_id,
                        out_predictions='None',
                        top=0)

    comb_rec = get_recommendations_from_dicts(rec1, rec2, n=5, c=0.5)

    if all:
        return (list(comb_rec.keys()), # Ids of the movies
               list(comb_rec.values()), # Scores
               [rec1[movie_id] for movie_id in list(comb_rec.keys())], # Pred. ratings for user 1
               [rec2[movie_id] for movie_id in list(comb_rec.keys())]) # Pred. ratings for user 2
    else:
        return list(comb_rec.keys())




def main1():
    rec1 = {73: 4, 58: 3, 38: 3, 14: 3, 53: 3, 43: 2, 0: 1, 75: 1}
    rec2 = {43: 5, 13: 5, 53: 5, 75: 5, 58: 2, 82: 2, 14: 2, 0: 1}

    comb_rec = get_recommendations_from_dicts(rec1, rec2, n=5)

    print('Ids of common recommendations:', list(comb_rec.keys()))

def main2():
    ids, scores, rat1, rat2 = get_combined_recommendations(1, 2, all=True)

    print('ids:', ids)
    print('scores:', scores)
    print('rat1:', rat1)
    print('rat2:', rat2)


if __name__ == '__main__':

    main2()


